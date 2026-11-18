import sys
from electrons import plot_electron_results, simulate_electrons
from linac_design import design_linac
from rf_errors import plot_rf_error_results, simulate_frequency_errors
from synchrotron import (
    plot_synchrotron_results,
    simulate_synchrotron_oscillation,
)
from tracking import generate_particle_bunch, track_bunch
from visualizer import plot_cell_lengths, plot_phase_space


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
    )  #[cite: 10]

    num_cells = len(cell_lengths)
    total_len = z_positions[-1]
    print(
        f"    -> Celdas generadas: {num_cells} | Longitud total:"
        f" {total_len:.2f} m"
    )  #[cite: 1, 18]
    print(
        f"    -> Rango de celdas: {cell_lengths[0] * 100:.2f} cm a"
        f" {cell_lengths[-1] * 100:.2f} cm"
    )  #[cite: 18]
    plot_cell_lengths(cell_lengths, filename="fig01_diseno.png")

    # -------------------------------------------------------------------------
    # ETAPA 2: SEGUIMIENTO DEL PAQUETE DE PROTONES (3000 PARTÍCULAS)
    # -------------------------------------------------------------------------
    print("\n[2/5] Simulando seguimiento del paquete de 3000 protones...")
    T0_bunch, phi0_bunch = generate_particle_bunch(
        num_particles=3000, phi_s_deg=-30.0, seed=20261919
    )  #[cite: 10, 14, 15]
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
    print(
        "\n[3/5] Analizando oscilaciones de sincrotrón para perturbación de"
        " +3°..."
    )
    delta_phi, mu_theory, mu_sim = simulate_synchrotron_oscillation(
        perturbation_deg=3.0, phi_s_deg=-30.0
    )  #[cite: 16]
    print(f"    -> Avance de fase teórico inicial: {mu_theory[0]:.2f}°/celda")
    print(f"    -> Avance de fase medido (1ª semioscilación): {mu_sim:.2f}°/celda")
    print(
        f"    -> Amplitud de oscilación: {delta_phi[0]:.2f}° (Entrada) ->"
        f" {abs(delta_phi[-1]):.2f}° (Salida)"
    )  #[cite: 19]
    plot_synchrotron_results(delta_phi, mu_theory, mu_sim)

    # -------------------------------------------------------------------------
    # ETAPA 4: ANÁLISIS DE SENSIBILIDAD A ERRORES EN LA FRECUENCIA RF
    # -------------------------------------------------------------------------
    print("\n[4/5] Evaluando sensibilidad a errores de frecuencia RF (0% a 4%)...")
    rf_results, _ = simulate_frequency_errors(
        error_list=[0.0, 0.002, 0.005, 0.01, 0.02, 0.04]
    )  #[cite: 17]
    plot_rf_error_results(rf_results)

    # -------------------------------------------------------------------------
    # ETAPA 5: COMPARACIÓN CON ELECTRONES RELATIVISTAS (10 MeV)
    # -------------------------------------------------------------------------
    print(
        "\n[5/5] Simulando dinámica de electrones relativistas (10 MeV, 60"
        " celdas)..."
    )
    e_hist_T, e_hist_phi, e_phases = simulate_electrons(
        T_0=10.0, num_cells=60
    )  #[cite: 11, 18]
    plot_electron_results(e_hist_T, e_hist_phi, e_phases)

    print("\n=================================================================")
    print("   SIMULACIÓN COMPLETA FINALIZADA CON ÉXITO")
    print("   Todas las gráficas han sido generadas y guardadas.")
    print("=================================================================")


if __name__ == "__main__":
    run_full_simulation()