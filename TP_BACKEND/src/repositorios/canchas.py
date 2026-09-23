from src.repositorios.db import conexion_db

def buscar_canchas(
    id_deporte=None,
    nombre=None,
    techada=None,
    activa=None,
    limit=10,
    offset=0,
):
  condiciones, parametros = [], []

  if id_deporte is not None:
    condiciones.append('id_deporte = %s')
    parametros.append(id_deporte)
  if nombre:
    condiciones.append('LOWER(nombre) LIKE %s')
    parametros.append(f'%{nombre.lower()}%')
  if techada is not None:
    condiciones.append('techada = %s')
    parametros.append(techada)
  if activa is not None:
    condiciones.append('activa = %s')
    parametros.append(activa)

  where = ' WHERE ' + ' AND '.join(condiciones) if condiciones else ''
  conn = conexion_db()
  try:
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f'SELECT COUNT(*) as total FROM CANCHAS{where}', parametros)
    total = cursor.fetchone()['total']

    sql = (
        f'SELECT id_cancha, nombre, id_deporte, precio_hora, techada, activa FROM'
        f' CANCHAS{where} ORDER BY id_cancha ASC LIMIT %s OFFSET %s'
    )
    cursor.execute(sql, parametros + [limit, offset])
    canchas = cursor.fetchall()

    for c in canchas:
      c['techada'] = bool(c['techada'])
      c['activa'] = bool(c['activa'])

    cursor.close()
    return canchas, total
  finally:
    conn.close()


def guardar_cancha(nombre, id_deporte, precio_hora, techada, activa):
  conn = conexion_db()
  try:
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO CANCHAS (nombre, id_deporte, precio_hora, techada,'
        ' activa) VALUES (%s, %s, %s, %s, %s)',
        [nombre, id_deporte, precio_hora, techada, activa],
    )
    conn.commit()
    cancha_id = cursor.lastrowid
    cursor.close()
    return cancha_id
  finally:
    conn.close()


def obtener_cancha_por_id(cancha_id):
  conn = conexion_db()
  try:
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        'SELECT id_cancha, nombre, id_deporte, precio_hora, techada, activa FROM'
        ' CANCHAS WHERE id_cancha = %s',
        [cancha_id],
    )
    cancha = cursor.fetchone()
    if cancha:
      cancha['techada'] = bool(cancha['techada'])
      cancha['activa'] = bool(cancha['activa'])
    cursor.close()
    return cancha
  finally:
    conn.close()


def actualizar_cancha_db(cancha_id, campos):
  if not campos:
    return
  set_sql = [f'{k} = %s' for k in campos.keys()]
  params = list(campos.values()) + [cancha_id]
  conn = conexion_db()
  try:
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE CANCHAS SET {', '.join(set_sql)} WHERE id_cancha = %s", params
    )
    conn.commit()
    cursor.close()
  finally:
    conn.close()


def eliminar_cancha_db(cancha_id):
  """Ejecuta el DELETE en MySQL para borrar la cancha de la base de datos."""
  conn = conexion_db()
  try:
    cursor = conn.cursor()
    cursor.execute('DELETE FROM CANCHAS WHERE id_cancha = %s', [cancha_id])
    conn.commit()
    cursor.close()
  finally:
    conn.close()


def buscar_canchas_libres(
    start_iso, end_iso, id_deporte=None, techada=None, limit=10, offset=0
):
  sql = """
        SELECT c.id, c.nombre, c.id_deporte, c.precio_hora, c.techada, c.activa
        FROM canchas c
        WHERE c.activa = TRUE
          AND NOT EXISTS (
              SELECT 1 FROM reservas r
              WHERE r.id_cancha = c.id AND r.estado = 'confirmada'
                AND r.fecha_hora_inicio < %s AND r.fecha_hora_fin > %s
          )
    """
  params = [end_iso, start_iso]

  if id_deporte is not None:
    sql += ' AND c.id_deporte = %s'
    params.append(id_deporte)
  if techada is not None:
    sql += ' AND c.techada = %s'
    params.append(techada)

  conn = conexion_db()
  try:
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT COUNT(*) as total FROM ({sql}) AS sub', params)
    total = cursor.fetchone()['total']

    sql += ' ORDER BY c.id ASC LIMIT %s OFFSET %s'
    cursor.execute(sql, params + [limit, offset])
    canchas = cursor.fetchall()

    for c in canchas:
      c['techada'] = bool(c['techada'])
      c['activa'] = bool(c['activa'])

    cursor.close()
    return canchas, total
  finally:
    conn.close()

