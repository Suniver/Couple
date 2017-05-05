# coding=gbk
# program name: TLcreatePowerInpFile.py
# ���������ڽ�RMC���Ӷ���ѧ������inp.tallyN�ļ�ת����CTFԤ�������ɶ���power.inp.n�ļ�

import os
import sys
import glob
import re
import TLcalPowerDistribution
import TLprintPowerInpFile

def createPowerInpFile(IterationStep, InitialAbsPower, TimePointList):
    
    Xnodes = 17             #Tally�ļ��еĺ���ڵ���
    Ynodes = 17             #Tally�ļ��е�����ڵ���
    Znodes = 20             #Tally�ļ��еĸ߶���ڵ���
    GuideTubeNumber = 25    #����ܵ�����
    MeshTallyNameList = sorted(glob.glob('inp.tally*'),key=os.path.getmtime)    #��ȡ��ǰ�ļ����µ�inp.tallyN������
    
    AbsPowerOfEveryStep = [ 0 for i in range(0,len(MeshTallyNameList))]         #�������洢ÿ��ʱ�䲽��ȫ�Ѿ��Թ���
    AbsPowerOfEveryStep[0] = InitialAbsPower                                    #��һ��ʱ�䲽��ȫ�Ѿ��Թ���Ϊ��1.0MWe
    
    FetchFile = open('fetch','r')                                               #��fetch�ļ���fetch�ļ�����ÿ��ʱ�䲽��ȫ����Թ���
    RelativePowerList = re.findall('Power:([+-]*[.\d]+[Ee][+-]*[\d]+)',FetchFile.read())    #��fetch�ļ���ÿ��ʱ�䲽��ȫ����Թ�����ȡ����Թ����б���
    FetchFile.close()                                                           #�ر�fetch�ļ�
    
    AbsPowerOfEveryStep[IterationStep] =    AbsPowerOfEveryStep[0] * \
                                            float(RelativePowerList[IterationStep]) / float(RelativePowerList[0]) #�������µ�ʱ�䲽�ľ��Թ���
    
    MeshTallyFile = open(MeshTallyNameList[IterationStep],'r')      #�����µ�Tally�ļ�
    TallyAveList = re.findall('\s+\d+\s+([+-]*[.\d]+[Ee][+-]*[\d]+)',MeshTallyFile.read())   #��Tally�ļ��е����е�ave�浽�ַ����б���
    MeshTallyFile.close()                                           #�ر�Tally�ļ�
    
    AsbMeshPowerList = [ 0 for j in range(0,len(TallyAveList))]     #��Tally�ļ��е�ÿ��mesh����Թ���ת��ɾ��Թ���
    TallySum = 0.0                                                  #
    for TallyAve in TallyAveList:                                   #�������Tally�ļ��е�����Ave�ĺ�
        TallySum += float(TallyAve)                                 #
    for j in range(0, len(TallyAveList)):                           #Ȼ�����Tally�ļ���ÿ��mesh�ľ��Թ���
        AsbMeshPowerList[j] = AbsPowerOfEveryStep[IterationStep] * float(TallyAveList[j]) / TallySum
    
    AbsAxialPower = TLcalPowerDistribution.calAxialPowerDistribution(AsbMeshPowerList, Xnodes, Ynodes, Znodes)    #��ÿһ��Ĺ��ʼӺͣ�����tally�ļ���ÿ���������Ĺ��ʷֲ�
    AxialPowerFactor = AbsAxialPower                                #�����һ��������������
    for j in range(0, len(AxialPowerFactor)):
        AxialPowerFactor[j] = AbsAxialPower[j] / ( AbsPowerOfEveryStep[IterationStep] / Znodes)
    
    AxialPowerNodeFactor = [ 0 for j in range(0,21)]    #��ΪCTFҪ�������������ڵ����Թ��ʣ���RMC�������������mesh����Թ��ʣ�����Ҫ��mesh����ת��Ϊ�ڵ㹦�ʣ�ת������Ҫ���ֹ�һ��
    #�������ּ򵥵Ĺ�һ���ǿ��Ա�CTF������ȷ�����
    for j in range(0, len(AxialPowerNodeFactor)):
        if j == 0:
            AxialPowerNodeFactor[j] = AxialPowerFactor[j]
        elif j == len(AxialPowerNodeFactor) - 1 :
            AxialPowerNodeFactor[j] = AxialPowerFactor[j-1]
        else:
            AxialPowerNodeFactor[j] = ( AxialPowerFactor[j-1] + AxialPowerFactor[j] ) / 2
    
    #���������Ի�������Ϊ��һ��׼��ķ�������CTF��Ϊ����ȷ����
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
    
    AbsRadialPower = TLcalPowerDistribution.calRadialPowerDistribution(AsbMeshPowerList, Xnodes, Ynodes, Znodes)    #��ÿ�����Ĺ��ʼӺͣ����㾶��ľ��Թ��ʷֲ�
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
    InitialAbsPower = 1.0 #��λ��MWe
    IterationStep = 19
    createPowerInpFile(IterationStep, InitialAbsPower, TimePointList)