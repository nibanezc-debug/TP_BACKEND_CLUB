import mysql.connector
from flask import Flask, request, jsonify
from src.rutas.deportes import mostrar_deportes_bp
from src.repositorios.db import conexion_db

app = Flask(__name__)

app.register_blueprint(mostrar_deportes_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000) 