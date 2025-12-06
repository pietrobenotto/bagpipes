import numpy as np
import matplotlib.pyplot as plt
import bagpipes as pipes


#metallicità 0.8, 1 1.2
#sfh 
import os
path = os.path.dirname(os.path.abspath(pipes.__file__))+"/models/grids/luminosity_grid_550nm.npz"

wavs=np.linspace(5500,5505,3)


redshift    = 0
logU        = -2


metallicities = pipes.config.metallicities
ages= pipes.config.age_sampling

grid = np.zeros((metallicities.shape[0], ages.shape[0])) 

new=True
for met_i in range(len(metallicities)):
    for age_i in range(len(ages)):
    
        burst={}
        burst["metallicity"]=metallicities[met_i]
        burst["massformed"]=8
        burst["age"]=ages[age_i]/1.e9
            
        nebular = {}
        nebular["logU"] = logU

        dust = {}
        dust["type"] = "Calzetti"   # Attenuation law: "Calzetti", "Cardelli", "CF00" or "Salim"
        dust["Av"] = 0     # Absolute attenuation in the V band: magnitudes

        model_components = {}
        model_components["redshift"] = redshift
        model_components["t_bc"] = 0.01
        model_components["burst"] = burst
        model_components["nebular"] = nebular
        model_components["veldisp"]=5
        model_components["dust"]=dust
        model_components["R"]=100
        model_components["ID"]="mock"

        if new:
            galaxy = pipes.model_galaxy(model_components,spec_wavs=wavs,spec_units="mujy")
            new =False
        else:
            galaxy.update(model_components)

        #print(ages[age_i]/1e9,galaxy.sfh.mass_weighted_age,galaxy.sfh.luminosity_weighted_age)


        #wavs = galaxy.spectrum[:,0]
        #spectrum = galaxy.spectrum[:,1]
        #plt.plot(wavs,spectrum)
        #plt.yscale("log")
        #plt.axvline(5500)
        #plt.show()

        #from scipy.ndimage import gaussian_filter1d
        #spectrum = gaussian_filter1d(spectrum,50)
        #np.savetxt("galaxy_spectrum.dat",np.c_[wavs,spectrum])

        grid[met_i, age_i] = galaxy.spectrum[0,1]

grid /= np.max(grid)
for met_i in range(len(metallicities)):
    plt.scatter(ages,grid[met_i],marker=".",label=metallicities[met_i])
plt.yscale("log")
plt.xscale("log")
plt.legend()


np.savez(path, metallicities=metallicities, ages = ages, grid  = grid)
plt.show()