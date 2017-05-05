# coding=gbk
# program name: TL_print_power_inp.py
# 此程序用来生成power.inp.N文件
# to complete 目前程序中的一些参数，如轴向分层等，都还是写死的，后期需要更正。
import os
from TLcalPowerDistribution import printRadialPower

def printpower(TimePoint, AbsTotalPower, TallyFileName, AxialFactor, RadialFactor, Xnodes, Ynodes, Znodes):
    power = open('power.inp.%s'%1,'w')
    print >> power, '\
*************************************************\n\
*       TOTAL POWER AND POWER PROFILES          *\n\
*************************************************\n\
*'
    print >> power, r'{transient time}'
    print >> power, TimePoint
    print >> power, '\
******************\n\
*   Total power  *\n\
******************\n\
*\n\
* Power in MWth and total numer of fuel assemblies'
    print >> power, AbsTotalPower
    print >> power, '\
*\n\
************************\n\
*    Power profiles    *\n\
************************\n\
*\n\
* Number of pairs (height/relative power) of axial profile /Heights refered to the beginning of active fuel (BAF)/'
    print >> power, '21'
    print >> power, '* Number of pairs (height/relative power) of axial profile /Heights refered to the beginning of active fuel (BAF)/'
    for i in range(0,Znodes+1):
        print >> power, '%s    '%(183*i),AxialFactor[i]
    print >> power, '\
*******************************\n\
*Core Radial Power Factors\n\
*******************************\n\
**This specifies the power factors to be\n\
**applied to each whole assembly.  Values\n\
**must normalize to one.'
    print >> power, 1.0
    print >> power, '\
*******************************\n\
*Assembly Radial Power Factors*\n\
*******************************'
    print >> power, r'{number of assembly maps}'
    print >> power, 1
    print >> power, r'{assembly power factor index map}'
    print >> power, 1
    print >> power, r'{1}'
    print >> power, printRadialPower(RadialFactor, Xnodes, Ynodes)