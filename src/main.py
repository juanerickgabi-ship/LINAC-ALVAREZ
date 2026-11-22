import sys
import pandas as pd


from electrons import (
    export_electrons_to_csv,
    plot_electron_results,
    simulate_electrons,
)
from linac_design import design_linac, export_design_to_csv

from rf_errors import (
    export_rf_errors_to_csv,
    plot_rf_error_results,
    simulate_frequency_errors,)
from synchrotron import (
    export_synchrotron_to_csv,
    plot_synchrotron_results,
    simulate_synchrotron_oscillation,)

from tracking import generate_particle_bunch, track_bunch

from visualizer import (
    plot_cell_lengths, plot_phase_space, 
    plot_electric_field_profile, plot_adiabatic_damping_evolution,
    plot_kinematic_profile,)


def run_full_simulation():
    print("=================================================================")
    print("   SIMULADOR DE ACELERADOR LINEAL (LINAC TIPO ÁLVAREZ)           ")
    print("   Proyecto de Física Computacional 2                            ")
    print("=================================================================\n")

    # -------------------------------------------------------------------------
    # ETAPA 1: DISEÑO DE CELDAS Y GEOMETRÍA (PARTÍCULA SÍNCRONA)
    # -------------------------------------------------------------------------
    print("[1/5] Ejecutando diseño de celdas para el protón síncrono...")
    cell_lengths, T_sync, z_positions = design_linac(
        T_init=3.0, T_final=50.0, qV_gap=1.0, phi_s_deg=-30.0, f_rf=352.2e6
    )

    num_cells = len(cell_lengths)
    total_len = z_positions[-1]
    print(
        f"    -> Celdas generadas: {num_cells} | Longitud total:"
        f" {total_len:.2f} m"
    )
    print(
        f"    -> Rango de celdas: {cell_lengths[0] * 100:.2f} cm a"
        f" {cell_lengths[-1] * 100:.2f} cm"
    )  #[cite: 18]
    
    plot_cell_lengths(cell_lengths, filename="fig01_diseno.png")
    export_design_to_csv(cell_lengths, T_sync, z_positions)
    
    
    # -------------------------------------------------------------------------
    # ETAPA 2: SEGUIMIENTO DEL PAQUETE DE PROTONES (3000 PARTÍCULAS)
    # -------------------------------------------------------------------------
    print("\n[2/5] Simulando seguimiento del paquete de 3000 protones...")
    T0_bunch, phi0_bunch = generate_particle_bunch(
        num_particles=3000, phi_s_deg=-30.0, seed=20261919
    ) 
    hist_T, hist_phi = track_bunch(
        cell_lengths, T0_bunch, phi0_bunch, qV_gap=1.0, f_rf=352.2e6
    )  #[cite: 14]

    phi_final = hist_phi[-1]
    phi_s_rad = -30.0 * (3.141592653589793 / 180.0)
    captured = (
        abs((phi_final - phi_s_rad) * (180.0 / 3.141592653589793)) < 60.0
    )  #[cite: 15]
    print(
        f"    -> Captura longitudinal (|Δϕ| < 60°):"
        f" {(sum(captured) / 3000) * 100:.1f}%"
    )  #[cite: 15, 18]
    plot_phase_space(
        hist_T,
        hist_phi,
        T_sync,
        phi_s_deg=-30.0,
        filename="fig02_espacio_fases.png",
    )  #[cite: 19]

  # -------------------------------------------------------------------------
    # ETAPA 3: OSCILACIONES DE SINCROTRÓN Y AMORTIGUAMIENTO ADIABÁTICO
    # -------------------------------------------------------------------------
    print("\n[3/5] Analizando oscilaciones de sincrotrón para perturbación de +3°...")
    delta_phi, mu_theory, sim_cells_mid, sim_mu_points = simulate_synchrotron_oscillation(
        perturbation_deg=3.0, phi_s_deg=-30.0
    )
    print(f"    -> Avance de fase teórico inicial: {mu_theory[0]:.2f}°/celda")
    print(f"    -> Amplitud de oscilación: {delta_phi[0]:.2f}° (Entrada) -> {abs(delta_phi[-1]):.2f}° (Salida)")
    
    plot_synchrotron_results(delta_phi, mu_theory, sim_cells_mid, sim_mu_points)
    export_synchrotron_to_csv(delta_phi, mu_theory, sim_cells_mid, sim_mu_points)

    # -------------------------------------------------------------------------
    # ETAPA 4: ANÁLISIS DE SENSIBILIDAD A ERRORES EN LA FRECUENCIA RF
    # -------------------------------------------------------------------------
    print("\n[4/5] Evaluando sensibilidad a errores de frecuencia RF (0% a 4%)...")
    rf_results, _ = simulate_frequency_errors(
        error_list=[0.0, 0.002, 0.005, 0.01, 0.02, 0.03, 0.04])
    
    plot_rf_error_results(rf_results)
    export_rf_errors_to_csv(rf_results)

    # -------------------------------------------------------------------------
    # ETAPA 5: COMPARACIÓN CON ELECTRONES RELATIVISTAS (10 MeV)
    # -------------------------------------------------------------------------
    print(
        "\n[5/5] Simulando dinámica de electrones relativistas (10 MeV, 60"
        " celdas)..."
    )
    e_hist_T, e_hist_phi, e_phases = simulate_electrons(T_0=10.0, num_cells=60)
    
    plot_electron_results(e_hist_T, e_hist_phi, e_phases)
    export_electrons_to_csv(e_hist_T, e_hist_phi, e_phases)
    
    
    
    #CAMPO ELECTRICO Y VELOCIDAD RELATIVISTA
        
    # Cargar datos del diseño y campos
    df_diseno = pd.read_csv("resultados/diseno_celdas.csv")
    
    # 1. Graficar perfil de campos eléctricos en metros reales
    plot_electric_field_profile(
        z_positions=z_positions,
        E0_vals=df_diseno["E0_MV_m"].values,
        Eacc_vals=df_diseno["E_acc_MV_m"].values,)
    
    # Ejecutar la gráfica cinemática
    plot_kinematic_profile(
        z_positions=z_positions,
        beta_vals=df_diseno["Beta"].values,
        T_sync=T_sync,
        save_fig=True,
        filename="fig08_perfil_cinematico.png",
)
    
    # 2. Graficar la evolución cuantitativa del amortiguamiento adiabático
    plot_adiabatic_damping_evolution(hist_T, hist_phi, T_sync, phi_s_deg=-30.0)
    
    

    print("\n=================================================================")
    print("   SIMULACIÓN COMPLETA FINALIZADA CON ÉXITO")
    print("   Todas las gráficas han sido generadas y guardadas.")
    print("   Los resultados numéricos han sido exportados a archivos CSV.")
    print("=================================================================")


if __name__ == "__main__":
    run_full_simulation()