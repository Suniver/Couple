# coding = gbk
# module name: H5postprocess.py
# this module can extract certain kind of data from SplitedDeckFile.out, such as:
# rod node no.
# fuel temperature(center)
# 此模块所有函数的输入参数都是字符串
import re
import os
import sys

def getRodNumber(WholeFileString):
    return int(re.findall('rod no. *(\d+)',WholeFileString)[0])
    
def getSurfaceNumber(WholeFileString):
    return int(re.findall('surface no. *(\d+)',WholeFileString)[0])
    
def getSolutionTime(WholeFileString):
    return float(re.findall('simulation time = *(\d*.\d+)',WholeFileString)[0])
    
def getChannelNumber(WholeFileString):
    return int(re.findall('fluid properties for channel *(\d+)',WholeFileString)[0])
    
def getNodeNumber(Line):
    return int(re.findall('^ *(\d+) +',Line)[0])
    
def getRodCenterTemperature(Line):
    return float(re.findall('(\d+.\d+) +\d+.\d+ *\n',Line)[0])
    
def existNodeNumber(Line):
    return re.findall('^ *(\d+) +\** +(\d*.*\d+)',Line) != []
    
def existLiquidDensity(Line):
    return re.findall(' +\d+.\d+ +(\d+.\d+) +\d+.\d+ +\d+.\d+ +\d+.\d+\n',Line) != []
    
def getLiquidDensity(Line):
    return float(re.findall(' +\d+.\d+ +(\d+.\d+) +\d+.\d+ +\d+.\d+ +\d+.\d+\n',Line)[0])

# unit test #单元测试
if __name__ == '__main__':

    # locate file path to unit test file folder path
    RootFolder = sys.path[0]
    os.chdir(os.path.join(RootFolder,'unit test postprocess'))
    
    # test all the functions
    with open('postprocess-testfile-rod','r') as TestFile:
        WholeTestFileString = TestFile.read()
        print 'Rod Number = ',getRodNumber(WholeTestFileString)
        print 'Surface Number = ',getSurfaceNumber(WholeTestFileString)
        print 'Solution Time = ',getSolutionTime(WholeTestFileString)

    with open('postprocess-testfile-rod','r') as TestFile:
        for line in TestFile:
            if existNodeNumber(line):
                print 'Node Number = ',getNodeNumber(line),' RodCenterTemperature = ',getRodCenterTemperature(line)
                
    with open('postprocess-testfile-channel','r') as TestFile:
        WholeTestFileString = TestFile.read()
        print 'Channel Number = ',getChannelNumber(WholeTestFileString)
        print 'Solution Time = ',getSolutionTime(WholeTestFileString)
        
    with open('postprocess-testfile-channel','r') as TestFile:
        for line in TestFile:
            if existLiquidDensity(line):
                print 'Node Number = ',getNodeNumber(line),' Density = ',getLiquidDensity(line)