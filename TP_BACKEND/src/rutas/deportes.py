from flask import Flask, request, jsonify,Blueprint
from src.validaciones.db import conexion_db

mostrar_deportes_bp = Blueprint('mostrar_deportes_bp', __name__)

@mostrar_deportes_bp.route('/deportes', methods=['GET'])
def mostrar_deportes():
    conn = conexion_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM DEPORTES;")
    resultado = cursor.fetchall()
  
    cursor.close()
    conn.close()

    return jsonify(resultado)