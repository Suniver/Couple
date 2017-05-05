# coding = gbk
# program name: TransientCoupleDriver
# This program is the driver of RMC-CTF coupling calculation # 此程序是RMC-CTF瞬态耦合计算的主驱动程序

import sys
import os
import CheckFiles
import SteadyCoupleCalculation
import TransientCoupleCalculation

# input block       #输入模块
FileNameList = ['RMC.exe','cobratf','cobratf_preprocessor']
FileNameList = FileNameList + ['TransientCoupleDriver.py','CheckFiles.py']

# calculation block #计算模块
os.chdir(sys.path[0])       #将程序脚本的执行目录设置到.py脚本文件的存放目录

if CheckFiles.existFiles(FileNameList):          #检查程序（二进制程序RMC与CTF、.py脚本）、输入文件等是否存在

    SteadyCoupleCalculation.calculate()     # to complete 进行稳态计算
    SteadyCoupleCalculation.fileProcessing()# to complete 处理稳态输出文件，变成RMC可读的h5文件（存有进行下一步瞬态计算所必要的信息）
                                            # 可以使用接续计算，也可以对中子动力学的稳态计算模块进行修改
                                            # 这一步需要产生
                                            
    TransientCoupleCalculation.calcuate()   # to complete 进行瞬态计算