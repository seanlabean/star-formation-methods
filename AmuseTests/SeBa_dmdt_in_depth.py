# We are interested in if there are any discrepancies in how stellar mass evolution
# is handled/reported in Torch. 
# Questions:
#     1. How do SeBa methods for dmdt calculation compare?
#        a. SeBa evolve through star's full track starting from star's initial mass
#           to time t. Evolve again to t+dt. dmdt = (m(t)-m(t+dt))/dt
#        b. SeBa evolve over short-ish time step using star's current mass from time t to dt
#           dmdt = (current_mass - m(t+dt))/dt
#        c. Vink 2000 prescription (outside of SeBa) used in Torch.
# -SCL 08/23/2020

import numpy as np

from amuse.community.seba.interface import SeBaInterface, SeBa

from amuse.units import units
from amuse.units import constants
from amuse.datamodel import Particle
from amuse.datamodel import Particles
from PulsStellarWindClass import PulsStellarWind

worker = SeBa()
initial_mass = 50.0 | units.MSun # The ZAMS mass of our star
star_age = 1.0 | units.Myr # The star's age at the previous evolution call (corresponding to m(t) above) 
dt = 100.0 | units.yr # The simulation time that has passed since the previous evolution call.

print "======= Run 1 ======="
print "======= What Torch 'seba' Method Does======="
print "Evolve star from ZAMS to t"
se_time_t, se_mass_t, se_radius_t, se_lum_t, se_temp_t, se_evol_time_t, se_type_t = worker.evolve_star(initial_mass, star_age, 0.02)

worker.stop()

worker = SeBa()
initial_mass = 50.0 | units.MSun # The ZAMS mass of our star
star_age = 1.0 | units.Myr # The star's age at the previous evolution call (corresponding to m(t) above) 
dt = 100.0 | units.yr # The simulation time that has passed since the previous evolution call.

print "Evolve same star from ZAMS to t+dt"
se_time_tdt, se_mass_tdt, se_radius_tdt, se_lum_tdt, se_temp_tdt, se_evol_time_tdt, se_type_tdt = worker.evolve_star(initial_mass, star_age+dt, 0.02)

worker.stop()

dm_dt = (se_mass_t - se_mass_tdt)/dt

print "Initial Mass: ", initial_mass
print "star age: ", star_age, " dt: ", dt
print "star mass at t: ", se_mass_t
print "star mass at t+dt: ", se_mass_tdt
print "star type: ", se_type_tdt

print "Mass loss rate: ", dm_dt.value_in(units.MSun / units.s)






print "======= Run 2 ======="
worker = SeBa()
print "Evolve star from mass at time t from Run 1 to t+dt"

se_time_tdt_run2, se_mass_tdt_run2, se_radius_tdt_run2, se_lum_tdt_run2, se_temp_tdt_run2, se_evol_time_tdt_run2, se_type_tdt_run2 = worker.evolve_star(se_mass_t, star_age+dt, 0.02)

worker.stop()

dm_dt = (se_mass_t - se_mass_tdt_run2)/dt

print "Starting mass m(t): ", se_mass_t
print "star age: ", star_age, " dt: ", dt
print "star mass at t: ", se_mass_t
print "star mass at t+dt: ", se_mass_tdt
print "star type: ", se_type_tdt_run2

print "Mass loss rate: ", dm_dt.value_in(units.MSun / units.s)

worker.stop()



print "======= Run 3 ======="

star_wind = PulsStellarWind(se_temp_tdt, se_mass_t, se_lum_tdt, se_radius_tdt)

dm_dt = star_wind.dm_dt
final_mass = se_mass_t - dm_dt * dt
print "Starting mass m(t): ", se_mass_t
print "star age: ", star_age, " dt: ", dt
print "star mass at t: ", se_mass_t
print "star mass at t+dt: ", final_mass
print "star type: ", se_type_tdt

print "Mass loss rate: ", dm_dt.value_in(units.MSun / units.s)


