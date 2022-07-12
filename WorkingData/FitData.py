import numpy as np
import matplotlib.pylab as plt
import h5py as h5
from scipy.optimize import fmin
import scipy.stats as scp
from glob import glob

# GENERAR  FIGURA
fig ,ax = plt.subplots( nrows=3, ncols=4,figsize=(32,18) )

# ASIGNADO MAPA DE COLORES
NUM_COLORS = 11
cm =  plt.get_cmap('gist_gray')
ax[-1,-1].set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )
#ax.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )

# Define loss_f function.
def loss_f(params, data_in):

    mu = params[0]
    loss = 0
    
    for i in range( len(data_in) ):

        loglikelihood = scp.poisson.logpmf(data_in[i], mu)
        loss_to_add = - loglikelihood
        loss += loss_to_add 

    return loss

def plotAx(pos, pdata, nameData):

    ax.flat[pos].set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )
    ax.flat[pos].hist(pdata , bins=55, range=(10.0,14.5), label=nameData, density = False)
    ax.flat[pos].set_ylabel("N bin")
    ax.flat[pos].set_xlabel('log$_{10}$ M$_\odot$')
    #ax.flat[pos].set_ylim(0,7500)
    ax.flat[pos].legend(loc=1)
    ax.flat[-1].hist(pdata , bins=55, range=(10.0,14.5), label=nameData, density = False)

    return None


run = "RunCanonica"
data = "subhalo"
namepath = "/home/martin/Documentos/Tesis/WorkingData/StandardResolution/" + run + "/" + data

#Checar todos los archivos / GENERAR LISTA DE LOS ARCHIVOS ENCONTRADOS
arch = glob(namepath + '/*')
arch.sort()

j = 0
for i in arch:
    a = i.split('/')[-1] #Selecion del archivo

    #OPEN FILE
    z = h5.File(namepath + "/" + a , "r")
    d = str( round( z[ 'Header' ].attrs[ 'Redshift' ],  ndigits = 2 ) ) #OBTENCION DE REDSHIFT A DOS DECIMALES
    if 'Subhalo' and 'Group' in z:

        zMass = z['Subhalo']['SubhaloMass'][:] * 1e10
        log10zMass = np.log10(zMass)

        #param0 = np.array( [1.], dtype=np.float64 )  # PARAMETER GUESS
        #mini = fmin( loss_f, param0, args=(log10zMass,) )
        #lamd = mini[0] # PARAMETER SELEC
        
        
        
        
        #PLOTTING
        plotAx(pos=j, pdata=log10zMass, nameData='z = ' + d )
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