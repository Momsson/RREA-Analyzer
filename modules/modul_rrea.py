# modules/modul_rrea.py
import numpy as np

def rrea_simulation(E_a, E_t, n0=1e3, z_max=0.1, dz0=0.001, l0=0.01):
    """
    Simuluje RREA lavínu elektrónov.
    
    Parametre:
        E_a: aplikované elektrické pole [V/m]
        E_t: kritické pole [V/m]
        n0: počiatočná hustota elektrónov
        z_max: maximálna dĺžka simulácie [m]
        dz0: základný krok simulácie [m]
        l0: mierkovací faktor [m]
    
    Výstup:
        n: numpy pole hustoty elektrónov
        z: numpy pole pozícií pozdĺž osi z
    """
    if E_a <= E_t:
        return np.array([n0]), np.array([0.0])

    l_r = (E_a / E_t) / (1 - E_t / E_a) * l0
    z = [0.0]
    n = [n0]

    while z[-1] < z_max:
        dz = dz0 / (1 + n[-1]/n0)  # adaptívny krok podľa rastu
        n_next = n[-1] * np.exp(dz / l_r)
        z.append(z[-1] + dz)
        n.append(n_next)

    return np.array(n), np.array(z)