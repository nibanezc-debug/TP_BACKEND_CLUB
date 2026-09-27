from datetime import datetime, timedelta, timezone

from src.repositorios import reservas as repo_reservas
from src.repositorios import socios as repo_socios
from src.repositorios import canchas as repo_canchas


ZONA_HORARIA = timezone(timedelta(hours=-3))


def convertir_fecha_hora(valor):
    return datetime.strptime(
        valor,
        '%Y-%m-%dT%H:%M:%S.%f%z',
    )


def crear_reserva(datos):
    id_socio = datos['id_socio']
    id_cancha = datos['id_cancha']
    fecha_hora_inicio = datos['fecha_hora_inicio']
    fecha_hora_fin = datos['fecha_hora_fin']

    socio = repo_socios.obtener_socio_por_id(id_socio)

    if socio is None:
        return None, 'SOCIO_NO_ENCONTRADO'

    if not socio['activo']:
        return None, 'SOCIO_INACTIVO'

    cancha = repo_canchas.obtener_cancha_por_id(id_cancha)

    if cancha is None:
        return None, 'CANCHA_NO_ENCONTRADA'

    if not cancha['activa']:
        return None, 'CANCHA_INACTIVA'

    precio_hora = cancha['precio_hora']

    if type(precio_hora) is not int or precio_hora <= 0:
        return None, 'TARIFA_INVALIDA'

    if repo_reservas.existe_superposicion_cancha(
        id_cancha,
        fecha_hora_inicio,
        fecha_hora_fin,
    ):
        return None, 'CANCHA_OCUPADA'

    if repo_reservas.existe_superposicion_socio(
        id_socio,
        fecha_hora_inicio,
        fecha_hora_fin,
    ):
        return None, 'SOCIO_OCUPADO'

    inicio = convertir_fecha_hora(fecha_hora_inicio)
    fin = convertir_fecha_hora(fecha_hora_fin)

    duracion_horas = int(
        (fin - inicio).total_seconds() / 3600
    )

    precio_total = duracion_horas * precio_hora

    id_reserva = repo_reservas.guardar_reserva(
        id_socio,
        id_cancha,
        fecha_hora_inicio,
        fecha_hora_fin,
        precio_hora,
        precio_total,
    )

    return id_reserva, None


def cambiar_estado_reserva(id_reserva, nuevo_estado):
    reserva = repo_reservas.obtener_reserva_por_id(id_reserva)

    if reserva is None:
        return None, 'RESERVA_NO_ENCONTRADA'

    estado_actual = reserva['estado']

    # Repetir el estado actual es válido y no modifica nada.
    if estado_actual == nuevo_estado:
        return reserva, None

    # Una reserva cancelada o finalizada ya no puede cambiar.
    if estado_actual in ('cancelada', 'finalizada'):
        return None, 'TRANSICION_INVALIDA'

    ahora = datetime.now(ZONA_HORARIA)

    fecha_inicio = convertir_fecha_hora(
        reserva['fecha_hora_inicio']
    )

    fecha_fin = convertir_fecha_hora(
        reserva['fecha_hora_fin']
    )

    if nuevo_estado == 'cancelada':
        if ahora >= fecha_inicio:
            return None, 'CANCELACION_FUERA_DE_TERMINO'

    elif nuevo_estado == 'finalizada':
        if ahora < fecha_fin:
            return None, 'FINALIZACION_ANTICIPADA'

    else:
        return None, 'TRANSICION_INVALIDA'

    repo_reservas.actualizar_estado_reserva(
        id_reserva,
        nuevo_estado,
    )

    reserva['estado'] = nuevo_estado

    return reserva, None
