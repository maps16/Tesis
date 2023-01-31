# Librerias
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cplt
import h5py as h5
from glob import glob
from scipy.stats import exponnorm as scp

# Creando Figura para plot
#NUM_COLORS = 5
fig ,ax = plt.subplots( nrows=4, ncols=5, figsize=(16,10), num='MassDistSep' )
fig2 ,ax2 = plt.subplots(nrows=1, ncols=1 ,num='MassDist', figsize=(5.5,5.5) )
NUM_COLORS = 40#len(arch)
cm1 = plt.cm.tab20(np.linspace(0,1,20))   # type: ignore
cm2 = plt.cm.tab20b(np.linspace(0,1,20))  # type: ignore
cmT = np.vstack((cm1, cm2))
cm  = cplt.LinearSegmentedColormap.from_list('Tab30', cmT)

ax2.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )

def plotAx(pos, pdata, nameData, num_bin, *param):
    '''
    Metodo para graficar en diferentes ax
    pos         Posicion del grafico en la figura
    pdata       Arreglo con los Datos 1D
    nameData    Nombre de los datos
    num_bin     Numero de Bins del Histograma
    *param      Parametros de ajuste
    '''

    X = np.linspace( np.min(pdata), np.max(pdata), 10000 )      # Puntos Para Graficar PDF
    bsz = ( np.max(pdata) - np.min(pdata) ) / bins              # Bin Size
    k, loc, scale = param[0], param[1], param[2]                # Parametros de Ajuste
    
    simple = nameData.split(',')[:3]
    simple[-1] = simple[-1].split('\n')[0]
    simplename = ''
    for string in simple:
        simplename += string + ' '
    
    plt.figure('MassDistSep')
    # Plotting Hist
    ax.flat[pos].hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False)  # type: ignore
    
    # Plotting PDF
    ax.flat[pos].plot( X, scp.pdf(X, k,loc,scale) * len(pdata) * bsz, label= nameData)  # type: ignore

    #Plot Acumulado
    plt.figure('MassDist')
    #ax2.hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False, label=simplename, alpha=0.9)
    ax2.plot( X, scp.pdf(X, k, loc, scale) * len(pdata) * bsz, label=simplename)
    
    # Ajustes de la figura
    # ax.flat[pos].set_xlim(round(np.min(pdata))  , 15.)
    # ax.flat[pos].set_ylabel("Número de halos")
    # ax.flat[pos].set_xlabel('log$_{10}$ M$_\odot$')
    ax.flat[pos].legend(loc=1)  # type: ignore
    print('Min=',min(pdata), ', Max=',max(pdata) )
    return None


# Localizacion de datos
sim = 'RunHighLam'
data_Name = 'subhalo'                                                   # Tipo de Dato
path = '/home/martin/Documentos/Tesis/WorkingData/StandardResolution'   # Ubicacion
# Identtificando el snapshot 017 del catalogo de halos
archivos = glob( path + '/' + sim + '/' + data_Name + '/*.hdf5')
archivos.sort()

temp_exit = 0
bins = 55
for i in archivos:
    
    #Abriendo el archivo
    file_data = h5.File(i, mode='r')
    if 'Subhalo' and 'Group' in file_data:

        Omega0, OmegaL, OmegaB, redshift = file_data['Parameters'].attrs['Omega0'], file_data['Parameters'].attrs['OmegaLambda'], file_data['Parameters'].attrs['OmegaBaryon'], file_data['Header'].attrs['Redshift'] # Obtenido paramtros cosmologicos
        
        # Extrayendo las masas de los halos
        mass = file_data['Subhalo']['SubhaloMass'][:] * 1e10  # type: ignore
        logmass = np.log10(mass)
        
        # Calculo de los paramtros Exponencial Normal
        k, loc, scale = scp.fit(logmass)

        # LABEL, escrito de los labels
        mean, std = scp.mean(k,loc,scale), scp.std(k,loc,scale)             #Calculo de Mean y STD
        nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) + ', ' + r'$\Omega_B=$'+str(OmegaB) + '\n  Mean =' + str(round(mean, ndigits=4)) + ', std =' + str(round(std,ndigits=4))  # type: ignore
        nameParam = 'z = ' +str( round(redshift,1) )  # type: ignore
       
        # Funcion de Ploteo Checar Funciones 
        plotAx(temp_exit, logmass, nameParam, bins, k,loc,scale, mean, std  )

        temp_exit += 1
        # print(temp_exit)
    file_data.close()

# Ajuste de la figura
plt.figure('MassDistSep')
fig.supylabel('Número de halos')
fig.supxlabel('log$_{10}$ M$_\odot$')# type: ignore
#plt.tight_layout(h_pad = hspace, w_pad=wspace ,rect=(left,bottom,right,top))
fig.tight_layout(h_pad=0.001,w_pad=0.001,rect=(0.0,0.0,1.0,1.0))
# fig.tight_layout()
ax.flat[-1].axis('off')  # type: ignore Temporalmente
# ax.flat[-2].axis('off')  # type: ignore Temporalmente
fig.savefig('Documento/images/'+sim+'/Mass_Dist_'+sim+'Sep.png')


plt.figure('MassDist')
plt.title('Distribución de masa')
ax2.legend(loc='best', ncol=2)
ax2.set_xlim(10.05,14.4)
ax2.set_ylim(-25,2900)
ax2.set_ylabel("Número de halos")
ax2.set_xlabel('log$_{10}$ M$_\odot$') # type: ignore
fig2.tight_layout( rect=(0.0, 0, 1, 1.0) )
fig2.savefig('Documento/images/'+sim+'/Mass_Dist_'+sim+'.png')

# plt.close('MassDistSep')
plt.show()