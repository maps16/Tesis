#===============================================================================
# Script para transformar snapshots de GADGET-4 HDF5 a snapshot de GADGET-2
#   Usando pynbody (En Teoria funciona de cualquier formato a GADGET-2)
#                               Martin Paredes
#===============================================================================
# LIBRERIAS
import glob as gl
import pynbody as pnb
import numpy as np
import subprocess as subp
import time

#FUNCION PARA CAMBIAR EL FORMATO
def change(data): #data es el string del nombre del archivo (direccion del archivo)
    s = pnb.load(data) #CARGAR SNAPSHOT ORIGINAL
    ndat = str.split(data,'.')[0] # Tomando el nombre de salida para el snapshot a Gadget-2 (se puede usar algo diferente)
    s.write(filename = ndat, fmt = pnb.gadget.GadgetSnap) # CAMBIAR EL FORMATO
    subp.call( [ 'mv', ndat, '/home/martin/Documentos/Tesis/Corridas/CorridasServidor/Run1/gadget2/.' ]  ) #MOVERLO A LA CARPETA DESEADA

#Cargar lista de nombre de archivos
arch = gl.glob('/home/martin/Documentos/Tesis/Corridas/CorridasServidor/Run1/gadget4/snapshot*', recursive = False)

for i in arch:
    change(i) #LLAMAR FUNCION
    print(time.ctime()) # Ver tiempos de cuando termino de correr
