#! /usr/bin/env python
import numpy as np
import subprocess 
import time 
#from glob import glob

def newParams(ArchParam, Ome0, OmeL, OmeB):
    #Reescribir linea 27
    l26 = ArchParam[26][0:26]
    l26 = l26 + str(Ome0)
    ArchParam[26] = l26

    l27 = ArchParam[27][0:26]
    l27 = l27 + str(OmeL)
    ArchParam[27] = l27

    l28 = ArchParam[28][0:26]
    l28 = l28 + str(OmeB)
    ArchParam[28] = l28

    with open('newparam.txt','x') as file:
        for l in ArchParam:
            file.write(l+'\n')
        file.close()

    #randomV = str( int( np.random.random(1) * 10) )
    #randomV = 'newparam' + randomV + '.txt'
    #subprocess.call(['mv','newparam.txt',randomV])

    return ArchParam

#Tomar Archivo Param.txt Base y Leerlo
with open('param.txt', 'r') as archO:
    dOrig = archO.read().splitlines()
    archO.close()
#Tomar Archivo para nuevas cosmoslogias    
with open('type.txt', 'r') as val:
    values = val.read().splitlines()[1:] #Se salta en encabezado
    val.close()


j=1
print( time.ctime() )
for newVal in  values:
    Omega0, OmegaLambda, OmegaBaryon = np.float16(newVal.split(sep=',') )
    
    s = newParams(dOrig, Omega0, OmegaLambda, OmegaBaryon)

    DirN = '../run' + str(j)
    print( time.ctime() )
    subprocess.call( [ 'mpirun', '-np', '24', './Gadget4_SubFind','newparam.txt'] )
    #subprocess.run( [ 'cat','newparam.txt'] )
    
    subprocess.run( [ 'mkdir', DirN, 'output' ] )
    subprocess.run( [ 'cp','-r','output/','newparam.txt','newparam.txt-usedvalues',DirN ] )
    subprocess.run( [ 'rm','-r', 'newparam.txt', 'output/'], )
    j += 1
    print( time.ctime() )
    # print(newVal)
    # print(Omega0, OmegaLambda, OmegaBaryon)
#ewald_table_1-1-1_64-64-64_precision8-order3.dat