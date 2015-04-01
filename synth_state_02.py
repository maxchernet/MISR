#State parameters for generation of synthetic data
#Different crops
import numpy as np
from collections import OrderedDict
from Read_SPARC_BD import *
#['A1' 'A2' 'B1' 'C1' 'C9' 'C10' 'G1' 'G1' 'G1' 'G1' 'On3' 'P2' 'P3' 'SF1' 'SF1' 'SF1' 'SF3' 'V1']
def get_state(camera='0'):
        c=0
        if (camera == '0'): c=0
        if (camera == '+36'): c=1
        if (camera == '-36'): c=2
        if (camera == '+55'): c=3
        if (camera == '-55'): c=4
        h = [0.5, 0.5, 0.5, 1.7, 1.6, 2., 0.4, 0.4, 0.4, 0.4, 0.5, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        rpl = [0.01, 0.01, 0.3, 0.1, 0.1, 0.1, 0.02, 0.02, 0.02, 0.02, 0.025, 0.05, 0.05, 0.15, 0.15, 0.15, 0.15, 0.07]
        lad = [1,1,5,2,2,2,2,2,2,2,2,5,5,1,1,1,1,1]
        param_name = ['xlai', 'xhc', 'rpl', 'xkab', 'scen', 'xkw', 'xkm', 'xleafn', 'xs1', 'xs2', 'xs3', 'xs4', 'lad', 'vza', 'vaa', 'sza', 'saa']
        params = np.zeros((18, 17))
        sample, proba_0, ang, field = sparc_bd()
        for i in xrange(18):
                        #xlai
                        params[i,0]=np.exp(-sample[i,3]/2.)
                        #xhc
                        params[i,1]=h[i]
                        #rpl
                        params[i,2]=rpl[i]
                        #xkab
                        params[i,3]=np.exp(-sample[i,2]/100.)
                        #scen
                        params[i,4]=0.
                        #xkw
                        xkw = sample[i,6]*0.0001
                        params[i,5]=np.exp(-xkw*50.)
                        #xkm
                        xkm = sample[i,5]*0.00001
                        params[i,6]=np.exp(-100.*xkm)
                        #xleafn
                        params[i,7]=1.5
                        #xs1
                        params[i,8]=0.5
                        #xs2
                        params[i,9]=0
                        #xs3
                        params[i,10]=0
                        #xs4
                        params[i,11]=0
                        #lad
                        params[i,12]=lad[i]
                        #vza
                        params[i,13]=ang[i,c,2]
                        #vaa
                        params[i,14]=ang[i,c,3]
                        #sza
                        params[i,15]=ang[i,c,0]
                        #saa
                        params[i,16]=ang[i,c,1]+180
        return params, field
#params = get_state()
#print params[0,0]
