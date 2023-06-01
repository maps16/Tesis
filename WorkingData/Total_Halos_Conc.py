import h5py as h5
import matplotlib.pyplot as plt
from glob import glob

# Generando Figura
fig ,ax = plt.subplots( nrows = 1, ncols = 1, figsize = ( 6, 6 ) )

# Loc de archivos para trabajar
data = 'subhalo'
dataParam = 'SubhaloMass'
run = glob('WorkingData/StandardResolution/*')
run.sort()

# Extableciendo los arrays para diferentes valores de interes
N_Subhalos = []
z = []
nameParam = ''

# Corriendo sobre las diferentes Cosmologias
for x in run:
    
    # Limpiendo las listas para las nuevas Cosmologias
    N_Subhalos.clear()
    z.clear()

    # Identificando todos los archivos dentro de las Cosmologias
    namepath = '/home/martin/Documentos/Tesis/' + x + '/' + data
    arch = glob(namepath + '/*')
    arch.sort()

    # Iterando sobre todos los archivos
    for i in arch:
           
        # Abrir los HDF5
        file_data = h5.File(i, mode="r")
        
        # Trabajando solo con los archivos que contienen subhalos
        if 'Subhalo' and 'Group' in file_data:

            # Extrayendo parametros de la simulación
            Omega0, OmegaL = file_data['Parameters'].attrs['Omega0'], file_data['Parameters'].attrs['OmegaLambda']
            
            # Label identificando cada cosmologia
            nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) 
            
            #Extrayendo Datos Deseados
            N_subh = file_data['Header'].attrs['Nsubhalos_Total']
            z_Cal = file_data['Header'].attrs['Redshift']
            
            # Guardando los valoares en los arrays
            N_Subhalos.append(N_subh)
            z.append(z_Cal)
            # print('Total =' , N_subh, ', z=',z_Cal )
    
        
        file_data.close()

    # print(max(N_Subhalos))                
    print('Primeros Halos en z= ', round( max(z), 0), ', Total de Corridas =', len(z), ', Corrio ' , nameParam , ', Max Halos:' , max(N_Subhalos), ', Last Total:' , N_Subhalos[-1]  )
    
    ax.plot(z, N_Subhalos,'o-' , label=nameParam)

fig.suptitle('Evolución del número de halos total')
ax.set_ylabel('Total Halos')
ax.set_xlabel('Redshift (z)')
ax.set_xlim(round( max(z), ndigits=0 )+.5, -0.5)
ax.legend(loc='best')

fig.tight_layout()
plt.savefig('Documento/images/Conc/TotalHalos_Conc.png')
plt.show()