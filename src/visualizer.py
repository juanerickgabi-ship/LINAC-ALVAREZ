import matplotlib.pyplot as plt
import numpy as np
import os


from linac_design import design_linac
from tracking import generate_particle_bunch, track_bunch


def plot_phase_space(
    hist_T: np.ndarray,
    hist_phi: np.ndarray,
    T_sync: np.ndarray,
    phi_s_deg: float = -30.0,
    save_fig: bool = True,
    filename: str = "fig_espacio_fases.png",
):
    """Grafica la distribución del paquete de partículas en el espacio de fases

    longitudinal (Delta T vs Delta phi) comparando la entrada (celda 0) y la
    salida.
    """
    phi_s_rad = np.radians(phi_s_deg)

    # 1. Desviaciones de fase (grados) y energía (keV) en la entrada y salida[cite: 15, 19]
    delta_phi_init = np.degrees(hist_phi[0] - phi_s_rad)
    delta_T_init = (hist_T[0] - T_sync[0]) * 1000.0  # Convertir a keV

    delta_phi_final = np.degrees(hist_phi[-1] - phi_s_rad)
    delta_T_final = (hist_T[-1] - T_sync[-1]) * 1000.0  # Convertir a keV[cite: 19]

    # 2. Crear panel con subplots comparativos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    # Visualización en la entrada (Inyección)
    ax1.scatter(
        delta_phi_init,
        delta_T_init,
        color="#1f77b4",
        alpha=0.35,
        s=8,
        label="Inyección",
    )
    ax1.axhline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.7)
    ax1.axvline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.7)
    ax1.set_title(
        r"Entrada ($T_0 = 3.0$ MeV)", fontsize=12, fontweight="bold"
    )
    ax1.set_xlabel(r"Desviación de fase $\Delta\phi$ (grados)", fontsize=11)
    ax1.set_ylabel(
        r"Desviación de energía $\Delta T$ (keV)", fontsize=11
    ) 
    ax1.set_xlim(-60, 60)
    ax1.set_ylim(-1000, 1000)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper right")

    # Visualización en la salida (Compresión adiabática de fase)
    ax2.scatter(
        delta_phi_final,
        delta_T_final,
        color="#d62728",
        alpha=0.35,
        s=8,
        label="Salida final",
    )
    ax2.axhline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.7)
    ax2.axvline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.7)
    ax2.axvline(
        -60,
        color="darkgray",
        linestyle=":",
        linewidth=1.2,
        label=r"Captura ($\pm 60^\circ$)",
    )  #[cite: 15]
    ax2.axvline(60, color="darkgray", linestyle=":", linewidth=1.2)
    ax2.set_title(
        r"Salida ($T_{final} \approx 50.0$ MeV)", fontsize=12, fontweight="bold"
    )  #[cite: 10]
    ax2.set_xlabel(r"Desviación de fase $\Delta\phi$ (grados)", fontsize=11)
    ax2.set_xlim(-60, 60)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right")

    plt.suptitle(
        f"Espacio de Fases Longitudinal (LINAC Álvarez, $\phi_s ="
        f" {phi_s_deg}^\circ$)",
        fontsize=13,
        fontweight="bold",
    )
    plt.tight_layout()

    if save_fig:
        os.makedirs("figuras", exist_ok=True)
        filepath = os.path.join("figuras", filename)
        plt.savefig(filepath, dpi=300)
        print(f"Gráfica guardada correctamente como '{filepath}'")

    plt.show()


