import numpy as np
from linac_design import design_linac
from physics import C_LIGHT, M_PROTON_MEV, get_beta


def generate_particle_bunch(
    num_particles: int = 3000,
    T_0: float = 3.0,
    phi_s_deg: float = -30.0,
    sigma_phi_deg: float = 15.0,
    sigma_T_fraction: float = 0.005,
    seed: int = 20261919,
):
    """Genera el paquete inicial de partículas con desviaciones gaussianas

    alrededor de la partícula síncrona[cite: 10, 14].
    """
    np.random.seed(seed)  # Semilla fija para reproducibilidad[cite: 10, 15]

    phi_s_rad = np.radians(phi_s_deg)
    sigma_phi_rad = np.radians(sigma_phi_deg)  # 15° en radianes[cite: 10, 14]

    # Generar variaciones normales estándar[cite: 10, 14]
    delta_phi = np.random.normal(0.0, sigma_phi_rad, num_particles)
    delta_T = np.random.normal(0.0, sigma_T_fraction * T_0, num_particles)

    # Arreglos de estado inicial (fase en rad, energía en MeV)[cite: 10, 14]
    phi_0 = phi_s_rad + delta_phi
    T_0_bunch = T_0 + delta_T

    return T_0_bunch, phi_0


def track_bunch(
    cell_lengths: np.ndarray,
    particles_T: np.ndarray,
    particles_phi: np.ndarray,
    qV_gap: float = 1.0,
    f_rf: float = 352.2e6,
    error_f: float = 0.0,
    m_MeV: float = M_PROTON_MEV,
):
    """Propaga el paquete de partículas celda por celda aplicando las ecuaciones

    discretas del LINAC[cite: 9, 11, 14].

    Retorna:
        history_T: Matriz de forma (N_celdas + 1, N_partículas) con las energías.
        history_phi: Matriz de forma (N_celdas + 1, N_partículas) con las
        fases.
    """
    # Frecuencia angular modificada si se evalúan errores de RF[cite: 14, 17]
    omega = 2.0 * np.pi * f_rf * (1.0 + error_f)

    num_cells = len(cell_lengths)
    num_particles = len(particles_T)

    # Reservar espacio para almacenar la trayectoria de todas las partículas
    history_T = np.zeros((num_cells + 1, num_particles))
    history_phi = np.zeros((num_cells + 1, num_particles))

    # Guardar condiciones en la entrada (celda 0)
    history_T[0] = particles_T
    history_phi[0] = particles_phi

    T_curr = particles_T.copy()
    phi_curr = particles_phi.copy()

    # Iterar celda por celda (n = 0, 1, ..., N_celdas-1)
    for n in range(num_cells):
        L_n = cell_lengths[n]

        # 1. Ganancia de energía cinética en la brecha: T_{n+1} = T_n + qV * cos(phi_n)[cite: 9, 11, 14]
        T_curr += qV_gap * np.cos(phi_curr)

        # 2. Actualización de velocidad relativista: beta_{n+1}[cite: 9, 11, 14]
        beta = get_beta(T_curr, m_MeV)

        # 3. Avance de fase por tiempo de tránsito en el tubo: phi_{n+1} = phi_n + omega*(L_n / (beta*c)) - 2pi[cite: 9, 11, 14]
        dt = L_n / (beta * C_LIGHT)
        phi_curr = phi_curr + omega * dt - 2.0 * np.pi

        # Guardar en la historia de la celda n+1
        history_T[n + 1] = T_curr
        history_phi[n + 1] = phi_curr

    return history_T, history_phi


if __name__ == "__main__":
    # 1. Diseñar el acelerador de referencia (phi_s = -30°)[cite: 10]
    cell_lengths, T_sync, _ = design_linac()

    # 2. Generar el haz inicial de 3000 protones[cite: 10, 14]
    T0_bunch, phi0_bunch = generate_particle_bunch()

    # 3. Simular el paso por las 55 celdas[cite: 1, 18]
    hist_T, hist_phi = track_bunch(cell_lengths, T0_bunch, phi0_bunch)

    # 4. Evaluación del criterio de captura al final (|Delta phi| < 60°)[cite: 15, 18]
    phi_final = hist_phi[-1]
    T_final = hist_T[-1]
    phi_s_final = np.radians(-30.0)
    T_s_final = T_sync[-1]

    delta_phi_final_deg = np.degrees(phi_final - phi_s_final)
    captured = np.abs(delta_phi_final_deg) < 60.0  #[cite: 15]
    capture_percentage = (np.sum(captured) / len(captured)) * 100.0  #[cite: 15]

    print("=========================================")
    print("   RESULTADOS DEL SEGUIMIENTO DEL HAZ")
    print("=========================================")
    print(f"Partículas simuladas: {len(T0_bunch)}")
    print(
        f"Desviación estándar inicial de fase: 15.0° (Simulada:"
        f" {np.degrees(np.std(phi0_bunch - np.radians(-30.0))):.2f}°)"
    )
    print(f"Partículas capturadas (|Δϕ| < 60°): {capture_percentage:.1f}%")
    print(
        f"Energía promedio final del haz: {np.mean(T_final[captured]):.2f} MeV"
    )
    print("=========================================")