import pandas as pd
import numpy as np

np.random.seed(42)

n = 100_000

# -----------------------------
# Base features
# -----------------------------
timestamp = pd.date_range(start="2022-01-01", periods=n, freq="min")

bogie_id = np.random.randint(1000, 5000, n)
operation_mode = np.random.choice(["normal", "heavy_load", "eco", "emergency"], n, p=[0.65, 0.2, 0.1, 0.05])
track_condition = np.random.choice(["dry", "wet", "icy"], n, p=[0.75, 0.2, 0.05])
curve_class = np.random.choice(["straight", "moderate", "sharp"], n, p=[0.6, 0.3, 0.1])
track_gradient = np.random.normal(1.5, 1.2, n)

speed_kmh = np.clip(np.random.normal(90, 25, n), 20, 180)
load_tons = np.clip(np.random.normal(450, 120, n), 100, 900)

external_temp_c = np.random.normal(15, 15, n)
humidity_pct = np.clip(np.random.normal(60, 20, n), 10, 100)

days_since_inspection = np.random.randint(0, 120, n)
days_since_last_maint = np.random.randint(0, 250, n)

# -----------------------------
# Vibrations
# -----------------------------
vibration_x_rms = np.random.normal(2.5, 1.2, n)
vibration_y_rms = np.random.normal(2.3, 1.1, n)
vibration_z_rms = np.random.normal(2.1, 1.0, n)

# -----------------------------
# Temperatures
# -----------------------------
bogie_temp_c = np.random.normal(65, 15, n)
wheel_temp_left_c = np.random.normal(70, 18, n)
wheel_temp_right_c = np.random.normal(70, 18, n)

# -----------------------------
# Risk score (hidden logic)
# -----------------------------
risk_score = (
    0.02 * vibration_x_rms +
    0.02 * vibration_y_rms +
    0.02 * vibration_z_rms +
    0.01 * bogie_temp_c +
    0.005 * wheel_temp_left_c +
    0.005 * wheel_temp_right_c +
    0.01 * days_since_last_maint +
    0.008 * days_since_inspection +
    0.002 * load_tons
)

# Normalización suave
risk_score = (risk_score - risk_score.min()) / (risk_score.max() - risk_score.min())

# -----------------------------
# Fault generation (~15%)
# -----------------------------
fault_prob = 0.05 + 0.4 * risk_score
target_fault = (np.random.rand(n) < fault_prob).astype(int)

# -----------------------------
# Fault type
# -----------------------------
fault_type = np.where(
    target_fault == 0,
    "none",
    np.random.choice(["bearing", "overheat", "wheel_flat", "suspension"], n)
)

# -----------------------------
# Alarm Level
# -----------------------------
alarm_level = np.where(
    risk_score > 0.85, "critical",
    np.where(risk_score > 0.65, "high",
    np.where(risk_score > 0.4, "medium", "low"))
)

# -----------------------------
# Bogie health score
# -----------------------------
bogie_health_score = np.clip(100 - (risk_score * 100), 0, 100)

# -----------------------------
# Final DataFrame
# -----------------------------
df = pd.DataFrame({
    "timestamp": timestamp,
    "bogie_id": bogie_id,
    "operation_mode": operation_mode,
    "track_condition": track_condition,
    "curve_class": curve_class,
    "track_gradient": track_gradient,
    "speed_kmh": speed_kmh,
    "load_tons": load_tons,
    "external_temp_c": external_temp_c,
    "humidity_pct": humidity_pct,
    "days_since_inspection": days_since_inspection,
    "vibration_x_rms": vibration_x_rms,
    "vibration_y_rms": vibration_y_rms,
    "vibration_z_rms": vibration_z_rms,
    "bogie_temp_c": bogie_temp_c,
    "wheel_temp_left_c": wheel_temp_left_c,
    "wheel_temp_right_c": wheel_temp_right_c,
    "bogie_health_score": bogie_health_score,
    "fault_type": fault_type,
    "target_fault": target_fault,
    "alarm_level": alarm_level,
    "days_since_last_maint": days_since_last_maint
})

# -----------------------------
# Save CSV
# -----------------------------
df.to_csv("train_predictive_maintenance_dataset.csv", index=False)

print("Dataset generated: train_predictive_maintenance_dataset.csv")
print("Fault rate:", df["target_fault"].mean())
