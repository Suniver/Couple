# coding = gbk
# module name: H5preprocess.py
# this module will help get the name of the CTF *.out file,
# help create a new folder named whatever you like
# help get the total rod number and the total rod node number
import glob
import re
import sys
import os

def getLargeDeckFileName():

    LargeDeckFileNameList = sorted(glob.glob('*.out'),key=os.path.getmtime)
    existsDeckFile = LargeDeckFileNameList != []
    
    while not existsDeckFile:
        print 'Warning!! Do not exist a *.out file!'
        print 'Put your *.out file in the same directory this python script'
        raw_input('If you have put your file in the right directory, press enter')
        LargeDeckFileNameList = sorted(glob.glob('*.out'),key=os.path.getmtime)
        existsDeckFile = LargeDeckFileNameList != []
    
    return LargeDeckFileNameList[0]

def getTotalAssemNumber():
    # read from inp file
    InpFileName = 'H5inp'
    InpFile = open(InpFileName)
    InpFileString = InpFile.read()
    return int(re.findall('assemnumber +(\d+)',InpFileString)[0])

def getTotalRodNumber():
    # read from inp file
    InpFileName = 'H5inp'
    InpFile = open(InpFileName)
    InpFileString = InpFile.read()
    return int(re.findall('rodnumber +(\d+)',InpFileString)[0])

def getTotalRodNodeNumber():
    # read from inp file
    InpFileName = 'H5inp'
    InpFile = open(InpFileName)
    InpFileString = InpFile.read()
    return int(re.findall('rodnodenumber +(\d+)',InpFileString)[0])

def getTotalSurfaceNumber():
    # read from inp file
    InpFileName = 'H5inp'
    InpFile = open(InpFileName)
    InpFileString = InpFile.read()
    return int(re.findall('surfacenumber +(\d+)',InpFileString)[0])
    
def getTotalChannelNodeNumber():
    # read from inp file
    InpFileName = 'H5inp'
    InpFile = open(InpFileName)
    InpFileString = InpFile.read()
    return int(re.findall('channelnodenumber +(\d+)',InpFileString)[0])
    
def getTotalChannelNumber():
    # read from inp file
    InpFileName = 'H5inp'
    InpFile = open(InpFileName)
    InpFileString = InpFile.read()
    return int(re.findall('channelnumber +(\d+)',InpFileString)[0])
    
def createNewFolder(NewFolderNameString):
    curDir = sys.path[0]
    newDir = NewFolderNameString
    if not os.path.isdir(os.path.join(curDir,newDir)):
        os.mkdir(os.path.join(curDir,newDir))
        
    
# unit test
if __name__ == '__main__':
    # set dir to the local dir
    RootFolder = sys.path[0]
    os.chdir(RootFolder)
    # function test
    print 'Deck File Name is ',getLargeDeckFileName()
    createNewFolder('preprocesstest')
    print 'Total Rod Number = ',getTotalRodNumber()
    print 'Total Rod Node Number = ',getTotalRodNodeNumber()
    print 'Total Surface Number = ',getTotalSurfaceNumber()
    print 'Total Channel Number = ',getTotalChannelNumber()
    print 'Total Channel Node Numebr = ',getTotalChannelNodeNumber()