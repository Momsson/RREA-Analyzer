# modules/modul_dose.py
import numpy as np

def compute_dose(photon_flux, conversion_factor=1e-6, quality_factor=1.0):
    """
    Prepočíta tok fotónov na dávku (Gray) a jednotky Sievert.
    
    Parametre:
        photon_flux: numpy pole toku fotónov
        conversion_factor: Gy/foton
        quality_factor: faktor pre prevod na Sv
    
    Výstup:
        dose_Gy: numpy pole absorbovanej dávky [Gy]
        dose_Sv: numpy pole dávky v Sievert [Sv]
    """
    dose_Gy = photon_flux * conversion_factor
    dose_Sv = dose_Gy * quality_factor
    return dose_Gy, dose_Sv