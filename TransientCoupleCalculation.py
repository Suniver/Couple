# coding = gbk
# program name:TransientCoupleCalculation.py
# This program helps to manager the transient coupling calculation of RMC and CTF
# 此程序负责控制RMC和CTF瞬态耦合的流程
# 程序流程：
# 在每一次循环中：
#   运行一次接续计算的RMC
#   删除上一步的power.inp.n文件，处理RMC输出的Tally文件，变成CTF预处理器可用的power.inp.n文件
#   运行CTF计算，计算两步（这个地方可以进行优化尝试！）
#   处理CTF输出的.out文件，变成RMC接续计算可用的h5文件
#   删除CTF输出的.out文件

import os
import sys
from TLcreatePowerInpFile import createPowerInpFile

def calculate(NeutronicsCommand, ThermHyCommand, OutToHDF5Command, TimePointList, InitialAbsPower):

    for IterationStep in range(1,len(TimePoints)+1):                                                                                          #power.inp.0, power.inp.1, power(N-1).inp*, inp.tally(N-1)*,             TransientCTF.h5
        
        os.system(NeutronicsCommand)                            #to complete 这个地方的NeutronicsCommand基本上就是'python step.py'              #power.inp.0, power.inp.1, power(N-1).inp*, inp.tally(N-1)*, inp.tallyN, TransientCTF.h5
                                                                #所以后续需要针对step.py进行优化
                                                                #这一步产生了一个tally文件：inp.tallyN，其中N为这一步是第几个迭代步
                                                                
        os.rename('power.inp.0','Power%s.inp'%(n-1) )           #把上一步用到的power.inp.0重命名为PowerN.inp，其中N为上一步是第几个迭代         #             power.inp.1, powerN.inp*,     inp.tally(N-1)*, inp.tallyN, TransientCTF.h5
        os.rename('power.inp.1','power.inp.0')      )           #把上一步用到的power.inp.1重命名为power.inp.0，以供接下来CTF预处理器使用        #power.inp.0,              powerN.inp*,     inp.tally(N-1)*, inp.tallyN, TransientCTF.h5
        
        createPowerInpFile(IterationStep, InitialAbsPower, TimePointList)
                                                                #把inp.tallyN文件转化为power.inp.1文件                                          #power.inp.0, power.inp.1, powerN.inp*,     inp.tally(N-1)*, inp.tallyN, TransientCTF.h5
        
        os.system(ThermHyCommand)                               #运行CTF，计算得到包含两个时间步的.out文件                                      #power.inp.0, power.inp.1, powerN.inp*,     inp.tallyN,                  TransientCTF.h5,  deck.out
                                                                #to complete：在运行CTF之前，还要运行预处理器
        
        os.system(OutToHDF5Command)                             #把包含两个时间步的.out文件转换为RMC接续计算可读的h5文件                        #power.inp.0, power.inp.1, powerN.inp*,     inp.tallyN,                  TransientCTF.h5+, deck.out
        
        os.remove('deck.out')                                   #把这一步CTF运行所得的.out文件删除                                              #power.inp.0, power.inp.1, powerN.inp*,     inp.tallyN,                  TransientCTF.h5+
        
if __name__=='__main__':

    os.chdir(sys.path[0])
    
    NeutronicsCommand   = 'python step.py'
    ThermHyCommand      = 'cobratf'
    OutToHDF5Command    = 'python H5CTFoutToHDF5.py'
    InitialAbsPower     = 1.0 #单位MWe
    TimePointList = [0.0,2.6,2.8,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4] + \
                    [4.2+i*0.2 for i in range(15)] + \
                    [7.2+i*0.1 for i in range(20)]
    
    calculate(NeutronicsCommand, ThermHyCommand, OutToHDF5Command, TimePointList, InitialAbsPower)