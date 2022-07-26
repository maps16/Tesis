# Librerias
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from glob import glob
from scipy.stats import exponnorm as scp

# Creando Figura para plot
#NUM_COLORS = 5
fig ,ax = plt.subplots( nrows=3, ncols=3, figsize=(16,10) )
#cm =  plt.get_cmap('gist_gray')
#ax[-1,-1].set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )

def plotAx(pos, pdata, nameData, num_bin, *param):
    '''
    Metodo para graficar en diferentes ax
    pos         Posicion del grafico en la figura
    pdata       Arreglo con los Datos 1D
    nameData    Nombre de los datos
    num_bin     Numero de Bins del Histograma
    *param      Parametros de ajuste
    '''

    X = np.linspace( np.min(logmass), np.max(logmass), 10000 )  # Puntos Para Graficar PDF
    bsz = ( np.max(logmass) - np.min(logmass) ) / bins          # Bin Size
    k, loc, scale = param[0], param[1], param[2]                # Parametros de Ajuste
    
    simple = nameData.split(',')[:3]
    simple[-1] = simple[-1].split('\n')[0]
    simplename = ''
    for string in simple:
        simplename += string + ' '
    

    # Plotting Hist
    ax.flat[pos].hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False)
    
    # Plotting PDF
    ax.flat[pos].plot( X, scp.pdf(X, k,loc,scale) * len(pdata) * bsz, label= nameData)

    #Plot Acumulado
    ax[-1,-1].hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False, label=simplename, alpha=0.5)
    
    # Ajustes de la figura
    #ax.flat[pos].set_xlim(round(np.min(pdata))  , 15.)
    ax.flat[pos].set_ylabel("N bin")
    ax.flat[pos].set_xlabel('log$_{10}$ M$_\odot$')
    ax.flat[pos].legend(loc=1)
    
    return None


# Localizacion de datos
data_Name = 'subhalo'                                                   # Tipo de Dato
path = '/home/martin/Documentos/Tesis/WorkingData/StandardResolution'   # Ubicacion
# Identtificando el snapshot 017 del catalogo de halos
archivos = glob( path + '/*/' + data_Name + '/*017.hdf5')
archivos.sort()

temp_exit = 0
bins = 55
for i in archivos:

    #Abriendo el archivo
    file_data = h5.File(i, mode='r')
    Omega0, OmegaL, OmegaB = file_data['Parameters'].attrs['Omega0'], file_data['Parameters'].attrs['OmegaLambda'], file_data['Parameters'].attrs['OmegaBaryon'] # Obtenido paramtros cosmologicos
    
    # Extrayendo las masas de los halos
    mass = file_data['Subhalo']['SubhaloMass'][:] * 1e10
    logmass = np.log10(mass)
    
    # Calculo de los paramtros Exponencial Normal
    k, loc, scale = scp.fit(logmass)

    # LABEL, escrito de los labels
    mean, std = scp.mean(k,loc,scale), scp.std(k,loc,scale)             #Calculo de Mean y STD
    nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) + ', ' + r'$\Omega_B=$'+str(OmegaB) + '\n  Mean =' + str(round(mean, ndigits=4)) + ', std =' + str(round(std,ndigits=4))

   

    # Funcion de Ploteo Checar Funciones 
    plotAx(temp_exit, logmass, nameParam, bins, k,loc,scale, mean, std  )

    #Calculo de Media, STD en pantalla
    # print('Mean: ' +  str( mean ) )
    # print('STD : ' +  str( std ) )

    # Debug
    # print( logmass )
    # print(Omega0, OmegaL, OmegaB , Omega0+OmegaB+OmegaL)
    # if temp_exit == 0:
    #     plt.legend(loc=1)
    #     plt.show() # Uncomment for only one run
    #     exit()
    temp_exit += 1
    file_data.close()

# Ajuste de la figura
ax.flat[-1].legend(loc=1)
ax.flat[-1].set_xlim(9.9,15.)
ax.flat[-1].set_ylabel("N bin")
ax.flat[-1].set_xlabel('log$_{10}$ M$_\odot$')
#plt.tight_layout(h_pad = hspace, w_pad=wspace ,rect=(left,bottom,right,top))
plt.tight_layout(h_pad=0.108,w_pad=0.116,rect=(0.0,0.0,1.0,1.0))
plt.show()
'''
top=0.988,
bottom=0.048,
left=0.031,
right=0.991,
hspace=0.108,
wspace=0.116
'''
