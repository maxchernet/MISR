#To be able to read csv formated files, we will first have to import the
#csv module.
import csv
import numpy as np

def read_csv(csv_file, row_july):
        brf = np.zeros((4,9))
        ifile = open(csv_file, 'rb')
        reader = csv.reader(ifile)
        rownum = 0
        date=''
        for row in reader:
                #print row
                colnum=0
                if (rownum == row_july):
                        #print '%s %s %s' % (row,colnum, rownum)
                        #print row[6:42]
                        brf = np.array(row[6:42])
                        #print brf
                        date = '.'.join([row[3].strip(), row[4].strip(), row[5].strip()])
                        #print 'date=', date
                        colnum += 1              
                rownum += 1
        ifile.close()
        flag=True
        #print 'sum=', np.sum(brf.astype(float))
        if np.sum(brf.astype(float)) == 0.0: flag=False
        return brf, date, flag

def read_etm(point):
        return np.array([0.05,0.1,0.14,0.3])

#****************************************************************************************************************************
def save_dat(save_path='/home/max/misr/data_misr/', misr_path='P201_B059', etm_file='/media/sf_MISR_EOLDAS/etm_pix_spectra.dat', landsat_ref=19, ang_sample = [4,3,5,2,6,1,7,0,8]):
        misr_ang = ang_sample
        #misr_path - MISR path and row
        #misr_path = 'P201_B059'
        #etm_file - landsat file which is used for choosing proper pixels
        #landsat_ref - a number of a line in a *.csv file with closest date to landsat reference spectra
        #landsat_ref=19

        f=open(etm_file)
        tmp_list_etm = f.read().split('endec')
        f.close()
        n_samples=18
        etm = np.zeros((n_samples+1, 6))
        for i in range(1,n_samples+1):
                tmp = np.array(tmp_list_etm[i].split()).astype(float)
                tmp=tmp*0.0001
                etm[i,:] = tmp

        etm = etm[:, 0:4]
        #misr_ang = [4,3,5,2,6,1,7,0,8]
        points = ['+000_+000', '+000_+001', '+000_-001', '+001_+000', '+001_+001', '+001_-001', '-001_+000', '-001_+001', '-001_-001']
        min_point = 0
        brf_min = np.zeros((9,4))
        #The loop by samples
        for point in range(1,19):
                date_list=['']
                tmp_min=4.
                for s in points:
                        (brf, date, flag) = read_csv('/media/sf_Barrax/MISR/18_points_new/TS_tree_Csvs/%s_barrax/chl%d/BRF/BRF/BRF_V1.04-1_%s_barrax_chl%d_%s_BRF.csv'%(misr_path, point, misr_path, point, s), landsat_ref)
                        brf = brf.reshape(9,4)
                        #print 'etm+', etm[point,:]
                        #print 'misr', brf[4,:].astype(float)
                        diff = sum(abs(etm[point,:] - brf[4,:].astype(float)))
                        if diff <= tmp_min: 
                                tmp_min=diff
                                point_min = s
                                brf_min = brf
                        #print diff
                print 'sample N: ', point
                print 'min point: ',point_min
                #print 'min difference', tmp_min
                print 'ref. landsat date:', date
                print '***'
                #The loop by date rows in .csv file
                for i in range(19, 20):
                        (brf, date, flag1) = read_csv('/media/sf_Barrax/MISR/18_points_new/TS_tree_Csvs/%s_barrax/chl%d/BRF/BRF/BRF_V1.04-1_%s_barrax_chl%d_%s_BRF.csv'%(misr_path, point, misr_path, point, point_min), i)
                        print 'flag ', flag1, date
                        print i
                        (ang, date, flag) = read_csv('/media/sf_Barrax/MISR/18_points_new/TS_tree_Csvs/%s_barrax/chl%d/L1B/L1B3/L1B_V1.04-1_%s_barrax_chl%d_%s_L1B3.csv'%(misr_path, point,misr_path, point, point_min), i+1)
                        print i
                        print 'flag ', flag, date
                        if flag1 !=0:
                                date_list.append(date)
                                brf = brf.reshape(9,4)
                                ang = ang.reshape(4,9)
                                #n_ang - the number of VZA. For *.dat file with all angles: for n_ang in range(9,10): 
                                for n_ang in xrange(np.size(ang_sample)):#in range(1,10):
                                        print n_ang
                                        f = open(save_path+'misr_%s_%s_chl%d_ang%d_brf.brf'%(misr_path, date, point, n_ang+1), 'w')
                                        #f.write('#PARAMETERS time mask vza vaa sza saa 443.0 555.0 670.0 865.0 sd-443.0 sd-555.0 sd-670.0 sd-865.0\n')
                                        f.write('BRDF %d 4 443.0 555.0 670.0 865.0 0.0040 0.0044 0.0047 0.0054\n'%n_ang)
                                        #for i in misr_ang[0:n_ang]:
                                        for i in xrange(np.size(ang_sample[n_ang])):
                                                #f.write('%d %d %s %s %s %s %s %s %s %s\n'%(1, 1, ang[2,i], ang[3,i], ang[0,i], ang[1,i], brf[i,0], brf[i,1], brf[i,2], brf[i,3]))
                                                f.write('%d %d %s %s %s %s %s %s %s %s\n'%(1, 1, ang[2,ang_sample[n_ang][i]], ang[3,ang_sample[n_ang][i]], \
                                                        ang[0,ang_sample[n_ang][i]], ang[1,ang_sample[n_ang][i]],\
                                                        brf[ang_sample[n_ang][i],0], brf[ang_sample[n_ang][i],1], brf[ang_sample[n_ang][i],2], brf[ang_sample[n_ang][i],3]))
                                        f.close()
                                print date
        date_list.remove('')
        #print date_list
        import datetime
        for i in range(1,2):
                #time_count=
                f_out = open(save_path+'misr_%s_chl%d_ang3.brf'%(misr_path, i),'w')
                f_out.write('BRDF %d 4 443.0 555.0 670.0 865.0 0.016 0.0176 0.0188 0.0216\n'%(len(date_list)*3))
                for date_str in date_list:
                        doy = str( datetime.datetime.strptime(date_str, '%Y.%m.%d').timetuple().tm_yday )
                        f_in = open(save_path+'misr_%s_%s_chl%d_ang3_brf.brf'%(misr_path, date_str, i))
                        tmp_str =  f_in.read().split('\n')[1:]
                        for line in tmp_str[:-1]:
                                #print tmp_str
                                line = line.split()
                                line[0]=doy
                                f_out.write(' '.join(line))
                                #f_out.write(f_in.read().split('\n')[1:])
                                f_out.write('\n')
                        f_in.close()
                f_out.close()
        return ang
        print 'Done MISR csv!'
