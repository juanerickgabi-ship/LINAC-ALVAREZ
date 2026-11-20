# Simulación Dinámica de un Acelerador Lineal (LINAC tipo Álvarez)

Este repositorio contiene la simulación desde cero de la dinámica longitudinal de un haz de protones y electrones en un Acelerador Lineal (LINAC) tipo Álvarez, desarrollada para la materia de **Física Computacional 2**.

## 📌 Características de la Simulación

- **Diseño Geométrico:** Cálculo iterativo de la longitud de las celdas síncronas ($L_n = \beta_{n}\lambda$) para acelerar protones de 3 MeV a 50 MeV en 55 celdas (10.59 m).
- **Seguimiento del Haz:** Simulación vectorizada de 3000 partículas con dispersión normal en fase y energía ($\sigma_\phi = 15^\circ$, $\sigma_T/T_0 = 0.5\%$).
- **Estabilidad de Fase:** Verificación del amortiguamiento adiabático y oscilaciones de sincrotrón ($\mu$).
- **Sensibilidad de RF:** Análisis del efecto de errores de frecuencia en la radiofrecuencia (0% a 4%).
- **Dinámica Relativista de Electrones:** Comparación con electrones ultrarelativistas ($10\text{ MeV}$) en celdas de longitud constante.

---

## 🛠️ Requisitos e Instalación

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

Para ejecutar la simulación completa, generar todas las gráficas en la carpeta `figuras/` y generar los archivos numericos en formato `.csv` en la carpeta `resultados` :

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