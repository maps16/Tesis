import numpy as np
from glob import glob
from scipy.stats import exponnorm as scp
import matplotlib.pyplot as plt
import h5py as h5

#Generando Figura
fig1, ax1 = plt.subplots( nrows=1, ncols=1, num='mean', figsize=(5.5,5.5) )
fig2, ax2 = plt.subplots( nrows=1, ncols=1, num='std', figsize=(5.5,5.5) )

# Loc de archivos para trabajar
sim = 'RunCanonica'
data = "subhalo"
run = glob('WorkingData/StandardResolution/*') #Ubicanco las carpetas de las diferentes cosmologias
run.sort()
run = range(1) #['WorkingData/StandardResolution/RunCanonica']

# Corriendo sobre las diferentes cosmologias
for x in run:
    # x = x.split('/')[-1]
    namepath = "/home/martin/Documentos/Tesis/WorkingData/StandardResolution/" + sim + "/" + data
   
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
            VMaxRad = file_data['Subhalo']['SubhaloVelDisp'][:] * 1e0  # type: ignore

            # Calculado los parametros para el ajuste
            k, loc, scale = scp.fit(VMaxRad,)
            # Calculo de la media y desviacion estandar
            mean_cal, std_cal = scp.mean(k, loc,scale), scp.std(k, loc,scale)

            # Guardando los valoares en los arrays
            mean.append(mean_cal)
            std.append(std_cal)
            z .append(z_cal)
            print('z=',round(z_cal,ndigits=2),', mean=',round(mean_cal, ndigits=2),', std=',round(std_cal,ndigits=2), sep=' ')  # type: ignore

        file_data.close()

    if len(mean) != 0 : 
        ax1.plot(z, mean, label=nameParam, marker='o') # type: ignore
    if len(std) != 0: 
        ax2.plot(z, std, label=nameParam, marker='o')  # type: ignore      

ax1.set_xlabel('z')
ax2.set_xlabel('z')
ax1.set_ylabel('$\mu$ (km/s)')#type: ignore
ax2.set_ylabel('$\sigma$ (km/s)')#type: ignore
ax1.set_xlim((17.5,-0.5))
ax2.set_xlim((17.5,-0.5))
ax1.legend(loc='best')
ax2.legend(loc='best')


fig1.tight_layout()
# fig1.savefig('Documento/images/'+sim+'/VelDisp_Mean_'+sim+'.png')
fig2.tight_layout()
# fig2.savefig('Documento/images/'+sim+'/VelDisp_Std_'+sim+'.png')
plt.show()