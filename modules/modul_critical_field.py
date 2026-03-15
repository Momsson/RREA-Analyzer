# modules/modul_critical_field.py

def critical_field(materials, thicknesses=None, adjust_for_material=True):
    """
    Vypočíta kritické pole E_t.
    
    Parametre:
        materials: objekt Material alebo zoznam materiálov
        thicknesses: zoznam hrúbok materiálov (m), len pri kombinácii vrstiev
        adjust_for_material: bool, ak True, E_t sa upraví podľa hustoty a I materiálu
    """
    m = 9.10938356e-31      # kg, hmotnosť elektrónu
    e = 1.602176634e-19     # C, elementárny náboj
    c = 3e8                 # m/s, rýchlosť svetla
    tau = 1e-12             # s, charakteristický čas

    def compute_Et(mat):
        E_t = (21.7 * m * c) / (e * tau)
        if adjust_for_material:
            N_ref = 1e28
            I_ref = 100  # eV
            alpha, beta = 0.5, 0.3
            E_t *= (mat.N_m / N_ref)**alpha * (mat.I / I_ref)**beta
        return E_t

    if isinstance(materials, list):
        if thicknesses is None or len(thicknesses) != len(materials):
            raise ValueError("Pri kombinovaných materiáloch musí byť rovnaký počet hrúbok")
        Ets = [compute_Et(mat) for mat in materials]
        # vážený priemer podľa hrúbky
        E_t_combo = sum(E * d for E, d in zip(Ets, thicknesses)) / sum(thicknesses)
        return E_t_combo
    else:
        return compute_Et(materials)