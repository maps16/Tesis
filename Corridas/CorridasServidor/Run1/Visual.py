# SIMULATION Plotting
# AUTHOR Martin Paredes

#LIBRARIES
import pynbody as pnb
import pynbody.plot.sph as sph
import matplotlib.pyplot as plt
#import numpy as np
print ("Librerias Lista")


#GENERAR FIGURA PARA EL PLOT
plt.ion() #Interactive ON
fig, ax = plt.subplots(1, 1, sharex= True, sharey= True, figsize=(10,10)  )

print ("Figura Lista")

#Ubicacion de los archivos
arcNameG4 = "/home/martin/Documentos/Tesis/Corridas/CorridasServidor/Run1/gadget4/"

#Cargar Snapshots
snap17 = pnb.load(filename= arcNameG4 + "snapshot_017.hdf5")
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

print ("Inicio Plotting")


#PLOTTING
sph.image(snap17, qty="rho", width = bxs * 0.50, cmap="Blues", av_z=True, title="Simulación con Gadget4 \n z=0", subplot= ax, show_cbar=True, clear = True, resolution=2000)


#Mostrar Plots
fig.tight_layout()                                                              #Ajustar Plot
#fig.savefig("/home/martin/Imágenes/SimG4Z0.png")                               #Guardar Plot en PNG
plt.show()                                                                      #Mostrar Plot



#TESTING
print("Hello World")
