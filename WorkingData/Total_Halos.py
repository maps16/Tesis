import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
# import pynbody as pnb
from matplotlib import cm
from glob import glob

fig ,ax = plt.subplots( nrows = 1, ncols = 1, figsize = ( 5, 5 ) )

run = "RunHighLam"
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
        redS.append(redSh)
        print('Corrio ' , a , ', Total =' , NTsubh, ', z=',redSh )
        z.close()
        #j += 1
    else:
        print('Satlo del archivo ' + a )
        z.close()
print('Primeros Halos en z= ', round( max(redS), 0), ', Total de Corridas =', len(redS)  )
#Nsubh = np.array( (redS, Nsubh), dtype=np.int32)
# print(redS, Nsubh)
ax.plot(redS, Nsubh,'o-')

fig.suptitle('Evolución del número de halos total')
ax.set_ylabel('Total Halos')
ax.set_xlabel('Redshift (z)')
ax.set_xlim(round( max(redS), 0 )+.5, -0.5)

fig.tight_layout()
plt.savefig('Documento/images/'+run+'/TotalHalos_'+run+'.png')
# plt.close('all')
plt.show()