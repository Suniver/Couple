# coding=gbk
# program name: TLcreatePowerInpFile.py
# 本程序用于将RMC中子动力学产生的inp.tallyN文件转换成CTF预处理器可读的power.inp.n文件

import os
import sys
import glob
import re
import TLcalPowerDistribution
import TLprintPowerInpFile

def createPowerInpFile(IterationStep, InitialAbsPower, TimePointList):
    
    Xnodes = 17             #Tally文件中的横向节点数
    Ynodes = 17             #Tally文件中的纵向节点数
    Znodes = 20             #Tally文件中的高度向节点数
    GuideTubeNumber = 25    #导向管的数量
    MeshTallyNameList = sorted(glob.glob('inp.tally*'),key=os.path.getmtime)    #获取当前文件夹下的inp.tallyN的名字
    
    AbsPowerOfEveryStep = [ 0 for i in range(0,len(MeshTallyNameList))]         #变量：存储每个时间步的全堆绝对功率
    AbsPowerOfEveryStep[0] = InitialAbsPower                                    #第一个时间步的全堆绝对功率为：1.0MWe
    
    FetchFile = open('fetch','r')                                               #打开fetch文件，fetch文件存有每个时间步的全堆相对功率
    RelativePowerList = re.findall('Power:([+-]*[.\d]+[Ee][+-]*[\d]+)',FetchFile.read())    #把fetch文件中每个时间步的全堆相对功率提取到相对功率列表中
    FetchFile.close()                                                           #关闭fetch文件
    
    AbsPowerOfEveryStep[IterationStep] =    AbsPowerOfEveryStep[0] * \
                                            float(RelativePowerList[IterationStep]) / float(RelativePowerList[0]) #计算最新的时间步的绝对功率
    
    MeshTallyFile = open(MeshTallyNameList[IterationStep],'r')      #打开最新的Tally文件
    TallyAveList = re.findall('\s+\d+\s+([+-]*[.\d]+[Ee][+-]*[\d]+)',MeshTallyFile.read())   #将Tally文件中的所有的ave存到字符串列表中
    MeshTallyFile.close()                                           #关闭Tally文件
    
    AsbMeshPowerList = [ 0 for j in range(0,len(TallyAveList))]     #把Tally文件中的每个mesh的相对功率转变成绝对功率
    TallySum = 0.0                                                  #
    for TallyAve in TallyAveList:                                   #首先求出Tally文件中的所有Ave的和
        TallySum += float(TallyAve)                                 #
    for j in range(0, len(TallyAveList)):                           #然后求出Tally文件中每个mesh的绝对功率
        AsbMeshPowerList[j] = AbsPowerOfEveryStep[IterationStep] * float(TallyAveList[j]) / TallySum
    
    AbsAxialPower = TLcalPowerDistribution.calAxialPowerDistribution(AsbMeshPowerList, Xnodes, Ynodes, Znodes)    #对每一层的功率加和，计算tally文件中每个组件轴向的功率分布
    AxialPowerFactor = AbsAxialPower                                #计算归一化的轴向功率因子
    for j in range(0, len(AxialPowerFactor)):
        AxialPowerFactor[j] = AbsAxialPower[j] / ( AbsPowerOfEveryStep[IterationStep] / Znodes)
    
    AxialPowerNodeFactor = [ 0 for j in range(0,21)]    #因为CTF要求输入的是轴向节点的相对功率，而RMC计算出来是轴向mesh的相对功率，所以要把mesh功率转化为节点功率，转化过程要保持归一化
    #下面这种简单的归一化是可以被CTF认作正确输入的
    for j in range(0, len(AxialPowerNodeFactor)):
        if j == 0:
            AxialPowerNodeFactor[j] = AxialPowerFactor[j]
        elif j == len(AxialPowerNodeFactor) - 1 :
            AxialPowerNodeFactor[j] = AxialPowerFactor[j-1]
        else:
            AxialPowerNodeFactor[j] = ( AxialPowerFactor[j-1] + AxialPowerFactor[j] ) / 2
    
    #下面这种以积分量作为归一化准则的方法不被CTF认为是正确输入
    # Power_sum = 0.0
    # for j in range(0, len(Power_axial_factor)):
        # Power_sum += Power_axial_factor[j]
    # for j in range(0, len(Power_axial_factor)):
        # Power_axial_factor[j] = Power_axial_factor[j] * 21 / Power_sum
    # for j in range(0,len(Power_axial_factor)):
        # if j == 0:
            # Power_sum += Power_axial_factor[j]
        # elif j == len(Power_axial_factor)-1:
            # Power_sum += Power_axial_factor[j]
        # else:
            # Power_sum += 2* Power_axial_factor[j]
    # for j in range(0,len(Power_axial_factor)):
        # Power_axial_factor[j] = Power_axial_factor[j] * 40 / Power_sum
    
    AbsRadialPower = TLcalPowerDistribution.calRadialPowerDistribution(AsbMeshPowerList, Xnodes, Ynodes, Znodes)    #对每根棒的功率加和，计算径向的绝对功率分布
    AbsRadialPowerFactor = AbsRadialPower
    for x in range(0,Xnodes):
        for y in range(0, Ynodes):
            AbsRadialPowerFactor[x][y] = AbsRadialPower[x][y] / (AbsPowerOfEveryStep[IterationStep] / (Xnodes*Ynodes-GuideTubeNumber))
    
    TLprintPowerInpFile.printpower(TimePointList[IterationStep],     AbsPowerOfEveryStep[IterationStep], \
                                   MeshTallyNameList[IterationStep], AxialPowerNodeFactor, \
                                   AbsRadialPowerFactor, Xnodes, Ynodes, Znodes)
                                   
if __name__=='__main__':
    
    os.chdir(os.path.join(sys.path[0],'unit test TLcreatePowerInpFile'))
    
    TimePointList = [0.0,2.6,2.8,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4] + \
                    [4.2+i*0.2 for i in range(15)] + \
                    [7.2+i*0.1 for i in range(20)]
    InitialAbsPower = 1.0 #单位：MWe
    IterationStep = 19
    createPowerInpFile(IterationStep, InitialAbsPower, TimePointList)