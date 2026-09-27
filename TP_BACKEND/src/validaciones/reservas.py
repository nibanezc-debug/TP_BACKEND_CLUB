import re
from datetime import datetime, timedelta, timezone, time


CAMPOS_POST = {
    'id_socio',
    'id_cancha',
    'fecha_hora_inicio',
    'fecha_hora_fin',
}

CAMPOS_PUT_ESTADO = {
    'estado',
}

PARAMETROS_GET = {
    'id_cancha',
    'id_socio',
    'estado',
    'fecha_desde',
    'fecha_hasta',
    '_limit',
    '_offset',
}

ESTADOS_VALIDOS = {
    'confirmada',
    'cancelada',
    'finalizada',
}

PATRON_FECHA_HORA = re.compile(
    r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-03:00$'
)

ZONA_HORARIA = timezone(timedelta(hours=-3))

HORA_APERTURA = time(8, 0, 0)
HORA_CIERRE = time(23, 0, 0)


def id_valido(valor):
    return type(valor) is int and valor > 0


def id_query_valido(valor):
    try:
        numero = int(valor)
        return str(numero) == valor and numero > 0
    except (ValueError, TypeError):
        return False


def fecha_valida(fecha):
    if not isinstance(fecha, str):
        return False

    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def convertir_fecha_hora(valor):
    if not isinstance(valor, str):
        return None

    if not PATRON_FECHA_HORA.match(valor):
        return None

    try:
        return datetime.strptime(
            valor,
            '%Y-%m-%dT%H:%M:%S.%f%z',
        )
    except ValueError:
        return None


def validar_intervalo(fecha_hora_inicio, fecha_hora_fin):
    inicio = convertir_fecha_hora(fecha_hora_inicio)
    fin = convertir_fecha_hora(fecha_hora_fin)

    if inicio is None or fin is None:
        return (
            False,
            'Las fechas y horas deben tener el formato '
            'YYYY-MM-DDTHH:MM:SS.ffffff-03:00',
        )

    if (
        inicio.minute != 0
        or inicio.second != 0
        or inicio.microsecond != 0
        or fin.minute != 0
        or fin.second != 0
        or fin.microsecond != 0
    ):
        return False, 'Las reservas deben comenzar y terminar en horas en punto'

    if inicio >= fin:
        return False, 'fecha_hora_inicio debe ser anterior a fecha_hora_fin'

    if inicio.date() != fin.date():
        return False, 'La reserva no puede atravesar la medianoche'

    if inicio.time() < HORA_APERTURA or fin.time() > HORA_CIERRE:
        return False, 'La reserva debe estar dentro del horario de 08:00 a 23:00'

    duracion = fin - inicio
    horas = duracion.total_seconds() / 3600

    if horas not in (1, 2, 3):
        return False, 'La reserva debe durar entre 1 y 3 horas completas'

    ahora = datetime.now(ZONA_HORARIA)

    if inicio <= ahora:
        return False, 'La reserva debe comenzar en un momento futuro'

    return True, None


def validar_reserva_POST(datos):
    if not isinstance(datos, dict):
        return False, 'El cuerpo debe ser un objeto JSON'

    desconocidos = set(datos) - CAMPOS_POST

    if desconocidos:
        return (
            False,
            f'Campos no permitidos: {", ".join(sorted(desconocidos))}',
        )

    faltantes = CAMPOS_POST - set(datos)

    if faltantes:
        return (
            False,
            f'Faltan campos obligatorios: {", ".join(sorted(faltantes))}',
        )

    if not id_valido(datos['id_socio']):
        return False, 'id_socio debe ser un entero positivo'

    if not id_valido(datos['id_cancha']):
        return False, 'id_cancha debe ser un entero positivo'

    return validar_intervalo(
        datos['fecha_hora_inicio'],
        datos['fecha_hora_fin'],
    )


def validar_reserva_GET(args):
    desconocidos = set(args) - PARAMETROS_GET

    if desconocidos:
        return (
            False,
            f'Parámetros no permitidos: {", ".join(sorted(desconocidos))}',
        )

    if 'id_cancha' in args and not id_query_valido(args['id_cancha']):
        return False, 'id_cancha debe ser un entero positivo'

    if 'id_socio' in args and not id_query_valido(args['id_socio']):
        return False, 'id_socio debe ser un entero positivo'

    if 'estado' in args and args['estado'] not in ESTADOS_VALIDOS:
        return (
            False,
            'estado debe ser confirmada, cancelada o finalizada',
        )

    if 'fecha_desde' in args and not fecha_valida(args['fecha_desde']):
        return False, 'fecha_desde debe tener el formato YYYY-MM-DD'

    if 'fecha_hasta' in args and not fecha_valida(args['fecha_hasta']):
        return False, 'fecha_hasta debe tener el formato YYYY-MM-DD'

    if 'fecha_desde' in args and 'fecha_hasta' in args:
        fecha_desde = datetime.strptime(
            args['fecha_desde'],
            '%Y-%m-%d',
        ).date()

        fecha_hasta = datetime.strptime(
            args['fecha_hasta'],
            '%Y-%m-%d',
        ).date()

        if fecha_desde > fecha_hasta:
            return False, 'fecha_desde debe ser menor o igual a fecha_hasta'

    if '_limit' in args:
        if (
            not args['_limit'].isdigit()
            or not 1 <= int(args['_limit']) <= 100
        ):
            return False, '_limit debe ser un entero entre 1 y 100'

    if '_offset' in args:
        if not args['_offset'].isdigit():
            return False, '_offset debe ser un entero mayor o igual a 0'

    return True, None


def validar_estado_PUT(datos):
    if not isinstance(datos, dict) or not datos:
        return False, 'El cuerpo debe ser un objeto JSON no vacío'

    desconocidos = set(datos) - CAMPOS_PUT_ESTADO

    if desconocidos:
        return (
            False,
            f'Campos no permitidos: {", ".join(sorted(desconocidos))}',
        )

    if 'estado' not in datos:
        return False, 'El campo estado es obligatorio'

    if datos['estado'] not in ESTADOS_VALIDOS:
        return (
            False,
            'estado debe ser confirmada, cancelada o finalizada',
        )

    return True, None
