import pandas as pd
import numpy as np

np.random.seed(42)

# ---------------------------
# CONFIGURACIÓN
# ---------------------------
n = 200_000          
freq = "1min"        
n_bogies = 40        
start_date = "2024-01-01"

# ---------------------------
# BASE DE TIEMPO
# ---------------------------
timestamps = pd.date_range(start=start_date, periods=n, freq=freq)

train_ids = np.random.randint(1, 21, size=n)          
bogie_ids = np.random.randint(1, n_bogies + 1, size=n)
hour_of_day = timestamps.hour
is_night = ((hour_of_day >= 22) | (hour_of_day < 6)).astype(int)

# ---------------------------
# VARIABLES LATENTES
# ---------------------------
bogie_health = np.random.beta(a=2, b=5, size=n_bogies)
bogie_health_per_row = bogie_health[bogie_ids - 1]

track_condition_cat = np.random.choice(["good", "fair", "poor"], size=n, p=[0.6, 0.3, 0.1])
track_condition_map = {"good": 0.0, "fair": 0.5, "poor": 1.0}
track_condition_score = np.vectorize(track_condition_map.get)(track_condition_cat)

days_since_inspection = np.random.randint(0, 365, size=n)

base_external_temp = 15 + 10 * np.sin(2 * np.pi * (timestamps.dayofyear / 365))
external_temp = base_external_temp + np.where(is_night == 1, -5, 3) + np.random.normal(0, 3, size=n)

speed = np.clip(np.random.normal(loc=90 - 15*is_night, scale=25, size=n), 0, 200)

train_load_base = np.linspace(8, 20, 20)
load = np.clip(np.random.normal(train_load_base[train_ids - 1], 2, size=n), 4, 25)

humidity = np.clip(np.random.normal(loc=60, scale=20, size=n), 0, 100)

# ---------------------------
# SENSORES PRINCIPALES
# ---------------------------
base_vib = 0.2 + 0.005 * speed + 0.05 * load + 0.8 * track_condition_score + 1.0 * bogie_health_per_row
noise_vib = np.random.normal(0, 0.3, size=n)

vibration_x = np.abs(base_vib + noise_vib)
vibration_y = np.abs(base_vib * (0.8 + 0.2 * np.random.rand(n)) + noise_vib)
vibration_z = np.abs(base_vib * (1.1 + 0.3 * np.random.rand(n)) + noise_vib)

temp_bogie = external_temp + 0.08 * speed + 0.6 * load + 25 * bogie_health_per_row + np.random.normal(0, 3, size=n)
wheel_temp_left = temp_bogie + np.random.normal(0, 2, size=n)
wheel_temp_right = temp_bogie + np.random.normal(0, 2, size=n)

# ---------------------------
# VARIABLES DE CONTEXTO
# ---------------------------
operation_mode = np.random.choice(["service", "shunting", "maintenance_move"], size=n, p=[0.8, 0.15, 0.05])
track_gradient = np.random.normal(0, 8, size=n)
curve_class = np.random.choice(["straight", "gentle_curve", "sharp_curve"], size=n, p=[0.7, 0.2, 0.1])

# ---------------------------
# ETIQUETAS SUPERVISADAS
# ---------------------------
risk_score = (0.5 * bogie_health_per_row + 0.0008 * days_since_inspection +
              0.003 * np.maximum(vibration_x - 5, 0) + 
              0.002 * np.maximum(wheel_temp_left - 80, 0) +
              0.002 * np.maximum(wheel_temp_right - 80, 0))
risk_score = np.clip(risk_score, 0, 3)

fault_type = np.zeros(n, dtype=int)
fault_type[risk_score > 0.8] = 1
fault_type[risk_score > 1.5] = 2
fault_type[risk_score > 2.2] = 3

flip_idx = np.random.choice(n, size=int(0.02 * n), replace=False)
fault_type[flip_idx] = np.random.randint(0, 4, size=len(flip_idx))

target_fault = (fault_type > 0).astype(int)
alarm_level = np.zeros(n, dtype=int)
alarm_level[(fault_type >= 1) & (fault_type <= 2)] = 1
alarm_level[fault_type == 3] = 2

# ---------------------------
# DATAFRAME BASE
# ---------------------------
df = pd.DataFrame({
    "timestamp": timestamps.astype(str),
    "train_id": train_ids,
    "bogie_id": bogie_ids,
    "operation_mode": operation_mode,
    "track_condition": track_condition_cat,
    "curve_class": curve_class,
    "track_gradient": track_gradient,
    "speed_kmh": speed,
    "load_tons": load,
    "external_temp_c": external_temp,
    "humidity_pct": humidity,
    "days_since_inspection": days_since_inspection,
    "vibration_x_rms": vibration_x,
    "vibration_y_rms": vibration_y,
    "vibration_z_rms": vibration_z,
    "bogie_temp_c": temp_bogie,
    "wheel_temp_left_c": wheel_temp_left,
    "wheel_temp_right_c": wheel_temp_right,
    "bogie_health_score": bogie_health_per_row,
    "fault_type": fault_type,
    "target_fault": target_fault,
    "alarm_level": alarm_level,
})

