import numpy as np
from glob import glob
from scipy.stats import norm as scp
import matplotlib.pyplot as plt
import h5py as h5

plt.figure(num='std',  figsize=(5.5,5.5) )
plt.figure(num='mean', figsize=(5.5,5.5) )

# Loc de archivos para trabajar
data = "subhalo"
run = glob('WorkingData/StandardResolution/*') #Ubicanco las carpetas de las diferentes cosmologias
run.sort()
run = ['WorkingData/StandardResolution/RunCanonica']

# Corriendo sobre las diferentes cosmologias
for x in run:
    x = x.split('/')[-1]
    namepath = "/home/martin/Documentos/Tesis/WorkingData/StandardResolution/" + x + "/" + data
   
    #Checar todos los archivos
    arch = glob(namepath + '/*')
    arch.sort()

    # Extableciendo/Limpiendo los arrays para diferentes valores de interes
    mean = []       # Media
    std  = []       # Desviacion Estandar
    z = []          # Redshift

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
            logmass = np.log10( file_data['Subhalo']['SubhaloHalfmassRad'][:] * 1e03)

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
        plt.figure('std')
        plt.gca()
        plt.plot(z, std, label=nameParam, marker='o')
    if len(mean) != 0:
        plt.figure('mean')
        plt.gca()
        plt.plot(z, mean, label=nameParam, marker='o')
        
plt.figure('std')
plt.xlabel('z (Redshift)')
plt.ylabel('$\sigma$(log$_{10}$Kpc)')
plt.xlim((15.25,-0.25))
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('Documento/images/HalfMassRad_Std.png')

plt.figure('mean')
plt.xlabel('z (Redshift)')
plt.ylabel('$\mu$ (log$_{10}$Kpc)')
plt.xlim((15.25,-0.25))
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('Documento/images/HalfMassRad_Mean.png')

plt.show()
