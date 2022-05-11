import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

fig ,ax = plt.subplots( nrows=1, ncols=1,figsize=(12,12) )
run = "Run8"
data = "fofsubhalo"
namepath = "/home/martin/Documentos/Tesis/WorkingData/" + run + "/" + data

# #CHECK FOR TYPE OF DATA
# if data == "fofsubhalo":
#     fileprefix = "/fof_subhalo_tab_"
# if data == "snaps":
#     fileprefix = "/snapshot_"
# if data == "subhalo":
#     print( "Not implemented" )

#Checar todos los archivos
arch = glob(namepath + '/*')
arch.sort()
for i in arch:
    a = i.split('/')[-1]
#    print(a)
    d = a.split('_')[-1].split('.')[0]


    #OPEN FILE
    z = h5.File(namepath + "/" + a , "r")
    if 'Subhalo' and 'Group' in z:
#HDF5 KEYS
#Config, Header, Parameter, Group, IDs, Subhalo
#['GroupAscale', 'GroupFirstSub', 'GroupLen', 'GroupLenType', 'GroupMass', 'GroupMassType', 'GroupNsubs', 'GroupOffsetType', 'GroupPos', 'GroupVel', 'Group_M_Crit200', 'Group_M_Crit500', 'Group_M_Mean200', 'Group_M_TopHat200', 'Group_R_Crit200', 'Group_R_Crit500', 'Group_R_Mean200', 'Group_R_TopHat200']
#['SubhaloCM', 'SubhaloGroupNr', 'SubhaloHalfmassRad', 'SubhaloHalfmassRadType', 'SubhaloIDMostbound', 'SubhaloLen', 'SubhaloLenType', 'SubhaloMass', 'SubhaloMassType', 'SubhaloOffsetType', 'SubhaloParentRank', 'SubhaloPos', 'SubhaloRankInGr', 'SubhaloSpin', 'SubhaloVel', 'SubhaloVelDisp', 'SubhaloVmax', 'SubhaloVmaxRad']
        #
        zMass = z['Subhalo']['SubhaloMass'][:] * 1e10
        log10zMass = np.log10(zMass)

        #PLOTTING
        ax.hist(log10zMass, bins = 55, range = (10.0,14.5), label = 'z' + d)

        print('Corrio ' + a)
        z.close()
    else:
        print('Satlo del archivo ' + a)
        z.close()

fig.suptitle('Distribucion de masa de Halos de Materia oscura')
plt.ylabel('N Bin')
plt.xlabel('log$_{10}$ M$_\odot$')
fig.tight_layout()
fig.legend()

#plt.ion()
plt.show()
