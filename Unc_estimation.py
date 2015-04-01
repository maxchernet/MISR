import numpy as np
from gp_emulator import *
import scipy.stats as ss

#Read input parameters file
f=open('/home/max/misr/output/misr_synth_P201_B059_2004.7.16_chl3_ang9_brf.params')
tmp = np.array(f.read().split('\n')[1].split()).astype(float)
f.close()
#Read parameters. We will change values of these parameters becouse we want know uncertainties of the spectral bands
params = tmp[2:12]
sd = tmp[16:26]
print params
print sd
n_params = 10
#min/max and distribution
#min_vals = np.array([ 0.08, 0.1, 0.001, 0.45, 0.001, 0.001, 0.1, 0.7, 0.01, -2.])
#max_vals = np.array([  0.9,  5.,   0.1,  0.9,     1,     1,   1, 2.5,    4,  2.])
dist=[]
n_train=50

#Get a distrubution for sampling
for k in xrange(n_params):
    if sd[k] !=0:
        dist.append(ss.norm(loc=params[k], scale=sd[k]))
# The training dataset is obtaiend by a LatinHypercube Design
x_train = lhd(dist=dist, size=n_train )
print x_train.shape
print x_train[0,:]
