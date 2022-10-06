# Librerias
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from glob import glob
from scipy.stats import norm as scp

# Creando Figura para plot
#NUM_COLORS = 5
fig ,ax = plt.subplots( nrows=3, ncols=6, figsize=(16,10), num='HalfMassRad-Dist-Sep' )
fig2 ,ax2 = plt.subplots(nrows=1, ncols=1 ,num='HalfMassRad-Dist', figsize=(5.5,5.5) )
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
    
    plt.figure('HalfMassRad-Dist-Sep')
    # Plotting Hist
    ax.flat[pos].hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False)
    
    # Plotting PDF
    ax.flat[pos].plot( X, scp.pdf(X,loc,scale) * len(pdata) * bsz, label= nameData)

    #Plot Acumulado
    plt.figure('HalfMassRad-Dist')
    #ax2.hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False, label=simplename, alpha=0.9)
    ax2.plot( X, scp.pdf(X,loc, scale) * len(pdata) * bsz, label=simplename)
    
    # Ajustes de la figura
    # ax.flat[pos].set_xlim(round(np.min(pdata))  , 15.)
    # ax.flat[pos].set_ylabel("Número de halos")
    # ax.flat[pos].set_xlabel('log$_{10}$Kpc')
    ax.flat[pos].legend(loc=1)
    
    return None


# Localizacion de datos
sim = 'RunInvertida'
data_Name = 'subhalo'                                                   # Tipo de Dato
path = '/home/martin/Documentos/Tesis/WorkingData/StandardResolution'   # Ubicacion
# Identtificando el snapshot 017 del catalogo de halos
archivos = glob( path + '/'+sim+'/' + data_Name + '/*.hdf5')
archivos.sort()

temp_exit = 0
bins = 55
for i in archivos:
    
        #Abriendo el archivo
    file_data = h5.File(i, mode='r')
    if 'Subhalo' and 'Group' in file_data:

        Omega0, OmegaL, OmegaB, redshift = file_data['Parameters'].attrs['Omega0'], file_data['Parameters'].attrs['OmegaLambda'], file_data['Parameters'].attrs['OmegaBaryon'], file_data['Header'].attrs['Redshift'] # Obtenido paramtros cosmologicos
        
        # Extrayendo las masas de los halos
        mass = file_data['Subhalo']['SubhaloHalfmassRad'][:] * 1e03
        logmass = np.log10(mass)
        
        # Calculo de los paramtros Exponencial Normal
        loc, scale = scp.fit(logmass)

        # LABEL, escrito de los labels
        mean, std = scp.mean(loc,scale), scp.std(loc,scale)             #Calculo de Mean y STD
        nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) + ', ' + r'$\Omega_B=$'+str(OmegaB) + '\n  Mean =' + str(round(mean, ndigits=4)) + ', std =' + str(round(std,ndigits=4))
        nameParam = 'z = ' +str( round(redshift,1) )
    

        # Funcion de Ploteo Checar Funciones 
        plotAx(temp_exit, logmass, nameParam, bins, loc,scale, mean, std  )

        temp_exit += 1
    file_data.close()

# Ajuste de la figura
plt.figure('HalfMassRad-Dist-Sep')
fig.supxlabel('log$_{10}$Kpc')
fig.supylabel('Número de halos')
#plt.tight_layout(h_pad = hspace, w_pad=wspace ,rect=(left,bottom,right,top))
fig.tight_layout(h_pad=0.001,w_pad=0.001,rect=(0.0,0.0,1.0,1.0))
# plt.tight_layout()
plt.savefig('Documento/images/'+sim+'/HalfMassRad_Dist_'+sim+'Sep.png')


plt.figure('HalfMassRad-Dist')
plt.title('Radio que contine la mitad de la masa')
ax2.legend(loc='best')
ax2.set_xlim(0.2, 2.8)
ax2.set_ylim(-15,2200)
ax2.set_ylabel("Número de halos")
ax2.set_xlabel('log$_{10}$ Kpc')
fig2.tight_layout()
plt.savefig('Documento/images/'+sim+'/HalfMassRad_Dist_'+ sim +'.png')

# plt.close('all')
plt.show()