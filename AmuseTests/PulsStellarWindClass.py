import numpy as np
from amuse.units import units
from amuse.units import constants

class PulsStellarWind(object):
    """Implementation of stellar winds based on Kudritzki and Puls ARAA 2000 and Vink A&A 2000."""

    def __init__(self, teff, mass, lum, radius):

        self.mass     = mass
        self.lum      = lum
        self.teff     = teff
        self.radius   = radius
        self.thom_sig()
        self.thom_Gam()
        self.vesc()
        self.vterm()
        self.dm_dt()

        return

    def thom_sig(self):
        if self.teff < 3e4 | units.K:
            self.thom_sig = 0.31 # | units.cm**2.0 / units.g
        elif 3e4|units.K <= self.teff < 3.5e4 | units.K:
            self.thom_sig = 0.32 # | units.cm**2.0 / units.g
        else:
            self.thom_sig = 0.33 # | units.cm**2.0 / units.g
        return

    def thom_Gam(self):
        self.thom_Gam = 7.66e-5*self.thom_sig/self.mass.value_in(units.MSun)*self.lum.value_in(units.LSun)
        return

    def vesc(self):
        self.vesc = np.sqrt(2.0*units.constants.G*self.mass*(1-self.thom_Gam)
                            /(self.radius)).as_quantity_in(units.km / units.s)
        return

    def vterm(self):
        if self.teff <= 1.0e4|units.K:
            self.vterm = self.vesc
        elif 1.0e4|units.K < self.teff < 2.1e4|units.K:
            self.vterm = 1.4*self.vesc
        else:
            self.vterm = 2.65*self.vesc
        return

    def dm_dt(self):
        # Above the bi-stability jump (larger than B1).
        if self.teff > 2.75e4|units.K:
            self.dm_dt = 10**(self.mass_loss1()) | units.MSun / units.yr
        # Below the bi-stability jump (smaller than B1).
        elif self.teff < 2.25e4|units.K:
            self.dm_dt = 10**(self.mass_loss2()) | units.MSun / units.yr
        # Linear interpolation between the two.
        else:
            xp = np.array([2.25e4, 2.75e4])
            fp = np.array([self.mass_loss2(2.25e4), self.mass_loss1(2.75e4)])
            self.dm_dt = 10**(np.interp(self.teff.value_in(units.K), xp, fp))  | units.MSun / units.yr
        return

    # Note we make the temp passable so we can interpolate if we need to
    # and we return a value here for the same reason.

    # Above the bi-stability jump (larger than B1).
    def mass_loss1(self, teff=None):

        if teff is None:
            teff = self.teff.value_in(units.K)

        log_dm_dt  = -6.697 + 2.194*np.log10(self.lum.value_in(units.LSun)/1e5) \
                            - 1.313*np.log10(self.mass.value_in(units.MSun)/30.0) \
                            - 1.226*np.log10(self.vterm/self.vesc/2.0) \
                            + 0.933*np.log10(teff/4e4) \
                            - 10.92*np.log10(teff/4e4)**2.0
        return log_dm_dt

    # Below the bi-stability jump (smaller than B1).
    def mass_loss2(self, teff=None):

        if teff is None:
            teff = self.teff.value_in(units.K)

        log_dm_dt  = -6.688 + 2.210*np.log10(self.lum.value_in(units.LSun)/1e5) \
                            - 1.339*np.log10(self.mass.value_in(units.MSun)/30.0) \
                            - 1.601*np.log10(self.vterm/self.vesc/2.0) \
                            + 1.07*np.log10(teff/2e4)
        return log_dm_dt


if __name__ == '__main__':
    pass
