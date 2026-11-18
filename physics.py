import numpy as np

# Constantes físicas fundamentales
C_LIGHT = 299792458.0       # Velocidad de la luz en m/s
M_PROTON_MEV = 938.27       # Masa en reposo del protón en MeV/c^2

def get_gamma(T_MeV: float | np.ndarray, m_MeV: float = M_PROTON_MEV):
    """Calcula el factor de Lorentz gamma dada la energía cinética T en MeV."""
    return 1.0 + (T_MeV / m_MeV)

def get_beta(T_MeV: float | np.ndarray, m_MeV: float = M_PROTON_MEV):
    """Calcula la velocidad normalizada beta = v/c dada la energía cinética T en MeV."""
    gamma = get_gamma(T_MeV, m_MeV)
    return np.sqrt(1.0 - 1.0 / (gamma**2))