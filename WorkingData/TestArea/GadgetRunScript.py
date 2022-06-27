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
    #obteniendo los parametros ha cambiar
    Omega0, OmegaLambda, OmegaBaryon = np.float16(newVal.split(sep=',') )
    
    #Creando nuevo archivos de parametros
    s = newParams(dOrig, Omega0, OmegaLambda, OmegaBaryon)

    #Log de Tiempo
    if not (j==1) : print( time.ctime() )
    
    DirN = '../run' + str(j)  # Nombre de la carpeta de la nueva corrida

    #Correr procesos
    subprocess.run( [ 'mkdir', DirN ] ) #Creando las carpetas
    subprocess.run( [ 'mkdir', 'output' ] )
    #subprocess.call( [ 'mpirun', '-np', '24', './Gadget4_SubFind','newparam.txt'] ) #Correr GADGET4
    subprocess.run( [ 'cat','newparam.txt'] ) #TESTING RUN
    
    
    subprocess.run( [ 'cp','-r','output/','newparam.txt','newparam.txt-usedvalues',DirN ] )
    subprocess.run( [ 'rm','-r', 'newparam.txt', 'output/'], )
    j += 1

print( time.ctime() )
