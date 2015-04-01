#Create EO-LDAS config files for arbitrary number of view angels (vza) 
#when each vza corresponds to single observational operator
#
def write_config(n_obs, bands, sds, conf_file, lst_state, lst_result, param_result, prior_result):
        #n_obs - a number of observation operators
        #conf_file - config file to write
        #lst_state - list of state files for each obs. op.
        #lst_result - forward result files for each obs. op.
        #param_result - output state parameters
        #prior_result - output prior
        f = open('/home/max/misr/conf/misr')
        part1_buf = f.read()
        part1_buf = part1_buf.replace('filename =', 'filename = \''+param_result+'\'', 1)
        f.close()
        f = open('/home/max/misr/conf/misr_prior')
        part_prior = f.read()
        f.close()
        f = open(conf_file, 'w')
        part_obs_buf = ''
        #part_prior_buf = ''
        part1_buf = part1_buf + '\nprior.name = Operator\nprior.datatypes = x, y'
        for i in xrange(n_obs):
                part1_buf = part1_buf + '\nobs%d.name=Observation_Operator\nobs%d.datatypes = x,y'%((i+1), (i+1))
                f1 = open('/home/max/misr/conf/misr_obs')
                part_obs = f1.read()
                f1.close()
                part_obs_new = part_obs.replace('.obs.', '.obs%d.'%(i+1))
                part_obs_new = part_obs_new.replace("names = '865.0'.split()", "names ="+"'"+bands[i]+"'.split()")
                part_obs_new = part_obs_new.replace("sd = '0.0054'.split()", "sd ="+"'"+str(sds[i])+"'.split()\n")
                part_obs_new = part_obs_new.replace('state =', 'state = \''+lst_state[i]+'\'')
                part_obs_new = part_obs_new.replace('filename =', 'filename = \''+lst_result[i]+'\'', 1)
                part_obs_new = part_obs_new.replace('semidiscrete1', 'semidiscrete%d'%(i+1), 1)
                part_obs_buf = part_obs_buf + part_obs_new+'\n'
        part_prior = part_prior.replace('filename =', 'filename = \''+prior_result+'\'', 1)
        f.write(part1_buf + '\n\n' + part_prior + '\n\n' + part_obs_buf)
        f.close()

def do_config(conf_file, n_obs, bands, sds, lst_state, lst_result, f_result_param, f_prior):
        write_config(n_obs, bands, sds, conf_file, lst_state, lst_result, f_result_param, f_prior)
        print 'Done do_config!'
        return conf_file
#do_config(1)
