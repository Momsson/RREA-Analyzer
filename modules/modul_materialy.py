# modules/modul_materialy.py
import csv

class Material:
    """
    Trieda reprezentuje fyzikálne vlastnosti materiálu pre RREA simulácie.
    
    Atribúty:
        name: ľudský názov materiálu (napr. "Kremeň")
        Z: atómové číslo
        N_m: hustota molekúl [m^-3]
        I: stredná ionizačná energia [eV]
        photon_efficiency: efektivita produkcie fotónov (0-1)
    """
    def __init__(self, name, Z, N_m, I, photon_efficiency):
        self.name = name
        self.Z = Z
        self.N_m = N_m
        self.I = I
        self.photon_efficiency = photon_efficiency

# Preddefinované materiály s chemickými vzorcami ako kľúče
materials_db = {
    "Bi4Ge3O12": Material("BGO", Z=83, N_m=4.13e28, I=800, photon_efficiency=0.3),
    "SiO2": Material("Kremeň", Z=14, N_m=2.65e28, I=173, photon_efficiency=0.1),
    "C5H8O2": Material("Akryl", Z=6, N_m=1.18e28, I=64, photon_efficiency=0.05),
}

def load_materials_from_csv(csv_file):
    """
    Načíta materiály z CSV a doplní ich do databázy.
    CSV formát: key,name,Z,N_m,I,photon_efficiency
    key: chemický vzorec, používa sa na get_material()
    """
    try:
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row['key']
                name = row['name']
                Z = int(row['Z'])
                N_m = float(row['N_m'])
                I = float(row['I'])
                photon_efficiency = float(row['photon_efficiency'])
                materials_db[key] = Material(name, Z, N_m, I, photon_efficiency)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV súbor {csv_file} sa nenašiel.")
    except KeyError as e:
        raise KeyError(f"CSV súbor chýba stĺpec: {e}")

def get_material(key):
    """
    Vráti objekt materiálu podľa chemického vzorca (key).
    
    Raises:
        ValueError ak materiál nie je v databáze
    """
    if key not in materials_db:
        raise ValueError(f"Materiál '{key}' nie je v databáze")
    return materials_db[key]