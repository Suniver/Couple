# -*- coding:utf-8 -*-
# program name: H5CTFoutToHDF5.py
# 
import re
import os
import sys
import glob
import shutil
import h5py
from H5extractRodDeckFile import extractRodDeckFile
from H5extractChannelDeckFile import extractChannelDeckFile
import H5RodInformation
import H5ChannelInformation
import H5preprocess
import H5postprocess

#input module #输入模块
skipSplit = True                                            #to complete 测试用，如果已经存在了被分割好的小文件，就跳过分割文件的步骤，能够节省大量时间
SplitedRodFileFolderName= 'SplitedRodDeckFiles'             #用于存放分割成的存储棒信息的小文件的文件夹的名字，叫做SplitedRodDeckFiles
SplitedChannelFileFolderName= 'SplitedChannelDeckFiles'     #用于存放分割成的存储通道信息的小文件的文件夹的名字，叫做SplitedChannelDeckFiles
TransientHDF5FileName   = 'TransientCTF.h5'                 #h5文件的名字叫做 TransientCTF.h5

# get the directory of the .out file                        #将脚本执行目录设置到文件存放目录
RootDir = sys.path[0]                                       #获取python脚本及deck.out文件存放的根目录
os.chdir(RootDir)                                           #脚本执行目录设置到根目录

# get the whole name of the .out file                       #获取deck.out文件的名字（必须以.out为后缀）
LargeDeckFileName = H5preprocess.getLargeDeckFileName()

# get geometic information                                          #获取相关几何信息
TotalAssemNumber        = H5preprocess.getTotalAssemNumber()        #获取组件的数量
TotalRodNumber          = H5preprocess.getTotalRodNumber()          #获取燃料棒的数量
TotalRodNodeNumber      = H5preprocess.getTotalRodNodeNumber()      #获取每根燃料棒被划分的节点数
TotalSurfaceNumber      = H5preprocess.getTotalSurfaceNumber()      #获取每根燃料棒的面数
TotalChannelNumber      = H5preprocess.getTotalChannelNumber()      #获取通道的数量
TotalChannelNodeNumber  = H5preprocess.getTotalChannelNodeNumber()  #获取通道的节点数量

##########   splite deck.out file 分割大文件   ##########
# create new folder that contains splited deck files                                #创建用于存放分割成的棒小文件的文件夹
# before creation, a check will be carried out;
# if the folder has already existed, it will be deleted in advance
SplitedRodFileParentDir     = os.path.join(RootDir,SplitedRodFileFolderName)        #获取父目录的路径
SplitedChannelFileParentDir = os.path.join(RootDir,SplitedChannelFileFolderName)    #获取父目录的路径

if not skipSplit:
    if os.path.isdir(SplitedRodFileParentDir):                      #已存在目录的话，则连同里面的文件一起删去
        shutil.rmtree(SplitedRodFileParentDir)
    if os.path.isdir(SplitedChannelFileParentDir):
        shutil.rmtree(SplitedChannelFileParentDir)
    H5preprocess.createNewFolder(SplitedRodFileFolderName)
    H5preprocess.createNewFolder(SplitedChannelFileFolderName)
    
    # split the .out file to many small time.rod.surface.out files  #把大的.out文件分割成一系列小的.out文件
    # each splited .out file contains the information of a single surface of a single rod

    with open(LargeDeckFileName,'r') as LargeDeckFile:              #打开大文件
        os.chdir(SplitedRodFileParentDir)                           #把脚本执行目录设置到存放棒小文件的父件夹中
        extractRodDeckFile(LargeDeckFile)                           #然后把大文件分割成棒小文件
    
    os.chdir(RootDir)
    with open(LargeDeckFileName,'r') as LargeDeckFile:              #打开大文件
        os.chdir(SplitedChannelFileParentDir)                       #把脚本执行目录设置到存放通道小文件的父件夹中
        extractChannelDeckFile(LargeDeckFile)                       #然后把大文件分割成通道小文件
    
##########   create .h5 file  创建.h5文件       #########
# create the .h5 file to store values got from the .out files       #创建h5文件，获得此文件是本程序的根本目的
os.chdir(RootDir)                                                   #把脚本执行目录设置到根目录下
TransientHDF5File = h5py.File(TransientHDF5FileName,'a')            #打开h5文件（若没有，则创建）

##########   extract temperature 提取温度信息   ##########
# Temperature stores the center temperature of all rods             #创建存放燃料棒温度的变量
Temperature = H5RodInformation.RodInformation(TotalAssemNumber, TotalRodNumber, TotalRodNodeNumber, TotalSurfaceNumber)

# Read every splited file and extract specific data of all the files to a certain file(ASCII file or HDF5 file)
SubRodFoldersNameList = os.listdir(SplitedRodFileParentDir)                     #获取存放分割文件的父目录下的子文件夹名称列表

