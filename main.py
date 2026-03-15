# hlavny_tool.py
import os
import numpy as np
import matplotlib.pyplot as plt

from modules.modul_materialy import get_material, load_materials_from_csv
from modules.modul_critical_field import critical_field
from modules.modul_rrea import rrea_simulation
from modules.modul_bremsstrahlung import bremsstrahlung_energy
from modules.modul_dose import compute_dose

# --- Načítanie dodatočných materiálov (voliteľné) ---
#load_materials_from_csv("extra_materials.csv")  # ak existuje

# --- Definícia experimentu ---
sequence = ["BGO", "SiO2", "Akryl"]       # sekvencia vrstiev
z_lengths = [0.03, 0.05, 0.02]            # hrúbky vrstiev v metroch
E_a = 5e10                                # aplikované pole [V/m]
n0 = 1e3                                  # počiatočná hustota elektrónov

# --- Priečinok na uloženie výsledkov ---
exp_folder = "results/experiment1"
os.makedirs(exp_folder, exist_ok=True)

# --- Spustenie simulácie ---
n_total = n0
z_total = 0.0

for mat_name, z_len in zip(sequence, z_lengths):
    mat = get_material(mat_name)
    
    # 1️⃣ Kritické pole pre aktuálnu vrstvu
    Et = critical_field(mat, adjust_for_material=True)
    
    # 2️⃣ RREA lavína
    n_e, z = rrea_simulation(E_a, Et, n0=n_total, z_max=z_len)
    
    # 3️⃣ Brzdné žiarenie + spätná väzba
    photon_flux, n_feedback = bremsstrahlung_energy(n_e, mat, feedback_factor=0.05)
    
    # 4️⃣ Dozimetria
    dose_Gy, dose_Sv = compute_dose(photon_flux, conversion_factor=1e-6, quality_factor=1.0)
    
    # 5️⃣ Uloženie dát do CSV
    np.savetxt(
        f"{exp_folder}/{mat.name}_data.csv",
        np.column_stack([z, n_e, photon_flux, dose_Gy, dose_Sv]),
        delimiter=",",
        header="z[m],n_e,photon_flux,dose_Gy,dose_Sv",
        comments=""
    )
    
    # 6️⃣ Príprava pre ďalšiu vrstvu
    n_total = n_e[-1] + n_feedback  # zahrnutie spätných elektrónov
    z_total += z_len

# --- Jednoduchá vizualizácia lavíny ---
plt.figure(figsize=(8,5))
for mat_name in sequence:
    data = np.loadtxt(f"{exp_folder}/{mat_name}_data.csv", delimiter=",", skiprows=1)
    plt.plot(data[:,0], data[:,1], label=f"{mat_name} n_e")
plt.xlabel("Z [m]")
plt.ylabel("Hustota elektrónov n_e")
plt.title("RREA lavína v sekvencii materiálov")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{exp_folder}/lavina.png")
plt.show()