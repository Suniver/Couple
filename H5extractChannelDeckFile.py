# coding = gbk
# module name : extractChannelDeckFile.py
# 这个程序用来帮助将体积较大的Deck.out文件分割成一系列小的xxx.out文件，每个文件都只存储某一个时间步下某个通道的所有信息
# 这个程序会在当前脚本的执行目录下新建一系列文件夹，文件夹的名字是小文件存储的时间信息。所有属于同一模拟时间的小文件都会被存储在对应文件夹下
import re
import os

def extractChannelDeckFile(DeckFile):
    
    readingStartLine    = False     #标识：是否正在读取小文件的第一行
    readingMiddleLine   = False     #标识：是否正在读取小文件的中间行
    readingEndLine      = False     #标识：是否正在读取小文件的结尾行
    
    SimulationTime  = 0             #变量，存储当前小文件中的时间信息
    ChannelNumber   = 0             #变量，存储当前小文件中的棒位信息
    #注释掉SurfaceNumber   = 0             #变量，存储当前小文件中的面位信息
    
    CacheFileName = 'Channel.cache' #变量：缓存文件的文件名
    
    StarLineCount   = 0             #变量：读取过的星号行的计数
    afterStartLine  = False         #标志：是否读过了首行
    
    curDir = os.getcwd()            #获取当前脚本的执行目录
    
    for line in DeckFile:           #对于大文件中的每一行：
        
        if re.findall('\*\*\*\*\*\*',line) != []:                   #如果发现了连续的星号：
            StarLineCount = StarLineCount + 1                       #   星号行的计数加1
        
        # classify this line to StartLine, MiddleLine or EndLine    #判断此行是开始行、中间行还是结尾行
        if re.findall('fluid properties for channel',line) != []:   #首行的判断标准：包含字符串'fluid properties for channel'
            readingStartLine = True     #设置此行是首行
            readingMiddleLine = False   #设置此行不是中间行
            readingEndLine = False      #设置此行不是结尾行
            afterStartLine = True       #设置读过了首行
            StarLineCount = 0           #星号行的计数归零
            ChannelNumber = int(re.findall('fluid properties for channel *(\d+)',line)[0])  #从首行中提取棒位信息
            SimulationTime = float(re.findall('simulation time = *(\d*.\d+)',line)[0])      #从首行中提取时间信息
            
        elif afterStartLine == True and StarLineCount == 1:     #末行的判断标准：读过了起始行，并且读到了第一个星号行
            readingStartLine = False    #设置此行不是首行
            readingMiddleLine = False   #设置此行不是中间行
            readingEndLine = True       #设置此行是结尾行
            afterStartLine = False      #因为读到了末行，所以设置并没有读过首行，初始化
            
        elif (afterStartLine == True) and (readingEndLine == False):    #中间行的判断标准：读过了起始行, 且没有读到末行
            #注释掉if readingStartLine == True:
            #注释掉    SurfaceNumber = int(re.findall('surface no. *(\d+)',line)[0]) #在首行的后一行中提取面位信息
                
            readingStartLine = False    #设置此行不是首行
            readingMiddleLine = True    #设置此行是中间行
            readingEndLine = False      #设置此行不是结尾行
            
        elif readingEndLine == True:    #如果上一次读取的是末行，则这次读取的肯定不是末行
            readingEndLine = False      #所以要对末行标识进行初始化
        
        # 根据所读行的性质，进行文件读写操作
        if readingStartLine:                        #如果读到了首行
            SplitedFile = open(CacheFileName,'w')   #   打开缓存文件
            SplitedFile.write(line)                 #   写入首行
            
        elif readingMiddleLine:                     #如果读到了中间行
            SplitedFile.write(line)                 #   写入中间行
            
        elif readingEndLine:                        #如果读到了末行
            SplitedFile.write(line)                 #   写入末行
            SplitedFile.close()                     #   关闭缓存文件
            
            # move splited file to new folder       #   把缓存文件移动到对应时间的文件夹中，并重命名
            newFileName = 'deck.Time%s.channel%s.out'%(SimulationTime, ChannelNumber)
            newDir = os.path.join(curDir,'%s'%SimulationTime)   #   新文件夹的路径是 当前执行目录路径+当前小文件的时间信息
            
            if not os.path.isdir(newDir): # check if the folder exists # 如果不存在新文件夹，则新建一个
                os.mkdir(newDir)
            
            os.rename(os.path.join(curDir,CacheFileName),os.path.join(newDir,newFileName)) # move the file by rename
            
            print 'One single channel deck file of simulation time %s, rod number %s has been splited successfully'%(SimulationTime, ChannelNumber)
        
#  common errors:
#1 windows error 183:
#  this error occurs because the os.rename() function. When the renamed file has already existed, the error raises.