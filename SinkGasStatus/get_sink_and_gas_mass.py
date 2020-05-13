import yt
yt.funcs.mylog.setLevel(40)
import numpy as np
import glob
import pickle

import argparse
import time

parser = argparse.ArgumentParser(description="Create .pickle data files containing time-series information about each sink particle and the gas on which they sit. Written by Sean Lewis, Drexel University")

parser.add_argument("-d", "--directory", default="./", help="Input directory for plot files. Make sure to append *plt* or something similar to the directory path.")

def empty_array():
    x = np.array([('name', np.zeros(len(data_files)),
                   np.zeros(len(data_files)),
                   np.zeros(len(data_files)),
                   np.zeros(len(data_files)),
                   np.zeros(len(data_files)),
                   np.zeros(len(data_files)))],
                 dtype=[('name', 'U10'),
                        ('time', object),
                        ('sink_mass', object),
                        ('gas_mass', object),
                        ('sink_accr', object),
                        ('stars_in_sink', object),
                        ('star_mass_sink', object)])
    return x

def find_gas_under_sink(data_set, center, radius):
    sph = data_set.sphere(center, radius)
    cell_vol = sph['dx'].min() ** 3
    #print sph['dens']
    stars_ind = np.where(sph['particle_type'] < 2.0)
    gas_mass_tot = 0
    for den in sph['dens']:
        gas_mass_tot += den * cell_vol

    star_masses = sph['particle_mass'][stars_ind]
    stars_mass_tot = star_masses.sum()
    num_stars = len(star_masses)
    return gas_mass_tot, star_mass_tot, num_stars

def get_sink_and_gas_mass(data_files):
    master_arr = empty_array()
    
    for ind, file_ in enumerate(data_files):
        #print file_
        #print ind
        ds = yt.load(file_)
        ad = ds.all_data()
        sim_time = ds.current_time.v
        
        sinks_ind = np.where(ad['particle_type'] > 1.0)
        
        #yes_sinks.any() == 2.0
        #print ad['particle_type'].v
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
                #print 'sink center: ', sink_center[0]
                sink_radius = (2.636687e17, 'cm')
                
                if str(sink.v) not in master_arr['name']:
                    new_arr = empty_array()

                    gas_mass, star_mass, num_stars = find_gas_under_sink(ds, sink_center, sink_radius)
                    
                    new_arr['name'] = sink_name
                    new_arr['time'][0][ind] = sim_time
                    new_arr['sink_mass'][0][ind] = ( ad['particle_mass'][sink_loc].v )
                    new_arr['gas_mass'][0][ind] = ( gas_mass.v )
                    new_arr['sink_accr'][0][ind] = ( ad['particle_accr_rate'][sink_loc].v )
                    new_arr['stars_in_sink'][0][ind] = ( num_stars )
                    new_arr['star_mass_sink'][0][ind] = ( star_mass.v )
                    
                    master_arr = np.vstack((master_arr,new_arr))
                else:
                    sink_arr_loc = np.where(master_arr['name'] == sink_name)

                    gas_mass, star_mass, num_stars = find_gas_and_stars_under_sink(ds, sink_center, sink_radius)
                    
                    master_arr[sink_arr_loc]['time'][0][ind] = sim_time
                    master_arr[sink_arr_loc]['sink_mass'][0][ind] = ( ad['particle_mass'][sink_loc].v )
                    master_arr[sink_arr_loc]['gas_mass'][0][ind] = ( gas_mass.v )
                    master_arr[sink_arr_loc]['sink_accr'][0][ind] = ( ad['particle_accr_rate'][sink_loc].v )
                    master_arr[sink_arr_loc]['stars_in_sink'][0][ind] = ( num_stars )
                    master_arr[sink_arr_loc]['star_mass_sink'][0][ind] = ( star_mass.v )
            #print master_arr['gas_mass']
        #print sink_ids
    return master_arr


if (__name__=="__main__"):
    args = parser.parse_args()
    files = args.directory + '*plt*'
    print files
    data_files = glob.glob(files)
    print data_files
    final_array = get_sink_and_gas_mass(data_files)
    pickle.dump(final_array, open("sink_and_star_data.pickle", "wb"))
