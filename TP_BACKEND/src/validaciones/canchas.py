def datos_validos_cancha_POST_PATCH(nombre=None, id_deporte=None, precio_hora=None, techada=None, activa=None):

    if nombre is not None:
        if not isinstance(nombre, str) or not nombre.strip():
            return False

    if id_deporte is not None:
        try:
            val_deporte = int(id_deporte)
            if val_deporte <= 0:
                return False
        except (ValueError, TypeError):
            return False

    if precio_hora is not None:
        if type(precio_hora) is not int or precio_hora <= 0:
            return False

    if techada is not None:
        if techada is not True and techada is not False:
            return False

    if activa is not None:
        if activa is not True and activa is not False:
            return False

    return True

def datos_validos_cancha_GET(nombre=None, id_deporte_str=None, techada_str=None, activa_str=None):

    if nombre is not None:
        if not isinstance(nombre, str) or not nombre.strip():
            return False

    if id_deporte_str is not None:
        try:
            id_deporte = int(id_deporte_str)
            if type(id_deporte) is not int or id_deporte <= 0:
                return False
        except (ValueError, TypeError):
            return False

    if techada_str is not None:
        if (techada_str and techada_str.lower() != "true") and (techada_str and techada_str.lower() != "false"):
            return False

    if activa_str is not None:
        if (activa_str and activa_str.lower() != "true") and (activa_str and activa_str.lower() != "false"):
            return False

    return True