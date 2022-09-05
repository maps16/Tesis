import numpy as np
from glob import glob
from scipy.stats import norm as scp
import matplotlib.pyplot as plt
import h5py as h5

#Generando Figuras
fig1, ax1 = plt.subplots( nrows=1, ncols=1, num='mean', figsize=(5.5,5.5) )
fig2 ,ax2 = plt.subplots( nrows=1, ncols=1, num='std', figsize=(5.5,5.5) )

# Loc de archivos para trabajar
data = "subhalo"
run = glob('WorkingData/StandardResolution/*') #Ubicanco las carpetas de las diferentes cosmologias
run.sort()
run = range(1)

# Corriendo sobre las diferentes cosmologias
for x in run:
    # x = x.split('/')[-1]
    namepath = "/home/martin/Documentos/Tesis/WorkingData/StandardResolution/" + 'RunCanonica' + "/" + data
   
    #Checar todos los archivos
    arch = glob(namepath + '/*')
    arch.sort()

    # Extableciendo/Limpiendo los arrays para diferentes valores de interes
    mean = []       # Media
    std  = []       # Desviacion Estandar
    z = []       # Redshift

    # Iterar sobre todos los archivos
    for i in arch:

        # Accediendo al archivo
        file_data = h5.File(i, 'r')

        # Trabajando solo con los archivos que contienen subhalos
        if 'Subhalo' and 'Group' in file_data:
            
            # Extrayendo parametros de la simulación
            Omega0, OmegaL, OmegaB, z_cal = file_data['Parameters'].attrs['Omega0'], file_data['Parameters'].attrs['OmegaLambda'], file_data['Parameters'].attrs['OmegaBaryon'], file_data[ 'Header' ].attrs[ 'Redshift' ]
            
            # Label identificando cada cosmologia
            nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) #+ ', ' + r'$\Omega_B=$'+str(OmegaB) 
            
            # Extrayendo la masa y calculando su Log10
            logmass = np.log10( file_data['Subhalo']['SubhaloMass'][:] * 1e10)

            # Calculado los parametros para el ajuste
            loc, scale = scp.fit(logmass,)
            # Calculo de la media y desviacion estandar
            mean_cal, std_cal = scp.mean(loc,scale), scp.std(loc,scale)

            # Guardando los valoares en los arrays
            mean.append(mean_cal)
            std.append(std_cal)
            z .append(z_cal)

        file_data.close()

    if len(std) != 0 : 
        ax1.plot(z, mean , label=nameParam, marker='o')
    if len(std) != 0 : 
        ax2.plot(z, std , label=nameParam, marker='o')        

ax1.set_xlabel('z')
ax2.set_xlabel('z')
ax1.set_ylabel('$\mu$ (log$_{10}$ M$_\odot$)')
ax2.set_ylabel('$\sigma$ (log$_{10}$ M$_\odot$)')
ax1.set_xlim((15.5,-0.2))
ax2.set_xlim((15.5,-0.2))
ax1.legend(loc='best')
ax2.legend(loc='best')


plt.figure(num='mean')
#plt.title('Masa media')
plt.tight_layout()
plt.savefig('Documento/images/RunCanonMassMean.png')
plt.close('mean')

plt.figure(num='std')
#plt.title('Dispersión de masa')
plt.tight_layout()
plt.savefig('Documento/images/RunCanonMassStd.png')

# plt.close('std')
# plt.xlabel('Redshift')
# plt.ylabel('$\sigma$')
# plt.xlim((25.05,-0.05))
# plt.legend(loc='best')
# plt.tight_layout()
plt.show()


