from src.repositorios.db import conexion_db


COLUMNAS = (
    'id_reserva AS id, '
    'id_socio, '
    'id_cancha, '
    'fecha_inicio AS fecha_hora_inicio, '
    'fecha_fin AS fecha_hora_fin, '
    'estado, '
    'tarifa_historica AS precio_hora, '
    'total AS precio_total'
)


def buscar_reservas(
    id_cancha=None,
    id_socio=None,
    estado=None,
    fecha_desde=None,
    fecha_hasta=None,
    limit=10,
    offset=0,
):
    condiciones = []
    parametros = []

    if id_cancha is not None:
        condiciones.append('id_cancha = %s')
        parametros.append(id_cancha)

    if id_socio is not None:
        condiciones.append('id_socio = %s')
        parametros.append(id_socio)

    if estado is not None:
        condiciones.append('estado = %s')
        parametros.append(estado)

    if fecha_desde is not None:
        condiciones.append('LEFT(fecha_inicio, 10) >= %s')
        parametros.append(fecha_desde)

    if fecha_hasta is not None:
        condiciones.append('LEFT(fecha_inicio, 10) <= %s')
        parametros.append(fecha_hasta)

    where = (
        ' WHERE ' + ' AND '.join(condiciones)
        if condiciones
        else ''
    )

    conn = conexion_db()

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            f'SELECT COUNT(*) AS total FROM RESERVAS{where}',
            parametros,
        )

        total = cursor.fetchone()['total']

        cursor.execute(
            f'''
            SELECT {COLUMNAS}
            FROM RESERVAS
            {where}
            ORDER BY id_reserva ASC
            LIMIT %s OFFSET %s
            ''',
            parametros + [limit, offset],
        )

        reservas = cursor.fetchall()

        cursor.close()

        return reservas, total

    finally:
        conn.close()


def obtener_reserva_por_id(id_reserva):
    conn = conexion_db()

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            f'''
            SELECT {COLUMNAS}
            FROM RESERVAS
            WHERE id_reserva = %s
            ''',
            [id_reserva],
        )

        reserva = cursor.fetchone()

        cursor.close()

        return reserva

    finally:
        conn.close()


def existe_superposicion_cancha(
    id_cancha,
    fecha_hora_inicio,
    fecha_hora_fin,
):
    conn = conexion_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT 1
            FROM RESERVAS
            WHERE id_cancha = %s
              AND estado = 'confirmada'
              AND fecha_inicio < %s
              AND fecha_fin > %s
            LIMIT 1
            ''',
            [
                id_cancha,
                fecha_hora_fin,
                fecha_hora_inicio,
            ],
        )

        resultado = cursor.fetchone()

        cursor.close()

        return resultado is not None

    finally:
        conn.close()


def existe_superposicion_socio(
    id_socio,
    fecha_hora_inicio,
    fecha_hora_fin,
):
    conn = conexion_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT 1
            FROM RESERVAS
            WHERE id_socio = %s
              AND estado = 'confirmada'
              AND fecha_inicio < %s
              AND fecha_fin > %s
            LIMIT 1
            ''',
            [
                id_socio,
                fecha_hora_fin,
                fecha_hora_inicio,
            ],
        )

        resultado = cursor.fetchone()

        cursor.close()

        return resultado is not None

    finally:
        conn.close()


def guardar_reserva(
    id_socio,
    id_cancha,
    fecha_hora_inicio,
    fecha_hora_fin,
    precio_hora,
    precio_total,
):
    conn = conexion_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO RESERVAS (
                id_socio,
                id_cancha,
                fecha_inicio,
                fecha_fin,
                tarifa_historica,
                total,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, 'confirmada')
            ''',
            [
                id_socio,
                id_cancha,
                fecha_hora_inicio,
                fecha_hora_fin,
                precio_hora,
                precio_total,
            ],
        )

        conn.commit()

        id_reserva = cursor.lastrowid

        cursor.close()

        return id_reserva

    finally:
        conn.close()


def actualizar_estado_reserva(id_reserva, nuevo_estado):
    conn = conexion_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            '''
            UPDATE RESERVAS
            SET estado = %s
            WHERE id_reserva = %s
            ''',
            [
                nuevo_estado,
                id_reserva,
            ],
        )

        conn.commit()

        cursor.close()

    finally:
        conn.close()
