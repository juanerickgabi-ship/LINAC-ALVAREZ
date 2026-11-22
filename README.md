# Simulación Dinámica y Diseño de un Acelerador Lineal (LINAC tipo Álvarez)

**Asignatura:** Física Computacional 2

**Nombre del Proyecto:** Proyecto: P19 - Acelerador Lineal de Protones

**Lenguaje y Entorno:** Python 3 | Visual Studio Code | Jupyter Notebook 

Este repositorio contiene la simulación desde cero de la dinámica longitudinal de un haz de protones y electrones en un Acelerador Lineal (LINAC) tipo Álvarez, desarrollada para la materia de **Física Computacional 2**.

## Descripción del Proyecto 
Este repositorio contiene la simulación dinámica, el diseño geométrico cinemático y el análisis de estabilidad longitudinal para un acelerador lineal (LINAC) tipo Álvarez. El sistema acelera protones desde una energía inicial de $T_0 = 3.0\text{ MeV}$ hasta una energía final de $T_f = 50.0\text{ MeV}$ operando a una frecuencia de radiofrecuencia (RF) de $f_{\text{RF}} = 352.2\text{ MHz}$ y una fase síncrona nominal de $\phi_s = -30^\circ$. El proyecto incluye:

1. Modelado Geométrico Discreto: Cálculo celda a celda de la condición de sincronismo síncrono $L_n = \beta_n \lambda$.
2. Seguimiento Multipartícula: Simulación discreta de $N = 3000$ partículas en el espacio de fases $(\Delta\phi, \Delta T)$.
3. Análisis de Oscilaciones y Liouville: Verificación cuantitativa de oscilaciones de sincrotrón y amortiguamiento adiabático ($\sigma_\phi \propto (\beta\gamma)^{-3/4}$).
4. Tolerancia a Errores de RF: Evaluación de sensibilidad del haz ante descalces de frecuencia de $0\%$ a $4\%$.
5. Estudio Comparativo con Electrones: Análisis de dinámica ultrarelativista ($\beta \approx 1$) en cavidades de celdas de longitud constante $L = \lambda$.


## Estructura del Repositorio

- LINAC ALVAREZ/
   * ├── P19-Acelerador-lineal.ipynb   # Notebook principal interactivo (Informe ejecutable)
   * ├── README.md                     # Documentación completa del repositorio
   * ├── requirements.txt              # Dependencias de Python (numpy, matplotlib, pandas)
   * ├── .gitignore                    # Archivos excluidos del control de versiones
   * ├── src/                          # Módulos Python del simulador
   + │   ├── physics.py                # Constantes físicas y conversión relativista
   + │   ├── linac_design.py           # Diseño geométrico síncrono y exportación CSV
   + │   ├── tracking.py               # Generación y seguimiento discreto del haz
   + │   ├── synchrotron.py            # Oscilaciones de sincrotrón no lineales
   + │   ├── rf_errors.py              # Análisis de errores de frecuencia RF
   + │   ├── electrons.py              # Simulación de electrones ultrarelativistas
   + │   ├── visualizer.py             # Generación de la suite de 11 figuras analíticas
   + │   └── main.py                   # Script unificador principal de ejecución
   * ├── figuras/                      # Suite de 11 gráficas exportadas en alta resolución (300 DPI)
   * └── resultados/                   # Datos numéricos tabulados en formato CSV
---

## Parametros Físicos

|Magnitud| Ecuación / Expresión| Descripción Física|
|:------:|:-------------------:|:-----------------:|
|Factor Gamma Relativista|$\gamma_n​=1 + \frac{T_n}{m_0​c^2}$​​|Relación masa-energía de la partícula|
|Factor Beta Relativista|$\beta_n​= \sqrt{1−\frac{1}{γ_n^2​}​}​$|Velocidad adimensional $\beta =v/c$|
|Condición de Sincronismo|$Ln​=\beta_n​ \lambda= \frac{​\beta_n​ c}{f_{RF}}$​|Longitud requerida de la celda n|
|Ganancia Síncrona por Celda|$\Delta T_n = qV_{gap​} cos(ϕs​)|Ganancia de energía síncrona constante|
|Gradiente Efectivo de Campo|$E_{acc,n}​= \frac{​qV_{gap​}cos(ϕs​)}{L_n}$|Campo eléctrico acelerador por metro (MV/m)|
|Gradiente Pico Nominal|$E_{0,n}​=\frac{​qV_{gap}}{L_n}$|Gradiente eléctrico máximo en la celda|
|Avance de Fase por Celda|$\mu_n ​= \frac{2\pi qV_{gap}​(−sin(\phi_s​))}{m_0 ​c^2 \beta_n^2​ \gamma_n^3}​$​​|Frecuencia angular de oscilación de sincrotrón|


## Archivo de Resultados `resultados/`

Los datos generados por la simulación se exportan automáticamente a la carpeta `resultados/`:
`diseno_celdas.csv`: Tabla principal de 55 celdas con geometría $L_n$, posición acumulada $z_n$, ganancia $\Delta T_n$, factores $\beta_n$, $\gamma_n$, $\cos(\phi_s)$ y campos $E_0$ y $E_{\text{acc}}$ ($\text{MV/m}$).
`sincrotron_trayectoria.csv`: Evolución celda a celda de la perturbación de fase $\delta\phi(n)$ ante una desviación inicial.
`sincrotron_avance_fase.csv`: Avance de fase síncrono teórico $\mu_n$ vs. empírico.
`rf_errores_sensibilidad.csv`: Porcentaje de captura, desplazamiento medio de fase de equilibrio $\langle\Delta\phi\rangle$ y energía media transmitida para barridos de error RF ($0\%$ a $4\%$).
`electrones_simulacion.csv`: Traza cinemática y de fase de electrones en 60 celdas constantes.

## Requisitos e Instalación

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/juanerickgabi-ship/LINAC-ALVAREZ.git](https://github.com/juanerickgabi-ship/LINAC-ALVAREZ.git)
   cd LINAC-ALVAREZ
   ```

2. Instalar las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

3. Instalar extensiones en VSCode (solo si se trabaja en este)


---

## 🚀 Ejecución del Proyecto

Para ejecutar la simulación completa, generar todas las gráficas en la carpeta `figuras/` y generar los archivos numericos en formato `.csv` en la carpeta `resultados/` :

```bash
python src/main.py
```
o tambien 

```bash
python P19-Acelerador-lineal.ipnyb
```


---

## 📁 Estructura del Repositorio

- `src/`: Código fuente modular en Python.
- `figuras/`: Gráficos en alta resolución del espacio de fases, celdas y errores.
- `resultados/`: Datos exportados de las simulaciones.
- `informe_acelerador_lineal/`: Documentación y reporte del proyecto.
- `P19-Acelerador-lineal.ipynb` : Notebook con el codigo fuente explicando cada parte del mismo.
- `Avances/` : Documentación de avances hechos durante el proyecto.