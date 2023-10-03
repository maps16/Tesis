# SIMULATION Plotting
# AUTHOR Martin Paredes

#LIBRARIES
import pynbody as pnb
import pynbody.plot.sph as sph
import matplotlib.pyplot as plt
#import numpy as np
print ("Librerias Lista")


#GENERAR FIGURA PARA EL PLOT
fig, ax = plt.subplots(1, 1, sharex= True, sharey= True, figsize=(6.8,5.5)  )

LEGEND_SIZE= 10
TICK_SIZE = 12
DEFAULT=6
SMALL_SIZE = 12
MEDIUM_SIZE = 16
BIGGER_SIZE = 14

plt.rc('font', size=DEFAULT)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=LEGEND_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

print ("Figura Lista")

#Ubicacion de los archivos
sim = 'RunHighLam'
arcNameG4 = "/home/martin/Documentos/Tesis/WorkingData/StandardResolution/"+sim+"/snapshot/"

#Cargar Snapshots
snap17 = pnb.load(filename= arcNameG4 + "snapshot_033.hdf5")
print ("Cargar snapshots Lista")

#Tratar en umidades fisicas
snap17.physical_units()

#Tamano de la caja obtenido del snapshot
bxs = snap17.properties["boxsize"]
#bxs = pnb.units.Unit("73.7 Mpc")

del snap17.properties["boxsize"]

#Traslado de Coordenadas del centro
snap17["x"] -= bxs * 0.5
snap17["y"] -= bxs * 0.5
snap17["z"] -= bxs * 0.5

# Extrayendo parametros de la simulación
Omega0, OmegaL, OmegaB, redshiftZ = snap17.properties['omegaM0'], snap17.properties['omegaL0'], snap17.properties['omegaB0'], snap17.properties[ 'Redshift' ]
                
# Label identificando cada cosmologia
nameParam = r'$\Omega_0=$'+str(Omega0) + ', ' + r'$\Omega_\lambda=$'+str(OmegaL) + ', ' + r'$z=$'+str(round(redshiftZ,2)) 


print ("Inicio Plotting: ", nameParam)


#PLOTTING
sph.image(snap17, qty="rho", width = bxs * 0.50, cmap="Blues", av_z=True, title=nameParam, subplot= ax, show_cbar=True, clear = True, resolution=500)    # type: ignore

#Mostrar Plots
ax.set_xlabel('x/kpc', fontsize=MEDIUM_SIZE)
ax.set_ylabel('y/kpc', fontsize=MEDIUM_SIZE)
ax.tick_params(axis='x', labelsize=TICK_SIZE)
ax.tick_params(axis='y', labelsize=TICK_SIZE)

fig.tight_layout()   #Ajustar Plot

ImageFileName ='Documento/images/'+sim+'/'+sim+'Z'+str(round(redshiftZ,1))+'.png'
fig.savefig(ImageFileName)                                                              #Guardar Plot en PNG
# plt.show()                                                                            #Mostrar Plot
