import numpy as np

# Constantes físicas fundamentales
C_LIGHT = 299792458.0  # Velocidad de la luz en m/s
M_PROTON_MEV = 938.27  # Masa en reposo del protón en MeV/c^2[cite: 4]
M_ELECTRON_MEV = 0.511  # Masa en reposo del electrón en MeV/c^2[cite: 17]


def get_gamma(T_MeV: float | np.ndarray, m_MeV: float = M_PROTON_MEV):
    """Calcula el factor de Lorentz gamma dada la energía cinética T en MeV[cite: 4, 11]."""
    # Evita energías negativas en partículas desfasadas[cite: 4, 11]
    T_safe = np.maximum(T_MeV, 0.0)
    return 1.0 + (T_safe / m_MeV)  #[cite: 4, 11]


def get_beta(T_MeV: float | np.ndarray, m_MeV: float = M_PROTON_MEV):
    """Calcula la velocidad normalizada beta = v/c dada la energía cinética T en MeV[cite: 4, 11]."""
    gamma = get_gamma(T_MeV, m_MeV)
    arg = 1.0 - 1.0 / (gamma**2)  #[cite: 4, 11]
    arg_safe = np.maximum(arg, 0.0)

    # Cota inferior en 1e-7 para evitar beta = 0 y división por cero en dt = L / (beta * c)[cite: 9, 11, 14]
    beta = np.sqrt(arg_safe)
    return np.maximum(beta, 1e-7)