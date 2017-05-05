# coding=gbk
# file name: TL_power_distribution_cal.py

def calAxialPowerDistribution(mesh_power, u, v, w):
# mesh_power contains all the absolute power of mesh(u,v,w)
# u, v, w represent there are u, v, w nodes in x, y, z directions respectively
    AxialPower = [0 for i in range(0,w)]
    for z in range(0,w):
        for y in range(0,v):
            for x in range(0,u):
                AxialPower[z] += mesh_power[x+u*y+u*v*z]
    return AxialPower

def calRadialPowerDistribution(mesh_power, u, v, w):
# mesh_power contains all the absolute power of mesh(u,v,w)
# u, v, w represent there are u, v, w nodes in x, y, z directions respectively
    RadialPower = [ [0 for i in range(0,u)] for j in range(0,v)]
    for x in range(0,u):
        for y in range(0,v):
            for z in range(w):
                RadialPower[x][y] += mesh_power[x+u*y+u*v*z]
    return RadialPower

def printRadialPower(RadialPower, u, v):
# RadialPower is a two-dimensional list contains the radial power factor
    string = ''
    for i in range(0,u):
        for j in range(0,v):
            string += ( '%.5f'%RadialPower[i][j] + '  ' )
            if (j == v-1):
                string += '\n'
    return string