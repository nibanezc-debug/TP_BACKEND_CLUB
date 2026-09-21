def datos_validos_cancha(nombre, id_deporte, precio_hora, techada, activa):
    valido = True

    if not nombre or id_deporte is None or precio_hora is None:
        valido = False
    if not isinstance(nombre, str) or not nombre.strip():
        valido = False
    if type(id_deporte) is not int or id_deporte <= 0:
        valido = False
    if type(precio_hora) is not int or precio_hora <= 0:
        valido = False
    if  (techada is not True) and (techada is not False):
        valido = False
    if  (activa is not True) and (activa is not False):
        valido = False

    return valido