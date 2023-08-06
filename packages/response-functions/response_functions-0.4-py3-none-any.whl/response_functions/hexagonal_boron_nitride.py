"""
Material parameters for hexagonal boron nitride
"""
import numpy as np
import warnings
from response_functions.common import *

lightspeed = 299792458. #m/s
cm_1 = 2*np.pi*lightspeed*1e2   # angular frequency from cm^-1

def permittivity_Geick(omega):
    """
    Epsilon of hexagonal boron nitride/epsilon_0.
    This is a two-component permittivity for in-plane electric field,
    out-of-plane electric field.

    This is based on Geick et al., 1966.
    Note that this BN is likely a fairly dirty sample with misaligned
    crystallites. It should not be used for exfoliated monocrystals of
    h-BN.
    """

    ## FROM GEICK (1966)
    perp = (4.95
            +(1.23e5/ 767.**2)*lor(omega, 767.*cm_1,35.*cm_1) #should be inactive
            +(3.49e6/1367.**2)*lor(omega,1367.*cm_1,29.*cm_1)
            )
    par  = (4.10
            +(3.25e5/ 783.**2)*lor(omega, 783.*cm_1, 8.*cm_1)
            +(1.04e6/1510.**2)*lor(omega,1510.*cm_1,80.*cm_1) # should be inactive
            )
    return perp, par

def permittivity_Cai(omega):
    """
    Epsilon of hexagonal boron nitride/epsilon_0.
    This is a two-component permittivity for in-plane electric field,
    out-of-plane electric field.

    This is based on Cai et al., 10.1016/j.ssc.2006.10.040 .
    """
    perp = (4.87
            +1.83*lor(omega, 1372.*cm_1, 0.)
            )
    par  = (2.95
            + 0.61*lor(omega, 746.*cm_1, 0.)
            )

    return perp, par

def permittivity_Cai_variable(omega,widthperp = 52.4, widthpar = 15.3):
    """
    Epsilon of hexagonal boron nitride/epsilon_0.
    This is a two-component permittivity for in-plane electric field,
    out-of-plane electric field.

    Optional parameters widthperp, widthpar are decay rates
    (in cm_1 -- WARNING: NON-CONSISTENT UNITS) to add losses to the
    Cai model (see permittivity_Cai) which does not specify losses.

    The default losses are made up.
    """
    warnings.warn('permittivity_Cai_variable is deprecated - WILL BE REMOVED')
    perp = (4.87
            +1.83*lor(omega, 1372.*cm_1, widthperp*cm_1)
            )
    par  = (2.95
            + 0.61*lor(omega, 746.*cm_1, widthpar*cm_1)
            )

    return perp, par

def permittivity_Cai_lossy(omega,decay_inplane=7*cm_1,decay_outplane=2*cm_1):
    """
    Epsilon of hexagonal boron nitride/epsilon_0.
    This is a two-component permittivity for in-plane electric field,
    out-of-plane electric field.

    Optional parameters decay_inplane, decay_outplane are amplitude decay
    rates (in s^-1) to add losses to the Cai model (see permittivity_Cai)
    which does not specify losses.
    Their default values are taken from permittivity_Caldwell().
    """
    perp = (4.87
            +1.83*lor(omega, 1372.*cm_1, decay_inplane)
            )
    par  = (2.95
            + 0.61*lor(omega, 746.*cm_1, decay_outplane)
            )

    return perp, par

def permittivity_Caldwell(omega):
    """
    Epsilon of hexagonal boron nitride/epsilon_0.
    This is a two-component permittivity for in-plane electric field,
    out-of-plane electric field.

    This is a "best guess" by J. Caldwell, used to produce Figure 1b in his
    paper arXiv:1404.0494.
    """
    perp = (4.90
            + 2.001*lor(omega, 1360.*cm_1, 7*cm_1)
            )
    par  = (2.95
            + 0.5262*lor(omega, 760.*cm_1, 2*cm_1)
            )

    return perp, par


def permittivity_Caldwell_isotopic(omega, isotope = ''):
    isotope_split = isotope.split(sep='_')
    switcher = {'10' : _permittivity_Caldwell_10,
                '11' : _permittivity_Caldwell_11,
                '' : _permittivity_Caldwell_mixed,
                'idealized' : _permittivity_Caldwell_idealized}
    kwargs = {}
    if len(isotope_split) > 1:
        kwargs["factor"] = float(isotope_split[1])

    return switcher[isotope_split[0]](omega,**kwargs)

def _permittivity_Caldwell_10(omega,**kwargs):
    
    perp = (5.1
            + 2.0400 * lor(omega, 1394.5*cm_1, 1.8*cm_1)
            )
    par  = (2.5
            + 0.3968 * lor(omega, 785.*cm_1, 1*cm_1)
            )

    return perp, par

def _permittivity_Caldwell_11(omega,**kwargs):
    
    perp = (5.32
            + 2.1267 * lor(omega, 1359.8*cm_1, 2.1*cm_1)
            )
    par  = (3.15
            + 0.5116 * lor(omega, 755.*cm_1, 1*cm_1)
            )
    return perp, par

def _permittivity_Caldwell_mixed(omega,**kwargs):
    
    perp = (4.90
            + 1.9049*lor(omega, 1366.2*cm_1, 7*cm_1)
            )
    par  = (2.95
            + 0.5262*lor(omega, 760.*cm_1, 2*cm_1)
            )
    return perp, par

def _permittivity_Caldwell_idealized(omega, factor):
    
    perp = (5.32
            + 2.1267 * lor(omega, 1359.8*cm_1, 2.1*cm_1*factor)
            )
    par  = (3.15
            + 0.5116 * lor(omega, 755.*cm_1, 1*cm_1*factor)
            )
    return perp, par


permittivity = permittivity_Cai