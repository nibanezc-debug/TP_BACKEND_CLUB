from datetime import datetime, time, timezone, timedelta

GMT_MINUS_3 = timezone(timedelta(hours=-3))

def validar_cancha_GET(args):

    permitidos = {'id_deporte', 'nombre', 'techada', 'activa', '_limit', '_offset'}
    for param in args.keys():
        if param not in permitidos:
            return False, f"Parámetro desconocido o no permitido: '{param}'"

    nombre = args.get('nombre')
    if nombre is not None and not nombre.strip():
        return False, "El parámetro 'nombre' no puede estar vacío"

    id_deporte = args.get('id_deporte')
    if id_deporte is not None:
        try:
            val = int(id_deporte)
            if val <= 0:
                return False, "'id_deporte' debe ser un entero positivo"
        except (ValueError, TypeError):
            return False, "'id_deporte' debe ser un entero válido"

    for bool_param in ['techada', 'activa']:
        val = args.get(bool_param)
        if val is not None and val.lower() not in ['true', 'false']:
            return False, f"El parámetro '{bool_param}' debe ser 'true' o 'false'"

    for pag_param in ['_limit', '_offset']:
        val = args.get(pag_param)
        if val is not None:
            try:
                num = int(val)
                if pag_param == '_limit' and not (1 <= num <= 100):
                    return False, "'_limit' debe estar entre 1 y 100"
                if pag_param == '_offset' and num < 0:
                    return False, "'_offset' debe ser un entero mayor o igual a 0"
            except (ValueError, TypeError):
                return False, f"'{pag_param}' debe ser un entero válido"

    return True, ""


def validar_cancha_POST(datos):

    if not isinstance(datos, dict) or not datos:
        return False, "El cuerpo JSON es obligatorio y no puede estar vacío"

    permitidos = {'nombre', 'id_deporte', 'precio_hora', 'techada', 'activa'}
    for campo in datos.keys():
        if campo not in permitidos:
            return False, f"Campo desconocido en el JSON: '{campo}'"

    obligatorios = ['nombre', 'id_deporte', 'precio_hora']
    for campo in obligatorios:
        if campo not in datos or datos[campo] is None:
            return False, f"El campo '{campo}' es obligatorio"

    nombre = datos['nombre']
    if not isinstance(nombre, str) or not nombre.strip():
        return False, "'nombre' debe ser una cadena de texto no vacía"

    id_deporte = datos['id_deporte']
    if type(id_deporte) is not int or id_deporte <= 0:
        return False, "'id_deporte' debe ser un entero positivo"

    precio_hora = datos['precio_hora']
    if type(precio_hora) is not int or precio_hora <= 0:
        return False, "'precio_hora' debe ser un entero positivo en centavos"

    for campo in ['techada', 'activa']:
        if campo in datos and type(datos[campo]) is not bool:
            return False, f"'{campo}' debe ser un booleano (true o false)"

    return True, ""


def validar_cancha_PATCH(datos):

    if not isinstance(datos, dict) or not datos:
        return False, "El cuerpo JSON no puede estar vacío en una actualización"

    permitidos = {'nombre', 'precio_hora', 'techada', 'activa'}
    for campo in datos.keys():
        if campo not in permitidos:
            return False, f"Campo no permitido o no editable: '{campo}'"

    if 'nombre' in datos:
        nombre = datos['nombre']
        if not isinstance(nombre, str) or not nombre.strip():
            return False, "'nombre' debe ser una cadena de texto no vacía"

    if 'precio_hora' in datos:
        precio_hora = datos['precio_hora']
        if type(precio_hora) is not int or precio_hora <= 0:
            return False, "'precio_hora' debe ser un entero positivo en centavos"

    for campo in ['techada', 'activa']:
        if campo in datos and type(datos[campo]) is not bool:
            return False, f"'{campo}' debe ser un booleano (true o false)"

    return True, ""


def validar_disponibles_GET(args):

    permitidos = {'fecha', 'hora_inicio', 'hora_fin', 'id_deporte', 'techada', '_limit', '_offset'}
    for param in args.keys():
        if param not in permitidos:
            return False, f"Parámetro desconocido: '{param}'"

    obligatorios = ['fecha', 'hora_inicio', 'hora_fin']
    for param in obligatorios:
        if not args.get(param):
            return False, f"El parámetro '{param}' es obligatorio"

    fecha_str = args['fecha']
    hora_ini_str = args['hora_inicio']
    hora_fin_str = args['hora_fin']

    try:
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return False, "'fecha' debe tener el formato YYYY-MM-DD"

    try:
        ini_t = datetime.strptime(hora_ini_str, "%H:%M").time()
        fin_t = datetime.strptime(hora_fin_str, "%H:%M").time()
    except ValueError:
        return False, "'hora_inicio' y 'hora_fin' deben tener el formato HH:MM"

    if ini_t.minute != 0 or ini_t.second != 0 or fin_t.minute != 0 or fin_t.second != 0:
        return False, "Las horas de inicio y fin deben ser en punto (ej: 08:00, 10:00)"

    club_apertura = time(8, 0)
    club_cierre = time(23, 0)

    if ini_t < club_apertura or ini_t >= club_cierre:
        return False, "La hora de inicio debe estar dentro del horario del club (08:00 a 22:00)"
    if fin_t <= club_apertura or fin_t > club_cierre:
        return False, "La hora de fin debe estar dentro del horario del club (09:00 a 23:00)"

    if ini_t >= fin_t:
        return False, "La hora de inicio debe ser anterior a la de fin y no se permite atravesar la medianoche"

    duracion_horas = fin_t.hour - ini_t.hour
    if not (1 <= duracion_horas <= 3):
        return False, "El intervalo debe ser de entre 1 y 3 horas completas"

    dt_inicio = datetime.combine(fecha_obj, ini_t).replace(tzinfo=GMT_MINUS_3)
    ahora_gmt3 = datetime.now(GMT_MINUS_3)

    if dt_inicio <= ahora_gmt3:
        return False, "El inicio de la consulta debe ser posterior al momento actual"

    id_deporte = args.get('id_deporte')
    if id_deporte is not None:
        try:
            val = int(id_deporte)
            if val <= 0:
                return False, "'id_deporte' debe ser un entero positivo"
        except (ValueError, TypeError):
            return False, "'id_deporte' debe ser un entero válido"

    techada = args.get('techada')
    if techada is not None and techada.lower() not in ['true', 'false']:
        return False, "'techada' debe ser 'true' o 'false'"

    return True, ""


def armar_intervalo_iso(fecha_str, hora_inicio_str, hora_fin_str):

    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    ini_t = datetime.strptime(hora_inicio_str, "%H:%M").time()
    fin_t = datetime.strptime(hora_fin_str, "%H:%M").time()

    dt_inicio = datetime.combine(fecha_obj, ini_t).replace(tzinfo=GMT_MINUS_3)
    dt_fin = datetime.combine(fecha_obj, fin_t).replace(tzinfo=GMT_MINUS_3)

    return dt_inicio.isoformat(), dt_fin.isoformat()