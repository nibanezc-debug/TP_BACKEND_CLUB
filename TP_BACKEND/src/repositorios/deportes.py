from src.repositorios.db import conexion_db


def obtener_deporte_por_id(id_deporte):
    conexion = conexion_db()
    cursor = conexion.cursor(dictionary=True)

    query = "SELECT id_deporte, deporte FROM DEPORTES WHERE id_deporte = %s"
    cursor.execute(query, (id_deporte,))
    deporte = cursor.fetchone()

    cursor.close()
    conexion.close()
    return deporte


def listar_deportes():
    conexion = conexion_db()
    cursor = conexion.cursor(dictionary=True)

    query = "SELECT id_deporte, deporte FROM DEPORTES"
    cursor.execute(query)
    deportes = cursor.fetchall()

    cursor.close()
    conexion.close()
    return deportes


def crear_deporte(nombre_deporte):
    conexion = conexion_db()
    cursor = conexion.cursor()

    query = "INSERT INTO DEPORTES (deporte) VALUES (%s)"
    cursor.execute(query, (nombre_deporte,))
    conexion.commit()

    id_nuevo = cursor.lastrowid
    cursor.close()
    conexion.close()
    return id_nuevo


def eliminar_deporte(id_deporte):
    conexion = conexion_db()
    cursor = conexion.cursor()

    query = "DELETE FROM DEPORTES WHERE id_deporte = %s"
    cursor.execute(query, (id_deporte,))
    conexion.commit()

    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    return filas_afectadas > 0