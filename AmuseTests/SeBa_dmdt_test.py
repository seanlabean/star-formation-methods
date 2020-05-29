import numpy 

from amuse.community.seba.interface import SeBaInterface, SeBa

from amuse.units import units
from amuse.units import constants
from amuse.datamodel import Particle
from amuse.datamodel import Particles

worker = SeBa()
initial_mass = 50.0 | units.MSun 
star_age = 0.11 | units.Myr # 0.01 | units.Myr
dt = 0.01 | units.Myr # 0.11 | units.Myr

print "======= Run 1 ======="
se_time, se_mass, se_radius, se_lum, se_temp, se_evol_time, se_type = worker.evolve_star(initial_mass, star_age, 0.02)

dm_dt = (initial_mass - se_mass)/dt

worker.stop()
print "Initial Mass: ", initial_mass
print "star age: ", star_age, " dt: ", dt
print "star mass: ", se_mass
print "star evol time: ", se_evol_time
print "Mass loss rate: ", dm_dt.value_in(units.MSun / units.s)

worker = SeBa()
initial_mass = 50.0 | units.MSun 
star_age = 0.01 | units.Myr # 0.01 | units.Myr
dt = 0.11 | units.Myr # 0.11 | units.Myr

print "======= Run 2 ======="
se_time, se_mass, se_radius, se_lum, se_temp, se_evol_time, se_type = worker.evolve_star(initial_mass, star_age, 0.02)

dm_dt = (initial_mass - se_mass)/dt

worker.stop()
print "Initial Mass: ", initial_mass
print "star age: ", star_age, " dt: ", dt
print "star mass: ", se_mass
print "star evol time: ", se_evol_time
print "Mass loss rate: ", dm_dt.value_in(units.MSun / units.s)

worker = SeBa()
initial_mass = 1.0 | units.MSun 
star_age = 0.01 | units.Myr # 0.01 | units.Myr
dt = 11.75 | units.Gyr # 0.11 | units.Myr

print "======= AMUSE Test ======="
se_time, se_mass, se_radius, se_lum, se_temp, se_evol_time, se_type = worker.evolve_star(initial_mass, star_age, 0.02)

dm_dt = (initial_mass - se_mass)/dt

worker.stop()
print "Initial Mass: ", initial_mass
print "star age: ", star_age, " dt: ", dt
print "star mass: ", se_mass
print "star evol time: ", se_evol_time
print "Mass loss rate: ", dm_dt.value_in(units.MSun / units.s)
