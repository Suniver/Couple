# coding = gbk
# program name: CheckFiles.py
# This program helps check if the files are ready for calculation
# 此程序用来检查用于瞬态计算的程序、文件等是否齐全
import os
import sys

def existFiles(FileNameList):
    #检查文件是否齐全的主程序
    #输入值：字符串列表。 由文件名组成
    #输出值：bool量。     如果文件齐全，输出True；文件不齐全，输出False
    
    ExecutionDir = os.getcwd()          #获取当前脚本的执行目录
    
    existFlag = True                    #返回值初始化为True
    
    for FileName in FileNameList:       #对文件名列表进行循环
        if not os.path.exists(os.path.join(ExecutionDir,FileName)): #如果不存在文件名对应的文件
            existFlag = False                                       #返回值设置为False
            print 'File \''+FileName+'\' does NOT exist!'           #输出错误信息
    
    return existFlag
    
# unit test #单元测试
if __name__=='__main__':
    
    os.chdir(os.path.join(sys.path[0],'unit test CheckFiles')) #设置脚本文件的执行目录为单元测试目录
    
    FileNameList = ['1','2','3','5']
    
    print existFiles(FileNameList)
    
    FileNameList = ['1','2','3','4']
    
    print existFiles(FileNameList)