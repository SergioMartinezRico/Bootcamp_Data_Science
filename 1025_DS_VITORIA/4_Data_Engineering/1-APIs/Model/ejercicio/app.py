# IMPORT
import sqlite3
import os
from flask import Flask, jsonify, request
import pickle
from sklearn.linear_model import LinearRegression

# configurar rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data/advertising.db')
MODEL_PATH = os.path.join(BASE_DIR, 'data/modelo_advertising.pkl')

# conexion a db
def get_db_connection():
  if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"No se encuentra el archivo {DB_PATH}")
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn

#cargar modelo pkl
try:
  with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
  print("Modelo cargado")
except FileNotFoundError:
    print("ERROR: No se encontró el archivo .pkl. Verifica la ruta.")
    model = None    
#inicializar app
app = Flask(__name__)
app.config["DEBUG"] = True #debug true para pruebas

@app.route("/", methods = ["GET"])
def home():
  return "Home"


# 1. Ofrezca la predicción de ventas a partir de todos los valores de gastos en publicidad. (/predict)
@app.route("/predict", methods = ["GET"])
def predict():
  # comprobar si hay modelo
  if not model:
    return jsonify({"error": "El modelo no está cargado"}), 500
  
  data = request.get_json()
  
  # Validamos que venga la estructura correcta del test
  if not data or 'data' not in data:
    return jsonify({"error": "Falta el campo 'data'"}), 400
  
  try:
    # El test envía [[100, 100, 200]]
    input_data = data['data'] 
    pred = model.predict(input_data)
    
    # Devolvemos la predicción
    return jsonify({"prediction": float(pred[0])}), 200
  except Exception as e:
    return jsonify ({"error": str(e)}), 500
  
# 2. Un endpoint para almacenar nuevos registros en la base de datos que deberás crear previamente.(/ingest)

@app.route("/ingest", methods=["POST"])
def ingest_data():
    data = request.get_json(force=True, silent=True)
    if not data or 'data' not in data:
        return jsonify({"error": "Falta el campo 'data'"}), 400

    try:
        conn = get_db_connection()
        query = "INSERT INTO campañas (TV, radio, newspaper, sales) VALUES (?, ?, ?, ?)"
        
        for registro in data['data']:
            conn.execute(query, (
                registro[0], 
                registro[1], 
                registro[2], 
                registro[3]
            ))
        conn.commit()
        return jsonify({'message': 'Datos ingresados correctamente'}), 200
        
    except Exception as e:
        
        print(f"!!! ERROR EN INGEST: {e}") 
        return jsonify({"error": str(e)}), 500
    finally:
         if 'conn' in locals(): conn.close()

# 3. Posibilidad de reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan. (/retrain)

@app.route("/retrain", methods=["POST"])
def retrain():
    # Usamos global para actualizar la variable 'model' que usa /predict
    global model

    try:
        conn = get_db_connection()
        
        cursor = conn.execute("SELECT TV, radio, newspaper, sales FROM campañas")
        rows = cursor.fetchall()
        
        if not rows:
            return jsonify({"error": "No hay datos para entrenar"}), 400
            
        X = []
        y = []
        for row in rows:
            # Usamos índices (0,1,2,3) para evitar problemas con nombres de columnas
            val_tv = float(row[0])
            val_radio = float(row[1])
            val_news = float(row[2])
            val_sales = float(row[3])
            
            X.append([val_tv, val_radio, val_news])
            y.append(val_sales)
        
        # --- AQUÍ ESTÁ LA SOLUCIÓN ---
        # No usamos 'model.fit(X,y)' porque el objeto 'model' viene del archivo .pkl
        # y tiene versiones incompatibles
        # En su lugar, creamos un NUEVO modelo limpio.
        
        print("Creando y entrenando un modelo nuevo desde cero...")
        new_model = LinearRegression()
        new_model.fit(X, y)
        
        # Sobrescribimos el archivo .pkl con el modelo nuevo que SÍ funciona
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(new_model, f)
        
        # Actualizamos el modelo en memoria
        model = new_model
            
        return jsonify({'message': 'Modelo reentrenado correctamente.'}), 200
        
    except Exception as e:
        print(f"!!! ERROR EN RETRAIN: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=8000)