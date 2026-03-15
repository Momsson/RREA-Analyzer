# modules/modul_bremsstrahlung.py
import numpy as np

def bremsstrahlung_energy(n_e, material, feedback_factor=0.05):
    """
    Prepočíta hustotu elektrónov na tok fotónov a simuluje spätnú väzbu fotoefektu.
    
    Parametre:
        n_e: numpy pole hustoty elektrónov pozdĺž z
        material: objekt Material
        feedback_factor: časť fotónov, ktoré generujú nové elektróny spätnou väzbou (0-1)
    
    Výstup:
        photon_flux: numpy pole toku fotónov
        n_feedback: počet nových elektrónov vytvorených spätnou väzbou
    """
    photon_flux = n_e * material.photon_efficiency
    n_feedback = photon_flux[0] * feedback_factor  # spätná väzba na začiatku vrstvy
    return photon_flux, n_feedback