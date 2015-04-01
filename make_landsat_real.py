import numpy as np

f=open('/media/sf_MISR_EOLDAS/etm_pix_spectra.dat')
str_angels = '16.0 8.0 26.65 301.0'
tmp_list = f.read().split('endec')
f.close()
wl = np.array(tmp_list[0].split()).astype(float)
n_samples = len(tmp_list)
nb = len(wl)

proba_int = np.zeros((n_samples, nb))
for i in range(1,n_samples-1):
        tmp = np.array(tmp_list[i].split()).astype(float)
        tmp=tmp*0.0001
        proba_int[i-1,:] = tmp

proba_sd = np.zeros(len(wl))
proba_sd[:] = 0.01
sd_str = '0.0041 0.0045 0.0047 0.0053 0.0079 0.0097'

for i in range(1, n_samples-1):
        f = open('/home/max/misr/data_landsat_real/etm_pix%d.brf'%i, 'w')
        f.write('BRDF 1 6 %s %s\n'%(' '.join(wl.astype(str)), sd_str))
        f.write('1 1 %s %s\n'%(str_angels, ' '.join(proba_int[i-1,:].astype(str))))
        f.close()
print 'Done!'

#BRDF %d 4 443.0 555.0 670.0 865.0 0.0040 0.0044 0.0047 0.0054
