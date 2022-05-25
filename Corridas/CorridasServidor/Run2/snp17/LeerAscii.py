#! /usr/bin/env python
#IMPORTACION DE LIBRERIAS
import numpy as np
import matplotlib.pyplot as plt
import h5py

#DEFINICION DE FUNCIONES

#LECTURA DE Archivo Ascii
arch = '/home/martin/Documentos/Tesis/Corridas/CorridasServidor/Run2/snp17/halos_0.0.ascii'
datos = np.genfromtxt(arch)

#datos[:, 0] -> Id
#datos[:, 1] -> NumPart
#datos[:, 2] -> mvir
#datos[:, 3] -> mbound_vir
#datos[:, 4] -> rvir
#datos[:, 8] -> x
#datos[:, 9] -> y
#datos[:,10] -> z



#etc checar halos_0.0.ascii
plt.ion()
#fig, ax = plt.subplots()
#ax.hist(datos[:, 2], bins =5200, range = (636700000, 174100000000000 ))


#bins = 5200

n = 3
#print( np.argsort(datos[:,2])[-n:] )
#print( datos[:, 0][np.argsort(datos[:,2])[-n:]] ) #Id
#print( datos[:, 1][np.argsort(datos[:,2])[-n:]] ) #NumPart
#print( datos[:, 2][np.argsort(datos[:,2])[-n:]] ) #mvir
#print( datos[:, 4][np.argsort(datos[:,2])[-n:]] ) #rvir
#print( datos[:, 8][np.argsort(datos[:,2])[-n:]] ) #x
#print( datos[:, 9][np.argsort(datos[:,2])[-n:]] ) #y
#print( datos[:,10][np.argsort(datos[:,2])[-n:]] ) #z

#/home/martin/Documentos/Tesis/Corridas/CorridasServidor/Run1/fof_tab_017.hdf5
fof = h5py.File('/home/martin/Documentos/Tesis/Corridas/CorridasServidor/Run2/fof_tab_017.hdf5', 'r')
fof.keys() #MUESTRA GRUPOS DE INFO
fofGr = fof['Group'] # EN "Group" SE ENCUENTRA TODA LA INFORMACION RELEVANTE A FOF
fofGr.keys() #<KeysViewHDF5 ['GroupAscale', 'GroupLen', 'GroupLenType', 'GroupMass', 'GroupMassType', 'GroupOffsetType', 'GroupPos', 'GroupVel']>
Massfof = fofGr['GroupMass']
Massfof[:] #ACCEDER A LOS DATOS DEL ARREGLO DE MASA
#fig2, ax2 = plt.subplots()
#ax2.hist(Massfof[:], bins =5200)


#massP = 9.3918816e+08 #Run1
massP = 2.1101243e+09 #Run2
#ROCKSTAR
log10Mass= np.log10( datos[:,1] * massP ) #MASA EN LOGARITMO10
fig, ax = plt.subplots()
ax.hist(log10Mass, bins = 12, range = ( 8.5, 14.5), label ='Rockstar Galaxies' )
plt.ylabel('N Bin')
plt.xlabel('log$_{10}$M$_\odot$')

#GADGET FOF
Massfof10 = Massfof[:] * 1e10 #CAMBIO DE UNIDADES
log10Massfof10 = np.log10(Massfof10)
ax.hist(log10Massfof10, bins = 12, range = ( 8.5, 14.5) , label= 'GADGET4 FoF')

ax.legend()

plt.show()
