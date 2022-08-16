import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
# import pynbody as pnb
from matplotlib import cm
from glob import glob

fig ,ax = plt.subplots( nrows = 1, ncols = 1, figsize = ( 9, 9 ) )

run = "RunCanonica"
data = "subhalo"
namepath = "/home/martin/Documentos/Tesis/WorkingData/StandardResolution/" + run + "/" + data

#/home/martin/Documentos/Tesis/WorkingData/StandardResolution
#Checar todos los archivos
arch = glob(namepath + '/*')
arch.sort()

Nsubh = []
redS = []
for i in arch:
    a = i.split('/')[-1]
#    print(a)
    d = a.split('_')[-1].split('.')[0]

    #OPEN FILE
    z = h5.File(namepath + "/" + a , "r")
    if 'Subhalo' and 'Group' in z:

        NTsubh = z['Header'].attrs['Nsubhalos_Total']
        redSh = z['Header'].attrs['Redshift']
        Nsubh.append(NTsubh)
        redS. append(redSh)
        print('Corrio ' + a  )
        z.close()
        #j += 1
    else:
        print('Satlo del archivo ' + a )
        z.close()

#Nsubh = np.array( (redS, Nsubh), dtype=np.int32)
print(redS, Nsubh)
ax.plot(redS, Nsubh)

fig.suptitle('Evolución del número de halos total')
ax.set_ylabel('Número Total Halos')
ax.set_xlabel('Redshift')
ax.set_xlim(15.5, -0.5)
#ax.set_xticks(np.arange( min(redS), max(redS) + 0.0 , 1.0) )
#ax.set_xticks(np.arange(15.0, 0.0, 1.0))
#ax.legend(loc=1)
#plt.xlabel('log$_{10}$ R (Mpc)')
ax.step


fig.tight_layout()
#plt.ion()
plt.show()

#/Header attrs
#<KeysViewHDF5 ['BoxSize', 'Git_commit', 'Git_date', 'Ngroups_ThisFile', 'Ngroups_Total', 'Nids_ThisFile', 'Nids_Total', 'Nsubhalos_ThisFile', 'Nsubhalos_Total', 'NumFiles', 'Redshift', 'Time']>
