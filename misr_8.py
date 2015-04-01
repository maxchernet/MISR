#Main module for the MISR-EOLDAS project
from csv_dat import *
from create_synth_misr_8 import *
from do_config_brf_02 import *
from synth_state_02 import *
from create_distr import *
import eoldas
from collections import OrderedDict
#*****************************************************************************************************
def do_misr_eoldas(bands, sds, out_dir, prefix, data_misr, data_misr_real, data_etm, real):
        #Read data from the JRC-csv files and save them in EO-LDAS *.brf files
        misr_ang = save_dat(save_path = data_misr_real)
        misr_ang = np.array([misr_ang]).astype(float)[0,:,:]
        for n_field in [0]:#xrange(18):
                #leaf angle distribution (lad) is fixed and it
                #different for each crop
                xlad = [1,1,5,2,2,2,2,2,2,2,2,5,5,1,1,1,1,1]
                #misr_ang = 
                n_ang = misr_ang.shape[1]
                #get a state for generation of synth data
                params, field = get_state()
                if real==0:
                        #Create synthetic data set. It uses the same geometry as real MISR data
                        create_synth(n_field, params[n_field,:], misr_ang, data_misr)

                #Do a first guess
                #If we have MISR only
                if data_etm == '': 
                        n_b=4
                        #Make a distribution
                        distr_file = '/home/max/misr/misr_distr_1'
                        ang_arr = [16.59, 284.22, 22.02, 319.10]
                #If we have MISR and ETM+
                else: 
                        n_b=6
                        #Make a distribution
                        distr_file = '/home/max/misr/etm_distr_1'
                        ang_arr = [16.0, 8.0, 26.65, 301.0]
                #create_distr(distr_file, ang_arr)
                #read train dataset from a file
                npzfile = np.load(distr_file+'.npz')
                #load train state parameters
                x_train = npzfile['arr_0']
                #train reflectance
                brf_train = npzfile['arr_1']
                real_misr = np.zeros((n_ang, n_b))
                #read synthetic or real satellite data created
                #on previous step
                for i in range(1, n_ang+1):
                    if data_etm == '':
                        #Open MISR data file (actually we use only nadir but here we read all view angles)
                        f = open(data_misr+'misr_P201_B059_2004.7.16_chl%d_ang%d.brf'%(n_field+1, i))
                    else:
                        #Open ETM+ data file (actually we use only nadir but here we read all view angles)
                        f = open(data_etm+'etm_chl%d.brf'%(n_field+1))

                    #nunmber if bands
                    tmp_lst = f.read().split('\n')
                    f.close()
                    real_misr[i-1,:] = tmp_lst[1].split()[6:6+n_b]
                    #it dependa on a number of bands
                    wl= tmp_lst[0].split()[3:3+n_b]
                wl = np.array(wl).astype(float)
                train_misr=[]
                #Reduce number of bands of trained dataset to 
                #a nummber of bands of satellite data
                for i in xrange(wl.size):
                    tmp = brf_train[:,wl[i]-400]
                    train_misr.append(tmp)
                train_misr = np.array(train_misr)
                #Find sum of difference
                sum_misr=[]
                n_train = brf_train.shape[0]
                for i in xrange(n_train):
                    sum_misr.append(np.sum(abs(real_misr[0,:] - train_misr[:,i])))
                #Find a minimum and this is an end of first guess
                min_i = np.argmin(sum_misr)

                #Initial values = first guess
                gamma_time = 0.05
                xlai = x_train[min_i,0]
                xhc = x_train[min_i,1]
                rpl = x_train[min_i,2]
                xkab = x_train[min_i,3]
                scen = x_train[min_i,4]
                xkw = x_train[min_i,5]
                xkm = x_train[min_i,6]
                xleafn = x_train[min_i,7]
                xs1 = x_train[min_i,8]
                xs2 = x_train[min_i,9]
                xs3 = 0
                xs4 = 0
                lad = xlad[n_field]

                #Prior values in Ordered dictonary
                prior = OrderedDict([('xlai', 0.37), \
                           ('xhc', 1.0),\
                           ('rpl', 0.15), \
                           ('xkab', 0.6),\
                           ('scen', 0.5),\
                           ('xkw', 0.6),\
                           ('xkm', 0.37),\
                           ('xleafn', 1.5),\
                           ('xs1', 1.0),\
                           ('xs2', 0),\
                           ('xs3', 0),\
                           ('xs4', 0),
                           ('lad', 1)])
                #Prior uncertainties
                prior_sd = OrderedDict([('xlai', 1.), \
                           ('xhc', 3.),\
                           ('rpl', 0.15), \
                           ('xkab', 0.4),\
                           ('scen', 0.5),\
                           ('xkw', 0.5),\
                           ('xkm', 0.7),\
                           ('xleafn', 1.),\
                           ('xs1', 3.),\
                           ('xs2', 2.),\
                           ('xs3', 0.001),\
                           ('xs4', 0.001),
                           ('lad', 0.001)])

                #Inicialize string with first values (LAI) from ordered dic
                prior_str = prior.values()[0]
                prior_sd_str = prior_sd.values()[0]
                #Make a strings with all other values from ordered dic
                for i in list(prior.values()[1:]): 
                        prior_str = '%s,%.3f'%(prior_str, i)
                for i in list(prior_sd.values()[1:]): 
                        prior_sd_str = '%s,%.3f'%(prior_sd_str, i)

                #lists of bands and sdandard deviations
                #bands = ['443.0 555.0 670.0 865.0']
                #sds = ['0.0040 0.0044 0.0047 0.0054']
                #483.0 560.0 662.0 835.0 1648.0 2206.0
                #0.0041 0.0045 0.0047 0.0053 0.0079 0.0097
                #out_dir = '/home/max/misr/out_synth_misr_75ang/'
                for i in xrange(1,n_ang+1):
                        #Define input an output files depending on one sensor or two sensors are used
                        if len(data_etm)=='':
                                f_state = [data_misr+'misr_P201_B059_2004.7.16_chl%d_ang%d.brf'%(n_field+1, i)]
                                f_result = [out_dir + 'misr_P201_B059_2004.7.16_chl%d_ang%d_brf.fwd'%(n_field+1, i)]
                        else:
                                f_state = [data_misr+'misr_P201_B059_2004.7.16_chl%d_ang%d.brf'%(n_field+1, i),\
                                        data_etm+'etm_chl%d.brf'%(n_field+1)]
                                f_result = [out_dir + 'misr_P201_B059_2004.7.16_chl%d_ang%d_brf.fwd'%(n_field+1, i),\
                                        out_dir + 'etm_chl%d.fwd'%(n_field+1)]
                        #f_state = ['/home/max/misr/data_misr_synth_75ang/misr_P201_B059_2004.7.16_chl%d_ang%d.brf'%(n_field+1, i)]
                        #f_result = [out_dir + '/misr_synth_P201_B059_2004.7.16_chl%d_ang%d_brf.fwd'%(n_field+1, i)]

                        f_result_param = out_dir + prefix+'_P201_B059_2004.7.16_chl%d_ang%d_brf.params'%(n_field+1, i)
                        f_prior = out_dir + prefix+'_P201_B059_2004.7.16_chl%d_ang%d_brf.prior'%(n_field+1, i)
                        #Name of a conf. file
                        conf_file = '/home/max/misr/conf/misr-etm_obs%d.conf'%len(bands)
                        #Make a config file
                        conf_file = do_config(conf_file, n_obs=len(bands), bands=bands, sds=sds, lst_state=f_state, lst_result=f_result, f_result_param=f_result_param, f_prior=f_prior)
                        print 'conf_file', conf_file
                        #Do inversion
                        #Command line
                        cmd = 'eoldas --conf=conf/eoldas_config.conf --conf=' + conf_file +\
                        ' --parameter.x.default=[%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f]'%(gamma_time, xlai, xhc, rpl, xkab, scen, xkw, xkm, xleafn, xs1, xs2, xs3, xs4, lad) + \
                        ' --operator.prior.y.sd=%s'%prior_sd_str + \
                        ' --operator.prior.y.state=[%s]'%prior_str + \
                        ' --logfile=/media/sf_JRC/log/misr_01.log'
                        self = eoldas.eoldas(cmd)
                        self.solve(write=True)
                        print 'Done inversion!'