for StateNumber in range(len(SubRodFoldersNameList)):                           #对所有子文件夹进行循环；每一次循环都能提取出对应时间步的全堆温度信息
    SubRodFolderName = SubRodFoldersNameList[StateNumber]
    
    #input module       #输入模块
    SubGrpName = 'STATE_%s'%(StateNumber+1)                                     #每个时间步的信息都存储到同一个h5组中，组的名字即时间（单位：s）
    TemperatureDatasetName = 'pin_fueltemps [F]'                                #设置存放棒温度的数据集的名称
    TemperatureUnit = 'degree Fahrenheit'                                       #设置存放棒温度的数据集的单位
    
    #excution module    #执行模块
    SplitedFileSubDir = os.path.join(SplitedRodFileParentDir,SubRodFolderName)  #获取子目录的路径
    os.chdir(SplitedFileSubDir)                                                 #把脚本执行目录设置到子目录
    SplitedDeckFileNameList = sorted(glob.glob('*.out'),key=os.path.getmtime)   #获取最底层目录下所有的文件名列表

    for SplitedDeckFileName in SplitedDeckFileNameList:
        
        with open(SplitedDeckFileName,'r') as SplitedDeckFile:                  #打开小文件
            FromSplitedDeckFile = SplitedDeckFile.read()                        #   读取小文件内容到字符串中
            AssemNumber = 1                                                     #   to complete 目前的耦合只涉及到一个组件
            RodNumber = H5postprocess.getRodNumber(FromSplitedDeckFile)         #   从字符串中获取棒位
            SurfaceNumber = H5postprocess.getSurfaceNumber(FromSplitedDeckFile) #   从字符串中获取面位
            
        with open(SplitedDeckFileName,'r') as SplitedDeckFile:                  #重新打开小文件（需要重新打开的原因是需要重置文件迭代器，具体可见我的CSDN博文）
            for FromLine in SplitedDeckFile:                                    #读取小文件的每一行
                
                if H5postprocess.existNodeNumber(FromLine):                                                   #如果这一行是数据行（即行内有在节点号）
                    NodeNumber = H5postprocess.getNodeNumber(FromLine)                                        #   读取节点号
                    PointTemperature = H5postprocess.getRodCenterTemperature(FromLine)                        #   读取温度
                    Temperature.setValue(PointTemperature,AssemNumber,RodNumber,NodeNumber,SurfaceNumber)   #   把位置信息（组件号，棒位，节点号，面位）和对应的温度存储到燃料棒温度变量中
    
    os.chdir(RootDir)
    
    Temperature.outputHDF5File(TransientHDF5File, SubGrpName, TemperatureDatasetName, TemperatureUnit)      #把当前时间步的温度信息存储到h5文件中
    TransientHDF5File['/'+SubGrpName].attrs['rod solution time'] = SubRodFolderName
    
##########   extract density 提取密度信息   ##########
# Density stores the channel liquid density of all rods             #创建存放通道冷却剂密度的变量
Density = H5ChannelInformation.ChannelInformation(TotalAssemNumber, TotalChannelNumber, TotalChannelNodeNumber)

# Read every splited file and extract specific data of all the files to a certain file(ASCII file or HDF5 file)
SubChannelFoldersNameList = os.listdir(SplitedChannelFileParentDir)             #获取存放分割文件的父目录下的子文件夹名称列表

for StateNumber in range(len(SubChannelFoldersNameList)):                       #对所有子文件夹进行循环；每一次循环都能提取出对应时间步的全堆温度信息
    SubChannelFolderName = SubChannelFoldersNameList[StateNumber]
    
    #input module       #输入模块
    SubGrpName = 'STATE_%s'%(StateNumber+1)                                     #每个时间步的信息都存储到同一个h5组中，组的名字即时间（单位：s）
    DensityDatasetName = 'liquid_density'                              #设置存放棒温度的数据集的名称
    DensityUnit = 'lbm/ft3'                                                     #设置存放棒温度的数据集的单位
    
    #excution module    #执行模块
    SplitedFileSubDir = os.path.join(SplitedChannelFileParentDir,SubChannelFolderName)  #获取子目录的路径
    os.chdir(SplitedFileSubDir)                                                         #把脚本执行目录设置到子目录
    SplitedDeckFileNameList = sorted(glob.glob('*.out'),key=os.path.getmtime)           #获取最底层目录下所有的文件名列表

    for SplitedDeckFileName in SplitedDeckFileNameList:
        
        with open(SplitedDeckFileName,'r') as SplitedDeckFile:                  #打开小文件
            FromSplitedDeckFile = SplitedDeckFile.read()                        #   读取小文件内容到字符串中
            AssemNumber = 1                                                     #   to complete 目前的耦合只涉及到一个组件
            ChannelNumber = H5postprocess.getChannelNumber(FromSplitedDeckFile) #   从字符串中获取通道位
            
        with open(SplitedDeckFileName,'r') as SplitedDeckFile:                  #重新打开小文件（需要重新打开的原因是需要重置文件迭代器，具体可见我的CSDN博文）
            for FromLine in SplitedDeckFile:                                    #读取小文件的每一行
                
                if H5postprocess.existLiquidDensity(FromLine):                                    #如果这一行是含有密度信息
                    NodeNumber = H5postprocess.getNodeNumber(FromLine)                            #   读取节点号
                    PointDensity = H5postprocess.getLiquidDensity(FromLine)                       #   读取密度
                    Density.setSIValue(PointDensity,AssemNumber,ChannelNumber,NodeNumber)         #   把位置信息（组件号，棒位，节点号）和对应的密度存储到燃料棒温度变量中
    
    os.chdir(RootDir)
    
    Density.outputTXTFile(SubGrpName)
    Density.outputHDF5File(TransientHDF5File, SubGrpName, DensityDatasetName, DensityUnit)      #把当前时间步的温度信息存储到h5文件中
    TransientHDF5File['/'+SubGrpName].attrs['channel solution time'] = SubChannelFolderName

TransientHDF5File.close()