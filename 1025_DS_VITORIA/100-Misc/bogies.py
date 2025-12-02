import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Parámetros de Simulación ---
N_REGISTROS = 500000
N_BOGIES = 40
INTERVALO_MINUTOS = 5

# Distribución de fallos y ruido
PROB_FALLO_BASE = 0.005 # Probabilidad base de que falle (0.5%)
PROB_VALOR_FALTANTE = 0.01 # ~1%
PROB_OUTLIER = 0.005 # ~0.5%

# --- 1. Generación de la Base Temporal y de Bogies ---

# Calcular el número de pasos de tiempo necesarios por bogie
N_PASOS_TIEMPO = int(N_REGISTROS / N_BOGIES)
if N_REGISTROS % N_BOGIES != 0:
    print(f"Aviso: El número de registros no es divisible por el número de bogies. Se generarán {N_PASOS_TIEMPO * N_BOGIES} registros.")
    N_REGISTROS = N_PASOS_TIEMPO * N_BOGIES

# Generar la secuencia de tiempo
start_time = datetime(2023, 1, 1, 0, 0, 0)
time_stamps = [start_time + timedelta(minutes=INTERVALO_MINUTOS * i) for i in range(N_PASOS_TIEMPO)]

# Crear el DataFrame base
df = pd.DataFrame({
    'timestamp': np.tile(time_stamps, N_BOGIES),
    'bogie_id': np.repeat(np.arange(1, N_BOGIES + 1), N_PASOS_TIEMPO)
})
df = df.sort_values(by=['bogie_id', 'timestamp']).reset_index(drop=True)

# --- 2. Generación de Variables Categóricas y Contextuales ---

TRACK_TYPES = ['high-speed', 'regional', 'freight']
TRACK_CONDITIONS = ['good', 'fair', 'poor']
OPERATION_MODES = ['normal', 'reduced', 'emergency']
FAILURE_TYPES = ['Bearing Failure', 'Wheel Wear', 'Brake System', 'Suspension', 'Empty']

df['track_type'] = np.random.choice(TRACK_TYPES, N_REGISTROS, p=[0.25, 0.45, 0.30])
df['track_condition'] = np.random.choice(TRACK_CONDITIONS, N_REGISTROS, p=[0.6, 0.3, 0.1])
df['operation_mode'] = np.random.choice(OPERATION_MODES, N_REGISTROS, p=[0.85, 0.10, 0.05])
df['rain'] = np.random.choice([0, 1], N_REGISTROS, p=[0.8, 0.2])
df['snow'] = np.random.choice([0, 1], N_REGISTROS, p=[0.95, 0.05])

# Métricas de uso y mantenimiento
df['km_since_maint'] = np.random.randint(500, 200000, N_REGISTROS)
df['days_since_inspection'] = np.random.randint(1, 365, N_REGISTROS)
df['last_intervention'] = np.random.randint(1, 1000, N_REGISTROS)
df['hours_total'] = np.random.randint(5000, 50000, N_REGISTROS)
df['defect_history'] = np.random.randint(0, 6, N_REGISTROS)

# --- 3. Generación de Variables Numéricas (Sensores) con Unidades y Consistencia ---

# 3.1. Temperatura ambiental (Weather Temp)
df['weather_temp'] = np.random.uniform(5, 35, N_REGISTROS)

# 3.2. Velocidad (Speed) y Carga (Load)
def get_speed_load(row):
    if row['track_type'] == 'high-speed':
        speed = np.random.normal(250, 20)
        load = np.random.normal(12000, 1000) # Pasajeros
    elif row['track_type'] == 'regional':
        speed = np.random.normal(100, 15)
        load = np.random.normal(10000, 1500) # Pasajeros/Carga ligera
    else: # freight
        speed = np.random.normal(70, 10)
        load = np.random.normal(30000, 5000) # Carga pesada
    return max(0, speed), max(1000, load)

speed_load = df.apply(get_speed_load, axis=1, result_type='expand')
df['speed'] = speed_load[0]
df['load'] = speed_load[1]