#********************************************************MAIN*****************************************************************************

data_misr_real = '/home/max/misr/data_misr_real_8/'

#--------------------------------------------------------
#lists of bands and sdandard deviations
data_misr = '/home/max/misr/data_misr_synth_8/'
data_etm = ''
bands = ['443.0 555.0 670.0 865.0']
sds = ['0.0040 0.0044 0.0047 0.0054']
out_dir = '/home/max/misr/out_synth_misr_8/'
#f_state=[]
f_state_dir_misr = '/home/max/misr/data_misr_synth_8/'
f_state_dir_etm = ''
#f_result = [out_dir + '/'+prefix]
prefix = 'misr_synth'
do_misr_eoldas(bands, sds, out_dir, prefix, data_misr, data_misr_real, data_etm, 0)
#----------------------------------------------------------

#lists of bands and sdandard deviations
data_misr = '/home/max/misr/data_misr_synth_8/'
data_etm = '/home/max/misr/data_landsat_synth/'
bands = ['443.0 555.0 670.0 865.0', '483.0 560.0 662.0 835.0 1648.0 2206.0']
sds = ['0.0040 0.0044 0.0047 0.0054', '0.0041 0.0045 0.0047 0.0053 0.0079 0.0097']
out_dir = '/home/max/misr/out_synth_misr_etm_8/'
f_state_dir_misr = '/home/max/misr/data_misr_synth_8/'
f_state_dir_etm = '/home/max/misr/data_landsat_synth/'
prefix = 'misr_etm_synth'
do_misr_eoldas(bands, sds, out_dir, prefix, data_misr, data_misr_real, data_etm, 0)
#----------------------------------------------------------
'''
#lists of bands and sdandard deviations
data_misr = '/home/max/misr/data_misr_real_8/'
data_etm = ''
bands = ['443.0 555.0 670.0 865.0']
sds = ['0.0040 0.0044 0.0047 0.0054']
out_dir = '/home/max/misr/out_real_misr_8/'
#f_state_dir_misr = '/home/max/misr/data_misr_synth_8/'
f_state_dir_etm = ''
prefix = 'misr_synth'
do_misr_eoldas(bands, sds, out_dir, prefix, data_misr, data_misr_real, data_etm, 1)
#--------------------------------------------------------------

data_misr = '/home/max/misr/data_misr_real_8/'
data_etm = '/home/max/misr/data_landsat_real/'
bands = ['443.0 555.0 670.0 865.0', '483.0 560.0 662.0 835.0 1648.0 2206.0']
sds = ['0.012 0.0132 0.0141 0.0162', '0.0041 0.0045 0.0047 0.0053 0.0079 0.0097']
out_dir = '/home/max/misr/out_real_misr_etm_8/'
prefix = 'misr_etm_real'
do_misr_eoldas(bands, sds, out_dir, prefix, data_misr, data_misr_real, data_etm, 1)
'''
print 'Done All!!!'

