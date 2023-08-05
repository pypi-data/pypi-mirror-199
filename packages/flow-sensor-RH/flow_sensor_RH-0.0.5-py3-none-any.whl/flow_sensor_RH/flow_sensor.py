import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.interpolate as interp
import flow_sensor_RH as fsRH

def getTh_C(Ta_C = 25, DTh = 50):
    """
    Get the heater temperature in degrees Celsius.
    
    Parameters:
        Ta_C - Ambient temperature in degrees Celsius
        DTh  - Constant temperature difference (Overheated temperature difference)
        default: 
            Ta_C = 25
            DTh = 50
        
    Returns:
        Th_C - Heater temperature in degrees Celsius
    """
    Th_C = Ta_C + DTh_C
    return Th_C

def getTf_C(Ta_C = 25, DTh = 50):
    """
    Get the film temperature in degrees Celsius.
    
    Parameters:
        Ta_C - Ambient temperature in degrees Celsius
        DTh  - Constant temperature difference (Overheated temperature difference)
        default: 
            Ta_C = 25
            DTh = 50
        
    Returns:
        Tf_C - Film temperature in degrees Celsius
    """
    Th_C = getTh_C(Ta_C = Ta_C, DTh = DTh)
    Tf_C = (Ta_C + Th_C) / 2.0
    return Tf_C

def getTf_K(Tf_C):
    """
    Get the film temperature in Kelvin.
    
    Parameters:
        Tf_C - Film temperature in degrees Celsius
        
    Returns:
        Tf_K - Film temperature in Kelvin
    """
    Tf_K = Tf_C + 273.15
    return Tf_K
    
def getPsv(Tf_C):
    """
    Get the saturated vapor pressure.
    
    Parameters:
        Tf_C - Film temperature in degrees Celsius
        
    Returns:
        Psv  - Saturated vapor pressure
    """
    Psv = 610.7 * 10**(7.5 * Tf_C / (237.3 + Tf_C))
    return Psv
    
def getFactor_PT(Tf_C):
    xi_1 = 3.53624e-4 + 2.93228e-5 * Tf_C \
           + 2.61474e-7 * Tf_C**2 + 8.57538e-9 * Tf_C**3
    xi_2 = np.exp(-10.7588 + 6.32529e-2 * Tf_C \
           - 2.53591e-4 * Tf_C**2 + 6.33784e-7 * Tf_C**3)
    Psv = getPsv(Tf_C)
    _, _, P0, _ = fsRH.get_constant.getConstant()
    Factor_PT = np.exp(xi_1 * (1 - Psv / P0) + xi_2 * (Psv / P0 - 1))
    return Factor_PT

def getxsv(Tf_C):
    Factor_PT = getFactor_PT(Tf_C)
    Psv = getPsv(Tf_C)
    _, _, P0, _ = fsRH.get_constant.getConstant()
    xsv = Factor_PT * Psv / P0
    return xsv

def getxv(Tf_C, RH):
    assert(RH >= 0.0 and RH <= 1.0), "RH should be in range [0, 1]"
    xsv = getxsv(Tf_C)
    xv = xsv * RH
    return xv
