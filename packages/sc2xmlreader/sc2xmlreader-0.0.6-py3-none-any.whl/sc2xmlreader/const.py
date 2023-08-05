"""Constants for sc2reader package"""
from __future__ import absolute_import
from enum import Enum

# Default config for Solvis Remote.
DEFAULT_USERNAME = "solvis"
DEFAULT_PASSWORD = "solvis"
HEATING_MANUFACTURER = "Solvis"

class VIA_DEVICE(Enum): 
                XML = 1, 
                ModBus = 2

class HEATING_DEVICE_TYPE(Enum): 
    SolvisMax_6 = 1, 
    SolvisMax_7 = 2, 
    SolvisStrato = 3,
    SolvisBen = 4 

class HEATING_TYPE(Enum): 
    Gas_Brennwert_SX = 1,
    Öl_Brennwert = 2,
    Öl_Niedertemperatur = 3,
    Pellet = 4,
    Fernwärme_FW = 5,
    Wärmepumpe_integriert = 6,
    Wärmepumpe_SolvisVaero = 7,
    Wärmepumpe_SolvisTeo = 8,
    Fremdhersteller = 9

class HEATING_CIRCUIT_TYPE(Enum):
    NONE = 0, 
    HT = 1,
    NT = 2