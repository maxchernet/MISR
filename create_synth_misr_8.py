#Synthetic expirement
#Generating synthetic sets of spectral data
#Uncertainties of Sentinel-2 bands:
#'0.2 0.5 0.5 0.5 0.2 0.2 0.5 0.5 0.2 0.2 0.5 1.0 1.0'
#Here all angles are solved by one observational operator
import numpy as np
import os
import semidiscrete as rt
#Functionto run semidiscrete model
#**********************************************************************************************
def run_semidiscrete(xlai,xhc,rpl,xkab,scen,xkw,xkm,xleafn,xs1,xs2,xs3,xs4,lad,vza,vaa,sza,saa):
        wl = np.identity(2101)
        bands = np.arange(1,2102)
        params = [xlai,xhc,rpl,xkab,scen,xkw,xkm,xleafn,xs1,xs2,xs3,xs4,lad]
        rt.rt_modelpre(bands, 2101)
        return rt.rt_model(1, params, vza, vaa, sza, saa, wl)

#**********************************************************************************************
def is_odd(num):
    return num & 0x1

#*********************************************************************************************
#Create ETM+ data
def do_etm(n_field, xparam):
        band_etm = np.array([483.0, 560.0, 662.0, 835.0, 1648.0, 2206.0])
        band_etm_sd = np.array([0.0041, 0.0044, 0.0047, 0.0053, 0.0079, 0.0097])
        etm_ang = [16., 8.1, 27.8, 303.2]
        #vza
        xparam[13] = etm_ang[0]
        #vaa
        xparam[14] = etm_ang[1]
        #sza
        xparam[15] = etm_ang[2]
        #saa
        xparam[16] = etm_ang[3]
        #run a model
        brf_full = run_semidiscrete(*xparam)
        brf_etm = np.zeros(6)
        for i in xrange(band_etm.shape[0]):
                brf_etm[i] = brf_full[:,band_etm[i]-400]
        #Write PROBA
        f = open('/home/max/misr/data_landsat_synth/etm_chl%d.brf'%(n_field+1), 'w')
        #Do first line for a data file, i.e. bands and their uncertainties
        band_etm_str=''
        for i in xrange(band_etm.shape[0]):
                band_etm_str = band_etm_str + ' %.2f'%band_etm[i]
        for i in xrange(band_etm.shape[0]):
                band_etm_str = band_etm_str + ' %.4f'%band_etm_sd[i]
        band_etm_str = 'BRDF 1 6 ' + band_etm_str + '\n'
        f.write(band_etm_str)
        #for i in xrange(np.size(ang_sample[ang])):
        brf_etm_str = ''
        for j in xrange(band_etm.shape[0]):
                brf_etm_str = brf_etm_str + ' %.4f'%brf_etm[j]
        f.write('%d %d %s %s %s %s %s\n'%(1, 1, etm_ang[0], etm_ang[1], etm_ang[2], etm_ang[3],\
                brf_etm_str))
        f.close()
#************************************************************************************************
#Create proba data which geometry is the same as real proba
def do_proba(n_field, xparam, proba_ang):
        #read the proba bands from a data file
        f=open('/home/max/misr/data_proba/sparc_bd_0.dat')
        band_proba = np.array(f.read().split('\n')[0].split()[7:69]).astype(float)
        f.close()
        band_proba_str=''
        for i in xrange(band_proba.shape[0]):
                band_proba_str = band_proba_str + ' %.2f'%band_proba[i]
        for i in xrange(band_proba.shape[0]):
                band_proba_str = band_proba_str + ' 0.001'
        band_proba_str = 'BRDF %d ' + band_proba_str + '\n'
        #Geometry for synthetic proba
        #0:vza, 1:vza, 2:sza, 3:saa
        #proba_ang = [8.41, 283.57, 20.81, 325.45]
        #vza
        xparam[13] = proba_ang[0]
        #vaa
        xparam[14] = proba_ang[1]
        #sza
        xparam[15] = proba_ang[2]
        #saa
        xparam[16] = proba_ang[3]
        #run a model
        brf_full = run_semidiscrete(*xparam)
        brf_proba_1 = np.zeros(62)
        for i in xrange(band_proba.size):
                brf_proba_1[i] = brf_full[:,band_proba[i]-400]
                #brf_proba[i] = tmp
        #Write PROBA
        f = open('/home/max/misr/data_proba/proba_synth_2004.7.16_chl%d_vza_%.1f_vaa_%.1f_brf.brf'%(n_field+1, proba_ang[0], proba_ang[1]), 'w')
        f.write(band_proba_str%1)
        #for i in xrange(np.size(ang_sample[ang])):
        brf_proba_str = ''
        for j in xrange(band_proba.shape[0]):
                brf_proba_str = brf_proba_str + ' %.4f'%brf_proba_1[j]
        f.write('%d %d %s %s %s %s %s\n'%(1, 1, proba_ang[0], proba_ang[1], proba_ang[2], proba_ang[3],\
                brf_proba_str))
        f.close()

