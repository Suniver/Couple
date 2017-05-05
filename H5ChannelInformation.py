# coding = gbk
# class name : H5ChannelInformation.py
import os
import sys
import math
import numpy as np
import h5py
import H5functionForHDF5

class ChannelInformation:
    """
    to complete
    ChannelInformation 这个类可以帮助存储燃料棒的某一特定信息
    使用方法：以存储包壳表面温度为例，
    建立变量：CladSurfaceTemperature = ChannelInformation(模型中燃料棒总数（包括控制棒、导向管等），所划分的总燃料棒节点数，每根燃料棒的面数)
    添加信息：CladSurfaceTemperature.setValue(设定值，燃料棒编号，节点号，面号)。若不添加的话，默认值为0.
    获取信息：
    """
    def __init__(self, TotalAssemCount, TotalChannelCount,       TotalNodeCount,):    # 构造函数
        #              总组件数         每个组件的通道数         总节点数（轴向分层）
        self.__Information       = np.zeros([TotalAssemCount,TotalChannelCount,TotalNodeCount],dtype=np.float)#创建一个全是0.0的ndarray
        self.__TotalAssemCount   = TotalAssemCount
        self.__TotalChannelCount = TotalChannelCount
        self.__TotalNodeCount    = TotalNodeCount
        
    def setValue(self, pointInformation, AssemNumber,      ChannelNumber,     NodeNumber,):  #设置通道某点处的值
        #              当前位置具体的值  当前位置组件编号  当前位置通道编号   当前位置节点编号
        #***** 输入检查
        #
        if AssemNumber<=0 or AssemNumber>self.__TotalAssemCount:            #组件编号超出总组件数
            print 'Assembly Number = %s : Error!'%AssemNumber
        elif ChannelNumber<=0 or ChannelNumber>self.__TotalChannelCount:    #通道编号超出每个燃料组件的通道数
            print 'Channel Number = %s : Error!'%ChannelNumber
        elif NodeNumber<=0 or NodeNumber>self.__TotalNodeCount:             #节点编号超出总节点数
            print 'Node Number = %s : error!'%NodeNumber
        #
        #***** 输入检查
        
        else:
        #存储信息
            self.__Information[AssemNumber-1, ChannelNumber-1, NodeNumber-1] = pointInformation

    def setSIValue(self, pointInformation, AssemNumber,      ChannelNumber,     NodeNumber,):  #设置通道某点处的值，单位从lbm/ft3转变成kg/m3
        #              当前位置具体的值  当前位置组件编号  当前位置通道编号   当前位置节点编号
        #***** 输入检查
        #
        if AssemNumber<=0 or AssemNumber>self.__TotalAssemCount:            #组件编号超出总组件数
            print 'Assembly Number = %s : Error!'%AssemNumber
        elif ChannelNumber<=0 or ChannelNumber>self.__TotalChannelCount:    #通道编号超出每个燃料组件的通道数
            print 'Channel Number = %s : Error!'%ChannelNumber
        elif NodeNumber<=0 or NodeNumber>self.__TotalNodeCount:             #节点编号超出总节点数
            print 'Node Number = %s : error!'%NodeNumber
        #
        #***** 输入检查
        
        else:
        #存储信息
            self.__Information[AssemNumber-1, ChannelNumber-1, NodeNumber-1] = pointInformation*16.01846443
    
    def __getArrayforHDF5(self):                                                #把内置Numpy数组转变为输出HDF5所需要的数据集
        # 2行3列的样子是：(TotalRowCount = 2, TotalColumnCount = 3)
        # 1 1 1
        # 1 1 1
        TotalRowCount    = int(math.sqrt(int(self.__TotalChannelCount)))        #计算得出一个组件一共有多少行 to complete:目前默认的是正方形组件
        TotalColumnCount = int(math.sqrt(int(self.__TotalChannelCount)))        #计算得出一个组件一共有多少列
        ArrayforHDF5 = np.zeros([TotalColumnCount, TotalRowCount, self.__TotalNodeCount, self.__TotalAssemCount],dtype=np.float)
        #
        for ColumnNumber in range(1, TotalColumnCount+1):
            for RowNumber in range(1, TotalRowCount+1):
                for NodeNumber in range(1, self.__TotalNodeCount+1):
                    for AssemNumber in range(1, self.__TotalAssemCount+1):
                        ChannelNumber = TotalColumnCount*(RowNumber-1) + ColumnNumber
                        ArrayforHDF5[ColumnNumber-1, RowNumber-1, NodeNumber-1, AssemNumber-1] = self.getValue(AssemNumber,ChannelNumber,NodeNumber)
        return ArrayforHDF5
        
    def __getPointValue(self, AssemNumber,      ChannelNumber,        NodeNumber): #获取某通道某点处的值(私有函数)
        #                     组件编号          棒位编号             节点编号 
        # 在调用此函数时，请先做输入检查
        return self.__Information[AssemNumber-1, ChannelNumber-1, NodeNumber-1]
        
    def getValue(self, AssemNumber, ChannelNumber, NodeNumber):             #获取某通道某点处的值
        
        #***** 输入检查
        #
        if AssemNumber<=0 or AssemNumber>self.__TotalAssemCount:            #组件编号超出总组件数
            print 'Assembly Number = %s : Error!'%AssemNumber
        elif ChannelNumber<=0 or ChannelNumber>self.__TotalChannelCount:    #通道编号超出每个燃料组件的通道数
            print 'Channel Number = %s : Error!'%ChannelNumber
        elif NodeNumber<=0 or NodeNumber>self.__TotalNodeCount:             #节点编号超出总节点数
            print 'Node Number = %s : error!'%NodeNumber
        #
        #***** 输入检查
        else:
            return self.__getPointValue(AssemNumber, ChannelNumber, NodeNumber)
        
    def getChannelValue(self, AssemNumber, ChannelNumber):                  #获取某通道(通道编号)的平均值
        AverageChannelValue = 0
        #***** 输入检查
        #
        if AssemNumber<=0 or AssemNumber>self.__TotalAssemCount:            #组件编号超出总组件数
            print 'Assembly Number = %s : Error!'%AssemNumber
        elif ChannelNumber<=0 or ChannelNumber>self.__TotalChannelCount:    #通道编号超出每个燃料组件的通道数
            print 'Channel Number = %s : Error!'%ChannelNumber
        #
        #***** 输入检查
        else:
            for NodeNumber in range(1, self.__TotalNodeCount+1):
                AverageChannelValue = AverageChannelValue + self.__getPointValue(AssemNumber, ChannelNumber, NodeNumber)
                
            return float(AverageChannelValue)/self.__TotalNodeCount
        
    def outputFile(self, FileName='output.info'):           #按照选定的格式输出文本文件
        # 参数一，FileName : 输出文件的名字，字符串
        # 参数二，FileType : 在'ave‘或者'surf’中二选一，字符串；
        #                    若选择'ave‘，则输出每个节点处的平均值；若选择'surf’，则输出每个节点处的四个面的值
        
        # to complete 没有考虑SurfaceNumber不是4的情况
        
        #***** 文件检查
        #
        if  os.path.exists(os.path.join(sys.path[0],FileName)):
            os.remove(os.path.join(sys.path[0],FileName))
        #
        #***** 文件检查
        
        File = open(FileName,'w')
        
        File.write('%-12s %-12s %-12s %-12s\n'%('assem no.','Channel no.','node no.','Ave'))
        
        for assembly in range(1,self.__TotalAssemCount+1):
            for Channel in range(1,self.__TotalChannelCount+1):
                for node in range(1,self.__TotalNodeCount+1):
                    if FileType == 'ave':
                        File.write('%-12d %-12d %-12d %-12f\n'%(assembly,Channel,node,self.getNodeValue(assembly,Channel,node) ) )
        return
    
    def outputTXTFile(self, FileName='STATE_1'):
        
        #***** 文件检查
        #
        if  os.path.exists(os.path.join(sys.path[0],FileName)):
            os.remove(os.path.join(sys.path[0],FileName))
        #
        #***** 文件检查
        
        File = open(FileName,'w')
        
        TXTarray = self.__getArrayforHDF5()
        
        # 2行3列的样子是：(TotalRowCount = 2, TotalColumnCount = 3)
        # 1 1 1
        # 1 1 1
        TotalRowCount    = int(math.sqrt(int(self.__TotalChannelCount)))        #计算得出一个组件一共有多少行 to complete:目前默认的是正方形组件
        TotalColumnCount = int(math.sqrt(int(self.__TotalChannelCount)))        #计算得出一个组件一共有多少列
        ArrayforHDF5 = np.zeros([TotalColumnCount, TotalRowCount, self.__TotalNodeCount, self.__TotalAssemCount],dtype=np.float)
        #
        for ColumnNumber in range(1, TotalColumnCount+1):
            for RowNumber in range(1, TotalRowCount+1):
                for NodeNumber in range(1, self.__TotalNodeCount+1):
                    for AssemNumber in range(1, self.__TotalAssemCount+1):
                        if ColumnNumber == TotalColumnCount and RowNumber == TotalRowCount and NodeNumber == self.__TotalNodeCount and AssemNumber == self.__TotalAssemCount:
                            File.write('%s'%TXTarray[ColumnNumber-1, RowNumber-1, NodeNumber-1, AssemNumber-1])
                        else:
                            File.write('%s\n'%TXTarray[ColumnNumber-1, RowNumber-1, NodeNumber-1, AssemNumber-1])
                        
    def outputHDF5File(self, H5File, GrpName, DatasetName, Unit):
        # 参数一，H5File      : 被写入的HDF5文件，HDF5文件
        # 参数二，DatasetName : 数据集的名称（包含其所在的组），字符串
        # 参数三，Unit        : 数据集内每个数据的单位，字符串
        H5functionForHDF5.deleteDatasetIfExist(H5File,GrpName,DatasetName)    #首先检查.h5文件中是否已经包含此数据集；如果是，则删去
        DatasetDir = '/'+GrpName+'/'+DatasetName                            #设置数据集的路径
        H5File[DatasetDir] = self.__getArrayforHDF5()                       #将相关信息存储到对应的数据集中
        H5File[DatasetDir].attrs['physical_units'] = Unit                   #设置数据集的属性
        
