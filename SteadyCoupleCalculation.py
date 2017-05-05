# coding = gbk
# program name: SteadyCoupleCalculation.py
# This program will help manager the steady couple calculation for RMC and CTF
# 此程序可以控制稳态耦合的进程
import os
import sys

def calculate(Command):
    os.system(Command)

if __name__=='__main__':
    
    os.chdir(os.path.join(sys.path[0],'unit test SteadyCoupleCalculation'))
    
    Command = 'ProgramForTest'
    calculate(Command)
    
    print 'This line will be displayed after you input your value.'