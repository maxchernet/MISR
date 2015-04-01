# Reading CHRIS SPARC BD
#
import numpy as np

def sparc_bd(f_bd='/media/sf_Barrax/Fields/bd_sparc_2004.txt'):
        f = open(f_bd, 'r')
        tmp_arr = f.read()
        f.close()
        list_arr = tmp_arr.split('\n')
        n_samples = 18
        n_bands = 62
        #Array of ground truth samples
        #sample_arr = np.zeros((n_samples, 7))
        #Array of PROBA reflectance
        #refl_arr = np.zeros((n_samples, n_bands))
        #List of field names
        field_lst = []
        #Angles
        ang = np.zeros((n_samples, 5, 4))
        #ground truth values
        sample = np.zeros((n_samples,8))
        #field names
        field = np.chararray(n_samples, itemsize=3)
        #Coordinates
        coord = np.zeros((n_samples, 2))
        #Values in the proba  cameras
        proba_0 = np.zeros((n_samples, 5, n_bands))
        #proba_36f = np.zeros((n_samples,n_bands))
        #proba_36a = np.zeros((n_samples,n_bands))
        #proba_55f = np.zeros((n_samples,n_bands))
        #proba_55a = np.zeros((n_samples,n_bands))
        #first line of the angular data
        sd = np.zeros(n_bands)
        ang_1 = 69-1
        ang_2 = 70-1
        ang_3 = 71-1
        ang_4 = 72-1
        ang_5 = 73-1
        field_1 = 65-1
        sample_1 = 66-1
        value_1 = 74-1
        #len(list_arr)
        j=0
        step=72
        for i in range(n_samples):
                ang[i,0,:] = list_arr[ang_1+j].split()
                ang[i,1,:] = list_arr[ang_2+j].split()
                ang[i,2,:] = list_arr[ang_3+j].split()
                ang[i,3,:] = list_arr[ang_4+j].split()
                ang[i,4,:] = list_arr[ang_5+j].split()
                field[i] = list_arr[field_1+j].split()[0] 
                coord[i] = list_arr[field_1+j].split()[5:7]
                sample[i,:] = list_arr[sample_1+j].split()
                #print list_arr[sample_1+j].split()
                for b in range(n_bands):
                        proba_0[i,0,b] = list_arr[value_1+j+b].split()[3]
                        proba_0[i,1,b] = list_arr[value_1+j+b].split()[4]
                        proba_0[i,2,b] = list_arr[value_1+j+b].split()[5]
                        proba_0[i,3,b] = list_arr[value_1+j+b].split()[6]
                        proba_0[i,4,b] = list_arr[value_1+j+b].split()[7]
                #print list_arr[j]
                j=j+step
        j=0
        proba_0 = proba_0 * 0.0001
        #proba_36f = proba_36f * 0.0001
        #proba_36a = proba_36a * 0.0001
        #proba_55f = proba_55f * 0.0001
        #proba_55a = proba_55a * 0.0001
        return sample, proba_0, ang, field
#sample_arr, proba_0, ang, field = sparc_bd()
#print sample_arr[17,2], sample_arr[17,3], sample_arr[17,4], sample_arr[17,5], sample_arr[17,6], sample_arr[17,7]
#print field
