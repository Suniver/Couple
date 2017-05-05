# coding = gbk
# program name: TransientCoupleDriver
# This program is the driver of RMC-CTF coupling calculation # �˳�����RMC-CTF˲̬��ϼ��������������

import sys
import os
import CheckFiles
import SteadyCoupleCalculation
import TransientCoupleCalculation

# input block       #����ģ��
FileNameList = ['RMC.exe','cobratf','cobratf_preprocessor']
FileNameList = FileNameList + ['TransientCoupleDriver.py','CheckFiles.py']

# calculation block #����ģ��
os.chdir(sys.path[0])       #������ű���ִ��Ŀ¼���õ�.py�ű��ļ��Ĵ��Ŀ¼

if CheckFiles.existFiles(FileNameList):          #�����򣨶����Ƴ���RMC��CTF��.py�ű����������ļ����Ƿ����

    SteadyCoupleCalculation.calculate()     # to complete ������̬����
    SteadyCoupleCalculation.fileProcessing()# to complete ������̬����ļ������RMC�ɶ���h5�ļ������н�����һ��˲̬��������Ҫ����Ϣ��
                                            # ����ʹ�ý������㣬Ҳ���Զ����Ӷ���ѧ����̬����ģ������޸�
                                            # ��һ����Ҫ����
                                            
    TransientCoupleCalculation.calcuate()   # to complete ����˲̬����