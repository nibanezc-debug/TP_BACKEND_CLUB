from flask import Blueprint, jsonify
from src.repositorios.db import conexion_db

mostrar_deportes_bp = Blueprint('mostrar_deportes_bp', __name__)

@mostrar_deportes_bp.route('/deportes', methods=['GET'])
def mostrar_deportes():
    conn = None
    cursor = None
    try:
        conn = conexion_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_deporte, deporte FROM DEPORTES;")
        resultado = cursor.fetchall()

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"mensaje": "Error al obtener los deportes", "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()