# IMPORT
import sqlite3
import os
from flask import Flask, jsonify, request
# conexion a db
db_name = "books.db"

def get_db_connection():
  if not os.path.exists(db_name):
    raise FileNotFoundError(f"No se encuentra el archivo {db_name}")
  conn = sqlite3.connect(db_name)
  conn.row_factory = sqlite3.Row
  return conn

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": f"Conectado a {db_name}"})

# 0.Ruta para obtener todos los libros

@app.route("/api/v1/books", methods=["GET"])
def get_all_books():
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM books")
        books = [dict(row) for row in cursor.fetchall()]
        return jsonify({"success": True, "count": len(books), "data": books}), 200
    except sqlite3.OperationalError as e:
        return jsonify({
            "error": "Error de Base de Datos", 
            "message": "Es probable que la tabla books o las columnas no existan.",
            "detail": str(e)
        }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if "conn" in locals(): conn.close()
# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route("/api/v1/stats/authors", methods=["GET"])
def get_author_stats():
    try:
        conn = get_db_connection()
        
        query = """
            SELECT author, COUNT(*) as total_books 
            FROM books 
            GROUP BY author 
            ORDER BY total_books DESC
        """
        cursor = conn.execute(query)
        stats = [dict(row) for row in cursor.fetchall()]
        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if "conn" in locals(): conn.close()
# 2.Ruta para obtener los libros de un autor
@app.route("/api/v1/books/search", methods=["GET"])
def get_books_by_author():
    author_name = request.args.get("author")
    if not author_name:
        return jsonify({"error": "Falta parámetro author"}), 400

    try:
        conn = get_db_connection()
        query = "SELECT * FROM books WHERE author LIKE ?"
        cursor = conn.execute(query, ("%" + author_name + "%",))
        books = [dict(row) for row in cursor.fetchall()]
        return jsonify({"success": True, "data": books}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if "conn" in locals(): conn.close()
# 3.Ruta para añadir un libro
@app.route("/api/v1/books", methods=["POST"])
def add_book():
    new_book = request.get_json()
    
    if not new_book or "title" not in new_book or "author" not in new_book:
        return jsonify({"error": "Faltan datos requeridos (title, author)"}), 400
    
    try:
        conn = get_db_connection()
        query = "INSERT INTO books (title, author, published) VALUES (?, ?, ?)"
        cursor = conn.execute(query, (
            new_book["title"], 
            new_book["author"], 
            new_book.get("published")
        ))
        conn.commit()
        return jsonify({"success": True, "id": cursor.lastrowid}), 201
    except Exception as e:
        if "conn" in locals(): conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if "conn" in locals(): conn.close()

if __name__ == "__main__":
    
    if not os.path.exists(db_name):
        print(f"⚠ ADVERTENCIA: No encuentro {db_name}. Asegúrate de poner el archivo en la carpeta.")
    
    app.run(debug=True, port=5000)