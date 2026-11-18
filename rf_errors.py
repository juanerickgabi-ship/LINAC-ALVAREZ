import matplotlib.pyplot as plt
import numpy as np

from linac_design import design_linac
from tracking import generate_particle_bunch, track_bunch


def simulate_frequency_errors(
    error_list: list[float] = [0.0, 0.002, 0.005, 0.01, 0.02, 0.04],
    phi_s_deg: float = -30.0,
    num_particles: int = 3000,
    seed: int = 20261919,
):
    """Simula el comportamiento del paquete de partículas ante distintos errores

    relativos en la frecuencia de radiofrecuencia[cite: 10, 17].
    """
    # 1. Diseñar el LINAC a la frecuencia de diseño nominal[cite: 10, 17]
    cell_lengths, T_sync, _ = design_linac(phi_s_deg=phi_s_deg)
    phi_s_rad = np.radians(phi_s_deg)

    # 2. Generar el paquete inicial reproducible de 3000 partículas[cite: 10, 14, 15]
    T0_bunch, phi0_bunch = generate_particle_bunch(
        num_particles=num_particles, phi_s_deg=phi_s_deg, seed=seed
    )

    results = []

    print("=================================================================")
    print("   EFECTO DE ERRORES EN LA FRECUENCIA DE RADIOFRECUENCIA (RF)    ")
    print("=================================================================")
    print(
        "Error RF (%) | Capturadas (%) | E_final (MeV) | Desplazamiento Fase"
        " (°)"
    )
    print("-----------------------------------------------------------------")

    for error_f in error_list:
        # Propagar el paquete con la frecuencia angular modificada omega = omega_0 * (1 + error_f)[cite: 14, 17]
        hist_T, hist_phi = track_bunch(
            cell_lengths, T0_bunch, phi0_bunch, error_f=error_f
        )

        T_final = hist_T[-1]
        phi_final = hist_phi[-1]

        # Evaluación del criterio de captura (|Delta phi| < 60°)[cite: 15]
        delta_phi_final_deg = np.degrees(phi_final - phi_s_rad)
        captured = np.abs(delta_phi_final_deg) < 60.0  #[cite: 15]
        capture_pct = (np.sum(captured) / num_particles) * 100.0  #[cite: 15]

        # Cálculo de la energía media final y del desplazamiento medio de fase de las partículas capturadas
        if np.sum(captured) > 0:
            mean_T_final = np.mean(T_final[captured])
            mean_phase_shift = np.mean(delta_phi_final_deg[captured])
        else:
            mean_T_final = 0.0
            mean_phase_shift = 0.0

        results.append({
            "error_f": error_f,
            "error_pct": error_f * 100.0,
            "capture_pct": capture_pct,
            "mean_T_final": mean_T_final,
            "phase_shift": mean_phase_shift,
            "hist_phi": hist_phi,
        })

        print(
            f"   {error_f * 100.0:4.1f} %     |    {capture_pct:5.1f} %    |"
            f"   {mean_T_final:6.2f} MeV  |       {mean_phase_shift:+5.1f}°"
        )

    print("=================================================================")
    return results, cell_lengths


def plot_rf_error_results(results):
    """Grafica el porcentaje de captura y el desplazamiento de fase frente al error de frecuencia."""
    errors_pct = [r["error_pct"] for r in results]
    capture_pcts = [r["capture_pct"] for r in results]
    phase_shifts = [r["phase_shift"] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

    # Panel 1: Porcentaje de captura vs Error de frecuencia
    ax1.plot(
        errors_pct,
        capture_pcts,
        "o-",
        color="#d62728",
        linewidth=2,
        markersize=6,
    )
    ax1.axhline(
        90,
        color="gray",
        linestyle="--",
        linewidth=0.8,
        label="Umbral crítico (90%)",
    )
    ax1.set_title(
        "Captura del Haz vs Error de Frecuencia RF",
        fontsize=11,
        fontweight="bold",
    )
    ax1.set_xlabel("Error relativo de frecuencia $\epsilon_f$ (%)", fontsize=10)
    ax1.set_ylabel("Partículas capturadas (%)", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend()

    # Panel 2: Desplazamiento de la fase media de equilibrio[cite: 19]
    ax2.plot(
        errors_pct,
        phase_shifts,
        "s-",
        color="#1f77b4",
        linewidth=2,
        markersize=6,
    )
    ax2.set_title(
        "Desplazamiento de Fase Media de Equilibrio",
        fontsize=11,
        fontweight="bold",
    )
    ax2.set_xlabel("Error relativo de frecuencia $\epsilon_f$ (%)", fontsize=10)
    ax2.set_ylabel(
        r"Desviación de fase media $\langle\Delta\phi\rangle$ (grados)",
        fontsize=10,
    )
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig("fig_error_frecuencia.png", dpi=300)
    print("\nGráfica guardada como 'fig_error_frecuencia.png'")
    plt.show()


if __name__ == "__main__":
    results, _ = simulate_frequency_errors()
    plot_rf_error_results(results)