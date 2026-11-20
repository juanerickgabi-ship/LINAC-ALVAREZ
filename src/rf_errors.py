import os
import matplotlib.pyplot as plt
import numpy as np
import csv

from linac_design import design_linac
from tracking import generate_particle_bunch, track_bunch


def simulate_frequency_errors(
    error_list: list[float] = [0.0, 0.002, 0.005, 0.01, 0.02, 0.03, 0.04],
    phi_s_deg: float = -30.0,
    num_particles: int = 3000,
    seed: int = 20261919,
):
    """Simula el comportamiento del paquete ante errores en la frecuencia RF."""
    cell_lengths, T_sync, _ = design_linac(phi_s_deg=phi_s_deg)
    phi_s_rad = np.radians(phi_s_deg)

    T0_bunch, phi0_bunch = generate_particle_bunch(
        num_particles=num_particles, phi_s_deg=phi_s_deg, seed=seed
    )

    results = []

    print("=================================================================")
    print("   EFECTO DE ERRORES EN LA FRECUENCIA DE RADIOFRECUENCIA (RF)    ")
    print("=================================================================")
    print("Error RF (%) | Capturadas (%) | E_final (MeV) | Desplazamiento Fase (°)")
    print("-----------------------------------------------------------------")

    for error_f in error_list:
        hist_T, hist_phi = track_bunch(
            cell_lengths, T0_bunch, phi0_bunch, error_f=error_f
        )

        T_final = hist_T[-1]
        phi_final = hist_phi[-1]

        delta_phi_final_deg = np.degrees(phi_final - phi_s_rad)
        captured = np.abs(delta_phi_final_deg) < 60.0
        capture_pct = (np.sum(captured) / num_particles) * 100.0

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
        })

        print(
            f"   {error_f * 100.0:4.1f} %     |    {capture_pct:5.1f} %    |"
            f"   {mean_T_final:6.2f} MeV  |       {mean_phase_shift:+5.1f}°"
        )

    print("=================================================================")
    return results, cell_lengths


def plot_rf_error_results(results):
    """Grafica las métricas de sensibilidad de frecuencia con etiquetas numéricas claras."""
    errors_pct = [r["error_pct"] for r in results]
    capture_pcts = [r["capture_pct"] for r in results]
    phase_shifts = [r["phase_shift"] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5))

    # -------------------------------------------------------------------------
    # PANEL 1: Captura del Haz
    # -------------------------------------------------------------------------
    ax1.plot(
        errors_pct,
        capture_pcts,
        "o-",
        color="#d62728",
        linewidth=2,
        markersize=6,
        label="Partículas capturadas",
    )
    ax1.axhline(
        90,
        color="gray",
        linestyle="--",
        linewidth=1.0,
        label="Criterio de Aceptación (90%)",
    )

    # Anotar porcentajes exactos sobre cada punto
    for x, y in zip(errors_pct, capture_pcts):
        offset_y = 2.5 if y < 90 else -4.0
        ax1.annotate(
            f"{y:.1f}%",
            (x, y),
            textcoords="offset points",
            xytext=(0, offset_y),
            ha="center",
            fontsize=8.5,
            color="#8c1111",
            weight="bold",
        )

    ax1.set_title(
        "Captura del Haz vs Error de Frecuencia RF",
        fontsize=12,
        fontweight="bold",
    )
    ax1.set_xlabel(r"Error relativo de frecuencia $\epsilon_f$ (%)", fontsize=10.5)
    ax1.set_ylabel("Partículas capturadas (%)", fontsize=10.5)
    ax1.set_ylim(45, 105)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="lower left")

    # -------------------------------------------------------------------------
    # PANEL 2: Desplazamiento de Fase Media
    # -------------------------------------------------------------------------
    ax2.plot(
        errors_pct,
        phase_shifts,
        "s-",
        color="#1f77b4",
        linewidth=2,
        markersize=6,
        label=r"Desplazamiento $\langle\Delta\phi_{eq}\rangle$",
    )

    # Anotar desfases exactos en grados sobre cada punto
    for x, y in zip(errors_pct, phase_shifts):
        ax2.annotate(
            f"{y:+.1f}°",
            (x, y),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=8.5,
            color="#0e4369",
            weight="bold",
        )

    ax2.set_title(
        "Desplazamiento de Fase Media de Equilibrio",
        fontsize=12,
        fontweight="bold",
    )
    ax2.set_xlabel(r"Error relativo de frecuencia $\epsilon_f$ (%)", fontsize=10.5)
    ax2.set_ylabel(
        r"Desviación de fase media $\langle\Delta\phi_{eq}\rangle$ (grados)",
        fontsize=10.5,
    )
    ax2.set_ylim(-0.5, 13.0)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper left")

    plt.tight_layout()

    # Guardar en la carpeta figuras
    os.makedirs("figuras", exist_ok=True)
    filepath = "figuras/fig04_error_frecuencia.png"
    plt.savefig(filepath, dpi=300)
    print(f"\nGráfica guardada exitosamente en '{filepath}'")
    plt.show()


if __name__ == "__main__":
    results, _ = simulate_frequency_errors()
    plot_rf_error_results(results)
    
    
def export_rf_errors_to_csv(
    results: list[dict],
    filename: str = "resultados/rf_errores_sensibilidad.csv",):
    
  """Exporta la tabla de sensibilidad del haz ante errores de frecuencia RF."""
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  with open(filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Error_RF_Relativo",
        "Error_RF_Pct",
        "Captura_Pct",
        "Energia_Media_Final_MeV",
        "Desplazamiento_Fase_Media_deg",
    ])

    for r in results:
      writer.writerow([
          f"{r['error_f']:.4f}",
          f"{r['error_pct']:.2f}",
          f"{r['capture_pct']:.2f}",
          f"{r['mean_T_final']:.4f}",
          f"{r['phase_shift']:.4f}",
      ])

  print(f" Datos de sensibilidad de RF exportados a '{filename}'")