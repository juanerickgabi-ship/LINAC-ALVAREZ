import numpy as np
from physics import C_LIGHT, M_PROTON_MEV, get_beta, get_gamma
import csv
import os


def design_linac(
    T_init: float = 3.0,
    T_final: float = 50.0,
    qV_gap: float = 1.0,
    phi_s_deg: float = -30.0,
    f_rf: float = 352.2e6,
    m_MeV: float = M_PROTON_MEV,
    max_cells: int = 100,
):
    """Calcula la geometría de celdas del LINAC Álvarez para la partícula síncrona[cite: 12, 13].

    Parámetros:
        T_init: Energía cinética inicial en MeV[cite: 10, 12].
        T_final: Energía cinética objetivo en MeV[cite: 10, 12, 13].
        qV_gap: Ganancia máxima de energía en el hueco en MeV[cite: 5, 10, 12].
        phi_s_deg: Fase síncrona en grados[cite: 5, 10, 12].
        f_rf: Frecuencia de radiofrecuencia en Hz[cite: 5, 10].
        m_MeV: Masa en reposo de la partícula en MeV/c^2[cite: 4, 12].
        max_cells: Límite de seguridad para el ciclo[cite: 13].

    Retorna:
        cell_lengths: Arreglo (N,) con las longitudes de cada celda en metros[cite: 13].
        T_sync: Arreglo (N+1,) con la evolución de la energía síncrona en
        MeV[cite: 13].
        z_positions: Arreglo (N+1,) con las posiciones longitudinales z de cada
        brecha en metros.
    """
    phi_s_rad = np.radians(phi_s_deg)  # Convertir fase a radianes[cite: 12]
    wavelength = C_LIGHT / f_rf  # Longitud de onda lambda = c / f[cite: 5, 10]

    T_sync = [T_init]
    cell_lengths = []
    z_positions = [0.0]

    T_curr = T_init

    # Proceso iterativo de diseño[cite: 12, 13]
    for _ in range(max_cells):
        if T_curr >= T_final:
            break  # Condición de parada cuando se alcanza la energía final[cite: 13]

        # 1. Ganancia de energía síncrona por brecha: Delta T_s = qV_gap * cos(phi_s)[cite: 7, 12]
        T_next = T_curr + qV_gap * np.cos(phi_s_rad)  #[cite: 12]
        T_sync.append(T_next)

        # 2. Velocidad relativista beta tras recibir la ganancia de energía[cite: 12, 13]
        beta_next = get_beta(T_next, m_MeV)  #[cite: 13]

        # 3. Condición de sincronización: L_n = beta_{n+1} * lambda[cite: 6, 13]
        L_n = beta_next * wavelength  #[cite: 6, 13]
        cell_lengths.append(L_n)

        # 4. Acumular posición z a lo largo del acelerador
        z_positions.append(z_positions[-1] + L_n)

        # Actualizar la energía para la siguiente iteración
        T_curr = T_next

    return np.array(cell_lengths), np.array(T_sync), np.array(z_positions)


if __name__ == "__main__":
    # Prueba del diseño con los parámetros de referencia del informe[cite: 10]
    cell_lengths, T_sync, z_positions = design_linac(
        T_init=3.0,  #[cite: 10]
        T_final=50.0,  #[cite: 10]
        qV_gap=1.0,  #[cite: 10]
        phi_s_deg=-30.0,  #[cite: 10]
        f_rf=352.2e6,  #[cite: 10]
    )

    num_cells = len(cell_lengths)
    total_length = z_positions[-1]

    print("=========================================")
    print("   RESULTADOS DEL DISEÑO DE CELDAS")
    print("=========================================")
    print(f"Número total de celdas: {num_cells}")
    print(f"Longitud total del LINAC: {total_length:.2f} m")
    print(
        f"Energía final alcanzada: {T_sync[-1]:.3f} MeV (Objetivo: 50.0 MeV)"
    )
    print(f"Primera celda (L_1): {cell_lengths[0] * 100:.2f} cm")
    print(f"Última celda  (L_{num_cells}): {cell_lengths[-1] * 100:.2f} cm")
    print(
        f"Gradiente medio de aceleración: {T_sync[-1] / total_length:.2f} MeV/m"
    )
    print("=========================================")

def export_design_to_csv(
    cell_lengths: np.ndarray,
    T_sync: np.ndarray,
    z_positions: np.ndarray,
    filename: str = "resultados/diseno_celdas.csv",
):
  """Exporta la geometría de celdas y la energía del protón síncrono a un archivo CSV."""
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  gamma_vals = get_gamma(T_sync[1:], M_PROTON_MEV)
  beta_vals = get_beta(T_sync[1:], M_PROTON_MEV)

  with open(filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Numero_Celda",
        "Longitud_Ln_m",
        "Posicion_Z_m",
        "Energia_Sync_MeV",
        "Beta",
        "Gamma",
    ])

    for n in range(len(cell_lengths)):
      writer.writerow([
          n + 1,
          f"{cell_lengths[n]:.6f}",
          f"{z_positions[n + 1]:.6f}",
          f"{T_sync[n + 1]:.6f}",
          f"{beta_vals[n]:.6f}",
          f"{gamma_vals[n]:.6f}",
      ])

  print(f" Datos de diseño exportados a '{filename}'")