#**********************************************************************************************
#Create synth. MISR
def do_misr(n_field, xparam, misr_ang, data_misr):
        n_ang = misr_ang.shape[1]
        print 'n_ang=', n_ang
        center = int(n_ang/2)

        #Array of view zenith angles
        #a1 = np.arange(3, n_ang+1, 2)
        #a2 = np.append(a1[::-1],0)
        #misr_ang = np.concatenate((a2,a1))

        brf_misr = np.zeros((n_ang, 4))

        #Array of view azimuth angles
        #misr_vaa = np.zeros(n_ang)
        #misr_vaa[0:center] = 90.
        #misr_vaa[center:n_ang] = 270.

        #Create MISR data
        for ang in xrange(n_ang):
                #vza
                xparam[13] = misr_ang[2,ang]
                #vaa
                xparam[14] = misr_ang[3,ang]
                #sza
                xparam[15] = misr_ang[0,ang]
                #saa
                xparam[16] = misr_ang[1,ang]
                #run a model
                brf_full = run_semidiscrete(*xparam)
                print 'angels', misr_ang[2,ang], misr_ang[3,ang], misr_ang[0,ang], misr_ang[1,ang]
                band = np.array([443, 555, 670, 865])
                b_min = [425,543,661,846]
                b_max = [467,573,683,886]
                for i in xrange(band.size):
                        tmp = brf_full[:,band[i]-400]
                        brf_misr[ang,i] = tmp
        ang_sample=np.array([int(n_ang/2)])
        for ang in xrange(n_ang):
                #Write MISR
                print 'ang_sample=', ang_sample
                f = open(data_misr + 'misr_P201_B059_2004.7.16_chl%d_ang%d.brf'%((n_field+1), (ang+1)), 'w')
                f.write('BRDF %d 4 443.0 555.0 670.0 865.0 0.0040 0.0044 0.0047 0.0054\n'%(ang+1))
                for i in xrange(np.size(ang_sample)):
                        f.write('%d %d %s %s %s %s %.4f %.4f %.4f %.4f\n'%(1, 1, misr_ang[2, ang_sample[i]], misr_ang[3, ang_sample[i]], \
                                misr_ang[0, ang_sample[i]], misr_ang[1, ang_sample[i]],\
                                brf_misr[ang_sample[i],0], brf_misr[ang_sample[i],1], brf_misr[ang_sample[i],2], brf_misr[ang_sample[i],3]))
                f.close()
                #create angular sampling array which determines position of angle in array of angles
                if is_odd(ang):
                        ang_sample=np.insert(ang_sample, 0, ang_sample[0]-1)
                else:
                        ang_sample=np.insert(ang_sample, len(ang_sample), ang_sample[len(ang_sample)-1]+1)

#*******************************************************************************************************
def create_synth(n_field, xparam, misr_ang, data_misr):

        do_proba(n_field, xparam, [8.41, 283.57, 20.81, 325.45])
        do_misr(n_field, xparam, misr_ang, data_misr)
        do_etm(n_field, xparam)

        print 'Done create synth!'
