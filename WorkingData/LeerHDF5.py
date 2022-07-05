import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from glob import glob

fig ,ax = plt.subplots( nrows=3, ncols=4,figsize=(32,18) )
#Asignando Mas Colores
NUM_COLORS = 11#len(arch)
cm =  plt.get_cmap('gist_gray')
ax[-1,-1].set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )
#ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )

def plotAx(pos, pdata, nameData):

    ax.flat[pos].set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )
    ax.flat[pos].hist(pdata , bins=55, range=(10.0,14.5), label=nameData)
    ax.flat[pos].set_ylabel("N bin")
    ax.flat[pos].set_xlabel('log$_{10}$ M$_\odot$')
    ax.flat[pos].set_ylim(0,7500)
    ax.flat[pos].legend(loc=1)
    ax.flat[-1].hist(pdata , bins=55, range=(10.0,14.5), label=nameData)

    return None



run = "RunCanonica"
data = "subhalo"
namepath = "/home/martin/Documentos/Tesis/WorkingData/StandardResolution/" + run + "/" + data


#Checar todos los archivos
arch = glob(namepath + '/*')
arch.sort()


j = 0
for i in arch:
    a = i.split('/')[-1] #Selecion del archivo
#    print(a)
#    d = a.split('_')[-1].split('.')[0]

    #OPEN FILE
    z = h5.File(namepath + "/" + a , "r")
    d = str( round( z[ 'Header' ].attrs[ 'Redshift' ],  ndigits = 2 ) ) #OBTENCION DE REDSHIFT A DOS DECIMALES
    if 'Subhalo' and 'Group' in z:
#HDF5 KEYS
#Config, Header, Parameter, Group, IDs, Subhalo
#['GroupAscale', 'GroupFirstSub', 'GroupLen', 'GroupLenType', 'GroupMass', 'GroupMassType', 'GroupNsubs', 'GroupOffsetType', 'GroupPos', 'GroupVel', 'Group_M_Crit200', 'Group_M_Crit500', 'Group_M_Mean200', 'Group_M_TopHat200', 'Group_R_Crit200', 'Group_R_Crit500', 'Group_R_Mean200', 'Group_R_TopHat200']
#['SubhaloCM', 'SubhaloGroupNr', 'SubhaloHalfmassRad', 'SubhaloHalfmassRadType', 'SubhaloIDMostbound', 'SubhaloLen', 'SubhaloLenType', 'SubhaloMass', 'SubhaloMassType', 'SubhaloOffsetType', 'SubhaloParentRank', 'SubhaloPos', 'SubhaloRankInGr', 'SubhaloSpin', 'SubhaloVel', 'SubhaloVelDisp', 'SubhaloVmax', 'SubhaloVmaxRad']
        #zMass = z['Subhalo']['SubhaloHalfmassRad'][:] # * 1e10
        zMass = z['Subhalo']['SubhaloMass'][:] * 1e10
        log10zMass = np.log10(zMass)

        #PLOTTING
        plotAx(pos=j, pdata=log10zMass, nameData='z = ' + d )
        #ax.hist(log10zMass, bins = 55, range = (10.0,14.5), label = 'z' + d)
        #ax.hist(log10zMass, bins = 55, label = 'z' + d)

        print('Corrio ' + a + ', j=' + str(j) )
        
        z.close()
        j += 1
    else:
        print('Satlo del archivo ' + a + ', j=' + str(j))
        z.close()

fig.suptitle('Distribución de masa de Halos de Materia oscura')
ax.flat[-1].set_ylabel('N Bin')
ax.flat[-1].set_xlabel('log$_{10}$ M$_\odot$')
ax[-1,-1].legend(loc=1)
#plt.xlabel('log$_{10}$ R (Mpc)')



fig.tight_layout()
plt.show()


""" top=0.959,
bottom=0.057,
left=0.03,
right=0.997,
hspace=0.18,
wspace=0.18 """