# 3.3. Temperatura de Rodamiento (Bearing Temp)
# Media base de 75°C. Añadir variabilidad.
df['temp_bearing'] = np.random.normal(75, 3, N_REGISTROS)

# 3.4. Vibraciones (Vib Vert/Lat)
def get_vibrations(row):
    # Condición de vía y tipo de operación impactan en la vibración
    if row['track_condition'] == 'poor' or row['operation_mode'] == 'emergency':
        vert_mean = 0.035
        lat_mean = 0.025
    elif row['track_condition'] == 'fair':
        vert_mean = 0.025
        lat_mean = 0.015
    else: # good
        vert_mean = 0.015
        lat_mean = 0.010

    # Impacto de la velocidad: a mayor velocidad, mayor vibración
    speed_factor = row['speed'] / 100 * 0.005 # pequeña contribución de la velocidad

    vib_vert = np.random.normal(vert_mean + speed_factor, 0.005)
    vib_lat = np.random.normal(lat_mean + speed_factor * 0.5, 0.003)

    return max(0.001, vib_vert), max(0.001, vib_lat)

vibrations = df.apply(get_vibrations, axis=1, result_type='expand')
df['vib_vert'] = vibrations[0]
df['vib_lat'] = vibrations[1]

# 3.5. Humedad (Humidity)
# Influenciada por lluvia/nieve
df['humidity'] = np.random.normal(60 + df['rain']*15 + df['snow']*10, 5)
df['humidity'] = df['humidity'].clip(30, 100)

# 3.6. Fuerza de Frenado (Brake Force)
# Coherente con la velocidad: frenado más fuerte a velocidades más altas o en emergencia
df['brake_force'] = (df['speed'] / 200) * np.random.normal(100, 10) + np.random.normal(10, 5)
df.loc[df['operation_mode'] == 'emergency', 'brake_force'] *= 1.5 # Más fuerte en emergencia
df['brake_force'] = df['brake_force'].clip(5, 500)

# 4. Generación de la Variable Objetivo: 'failed_next_48h'
df['failed_next_48h'] = 0

# Criterios de riesgo para el fallo (Probabilidad aumentada)
# Cuanto más alta la métrica, mayor el riesgo de fallo
temp_high_risk = df['temp_bearing'].quantile(0.95)
vib_vert_high_risk = df['vib_vert'].quantile(0.95)
vib_lat_high_risk = df['vib_lat'].quantile(0.95)
km_high_risk = df['km_since_maint'].quantile(0.85)
days_high_risk = df['days_since_inspection'].quantile(0.85)

# Función de probabilidad de fallo, basada en condiciones de riesgo
def calculate_failure_prob(row):
    prob = PROB_FALLO_BASE
    
    # Riesgo por Temperatura
    if row['temp_bearing'] > temp_high_risk:
        prob *= 4
    elif row['temp_bearing'] > df['temp_bearing'].quantile(0.90):
        prob *= 2

    # Riesgo por Vibración
    if row['vib_vert'] > vib_vert_high_risk or row['vib_lat'] > vib_lat_high_risk:
        prob *= 3
        
    # Riesgo por Mantenimiento
    if row['km_since_maint'] > km_high_risk or row['days_since_inspection'] > days_high_risk:
        prob *= 2
        
    # Asegurar que la probabilidad no exceda un límite razonable
    return min(prob, 0.5) # Máximo 50% de probabilidad de fallo en una entrada

# Aplicar la probabilidad de fallo y generar el fallo
df['failure_prob'] = df.apply(calculate_failure_prob, axis=1)
df['failed_next_48h'] = np.random.uniform(0, 1, N_REGISTROS) < df['failure_prob']
df['failed_next_48h'] = df['failed_next_48h'].astype(int)

# 4.1. Asignar 'failure_type' solo a los fallos
df['failure_type'] = np.where(df['failed_next_48h'] == 1, 
                               np.random.choice(FAILURE_TYPES[:-1], N_REGISTROS, p=[0.4, 0.3, 0.15, 0.15]), 
                               '') # Dejar vacío si no falla

