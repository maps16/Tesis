'''
CODE BASED ON Mike Saint-Antoine example to fit discrete distributoins
https://github.com/mikesaint-antoine/Comp_Bio_Tutorials/blob/main/parameter_estimation/discrete_distributions/fit_distributions.py
'''
# IMPORTS  
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco
import scipy.stats as scp


# Define loss_f function.
def loss_f(params, data_in):

    mu = params[0]
    loss = 0
    
    for i in range( len(data_in) ):

        loglikelihood = scp.poisson.logpmf(data_in[i], mu)
        loss_to_add = - loglikelihood
        loss += loss_to_add 

    return loss

# SAMPLE DATA (RANDOM)
szs = 3000
data = np.random.poisson(lam = 5, size = szs) + 0.0

#PLOTTING SAMPLE DATA
plt.hist(data, bins= int( np.max(data) ), density=False, alpha= 0.75, label= "Data" )

# PARAMETER CALCULATION
param0 = np.array( [1.], dtype=np.float64 )  # PARAMETER GUESS
mini = sco.fmin( loss_f, param0, args=(data,) )
lamd = mini[0] # PARAMETER SELEC

# DEBUG
print('lamda: ' + str(lamd))

# PLOTTING RANGE X
x = np.array( range(int(np.min(data)), int(np.max(data)) + 1 ) )
plt.scatter( x + 0.5, scp.poisson.pmf(x, lamd) * szs , color='red', label = 'Fit' )

# PLOTTING PARAMETERS
plt.legend(loc='best')
plt.show()
plt.clf()