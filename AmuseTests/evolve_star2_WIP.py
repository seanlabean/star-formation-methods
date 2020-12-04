"""
   Minimal routine for running a stellar evolution code
"""

from amuse.lab import *

def print_star(s, unfmt=False):
    p = s.particles[0]
    if unfmt:
        e = ' '
        print(f'{s.model_time.value_in(units.Myr)}', end=e)
        print(f'{p.mass.value_in(units.MSun)}', end=e)
        print(f'{p.radius.value_in(units.RSun)}', end=e)
        print(f'{p.luminosity.value_in(units.LSun)}', end=e)
        print(f'{p.temperature.value_in(units.K)}')
    else:
        e = '  '
        print(f't = {s.model_time.value_in(units.Myr):.2f} Myr', end=e)
        print(f'M = {p.mass.value_in(units.MSun):.2e} MSun', end=e)
        print(f'R = {p.radius.value_in(units.RSun):.2e} RSun', end=e)
        print(f'L = {p.luminosity.value_in(units.LSun):.2e} LSun', end=e)
        print(f'{p.stellar_type}')
    
def main(m, z, end_time, time_step, unfmt):
    stellar = Seba()
    stellar.parameters.metallicity = z
    stellar.particles.add_particle(Particle(mass=m))
    print_star(stellar, unfmt)
    
    while stellar.model_time < end_time-0.5*time_step:
        stellar.evolve_model(stellar.model_time+time_step)
        #print("evolve model:")
        print_star(stellar, unfmt)
        #_tmp = stellar.evolve_star(m, stellar.model_time+time_step, 0.02)
        #se_time, se_mass, se_radius, se_lum, se_temp, se_evol_time, se_type = _tmp
        #print(stellar.model_time.value_in(units.Myr), se_mass.value_in(units.MSun), se_radius.value_in(units.RSun), se_lum.value_in(units.LSun), se_temp.value_in(units.K)) 
        #print("evolve star:")
        #print("t =", stellar.model_time, " M = {:.2e}".format(se_mass.value_in(units.MSun)), "MSun",
        #      " R = {:.2e}".format(se_radius.value_in(units.RSun)), "RSun",
        #      " L = {:.2e}".format(se_lum.value_in(units.LSun)), "LSun ",  se_type)
        #print(" ")
        stellar.model_time += time_step
        if stellar.particles.stellar_type.number[0] >= 10: break #or se_type.value_in(units.stellar_type) >= 10: break	# remnant
        #if se_type.value_in(units.stellar_type) >= 10: break
        
    stellar.stop()

def new_option_parser():
    from amuse.units.optparse import OptionParser
    result = OptionParser()
    result.add_option("-d", unit=units.Myr,
                      dest="time_step", type="float", 
                      default=0.01|units.Myr,
                      help="time step of the simulation [%default]")
    result.add_option("-m", unit=units.MSun,
                      dest="m", type="float", default=50.0|units.MSun,
                      help="initial stellar mass [%default]")
    result.add_option("-t", unit=units.Myr,
                      dest="end_time", type="float", 
                      default=10.0|units.Myr,
                      help="end time of the simulation [%default]")
    result.add_option("-u", dest="unfmt", default=False,
                      action="store_true", help="unformatted output [%default]")
    result.add_option("-z", dest="z", type="float", 
                      default=0.02, help="metallicity [%default]")
    return result

if __name__ in ('__main__', '__plot__'):
    o, arguments  = new_option_parser().parse_args()
    main(**o.__dict__)
