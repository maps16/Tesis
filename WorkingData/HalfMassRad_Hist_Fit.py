# Librerias
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cplt
import h5py as h5
from glob import glob
from scipy.stats import norm as scp

# Creando Figura para plot
#NUM_COLORS = 5
fig ,ax = plt.subplots( nrows=4, ncols=5, figsize=(16,10), num='HalfMassRad-Dist-Sep' )
fig2 ,ax2 = plt.subplots(nrows=1, ncols=1 ,num='HalfMassRad-Dist', figsize=(6.5,6.5) )
NUM_COLORS = 40#len(arch)
cm1 = plt.cm.tab20(np.linspace(0,1,20))   # type: ignore
cm2 = plt.cm.tab20b(np.linspace(0,1,20))  # type: ignore
cmT = np.vstack((cm1, cm2))
cm  = cplt.LinearSegmentedColormap.from_list('Tab30', cmT)

ax2.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)] )

LEGEND_SIZE= 10
TICK_SIZE = 13
DEFAULT=9
SMALL_SIZE = 2
MEDIUM_SIZE = 18
BIGGER_SIZE = 16

plt.rc('font', size=DEFAULT)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=LEGEND_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

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
    loc, scale = param[0], param[1]                             # Parametros de Ajuste
    
    simple = nameData.split(',')[:3]
    simple[-1] = simple[-1].split('\n')[0]
    simplename = ''
    for string in simple:
        simplename += string + ' '
    
    plt.figure('HalfMassRad-Dist-Sep')
    # Plotting Hist
    ax.flat[pos].hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False)  # type: ignore
    
    # Plotting PDF
    ax.flat[pos].plot( X, scp.pdf(X, loc, scale) * len(pdata) * bsz, label= nameData)  # type: ignore

    #Plot Acumulado
    plt.figure('HalfMassRad-Dist')
    #ax2.hist(pdata , bins=num_bin, range=(np.min(pdata),np.max(pdata)), density = False, label=simplename, alpha=0.9)
    ax2.plot( X, scp.pdf(X, loc, scale) * len(pdata) * bsz, label=simplename)
    
    """     # Ajustes de la figura
    if(np.max(pdata)>=12.8): 
        ax.flat[pos].set_xlim(round(np.min(pdata)) , 12.8)

    if(np.max(pdata)<12.8): 
        #ax.flat[pos].set_xlim(np.min(pdata)-0.1  , np.max(pdata)+0.1 )
        print('sup') """

    # ax.flat[pos].set_ylabel("Número de halos")
    # ax.flat[pos].set_xlabel('log$_{10}$Kpc')
    ax.flat[pos].tick_params(axis='x', labelsize=TICK_SIZE)
    ax.flat[pos].tick_params(axis='y', labelsize=TICK_SIZE)
    ax.flat[pos].legend(loc=1)  # type: ignore
    print('z =', nameData ,', Min =',min(pdata), ', Max =',max(pdata) )
    return None


# Localizacion de datos
sim = 'RunCanonica'
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
        mass = file_data['Subhalo']['SubhaloHalfmassRad'][:] * 1e03  # type: ignore
        logmass = np.log10(mass)

        # Calculo de los paramtros Exponencial Normal
        loc, scale = scp.fit(logmass)

        # LABEL, escrito de los labels
        mean, std = scp.mean(loc,scale), scp.std(loc,scale)             #Calculo de Mean y STD
        nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) + ', ' + r'$\Omega_B=$'+str(OmegaB) + '\n  Mean =' + str(round(mean, ndigits=4)) + ', std =' + str(round(std,ndigits=4))  # type: ignore
        nameParam = 'z = ' +str( round(redshift,1) )  # type: ignore

        # Funcion de Ploteo Checar Funciones 
        plotAx(temp_exit, logmass, nameParam, bins, loc,scale, mean, std  )

        temp_exit += 1
        # print(temp_exit)
    file_data.close()

# Ajuste de la figura
plt.figure('HalfMassRad-Dist-Sep')
fig.supylabel('Número de halos')
fig.supxlabel('log$_{10}$r/Kpc')
#plt.tight_layout(h_pad = hspace, w_pad=wspace ,rect=(left,bottom,right,top))
fig.tight_layout(h_pad=0.001,w_pad=0.001,rect=(0.0,0.0,1.0,1.0))
# plt.tight_layout()
#ax.flat[-1].axis('off')  # type: ignore Temporalmente
#ax.flat[-2].axis('off')  # type: ignore Temporalmente
fig.savefig('Documento/images/'+sim+'/HalfMassRad_Dist_'+sim+'Sep.png')


plt.figure('HalfMassRad-Dist')
plt.title('Radio que contine la mitad de la masa')
ax2.legend(loc='best', ncol=2, columnspacing=0.5 )
ax2.set_xlim(0.2, 2.75)
ax2.set_ylim(-15,2200)
ax2.tick_params(axis='x', labelsize=TICK_SIZE)
ax2.tick_params(axis='y', labelsize=TICK_SIZE)
fig2.supylabel("Número de halos")
fig2.supxlabel('log$_{10}$ r/Kpc')
fig2.tight_layout()
fig2.savefig('Documento/images/'+sim+'/HalfMassRad_Dist_'+sim+'.png')

# plt.close('all')
plt.show()