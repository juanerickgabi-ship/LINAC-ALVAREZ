import matplotlib.pyplot as plt
import numpy as np
import os
import csv

from physics import C_LIGHT, M_ELECTRON_MEV
from tracking import track_bunch


def simulate_electrons(
    T_0: float = 10.0,
    num_cells: int = 60,
    f_rf: float = 352.2e6,
    qV_gap: float = 1.0,
    initial_phases_deg: list[float] = [-40.0, -20.0, 0.0, 20.0, 40.0],
):
    """Simula el comportamiento longitudinal de electrones relativistas en celdas constantes (L = lambda)."""
    wavelength = C_LIGHT / f_rf  # L_n = lambda constante
    cell_lengths = np.full(num_cells, wavelength)

    phi_0_arr = np.radians(np.array(initial_phases_deg))
    T_0_arr = np.full_like(phi_0_arr, T_0)

    # Seguimiento usando la masa en reposo del electrón (0.511 MeV)
    hist_T, hist_phi = track_bunch(
        cell_lengths=cell_lengths,
        particles_T=T_0_arr,
        particles_phi=phi_0_arr,
        qV_gap=qV_gap,
        f_rf=f_rf,
        m_MeV=M_ELECTRON_MEV,
    )

    print("=================================================================")
    print("      SIMULACIÓN DE ELECTRONES RELATIVISTAS (10 MeV, 60 celdas)  ")
    print("=================================================================")
    print("Fase Inyección (°) | Energía Final (MeV) | Deriva Total de Fase (°)")
    print("-----------------------------------------------------------------")

    for i, phi_init in enumerate(initial_phases_deg):
        T_fin = hist_T[-1, i]
        phase_drift = np.degrees(hist_phi[-1, i] - hist_phi[0, i])
        print(
            f"     {phi_init:^+5.1f}°        |"
            f"     {T_fin:6.2f} MeV     |"
            f"       {phase_drift:+5.2f}°"
        )

    print("=================================================================")
    return hist_T, hist_phi, initial_phases_deg


def plot_electron_results(hist_T, hist_phi, initial_phases_deg):
    """Grafica la ganancia de energía y la deriva de fase para electrones relativistas."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5))
    cells = np.arange(hist_T.shape[0])

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    linestyles = [
        "--",
        "--",
        "-",
        "-",
        "-",
    ]  # Punteado para fases negativas para hacer visible la superposición

    for i, phi_init in enumerate(initial_phases_deg):
        label_text = f"$\\phi_0 = {phi_init:+.0f}^\\circ$"

        # Panel 1: Evolución de Energía
        ax1.plot(
            cells,
            hist_T[:, i],
            linewidth=2.0 if phi_init == 0 else 1.8,
            linestyle=linestyles[i],
            color=colors[i],
            label=label_text,
        )

        # Anotar valor final de energía al final de la celda 60
        final_T = hist_T[-1, i]
        if phi_init >= 0:  # Evita duplicar etiquetas pegadas
            ax1.annotate(
                f"{final_T:.1f} MeV",
                (cells[-1], final_T),
                textcoords="offset points",
                xytext=(5, -3 if phi_init != 0 else -10),
                ha="left",
                fontsize=8.5,
                weight="bold",
                color=colors[i],
            )

        # Panel 2: Evolución de Fase
        ax2.plot(
            cells,
            np.degrees(hist_phi[:, i]),
            linewidth=1.8,
            linestyle=linestyles[i],
            color=colors[i],
            label=label_text,
        )

    # Configuración Panel 1
    ax1.set_title(
        "Ganancia de Energía de Electrones", fontsize=11.5, fontweight="bold"
    )
    ax1.set_xlabel("Número de celda $n$", fontsize=10.5)
    ax1.set_ylabel("Energía cinética $T$ (MeV)", fontsize=10.5)
    ax1.set_xlim(-1, 68)  # Margen para las anotaciones finales
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", fontsize=9)

    # Configuración Panel 2 (Ubicación de leyenda fuera del camino de los datos)
    ax2.set_title(
        "Deriva de Fase Longitudinal (Congelamiento de Fase)",
        fontsize=11.5,
        fontweight="bold",
    )
    ax2.set_xlabel("Número de celda $n$", fontsize=10.5)
    ax2.set_ylabel(r"Fase de arrival $\phi$ (grados)", fontsize=10.5)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right", fontsize=9)  # Mover a la derecha

    plt.tight_layout()

    # Guardar en la carpeta figuras
    os.makedirs("figuras", exist_ok=True)
    filepath = "figuras/fig05_estabilidad_electrones.png"
    plt.savefig(filepath, dpi=300)
    print(f"\nGráfica guardada exitosamente en '{filepath}'")
    plt.show()


def export_electrons_to_csv(
    hist_T: np.ndarray,
    hist_phi: np.ndarray,
    initial_phases_deg: list[float],
    filename: str = "resultados/electrones_simulacion.csv",
):
  """Exporta los resultados del estudio comparativo con electrones relativistas."""
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  with open(filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Fase_Inyeccion_deg",
        "Energia_Inicial_MeV",
        "Energia_Final_MeV",
        "Ganancia_Total_MeV",
        "Fase_Final_deg",
        "Deriva_Fase_Total_deg",
    ])

    for i, phi_init in enumerate(initial_phases_deg):
      T_init = hist_T[0, i]
      T_final = hist_T[-1, i]
      phi_final_deg = np.degrees(hist_phi[-1, i])
      drift_deg = np.degrees(hist_phi[-1, i] - hist_phi[0, i])

      writer.writerow([
          f"{phi_init:+.1f}",
          f"{T_init:.2f}",
          f"{T_final:.4f}",
          f"{(T_final - T_init):.4f}",
          f"{phi_final_deg:.4f}",
          f"{drift_deg:.4f}",
      ])

  print(f" Datos de electrones exportados a '{filename}'")

if __name__ == "__main__":
    hist_T, hist_phi, phases = simulate_electrons()
    plot_electron_results(hist_T, hist_phi, phases)


