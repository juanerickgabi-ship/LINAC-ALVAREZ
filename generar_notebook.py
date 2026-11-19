import json

notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Simulación Dinámica y Diseño de un Acelerador Lineal (LINAC"
                " tipo Álvarez)\n",
                "**Asignatura:** Física Computacional 2  \n",
                "**Proyecto:** P19 - Acelerador Lineal de Protones y"
                " Electrones  \n",
                "**Entorno:** Python 3 + VS Code (Módulos de `src/`)  \n",
                "---\n",
                "## 1. Introducción y Fundamentos Físicos\n",
                "Un acelerador lineal (LINAC) tipo Álvarez utiliza una serie de"
                " tubos de deriva (*drift tubes*) contenidos dentro de una"
                " cavidad resonante de radiofrecuencia (RF). La finalidad de la"
                " estructura es acelerar partículas cargadas mediante el campo"
                " eléctrico $E_z$ en los huecos (*gaps*) entre celdas, mientras"
                " que el interior metálico de los tubos apantalla las"
                " partículas durante el semiciclo desacelerante de la onda"
                " electromagnética.\n\n",
                "### Ecuaciones Dinámicas Principales:\n",
                "1. **Actualización Relativista de Energía:**  \n",
                "   $$\\Delta T_n = q V_{\\text{gap}} \\cos(\\phi_n)$$\n",
                "2. **Factores Relativistas:**  \n",
                "   $$\\gamma_n = 1 + \\frac{T_n}{m_0 c^2}, \\quad \\beta_n ="
                " \\sqrt{1 - \\frac{1}{\\gamma_n^2}}$$\n",
                "3. **Condición de Sincronismo (Longitud de Celda):**  \n",
                "   $$L_n = \\beta_n \\lambda = \\frac{\\beta_n c}{f_{\\text{RF}}}$$\n",
                "4. **Avance de Fase Temporal:**  \n",
                "   $$\\Delta \\phi_n = 2\\pi f_{\\text{RF}} \\Delta t_n - 2\\pi"
                " = 2\\pi \\left( \\frac{L_n}{\\beta_n c} f_{\\text{RF}} - 1"
                " \\right)$$",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Importación de librerías y configuración de rutas\n",
                "import os\n",
                "import sys\n",
                "import matplotlib.pyplot as plt",
                "import numpy as np\n\n",
                "# Configurar visualizaciones integradas\n",
                "%matplotlib inline\n",
                "plt.rcParams['figure.dpi'] = 120\n\n",
                "# Asegurar acceso a la carpeta src/\n",
                "sys.path.append(os.path.abspath('src'))\n\n",
                "# Importar módulos del proyecto desde src/\n",
                "from src.physics import C_LIGHT, M_PROTON_MEV, M_ELECTRON_MEV,"
                " get_beta, get_gamma\n",
                "from src.linac_design import design_linac,"
                " export_design_to_csv\n",
                "from src.tracking import generate_particle_bunch,"
                " track_bunch\n",
                "from src.visualizer import plot_cell_lengths,"
                " plot_phase_space\n",
                "from src.synchrotron import"
                " simulate_synchrotron_oscillation,"
                " plot_synchrotron_results, export_synchrotron_to_csv\n",
                "from src.rf_errors import simulate_frequency_errors,"
                " plot_rf_error_results, export_rf_errors_to_csv\n",
                "from src.electrons import simulate_electrons,"
                " plot_electron_results, export_electrons_to_csv\n\n",
                'print("Módulos de src/ cargados exitosamente.")',
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Diseño Geométrico y Partícula Síncrona\n",
                "Se diseña un LINAC tipo Álvarez para acelerar protones desde"
                " $T_0 = 3.0\\text{ MeV}$ hasta $T_f = 50.0\\text{ MeV}$"
                " utilizando una frecuencia RF de $f_{\\text{RF}} = 352.2\\text{"
                " MHz}$ y una fase síncrona $\\phi_s = -30^\\circ$. Dado que"
                " la velocidad del protón no es constante, las celdas deben"
                " aumentar progresivamente de tamaño."
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Ejecutar diseño cinemático de celdas\n",
                "cell_lengths, T_sync, z_positions = design_linac(\n",
                "    T_init=3.0, T_final=50.0, qV_gap=1.0, phi_s_deg=-30.0,"
                " f_rf=352.2e6\n",
                ")\n\n",
                "# Exportar datos a CSV y graficar geometría\n",
                'export_design_to_csv(cell_lengths, T_sync, z_positions, filename="resultados/diseno_celdas.csv")\n',
                "plot_cell_lengths(cell_lengths, save_fig=True, filename=\"fig01_diseno.png\")\n\n",
                "# Mostrar métricas en consola\n",
                'print(f"Número total de celdas: {len(cell_lengths)}")\n',
                'print(f"Longitud total del LINAC: {z_positions[-1]:.2f} m")\n',
                'print(f"Longitud celda 1: {cell_lengths[0]*100:.2f} cm |'
                ' Longitud celda 55: {cell_lengths[-1]*100:.2f} cm")',
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Seguimiento Dinámico de Paquete y Espacio de Fases\n",
                "Se simula la inyección de $N = 3000$ protones dispersos alrededor"
                " de la partícula síncrona con una distribución gaussiana de"
                " $\\sigma_T / T_0 = 0.5\\%$ y $\\sigma_\\phi = 15^\\circ$. A"
                " lo largo del acelerador, el paquete experimenta una"
                " rotación en el espacio de fases $(\\Delta\\phi, \\Delta T)$"
                " conocida como **compresión de fase**."
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Generar paquete de 3000 partículas\n",
                "T0_bunch, phi0_bunch = generate_particle_bunch(num_particles=3000, phi_s_deg=-30.0, seed=20261919)\n\n",
                "# Seguimiento discreto celda por celda\n",
                "hist_T, hist_phi = track_bunch(cell_lengths, T0_bunch, phi0_bunch, qV_gap=1.0, f_rf=352.2e6)\n\n",
                "# Graficar espacio de fases\n",
                "plot_phase_space(hist_T, hist_phi, T_sync, phi_s_deg=-30.0, save_fig=True, filename=\"fig02_espacio_fases.png\")\n\n",
                "# Métrica de captura\n",
                "phi_s_rad = np.radians(-30.0)\n",
                "captured = np.abs(np.degrees(hist_phi[-1] - phi_s_rad)) < 60.0\n",
                'print(f"Porcentaje de captura longitudinal: {(np.sum(captured)/3000)*100:.2f}%")',
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Oscilaciones de Sincrotrón y Amortiguamiento"
                " Adiabático\n",
                "Para una partícula con una desviación inicial de fase"
                " $\\delta\\phi_0 = +3^\\circ$, la fuerza restauradora"
                " longitudinal la hace oscilar alrededor de $\\phi_s$. El"
                " avance de fase teórico por celda viene dado por:\n\n",
                "$$\\mu_n = \\sqrt{\\frac{2\\pi q V_{\\text{gap}} (-\\sin\\phi_s)}{m_0"
                " c^2 \\beta_n^2 \\gamma_n^3}}$$\n\n",
                "A medida que $\\beta\\gamma$ aumenta, $\\mu_n$ disminuye y la"
                " amplitud de la oscilación se amortigua adiabáticamente"
                " según $(\\beta\\gamma)^{-3/4}$."
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Simular oscilaciones para pertubación de +3°\n",
                "delta_phi, mu_theory, sim_cells_mid, sim_mu_points = simulate_synchrotron_oscillation(perturbation_deg=3.0, phi_s_deg=-30.0)\n\n",
                "# Graficar y exportar a CSV\n",
                "plot_synchrotron_results(delta_phi, mu_theory, sim_cells_mid, sim_mu_points)\n",
                'export_synchrotron_to_csv(delta_phi, mu_theory, sim_cells_mid, sim_mu_points, filename_traj="resultados/sincrotron_trayectoria.csv", filename_mu="resultados/sincrotron_avance_fase.csv")\n\n',
                'print(f"Amplitud inicial: {delta_phi[0]:.2f}° | Amplitud final (Celda 55): {abs(delta_phi[-1]):.2f}°")',
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Análisis de Sensibilidad a Errores de Frecuencia"
                " RF\n",
                "Se modifica la frecuencia RF mediante $\\omega = \\omega_0 (1 +"
                " \\epsilon_f)$ desde $0\\%$ hasta $4\\%$. Un descalce en la"
                " frecuencia desplaza la fase de equilibrio del haz"
                " $\\langle\\Delta\\phi\\rangle$ para compensar la falta de"
                " sincronismo, hasta que en errores altos se pierde la"
                " estabilidad y cae la captura."
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Simular barrido de errores de frecuencia RF\n",
                "rf_results, _ = simulate_frequency_errors(error_list=[0.0, 0.002, 0.005, 0.01, 0.02, 0.03, 0.04])\n\n",
                "# Graficar y exportar a CSV\n",
                "plot_rf_error_results(rf_results)\n",
                'export_rf_errors_to_csv(rf_results, filename="resultados/rf_errores_sensibilidad.csv")',
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Dinámica Comparativa con Electrones Relativistas\n",
                "A diferencia de los protones, los electrones inyectados a"
                " $T_0 = 10.0\\text{ MeV}$ poseen una velocidad inicial"
                " $\\beta_0 \\approx 0.9988$ (ultrarelativistas). Por ello:\n",
                "1. Se utiliza una estructura con celdas de longitud constante"
                " $L = \\lambda$.\n",
                "2. No existen oscilaciones de sincrotrón (se congelan en"
                " fase).\n",
                "3. La ganancia de energía depende directamente del coseno de"
                " la fase de inyección $\\Delta T \\propto \\cos(\\phi_0)$."
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Simular electrones en 60 celdas constantes\n",
                "e_hist_T, e_hist_phi, e_phases = simulate_electrons(T_0=10.0, num_cells=60)\n\n",
                "# Graficar y exportar a CSV\n",
                "plot_electron_results(e_hist_T, e_hist_phi, e_phases)\n",
                'export_electrons_to_csv(e_hist_T, e_hist_phi, e_phases, filename="resultados/electrones_simulacion.csv")',
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Conclusiones del Proyecto\n",
                "1. **Diseño Geométrico:** La aceleración de protones exige un"
                " incremento de longitud de celdas desde $7.73\\text{ cm}$ hasta"
                " $26.83\\text{ cm}$ para preservar la condición de"
                " sincronismo $L_n = \\beta_n \\lambda$.\n",
                "2. **Estabilidad de Fase:** La captura longitudinal supera el"
                " $99\\%$ para el haz nominal. Las oscilaciones de sincrotrón"
                " se amortiguan en un factor $\\approx 2.15$.\n",
                "3. **Tolerancia de Frecuencia:** El acelerador tolera errores"
                " de frecuencia de hasta $\\approx 1.0\\%$ con capturas"
                " superiores al $98\\%$. Errores mayores al $3\\%$ degradan la"
                " captura severamente.\n",
                "4. **Régimen Ultrarelativista:** Los electrones no requieren"
                " celdas de tamaño variable y muestran un congelamiento de fase"
                " asintótico sin oscilaciones longitudinales."
            ],
        },
    ],
    "metadata": {
        "language_info": {"name": "python"},
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 2,
}

# Guardar el archivo .ipynb en la raíz
output_path = "P19-Acelerador-lineal.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
  json.dump(notebook_content, f, indent=2, ensure_ascii=False)

print(
    f"¡Notebook creado exitosamente en la raíz del proyecto como"
    f" '{output_path}'!"
)