# -*- coding:utf-8 -*-
# program name : H5functionForHDF5.py
# This program contains several simple functions help to handle the HDF5 files.
# 本程序包含几个可以帮助处理hdf5文件的函数
import os
import sys
import h5py

def deleteDatasetIfExist(H5File,GrpName,DatasetName):
    #删除.h5文件中指定的数据集。目前只能实现删除一级目录下的数据集
    #输入：
    #H5File     :   hdf5文件对象
    #GrpName    :   想要删除的数据集所在的组，字符串
    #DatasetName:   想要删除的数据集的名字，字符串
    existedGrpNameList = H5File.keys()                          #获取目标.h5文件中的所有组
    for existedGrpName in existedGrpNameList:                   #对于每一个组：
        if '%s'%GrpName == '%s'%existedGrpName:                 #   如果这个组是删除目标
            existedDatasetNameList = H5File[GrpName].keys()     #   则获取目标组内的所有数据集
            for existedDatasetName in existedDatasetNameList:   #   对于每一个数据集：
                if '%s'%DatasetName == '%s'%existedDatasetName: #       如果这个数据集是删除目标
                    del H5File[GrpName][DatasetName]            #       则删除这个数据集
                    
def deleteGrpIfExist(H5File,GrpName):
    #删除.h5文件中指定的组。目前只能实现删除一级组
    #输入：
    #H5File :   hdf5文件对象
    #GrpName:   想要删除的数据集所在的组，字符串
    existedGrpNameList = H5File.keys()                          #获取目标.h5文件中的所有组
    for existedGrpName in existedGrpNameList:                   #对于每一个组：
        if '%s'%GrpName == '%s'%existedGrpName:                 #   如果这个组是删除目标
            del H5File[GrpName]                                 #   则删除这个组
            
#unit test #单元测试
if __name__=='__main__':
    #注意：这个测试会改变测试目录下的'TransientCTF.h5'文件内容
    #所以建议在执行单元测试之前，首先对目录下的.h5文件进行备份
    #在执行单元测试之后，删除被改变过的.h5文件，并将备份文件拷贝进来
    os.chdir(os.path.join(sys.path[0],'unit test functionForHDF5')) #设置脚本的执行目录
    
    H5File = h5py.File('TransientCTF.h5','a')                   #以a方式打开.h5文件
    print H5File.keys()                                         #列出.h5文件中的一级组
    deleteDatasetIfExist(H5File,'0.51','pin_fueltemps [F]')     #删除0.51组下的pin_fueltemps [F]数据集
    print H5File.keys()                                         #列出.h5文件中的一级组
    deleteGrpIfExist(H5File,'0.51')                             #删除0.51组
    H5File.close()                                              #关闭.h5文件。注意：只有关闭.h5文件后，对此.h5文件执行的操作才会真正执行。