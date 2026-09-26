import re

# algo@algo.algo, sin espacios
PATRON_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

CAMPOS_POST = {'nombre', 'email'}
CAMPOS_PATCH = {'nombre', 'email', 'activo'}
PARAMETROS_GET = {'nombre', 'activo', '_limit', '_offset'}


def nombre_valido(nombre):
    return isinstance(nombre, str) and nombre.strip() != ''


def email_valido(email):
    return isinstance(email, str) and PATRON_EMAIL.match(email.strip()) is not None


def validar_socio_POST(datos):
    if not isinstance(datos, dict):
        return False, 'El cuerpo debe ser un objeto JSON'

    desconocidos = set(datos) - CAMPOS_POST
    if desconocidos:
        return False, f'Campos no permitidos: {", ".join(sorted(desconocidos))}'

    if 'nombre' not in datos or 'email' not in datos:
        return False, 'Los campos nombre y email son obligatorios'

    if not nombre_valido(datos['nombre']):
        return False, 'El nombre no puede estar vacío'

    if not email_valido(datos['email']):
        return False, 'El email no tiene un formato válido'

    return True, None


def validar_socio_PATCH(datos):
    if not isinstance(datos, dict) or not datos:
        return False, 'El cuerpo debe ser un objeto JSON no vacío'

    desconocidos = set(datos) - CAMPOS_PATCH
    if desconocidos:
        return False, f'Campos no permitidos: {", ".join(sorted(desconocidos))}'

    if 'nombre' in datos and not nombre_valido(datos['nombre']):
        return False, 'El nombre no puede estar vacío'

    if 'email' in datos and not email_valido(datos['email']):
        return False, 'El email no tiene un formato válido'

    # "is True / is False" para que 1, 0 o "true" (texto) no se cuelen
    if 'activo' in datos and datos['activo'] is not True and datos['activo'] is not False:
        return False, 'El campo activo debe ser true o false'

    return True, None


def validar_socio_GET(args):
    desconocidos = set(args) - PARAMETROS_GET
    if desconocidos:
        return False, f'Parámetros no permitidos: {", ".join(sorted(desconocidos))}'

    if 'nombre' in args and not args['nombre'].strip():
        return False, 'El filtro nombre no puede estar vacío'

    if 'activo' in args and args['activo'] not in ('true', 'false'):
        return False, 'El filtro activo solo admite true o false'

    if '_limit' in args:
        if not args['_limit'].isdigit() or not 1 <= int(args['_limit']) <= 100:
            return False, '_limit debe ser un entero entre 1 y 100'

    if '_offset' in args and not args['_offset'].isdigit():
        return False, '_offset debe ser un entero mayor o igual a 0'

    return True, None
