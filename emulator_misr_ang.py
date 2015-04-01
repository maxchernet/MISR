#Train and save emulators
from gp_emulator import *
from run_semidiscrete import *
import scipy.stats as ss

#**************************************************
#Read bounds of the parameters from .conf file
def read_bounds(conf_file):
        bounds = np.zeros((10,2))
        f = open(conf_file)
        list_opt = f.read().split('\n')
        for i in range(0,len(list_opt)):
                if '[parameter.x.assoc_bounds]' in list_opt[i]:
                        tmp_lst =  [ss.split('=') for ss in list_opt[i+2:i+12]]
                        j=0
                        for line in tmp_lst:
                                #print line
                                bounds[j,:] =  np.array(line[1].split(',')).astype(float)
                                j+=1
                        #print np.array(tmp_lst[0][2].split(',')).astype(float)
                        #print [ np.array(ss.split(',')).astype(float) for ss in tmp_lst[:][2]]
                        #print len(tmp_lst)
        return bounds
#****************************************************************
def create_emulator(vza, vaa, sza, saa):
        bounds = read_bounds('/home/max/misr/conf/misr_obs1.conf')
        min_vals = bounds[:,0]
        max_vals = bounds[:,1]
        n_params=10
        n_train=400
        y_obs = np.zeros((n_train, 2101))
        chl=1
        ang=1
        wl_full = np.arange(400,2501)
        ang_misr = [vza, vaa, sza, saa]
        dist=[]
        #Get a distrubution for sampling
        for k in xrange(n_params):
            dist.append(ss.uniform(loc=min_vals[k], scale=max_vals[k]-min_vals[k]))
        # The training dataset is obtaiend by a LatinHypercube Design
        x_train = lhd(dist=dist, size=n_train )
        print 'x_train shape:', x_train.shape
        for i in xrange(n_train):
                x_params = np.append(x_train[i,:], [0,0,5])
                x_params = np.append(x_params, ang_misr)
                y_obs[i,:] = run_semidiscrete(*x_params)[0,:]
        em = MultivariateEmulator (X=y_obs, y=x_train)
        em.dump_emulator('/home/max/misr/emul/emul_full_vza_%.1f_vaa_%.1f'%(vza,vaa))
#*******************************************************************
if __name__ == "__main__":
        create_emulator(70.23 8.73 22.02 319.10)
        create_emulator(60.33 5.92 22.02 319.10)
        create_emulator(46.57 225.05 22.02 319.10)
        create_emulator(29.33 345.07 22.02 319.10)
        create_emulator(16.59 284.21 22.02 319.10)
        create_emulator(30.75 228.19 22.02 319.10)
        create_emulator(47.76 214.47 22.02 319.10)
        create_emulator(61.29 208.85 22.02 319.10)
        create_emulator(71.32 205.99 22.02 319.10)
