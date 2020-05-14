import yt
yt.funcs.mylog.setLevel(40)
import numpy as np
import glob
import pickle

import argparse
import time

parser = argparse.ArgumentParser(description="Create .pickle data files containing time-series information about each sink particle and the gas on which they sit. Written by Sean Lewis, Drexel University")

parser.add_argument("-d", "--directory", default="./", help="Input directory for plot files. Make sure to append *plt* or something similar to the directory path.")

parser.add_argument("-r", "--radius", default=1.0, help="Radius from center of sink particle defining region where gas data is to be gathered. Default is the sink size: radius=1.0")

def empty_array():
    x = np.array([('name',
                   np.zeros(len(data_files)),
                   np.zeros(len(data_files)),
                   np.zeros(len(data_files)),
                   np.zeros(len(data_files)),
                   np.zeros(len(data_files)))]
                 dtype=[('name', 'U10'),
                        ('time', object),
                        ('gas_dens', object),
                        ('gas_pres', object),
                        ('gas_temp', object),
                        ('gas_cs', object)])
    return x

def find_gas_attr_under_sink(data_set, center, radius):
    sph = data_set.sphere(center, radius)
    cell_vol = sph['dx'].min() ** 3

    gas_dens = sph['dens'].mean()
    gas_temp = sph['temp'].mean()
    gas_pres = sph['pres'].mean()
    gas_cs = sph['gas','sound_speed'].mean()
    print gas_cs
    
    return gas_dens, gas_temp, gas_pres, gas_cs

def get_sink_and_gas_mass(data_files, radius):
    master_arr = empty_array()
    
    for ind, file_ in enumerate(data_files):
        print "Loading: ", file_
        ds = yt.load(file_)
        ad = ds.all_data()
        sim_time = ds.current_time.v
        
        sinks_ind = np.where(ad['particle_type'] > 1.0)
        
        if len(sinks_ind[0]) < 1.0:
            print 'No sinks'
            sink_ids = None
        else:
            sink_ids = ad['particle_tag'][sinks_ind]
            for sink in sink_ids:
                sink_name = str(sink.v)
                
                #find location of this particular sink.
                sink_loc = np.where(ad['particle_tag'] == sink)
                sink_center = ad['particle_position'][sink_loc].v[0]
                
                sink_radius = (radius * 2.636687e17, 'cm')
                
                if str(sink.v) not in master_arr['name']:
                    new_arr = empty_array()
                    print 'New sink formed.'
                    print 'Creating new structured numpy array.'
                    gas_dens, gas_temp, gas_pres, gas_cs = find_gas_attr_under_sink(ds, sink_center, sink_radius)
                    
                    new_arr['name'] = sink_name
                    new_arr['time'][0][ind] = sim_time
                    new_arr['gas_dens'][0][ind] = gas_dens.v
                    new_arr['gas_pres'][0][ind] = gas_pres.v
                    new_arr['gas_temp'][0][ind] = gas_temp.v
                    new_arr['gas_cs'][0][ind] = gas_cs.v
                    
                    master_arr = np.vstack((master_arr,new_arr))
                else:
                    sink_arr_loc = np.where(master_arr['name'] == sink_name)
                    
                    gas_dens, gas_temp, gas_pres, gas_cs = find_gas_attr_under_sink(ds, sink_center, sink_radius)
                    
                    master_arr[sink_arr_loc]['time'][0][ind] = sim_time
                    master_arr[sink_arr_loc]['gas_dens'][0][ind] = gas_dens.v
                    master_arr[sink_arr_loc]['gas_pres'][0][ind] = gas_pres.v
                    master_arr[sink_arr_loc]['gas_temp'][0][ind] = gas_temp.v
                    master_arr[sink_arr_loc]['gas_cs'][0][ind] = gas_cs.v

    return master_arr


if (__name__=="__main__"):
    args = parser.parse_args()
    files = args.directory + '*plt*'
    rad_multiplier = float(args.radius)
    data_files = glob.glob(files)
    final_array = get_sink_and_gas_mass(data_files, rad_multiplier)
    pickle.dump(final_array, open("gas_around_sink_data.pickle", "wb"))
