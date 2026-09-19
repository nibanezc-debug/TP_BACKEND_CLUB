import mysql.connector
from flask import Flask
from flask import Flask, request, jsonify

app = Flask(__name__)

def conexion_db():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password= 'lanzillotta',
        database= 'CLUB'
    )

@app.route("/")
def holaxd():
    return "hola xd lol"


if __name__ == '__main__':
    app.run(debug=True, port=5000)