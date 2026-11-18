import numpy as np
import matplotlib.pyplot as plt
from physics import get_beta, get_gamma

# Energía inicial de inyección del informe (3 MeV)
T_in = 3.0
gamma_0 = get_gamma(T_in)
beta_0 = get_beta(T_in)

print(f"--- Verificación Inicial ---")
print(f"Energía de inyección: {T_in} MeV")
print(f"Factor Gamma (γ): {gamma_0:.6f}")
print(f"Velocidad Beta (β = v/c): {beta_0:.6f}")

# Longitud de la primera celda a f = 352.2 MHz (lambda = c / f)
f_rf = 352.2e6
wavelength = 299792458.0 / f_rf
L_1 = beta_0 * wavelength

print(f"Longitud teórica de la 1ª celda: {L_1 * 100:.2f} cm")