import sqlite3
import os
import pickle
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Asegúrate de crear la carpeta data si no existe para evitar errores
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True) 

DB_PATH = os.path.join(BASE_DIR, 'data/advertising.db')
MODEL_PATH = os.path.join(BASE_DIR, 'data/modelo_advertising.pkl')

# Variable global para el modelo
model = None

# --- MODELOS DE DATOS (PYDANTIC) ---
# Esto sustituye tus validaciones manuales de "if 'data' not in data..."

class PredictRequest(BaseModel):
    # Esperamos una lista de listas de floats: [[100.0, 20.0, 30.0]]
    data: List[List[float]]

class IngestRequest(BaseModel):
    # Esperamos una lista de listas de floats (incluyendo sales): [[100.0, 20.0, 30.0, 500.0]]
    data: List[List[float]]

# --- FUNCIONES AUXILIARES ---

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"No se encuentra el archivo de base de datos en {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- LIFESPAN (Ciclo de vida) ---
# Esta es la forma "Pro" de cargar cosas al inicio en FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de arranque (Startup)
    global model
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            print("✅ Modelo cargado exitosamente.")
        else:
            print(f"⚠️ Aviso: No se encontró {MODEL_PATH}. El endpoint /predict fallará hasta que entrenes.")
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
    
    yield # Aquí corre la aplicación
    
    # Lógica de apagado (Shutdown) - opcional
    print("Apagando aplicación...")

# --- INICIALIZAR APP ---
app = FastAPI(title="Advertising Sales API", lifespan=lifespan)

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Advertising API is running"}

# 1. Predicción (/predict)
# CAMBIO: Usamos POST porque estamos enviando datos (JSON body)
@app.post("/predict")
def predict(payload: PredictRequest):
    global model
    if not model:
        raise HTTPException(status_code=500, detail="El modelo no está cargado o no existe.")
    
    try:
        # FastAPI ya validó que payload.data es una lista de floats
        input_data = payload.data
        pred = model.predict(input_data)
        
        # Devolvemos la primera predicción (igual que en tu flask)
        return {"prediction": float(pred[0])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

# 2. Ingesta de datos (/ingest)
@app.post("/ingest")
def ingest_data(payload: IngestRequest):
    conn = None
    try:
        conn = get_db_connection()
        # Nota: Asegúrate de que la tabla 'campañas' exista en tu DB
        query = "INSERT INTO campañas (TV, radio, newspaper, sales) VALUES (?, ?, ?, ?)"
        
        # Iteramos sobre los datos validados
        for registro in payload.data:
            # Pydantic asegura que registro es una lista de floats
            if len(registro) != 4:
                 raise HTTPException(status_code=400, detail=f"Cada registro debe tener 4 valores. Recibido: {registro}")
            
            conn.execute(query, tuple(registro))
        
        conn.commit()
        return {"message": "Datos ingresados correctamente"}

    except Exception as e:
        print(f"!!! ERROR EN INGEST: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

# 3. Reentrenar (/retrain)
@app.post("/retrain")
def retrain():
    global model
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT TV, radio, newspaper, sales FROM campañas")
        rows = cursor.fetchall()
        
        if not rows:
            raise HTTPException(status_code=400, detail="No hay datos en la DB para entrenar")
            
        X = []
        y = []
        for row in rows:
            val_tv = float(row[0])
            val_radio = float(row[1])
            val_news = float(row[2])
            val_sales = float(row[3])
            
            X.append([val_tv, val_radio, val_news])
            y.append(val_sales)
        
        print("🔄 Creando y entrenando modelo nuevo...")
        new_model = LinearRegression()
        new_model.fit(X, y)
        
        # Guardar en disco
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(new_model, f)
        
        # Actualizar en memoria
        model = new_model
            
        return {"message": "Modelo reentrenado y actualizado correctamente."}
        
    except Exception as e:
        print(f"!!! ERROR EN RETRAIN: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

# Para correrlo:
# uvicorn main:app --reload