def plot_cell_lengths(
    cell_lengths: np.ndarray,
    save_fig: bool = True,
    filename: str = "fig_celdas.png",
):
    """Grafica el crecimiento de la longitud de las celdas L_n = beta * lambda."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    cells = np.arange(1, len(cell_lengths) + 1)
    lengths_cm = cell_lengths * 100.0  # Convertir a cm[cite: 18]

    ax.plot(
        cells,
        lengths_cm,
        "o-",
        color="#2ca02c",
        linewidth=2,
        markersize=4,
        label=r"$L_n = \beta_{n}\lambda$",
    )  #[cite: 6]
    ax.set_title(
        "Geometría de Celdas de Deriva (Drift Tubes)",
        fontsize=12,
        fontweight="bold",
    )
    ax.set_xlabel("Número de celda $n$", fontsize=11)
    ax.set_ylabel("Longitud de celda $L_n$ (cm)", fontsize=11)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")

    plt.tight_layout()

    if save_fig:
        os.makedirs("figuras", exist_ok=True)
        filepath = os.path.join("figuras", filename)
        plt.savefig(filepath, dpi=300)
        print(f"Gráfica guardada correctamente como '{filepath}'")

    plt.show()


def plot_electric_field_profile(
    z_positions: np.ndarray,
    E0_vals: np.ndarray,
    Eacc_vals: np.ndarray,
    save_fig: bool = True,
    filename: str = "fig06_perfil_campos.png",):
        
    """Grafica el decaimiento del gradiente pico y síncrono a lo largo de la distancia real z [m]."""
    
    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Posiciones en el centro/final de celda
    z_m = z_positions[1:]

    ax.plot(
        z_m,
        E0_vals,
        "r--",
        linewidth=2.0,
        label=r"$E_0$ (Gradiente pico nominal = $qV_{\mathrm{gap}}/L_n$)",
    )
    ax.plot(
        z_m,
        Eacc_vals,
        "b-",
        linewidth=2.2,
        label=(
            r"$E_{\mathrm{acc}}$ (Efectivo síncrono ="
            r" $qV_{\mathrm{gap}}\cos\phi_s/L_n$)"
        ),
    )

    ax.set_xlabel("Posición longitudinal $z$ (m)", fontsize=11)
    ax.set_ylabel("Gradiente de Campo Eléctrico (MV/m)", fontsize=11)
    ax.set_title(
        "Atenuación Geométrica del Campo Eléctrico vs Distancia Real",
        fontsize=12,
        fontweight="bold",
    )
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", fontsize=9.5)

    plt.tight_layout()

    if save_fig:
        os.makedirs("figuras", exist_ok=True)
        filepath = os.path.join("figuras", filename)
        plt.savefig(filepath, dpi=300)
        print(f"Gráfica guardada en '{filepath}'")

    plt.show()
    
def plot_kinematic_profile(
    z_positions: np.ndarray,
    beta_vals: np.ndarray,
    T_sync: np.ndarray,
    save_fig: bool = True,
    filename: str = "fig08_perfil_cinematico.png",):
    
    """Grafica el perfil combinado de velocidad relativista beta = v/c (eje izq) y energía cinética T (eje der) vs distancia z [m]."""
    fig, ax1 = plt.subplots(figsize=(8.5, 4.5))

    # Posiciones longitudinales en metros (omitimos z=0 para alinear con las 55 celdas)
    z_m = z_positions[1:]

    # Eje Y Izquierdo: Velocidad Relativa beta = v/c
    color_beta = "#2ca02c"
    ax1.plot(
        z_m,
        beta_vals,
        "-",
        color=color_beta,
        linewidth=2.2,
        label=r"Velocidad relativa $\beta = v/c$",
    )
    ax1.set_xlabel("Posición longitudinal $z$ (m)", fontsize=11)
    ax1.set_ylabel(
        r"Velocidad Relativa $\beta$", color=color_beta, fontsize=11
    )
    ax1.tick_params(axis="y", labelcolor=color_beta)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Eje Y Derecho: Energía Cinética T [MeV]
    ax2 = ax1.twinx()
    color_T = "#9467bd"
    ax2.plot(
        z_m,
        T_sync[1:],
        "--",
        color=color_T,
        linewidth=2.0,
        label=r"Energía cinética $T$ (MeV)",
    )
    ax2.set_ylabel("Energía Cinética $T$ (MeV)", color=color_T, fontsize=11)
    ax2.tick_params(axis="y", labelcolor=color_T)

    plt.title(
        r"Perfil de Aceleración Cinemática ($\beta$ y $T$) vs Distancia Real",
        fontsize=12,
        fontweight="bold",
    )
    plt.tight_layout()

    if save_fig:
        os.makedirs("figuras", exist_ok=True)
        filepath = os.path.join("figuras", filename)
        plt.savefig(filepath, dpi=300)
        print(f"Gráfica guardada correctamente en '{filepath}'")

    plt.show()


def plot_adiabatic_damping_evolution(
    hist_T: np.ndarray,
    hist_phi: np.ndarray,
    T_sync: np.ndarray,
    phi_s_deg: float = -30.0,
    save_fig: bool = True,
    filename: str = "fig07_amortiguamiento_cuantitativo.png",):
    
    
    """Grafica la evolución cuantitativa celda por celda de sigma_phi y sigma_T para validar Liouville."""
    num_cells = hist_T.shape[0] - 1
    phi_s_rad = np.radians(phi_s_deg)

    sigma_phi = []
    sigma_T_keV = []

    for n in range(num_cells + 1):
        delta_phi_deg = np.degrees(hist_phi[n] - phi_s_rad)
        captured = np.abs(delta_phi_deg) < 60.0

        sigma_phi.append(np.std(delta_phi_deg[captured]))
        sigma_T_keV.append(np.std((hist_T[n, captured] - T_sync[n]) * 1000.0))

    fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
    cells = np.arange(num_cells + 1)

    # Eje Y Izquierdo: Dispersión de Fase
    color_phi = "#1f77b4"
    ax1.plot(
        cells,
        sigma_phi,
        "o-",
        color=color_phi,
        linewidth=1.8,
        markersize=4,
        label=r"Dispersión de Fase $\sigma_\phi$ (°)",)
    
    ax1.set_xlabel("Número de celda $n$", fontsize=11)
    ax1.set_ylabel(
        r"Dispersión de Fase $\sigma_\phi$ (grados)",
        color=color_phi,
        fontsize=11,)
    
    ax1.tick_params(axis="y", labelcolor=color_phi)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Eje Y Derecho: Dispersión de Energía
    ax2 = ax1.twinx()
    color_T = "#d62728"
    ax2.plot(
        cells,
        sigma_T_keV,
        "s-",
        color=color_T,
        linewidth=1.8,
        markersize=4,
        label=r"Dispersión de Energía $\sigma_T$ (keV)",)
    
    ax2.set_ylabel(
        r"Dispersión de Energía $\sigma_T$ (keV)", color=color_T, fontsize=11)
    
    ax2.tick_params(axis="y", labelcolor=color_T)

    plt.title(
        r"Demostración Cuantitativa del Amortiguamiento Adiabático"
        r" ($\sigma_\phi \propto (\beta\gamma)^{-3/4}$)",
        fontsize=12,
        fontweight="bold",)
    
    plt.tight_layout()

    if save_fig:
        os.makedirs("figuras", exist_ok=True)
        filepath = os.path.join("figuras", filename)
        plt.savefig(filepath, dpi=300)
        print(f"Gráfica guardada en '{filepath}'")

    plt.show()
    


  
  
if __name__ == "__main__":
    # 1. Obtener datos de la simulación de referencia
    cell_lengths, T_sync, _ = design_linac(phi_s_deg=-30.0)
    T0_bunch, phi0_bunch = generate_particle_bunch(
        phi_s_deg=-30.0, seed=20261919
    )
    hist_T, hist_phi = track_bunch(cell_lengths, T0_bunch, phi0_bunch)

    # 2. Renderizar y guardar figuras
    plot_phase_space(hist_T, hist_phi, T_sync, phi_s_deg=-30.0)
    plot_cell_lengths(cell_lengths)