# 5. Formateo de Strings con Unidades
columns_to_format = {
    'temp_bearing': " {:.2f} C",
    'vib_vert': " {:.5f} m/s2",
    'vib_lat': " {:.5f} m/s2",
    'speed': " {:.2f} km/h",
    'load': " {:.0f} kg",
    'humidity': " {:.1f} %",
    'brake_force': " {:.2f} kN",
    'weather_temp': " {:.1f} C"
}

# Columnas numéricas originales para aplicar ruido
numeric_cols = list(columns_to_format.keys())

for col, fmt_str in columns_to_format.items():
    # El mapa de formateo incluye un espacio inicial que se eliminará al aplicar missing/outliers
    df[col] = df[col].apply(lambda x: fmt_str.format(x)).str.strip()

# 6. Introducción de Valores Faltantes (~1%) y Outliers (~0.5%)

for col in numeric_cols:
    # Convertir temporalmente a float para operaciones de ruido/outliers
    # Nota: Los datos ya tienen las unidades y deben ser tratados como strings. 
    # Para la simulación de outliers/faltantes, manipularemos el string.

    # 6.1. Outliers
    outlier_mask = np.random.choice([False, True], N_REGISTROS, p=[1 - PROB_OUTLIER, PROB_OUTLIER])
    if col in ['temp_bearing']:
        # Temperaturas exageradamente altas
        df.loc[outlier_mask, col] = np.random.uniform(150, 250, outlier_mask.sum())
    elif col in ['vib_vert', 'vib_lat']:
        # Vibraciones fuera de rango
        df.loc[outlier_mask, col] = np.random.uniform(0.5, 1.5, outlier_mask.sum())
    elif col in ['speed']:
        # Velocidades imposibles
        df.loc[outlier_mask, col] = np.random.uniform(500, 800, outlier_mask.sum())

    # 6.2. Valores Faltantes (NaN)
    missing_mask = np.random.choice([False, True], N_REGISTROS, p=[1 - PROB_VALOR_FALTANTE, PROB_VALOR_FALTANTE])
    # Asegurarse de que los outliers que se convirtieron a float se conviertan a string con unidad
    # antes de aplicar el missing.
    if col in df.columns: # Re-aplicar el formato de string a los outliers
        fmt_str = columns_to_format[col].strip() # Obtener el formato limpio
        # Solo aplicar formato si es numérico (i.e. no es NaN ya por alguna razón)
        df.loc[outlier_mask, col] = df.loc[outlier_mask, col].apply(
            lambda x: f"{x:.2f}{fmt_str.split(' ')[-1]}" if isinstance(x, (int, float)) else x
        )

    # Aplicar NaN (Valor Faltante) como np.nan (que se guardará como celda vacía/string "nan" en CSV)
    df.loc[missing_mask, col] = np.nan

# 7. Formatear Columnas de Mantenimiento y Categóricas
df['km_since_maint'] = df['km_since_maint'].astype(str) + " km"
df['days_since_inspection'] = df['days_since_inspection'].astype(str) + " days"
df['last_intervention'] = df['last_intervention'].astype(str) + " days"
df['hours_total'] = df['hours_total'].astype(str) + " h"
df['defect_history'] = df['defect_history'].astype(str)

# 8. Reordenar Columnas
final_cols = [
    'timestamp', 'bogie_id', 'temp_bearing', 'vib_vert', 'vib_lat', 'speed', 'load', 
    'humidity', 'brake_force', 'weather_temp', 'rain', 'snow', 'track_type', 
    'track_condition', 'operation_mode', 'km_since_maint', 'days_since_inspection', 
    'last_intervention', 'hours_total', 'defect_history', 'failure_type', 'failed_next_48h'
]
df = df[final_cols]

# 9. Guardar el Dataset
filename = 'train_bogie_dataset.csv'
df.to_csv(filename, index=False)

print(f"\n✅ Dataset generado con éxito.")
print(f"👉 Registros generados: {len(df)}")
print(f"👉 Archivo guardado como: {filename}")
print(f"👉 Tasa de fallos (Clase 1): {df['failed_next_48h'].mean():.4f}")
print("\nPrimeras 5 filas del dataset:")
print(df.head())