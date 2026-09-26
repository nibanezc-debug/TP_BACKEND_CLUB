from src.repositorios.db import conexion_db

# Devolvemos "id" (y no "id_socio") porque así lo pide el swagger.
COLUMNAS = 'id_socio AS id, nombre, email, activo'


def _formatear(socio):
    # MySQL guarda los booleanos como 0/1; los pasamos a True/False
    socio['activo'] = bool(socio['activo'])
    return socio


def buscar_socios(nombre=None, activo=None, limit=10, offset=0):
    condiciones, parametros = [], []

    if nombre:
        condiciones.append('LOWER(nombre) LIKE %s')
        parametros.append(f'%{nombre.lower()}%')
    if activo is not None:
        condiciones.append('activo = %s')
        parametros.append(activo)

    where = ' WHERE ' + ' AND '.join(condiciones) if condiciones else ''

    conn = conexion_db()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(f'SELECT COUNT(*) AS total FROM SOCIOS{where}', parametros)
        total = cursor.fetchone()['total']

        cursor.execute(
            f'SELECT {COLUMNAS} FROM SOCIOS{where} ORDER BY id_socio ASC LIMIT %s OFFSET %s',
            parametros + [limit, offset],
        )
        socios = [_formatear(s) for s in cursor.fetchall()]

        cursor.close()
        return socios, total
    finally:
        conn.close()


def obtener_socio_por_id(id_socio):
    conn = conexion_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT {COLUMNAS} FROM SOCIOS WHERE id_socio = %s', [id_socio])
        socio = cursor.fetchone()
        cursor.close()
        return _formatear(socio) if socio else None
    finally:
        conn.close()


def obtener_socio_por_email(email):
    conn = conexion_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT {COLUMNAS} FROM SOCIOS WHERE email = %s', [email])
        socio = cursor.fetchone()
        cursor.close()
        return _formatear(socio) if socio else None
    finally:
        conn.close()


def guardar_socio(nombre, email):
    conn = conexion_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO SOCIOS (nombre, email, activo) VALUES (%s, %s, TRUE)',
            [nombre, email],
        )
        conn.commit()
        id_socio = cursor.lastrowid
        cursor.close()
        return id_socio
    finally:
        conn.close()


def actualizar_socio_db(id_socio, campos):
    # "campos" solo puede traer nombre, email o activo: eso ya lo
    # controló la capa de servicios antes de llegar acá.
    if not campos:
        return
    set_sql = [f'{columna} = %s' for columna in campos]
    parametros = list(campos.values()) + [id_socio]

    conn = conexion_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE SOCIOS SET {', '.join(set_sql)} WHERE id_socio = %s", parametros
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()
