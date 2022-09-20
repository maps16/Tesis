# Librerias
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from glob import glob
from scipy.stats import norm as scp

# Creando Figura para plot
#NUM_COLORS = 5
fig ,ax = plt.subplots( nrows=4, ncols=5, figsize=(16,10), num='HalfMassRadDistCanonRunSep' )
fig2 ,ax2 = plt.subplots(nrows=1, ncols=1 ,num='HalfMassRadDistCanonRun', figsize=(5.75,5.75) )
NUM_COLORS = 20#len(arch)
cm =  plt.get_cmap('tab20')
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

    X = np.linspace( np.min(logmass), np.max(logmass), 10000 )  # Puntos Para Graficar PDF
    bsz = ( np.max(logmass) - np.min(logmass) ) / bins          # Bin Size
    loc, scale = param[0], param[1]                             # Parametros de Ajuste
    
    simple = nameData.split(',')[:3]
    simple[-1] = simple[-1].split('\n')[0]
    simplename = ''
    for string in simple:
        simplename += string + ' '
    
    plt.figure('HalfMassRadDistCanonRunSep')
    # Plotting Hist
    ax.flat[pos].hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False)
    
    # Plotting PDF
    ax.flat[pos].plot( X, scp.pdf(X, loc,scale) * len(pdata) * bsz, label= nameData)

    #Plot Acumulado
    plt.figure('HalfMassRadDistCanonRun')
    #ax2.hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False, label=simplename, alpha=0.9)
    ax2.plot( X, scp.pdf(X, loc, scale) * len(pdata) * bsz, label=simplename)
    
    # Ajustes de la figura
    #ax.flat[pos].set_xlim(round(np.min(pdata))  , 15.)
    ax.flat[pos].set_ylabel("Número de halos")
    ax.flat[pos].set_xlabel('log$_{10}$ M$_\odot$')
    ax.flat[pos].legend(loc=1)
    
    return None


# Localizacion de datos
data_Name = 'subhalo'                                                   # Tipo de Dato
path = '/home/martin/Documentos/Tesis/WorkingData/StandardResolution'   # Ubicacion
# Identtificando el snapshot 017 del catalogo de halos
archivos = glob( path + '/RunCanonica/' + data_Name + '/*.hdf5')
archivos.sort()

temp_exit = 0
bins = 55
for i in archivos:
    
        #Abriendo el archivo
    file_data = h5.File(i, mode='r')
    if 'Subhalo' and 'Group' in file_data:

        Omega0, OmegaL, OmegaB, redshift = file_data['Parameters'].attrs['Omega0'], file_data['Parameters'].attrs['OmegaLambda'], file_data['Parameters'].attrs['OmegaBaryon'], file_data['Header'].attrs['Redshift'] # Obtenido paramtros cosmologicos
        
        # Extrayendo las masas de los halos
        mass = file_data['Subhalo']['SubhaloHalfmassRad'][:] * 1e10
        logmass = np.log10(mass)
        
        # Calculo de los paramtros Exponencial Normal
        loc, scale = scp.fit(logmass)

        # LABEL, escrito de los labels
        mean, std = scp.mean(loc,scale), scp.std(loc,scale)             #Calculo de Mean y STD
        nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) + ', ' + r'$\Omega_B=$'+str(OmegaB) + '\n  Mean =' + str(round(mean, ndigits=4)) + ', std =' + str(round(std,ndigits=4))
        nameParam = 'z = ' +str( round(redshift,1) )
    

        # Funcion de Ploteo Checar Funciones 
        plotAx(temp_exit, logmass, nameParam, bins, loc,scale, mean, std  )

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
plt.figure('HalfMassRadDistCanonRunSep')
#plt.tight_layout(h_pad = hspace, w_pad=wspace ,rect=(left,bottom,right,top))
plt.tight_layout(h_pad=0.001,w_pad=0.001,rect=(0.0,0.0,1.0,1.0))
# plt.tight_layout()
plt.savefig('Documento/images/HalfMassRadDistCanonRunSep.png')


plt.figure('HalfMassRadDistCanonRun')
plt.title('Distribución de masa')
ax2.legend(loc='best')
ax2.set_xlim(7.2,9.7)
ax2.set_ylim(-25,2200)
ax2.set_ylabel("Número de halos")
ax2.set_xlabel('log$_{10}$ M$_\odot$')
plt.tight_layout()
plt.savefig('Documento/images/HalfMassRadDistCanonRun.png')

plt.close('all')
#plt.show()
'''
top=0.988,
bottom=0.048,
left=0.031,
right=0.991,
hspace=0.108,
wspace=0.116
'''