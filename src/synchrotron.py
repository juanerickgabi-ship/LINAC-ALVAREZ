import os
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
    sin_term = -np.sin(phi_s_rad)  # -sin(-30°) = 0.5[cite: 8]

    # Factores relativistas de la partícula síncrona en cada celda[cite: 16]
    gamma = get_gamma(T_sync[1:], M_PROTON_MEV)
    beta = get_beta(T_sync[1:], M_PROTON_MEV)

    # Ecuación teórica: mu^2 = (2*pi * qV * -sin(phi_s)) / (mc^2 * beta^2 * gamma^3)[cite: 8, 16]
    mu_squared = (2.0 * np.pi * qV_gap * sin_term) / (
        M_PROTON_MEV * (beta**2) * (gamma**3)
    )
    mu_rad = np.sqrt(mu_squared)

    return np.degrees(mu_rad)  # Convertir a grados/celda


def simulate_synchrotron_oscillation(
    perturbation_deg: float = 3.0, phi_s_deg: float = -30.0
):
    """Simula la trayectoria de una partícula perturbada y calcula el avance de fase

    en cada semioscilación[cite: 16].
    """
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

    # Encontrar las posiciones de TODOS los cruces por cero mediante interpolación lineal[cite: 16]
    zero_crossings = []
    for i in range(len(delta_phi_deg) - 1):
        if delta_phi_deg[i] * delta_phi_deg[i + 1] <= 0:
            cell_zero = i - delta_phi_deg[i] / (
                delta_phi_deg[i + 1] - delta_phi_deg[i]
            )
            zero_crossings.append(cell_zero)

    # Calcular avance de fase mu = 180° / Delta_n para cada semioscilación[cite: 16]
    sim_cells_mid = []
    sim_mu_points = []
    for k in range(len(zero_crossings) - 1):
        semi_period = zero_crossings[k + 1] - zero_crossings[k]
        mu_k = 180.0 / semi_period
        cell_mid = (zero_crossings[k] + zero_crossings[k + 1]) / 2.0
        sim_cells_mid.append(cell_mid)
        sim_mu_points.append(mu_k)

    return (
        delta_phi_deg,
        mu_theory_deg,
        np.array(sim_cells_mid),
        np.array(sim_mu_points),
    )


def plot_synchrotron_results(
    delta_phi_deg, mu_theory_deg, sim_cells_mid, sim_mu_points
):
    """Grafica la oscilación de fase y la comparación continua vs discreta del avance de fase[cite: 18, 19]."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 7.5), sharex=True)
    cells = np.arange(len(delta_phi_deg))

    # Panel 1: Oscilación de la perturbación de fase
    ax1.plot(
        cells,
        delta_phi_deg,
        "o-",
        color="#1f77b4",
        linewidth=1.8,
        markersize=4,
        label=r"Simulado ($\delta\phi_0 = +3^\circ$)",
    )
    ax1.axhline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.7)
    ax1.set_ylabel(r"Desviación $\Delta\phi$ (grados)", fontsize=11)
    ax1.set_title(
        "Oscilaciones de Sincrotrón y Amortiguamiento Adiabático",
        fontsize=12,
        fontweight="bold",
    )
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper right")

    # Panel 2: Avance de fase mu_n (Curva teórica continua vs Puntos medidos por semioscilación)[cite: 16, 19]
    ax2.plot(
        cells[1:],
        mu_theory_deg,
        "r--",
        linewidth=2,
        label=r"Teórico $\mu_n$ (Modelación lineal)",
    )

    if len(sim_mu_points) > 0:
        ax2.plot(
            sim_cells_mid,
            sim_mu_points,
            "go-",
            linewidth=1.5,
            markersize=6,
            label=r"Simulado (Mediciones por semioscilación)",
        )

        # Anotar los valores medidos sobre cada punto verde
        for z, mu in zip(sim_cells_mid, sim_mu_points):
            ax2.annotate(
                f"{mu:.1f}°",
                (z, mu),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=9,
                color="darkgreen",
                weight="bold",
            )

    ax2.set_xlabel("Número de celda $n$", fontsize=11)
    ax2.set_ylabel(r"Avance de fase $\mu$ (°/celda)", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right")

    plt.tight_layout()

    # Guardar la imagen mejorada en la carpeta figuras
    os.makedirs("../LINAC ALVAREZ/figuras", exist_ok=True)
    filepath = "../LINAC ALVAREZ/figuras/fig03_sincrotron.png"
    plt.savefig(filepath, dpi=300)
    print(f"Gráfica actualizada y guardada correctamente en '{filepath}'")
    plt.show()


if __name__ == "__main__":
    delta_phi, mu_theory, sim_cells_mid, sim_mu_points = (
        simulate_synchrotron_oscillation()
    )

    print("=========================================")
    print("  RESULTADOS DE OSCILACIONES SINCROTRÓN")
    print("=========================================")
    print(f"Amplitud inicial: {delta_phi[0]:.2f}°")
    print(f"Amplitud final (Celda 55): {abs(delta_phi[-1]):.2f}°")
    print(f"Avance teórico inicial (Celda 1): {mu_theory[0]:.2f}°/celda")
    print(f"Avance teórico final (Celda 55): {mu_theory[-1]:.2f}°/celda")
    for i, (c, m) in enumerate(zip(sim_cells_mid, sim_mu_points), 1):
        print(f"Semioscilación {i} (Celda ~{c:.1f}): {m:.2f}°/celda")
    print("=========================================")

    plot_synchrotron_results(
        delta_phi, mu_theory, sim_cells_mid, sim_mu_points
    )