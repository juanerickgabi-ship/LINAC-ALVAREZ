import matplotlib.pyplot as plt
import numpy as np

from physics import C_LIGHT, M_ELECTRON_MEV, get_beta
from tracking import track_bunch


def simulate_electrons(
    T_0: float = 10.0,
    num_cells: int = 60,
    f_rf: float = 352.2e6,
    qV_gap: float = 1.0,
    initial_phases_deg: list[float] = [-40.0, -20.0, 0.0, 20.0, 40.0],
):
    """Simula el comportamiento longitudinal de electrones relativistas en 60 celdas constantes[cite: 11, 18]."""
    wavelength = C_LIGHT / f_rf  # Longitud de celda L = lambda[cite: 18]
    cell_lengths = np.full(num_cells, wavelength)  # Structure de L constante[cite: 18]

    # Convertir fases iniciales a radianes
    phi_0_arr = np.radians(np.array(initial_phases_deg))
    T_0_arr = np.full_like(phi_0_arr, T_0)

    # Simular seguimiento con masa de electrón[cite: 14]
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
    """Grafica la evolución de energía y fase para electrones."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    cells = np.arange(hist_T.shape[0])

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for i, phi_init in enumerate(initial_phases_deg):
        # Evolución de Energía
        ax1.plot(
            cells,
            hist_T[:, i],
            linewidth=1.8,
            color=colors[i],
            label=f"$\phi_0 = {phi_init}^\circ$",
        )
        # Evolución de Fase
        ax2.plot(
            cells,
            np.degrees(hist_phi[:, i]),
            linewidth=1.8,
            color=colors[i],
            label=f"$\phi_0 = {phi_init}^\circ$",
        )

    ax1.set_title(
        "Ganancia de Energía de Electrones", fontsize=11, fontweight="bold"
    )
    ax1.set_xlabel("Número de celda $n$", fontsize=10)
    ax1.set_ylabel("Energía cinética $T$ (MeV)", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")

    ax2.set_title(
        "Deriva de Fase Longitudinal (Sin Oscilaciones)",
        fontsize=11,
        fontweight="bold",
    )
    ax2.set_xlabel("Número de celda $n$", fontsize=10)
    ax2.set_ylabel(r"Fase de arrival $\phi$ (grados)", fontsize=10)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="lower left")

    plt.tight_layout()
    plt.savefig("fig_electrones.png", dpi=300)
    print("\nGráfica guardada como 'fig_electrones.png'")
    plt.show()


if __name__ == "__main__":
    hist_T, hist_phi, phases = simulate_electrons()
    plot_electron_results(hist_T, hist_phi, phases)