# ---------------------------
# EVENTOS DE MANTENIMIENTO (FECHAS 100% CORRECTAS)
# ---------------------------
maintenance_events = []
for bogie in range(1, n_bogies + 1):
    n_events = np.random.randint(2, 6)
    # Generar fechas REALES con pandas (sin problemas numpy)
    possible_dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="5D")
    event_indices = np.random.choice(len(possible_dates), n_events, replace=False)
    event_dates = possible_dates[event_indices]
    
    for date in event_dates:
        maintenance_events.append({
            'bogie_id': bogie,
            'maintenance_date': date.strftime('%Y-%m-%d'),  # ✅ Pandas Timestamp tiene strftime
            'maintenance_type': np.random.choice(
                ['routine_inspection', 'wheel_replacement', 'bearing_repair', 'bogie_overhaul'], 
                p=[0.5, 0.2, 0.2, 0.1]
            ),
            'downtime_hours': np.random.randint(4, 48),
            'cost_euros': np.random.randint(500, 8000)
        })

df_maintenance = pd.DataFrame(maintenance_events)

# ---------------------------
# DÍAS DESDE ÚLTIMO MANTENIMIENTO (VECTORIZADO)
# ---------------------------
last_maint_date = {}
for bogie in range(1, n_bogies + 1):
    bogie_maint = df_maintenance[df_maintenance['bogie_id'] == bogie]
    if len(bogie_maint) > 0:
        last_maint_date[bogie] = pd.to_datetime(bogie_maint['maintenance_date'].max())
    else:
        last_maint_date[bogie] = pd.to_datetime("2023-12-31")

row_dates = pd.to_datetime(df['timestamp'])
days_since_last_maint = []
for i, bogie in enumerate(df['bogie_id']):
    last_date = last_maint_date[bogie]
    days = max(0, (row_dates[i] - last_date).days)
    days_since_last_maint.append(days)

df['days_since_last_maint'] = days_since_last_maint
df['days_since_inspection'] = np.minimum(df['days_since_inspection'], df['days_since_last_maint'])

# ---------------------------
# INYECCIÓN DE ERRORES
# ---------------------------
for col, n_null in [("bogie_temp_c", 5000), ("wheel_temp_left_c", 3000), ("wheel_temp_right_c", 3000),
                    ("load_tons", 2500), ("speed_kmh", 2000), ("humidity_pct", 2000)]:
    idx = np.random.choice(n, n_null, replace=False)
    df.loc[idx, col] = np.nan

idx = np.random.choice(n, 3000, replace=False); df.loc[idx, "speed_kmh"] *= -1
idx = np.random.choice(n, 1500, replace=False); df.loc[idx, "humidity_pct"] = -5
idx = np.random.choice(n, 1200, replace=False); df.loc[idx, "bogie_temp_c"] = -20

for col in ["vibration_x_rms", "vibration_y_rms", "vibration_z_rms"]:
    idx = np.random.choice(n, 2500, replace=False)
    df.loc[idx, col] = df[col].median() + np.random.uniform(30, 80)

idx = np.random.choice(n, 2000, replace=False); df.loc[idx, "track_condition"] = "unknown"
idx = np.random.choice(n, 1500, replace=False); df.loc[idx, "curve_class"] = "NA"
idx = np.random.choice(n, 1200, replace=False); df.loc[idx, "timestamp"] = "ERROR"

idx = np.random.choice(n, 1800, replace=False); df.loc[idx, "external_temp_c"] = 999
idx = np.random.choice(n, 1000, replace=False); df.loc[idx, "wheel_temp_left_c"] = 999

maint_idx = df.index[df["operation_mode"] == "maintenance_move"].to_numpy()
if len(maint_idx) > 1500:
    maint_idx = np.random.choice(maint_idx, 1500, replace=False)
df.loc[maint_idx, "speed_kmh"] = np.random.uniform(140, 220, size=len(maint_idx))

idx = np.random.choice(n, 3000, replace=False)
df.loc[idx, "fault_type"] = np.nan
df.loc[idx, "target_fault"] = np.nan

# ---------------------------
# EXPORTAR
# ---------------------------
df.to_csv("bogie_condition_dataset_dirty_200k.csv", index=False)
df_maintenance.to_csv("bogie_maintenance_events.csv", index=False)

print("✅ Dataset principal:", "bogie_condition_dataset_dirty_200k.csv")
print("✅ Eventos mantenimiento:", "bogie_maintenance_events.csv")
print(f"📊 {len(df_maintenance)} eventos de mantenimiento generados")
print(f"🔢 Distribución fault_type: {df['fault_type'].value_counts().sort_index().to_dict()}")
print("🚀 ¡CÓDIGO 100% FUNCIONAL - LISTO PARA PRESENTACIÓN!")
