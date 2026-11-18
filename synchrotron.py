import matplotlib.pyplot as plt
import numpy as np

from linac_design import design_linac
from physics import C_LIGHT, M_PROTON_MEV, get_beta, get_gamma
from tracking import track_bunch


def calculate_theoretical_mu(
    T_sync: np.ndarray, qV_gap: float = 1.0, phi_s_deg: float = -30.0
):
    """Calcula el avance de fase teórico mu_n [grados/celda] en cada etapa del LINAC[cite: 8, 16]."""
    phi_s_rad = np.radians(phi_s_deg)
    sin_term = -np.sin(phi_s_rad)  # Debe ser positivo (-sin(-30°) = 0.5)[cite: 8]

    # Factores relativistas de la partícula síncrona en cada celda[cite: 16]
    gamma = get_gamma(T_sync[1:], M_PROTON_MEV)
    beta = get_beta(T_sync[1:], M_PROTON_MEV)

    # Fórmula teórica: mu^2 = (2*pi * qV * -sin(phi_s)) / (mc^2 * beta^2 * gamma^3)[cite: 8, 16]
    mu_squared = (2.0 * np.pi * qV_gap * sin_term) / (
        M_PROTON_MEV * (beta**2) * (gamma**3)
    )
    mu_rad = np.sqrt(mu_squared)

    return np.degrees(mu_rad)  # Convertir a grados/celda


def simulate_synchrotron_oscillation(
    perturbation_deg: float = 3.0, phi_s_deg: float = -30.0
):
    """Simula la trayectoria de una sola partícula con una perturbación inicial de fase[cite: 16]."""
    cell_lengths, T_sync, _ = design_linac(phi_s_deg=phi_s_deg)

    phi_s_rad = np.radians(phi_s_deg)
    T0_particle = np.array([T_sync[0]])
    phi0_particle = np.array([phi_s_rad + np.radians(perturbation_deg)])

    # Seguimiento celda a celda[cite: 14]
    hist_T, hist_phi = track_bunch(
        cell_lengths, T0_particle, phi0_particle, qV_gap=1.0, f_rf=352.2e6
    )

    # Desviación de fase en grados a lo largo del acelerador[cite: 16]
    delta_phi_deg = np.degrees(hist_phi[:, 0] - phi_s_rad)

    # Avance de fase teórico celda por celda[cite: 16]
    mu_theory_deg = calculate_theoretical_mu(
        T_sync, qV_gap=1.0, phi_s_deg=phi_s_deg
    )

    # Estimar avance de fase simulado en la primera semioscilación (cruces por cero)[cite: 16]
    zero_crossings = []
    for i in range(len(delta_phi_deg) - 1):
        if delta_phi_deg[i] * delta_phi_deg[i + 1] <= 0:
            # Interpolación lineal para estimar la posición exacta de la celda[cite: 16]
            cell_zero = i - delta_phi_deg[i] / (
                delta_phi_deg[i + 1] - delta_phi_deg[i]
            )
            zero_crossings.append(cell_zero)

    if len(zero_crossings) >= 2:
        semi_period_cells = zero_crossings[1] - zero_crossings[0]
        mu_sim_deg = 180.0 / semi_period_cells  # pi / Delta_n en grados[cite: 16]
    else:
        mu_sim_deg = np.nan

    return delta_phi_deg, mu_theory_deg, mu_sim_deg


def plot_synchrotron_results(delta_phi_deg, mu_theory_deg, mu_sim_deg):
    """Grafica la oscilación de fase y la amortiguación adiabática[cite: 18, 19]."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
    cells = np.arange(len(delta_phi_deg))

    # Panel 1: Oscilación de la perturbación de fase[cite: 16, 19]
    ax1.plot(
        cells,
        delta_phi_deg,
        "o-",
        color="#1f77b4",
        linewidth=1.8,
        markersize=3,
        label=r"Simulado ($\delta\phi_0 = +3^\circ$)",
    )
    ax1.axhline(0, color="black", linestyle="--", linewidth=0.8)
    ax1.set_ylabel(r"Desviación $\Delta\phi$ (grados)", fontsize=11)
    ax1.set_title(
        "Oscilaciones de Sincrotrón y Amortiguamiento Adiabático",
        fontsize=12,
        fontweight="bold",
    )
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper right")

    # Panel 2: Evolución del avance de fase mu_n (Teórico vs Medido)[cite: 16, 19]
    ax2.plot(
        cells[1:],
        mu_theory_deg,
        "r--",
        linewidth=2,
        label=r"Teórico $\mu_n$ (Eq. 13)",
    )
    if not np.isnan(mu_sim_deg):
        ax2.axhline(
            mu_sim_deg,
            color="green",
            linestyle="-.",
            linewidth=1.5,
            label=f"Simulado (1ª semioscilación): {mu_sim_deg:.1f}°/celda",
        )
    ax2.set_xlabel("Número de celda $n$", fontsize=11)
    ax2.set_ylabel(r"Avance de fase $\mu$ (°/celda)", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig("fig_sincrotron.png", dpi=300)
    print("Gráfica guardada como 'fig_sincrotron.png'")
    plt.show()


if __name__ == "__main__":
    delta_phi, mu_theory, mu_sim = simulate_synchrotron_oscillation()

    print("=========================================")
    print("  RESULTADOS DE OSCILACIONES SINCROTRÓN")
    print("=========================================")
    print(f"Amplitud inicial: {delta_phi[0]:.2f}°")
    print(f"Amplitud final (Celda 55): {abs(delta_phi[-1]):.2f}°")
    print(f"Avance de fase teórico inicial (Celda 1): {mu_theory[0]:.2f}°/celda")
    print(f"Avance de fase teórico final (Celda 55): {mu_theory[-1]:.2f}°/celda")
    print(f"Avance de fase simulado (1ª semioscilación): {mu_sim:.2f}°/celda")
    print("=========================================")

    plot_synchrotron_results(delta_phi, mu_theory, mu_sim)