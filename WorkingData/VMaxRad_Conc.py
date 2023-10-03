import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from glob import glob
from scipy.stats import norm as scp

#Generando Figura
fig1, ax1 = plt.subplots( nrows=1, ncols=1, num='mean', figsize=(6,6) )
fig2, ax2 = plt.subplots( nrows=1, ncols=1, num='std', figsize=(6,6) )

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


# Loc de archivos para trabajar
# sim = 'RunHighLam'
data = 'subhalo'
dataParam = 'SubhaloVmaxRad'

# Ubicando las carpetas de las diferentes Cosmologias
run = glob('WorkingData/StandardResolution/*')
run.sort()

# Extableciendo/Limpiendo los arrays para diferentes valores de interes
mean = []       # Media
std  = []       # Desviacion Estandar
z = []          # Redshift
nameParam = ''

# Corriendo sobre las diferentes Cosmologias
for x in run:

    # Limpiando las listas para las nuevas Cosmologias
    mean.clear()
    std.clear()
    z.clear()

    # Identificando todos los archivos dentro de las Cosmologias
    namepath = '/home/martin/Documentos/Tesis/' + x + '/' + data
    arch = glob(namepath + '/*')
    arch.sort()

    # Iterar sobre todos los archivos
    for y in arch:

        # Abrir los HDF5
        file_data = h5.File(y, mode='r')

        # Trabajando solo con los archivos que contienen subhalos
        if 'Subhalo' and 'Group' in file_data:
            
            # Extrayendo parametros de la simulación
            Omega0, OmegaL, OmegaB, z_cal = file_data['Parameters'].attrs['Omega0'], file_data['Parameters'].attrs['OmegaLambda'], file_data['Parameters'].attrs['OmegaBaryon'], file_data[ 'Header' ].attrs[ 'Redshift' ]

            # Label identificando cada cosmologia
            nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) 

            # Extrayendo el dato deseado
            got_data = file_data['Subhalo'][dataParam][:] * 1e03 # type: ignore
            

            # Buscando Ajuste
            loc, scale = scp.fit(got_data,)
            mean_cal, std_cal = scp.mean(loc,scale), scp.std(loc,scale) # Calculo de media y std

            # Guardando los valoares en los arrays
            mean.append(mean_cal)
            std.append(std_cal)
            z.append(z_cal)

            # print('z=',round(z_cal,ndigits=2),', mean=',round(mean_cal, ndigits=2),', std=',round(std_cal,ndigits=2), sep=' ')    # type: ignore

        file_data.close()

    if len(mean) != 0 : 
        ax1.plot(z, mean, label=nameParam, marker='o') 
    if len(std) != 0: 
        ax2.plot(z, std, label=nameParam, marker='o') 
    print(x.split('/')[-1],', z=',round(z[-1],ndigits=0),', mean=',round(mean[-1],ndigits=2), ', std=', round(std[-1],ndigits=2),', z=',round(z[1],ndigits=0),', mean=',round(mean[1],ndigits=2), ', std=', round(std[1],ndigits=2))

fig1.supxlabel('z')
fig2.supxlabel('z')
fig1.supylabel('$\mu$ (r/Kpc)')# type: ignore
fig2.supylabel('$\sigma$(r/Kpc)')# type: ignore
ax1.tick_params(axis='x', labelsize=TICK_SIZE)
ax1.tick_params(axis='y', labelsize=TICK_SIZE)
ax2.tick_params(axis='x', labelsize=TICK_SIZE)
ax2.tick_params(axis='y', labelsize=TICK_SIZE)
ax1.set_xlim(round(max(z),ndigits=0) + 0.5,-0.2)
ax2.set_xlim(round(max(z),ndigits=0) + 0.5,-0.2)
ax1.legend(loc='best')
ax2.legend(loc='best')

fig1.tight_layout()
fig1.savefig('Documento/images/Conc/VMaxRad_Mean_Conc.png')
fig2.tight_layout()
fig2.savefig('Documento/images/Conc/VMaxRad_Std_Conc.png')
plt.show()