# unit test
if __name__ =='__main__':
    import sys
    import os
    #to complete
    RootFolder = sys.path[0]
    os.chdir(RootFolder)
    
    AssemNumber = 193
    ChannelNumber = 289
    NodeNumber = 22
    SurfaceNumber = 4
    
    Temperature = ChannelInformation(AssemNumber, ChannelNumber, NodeNumber, SurfaceNumber) #测试构造函数
    
    PointValue = 0;
    for assem in range(1,AssemNumber+1):
        for Channel in range(1,ChannelNumber+1):
            for node in range(1,NodeNumber+1):
                for surface in range(1,SurfaceNumber+1):
                    PointValue = PointValue + 1
                    Temperature.setValue(PointValue, assem, Channel, node, surface)     #测试设置值
                
    Temperature.outputFile('info.ave')                          #测试输出文本文件，‘ave’格式
    Temperature.outputFile('info.error','avesurf')              #测试输出文本文件的错误处理
    
    H5testFile = h5py.File('test.pdeck.ctf.h5','w')
    Dataset = '/STATE_0001/pin_fueltemps [F]'
    Unit = 'degree Fahrenheit'
    Temperature.outputHDF5File(H5testFile, Dataset, Unit)       #测试输出h5文件
    
    #os.remove('info.ave')
    #os.remove('info.surf')