import mysql.connector

#pre:
#post: abre la conexion la base de datos

def conexion_db():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password= 'lanzillotta',
        database= 'CLUB'
    )
