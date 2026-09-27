from flask import Blueprint, jsonify, request

from src.repositorios import reservas as repo_reservas
from src.servicios import reservas as serv_reservas
from src.validaciones import reservas as valid_reservas
from src.servicios.paginacion import construir_links


reservas_bp = Blueprint('reservas_bp', __name__)


def error(code, message, status):
    return jsonify({
        'errors': [
            {
                'code': code,
                'message': message,
                'level': 'error',
            }
        ]
    }), status


@reservas_bp.route('/reservas', methods=['GET'])
def get_reservas():
    es_valido, mensaje = valid_reservas.validar_reserva_GET(
        request.args
    )

    if not es_valido:
        return error('BAD_REQUEST', mensaje, 400)

    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))

    id_cancha = request.args.get('id_cancha')
    id_socio = request.args.get('id_socio')
    estado = request.args.get('estado')
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')

    if id_cancha is not None:
        id_cancha = int(id_cancha)

    if id_socio is not None:
        id_socio = int(id_socio)

    reservas, total = repo_reservas.buscar_reservas(
        id_cancha=id_cancha,
        id_socio=id_socio,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limit=limit,
        offset=offset,
    )

    filtros = {
        clave: valor
        for clave, valor in request.args.items()
        if clave not in ('_limit', '_offset')
    }

    return jsonify({
        'reservas': reservas,
        '_links': construir_links(
            request.base_url,
            filtros,
            total,
            limit,
            offset,
        ),
    }), 200


@reservas_bp.route('/reservas', methods=['POST'])
def post_reserva():
    datos = request.get_json(silent=True)

    es_valido, mensaje = valid_reservas.validar_reserva_POST(
        datos
    )

    if not es_valido:
        return error('BAD_REQUEST', mensaje, 400)

    id_reserva, problema = serv_reservas.crear_reserva(datos)

    if problema == 'SOCIO_NO_ENCONTRADO':
        return error(
            'NOT_FOUND',
            'Socio no encontrado',
            404,
        )

    if problema == 'CANCHA_NO_ENCONTRADA':
        return error(
            'NOT_FOUND',
            'Cancha no encontrada',
            404,
        )

    if problema == 'SOCIO_INACTIVO':
        return error(
            'CONFLICT',
            'El socio está inactivo',
            409,
        )

    if problema == 'CANCHA_INACTIVA':
        return error(
            'CONFLICT',
            'La cancha está inactiva',
            409,
        )

    if problema == 'CANCHA_OCUPADA':
        return error(
            'CONFLICT',
            'La cancha no está disponible en ese horario',
            409,
        )

    if problema == 'SOCIO_OCUPADO':
        return error(
            'CONFLICT',
            'El socio ya tiene una reserva en ese horario',
            409,
        )

    if problema == 'TARIFA_INVALIDA':
        return error(
            'CONFLICT',
            'La cancha tiene una tarifa inválida',
            409,
        )

    return jsonify({
        'id': id_reserva,
    }), 201


@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def get_reserva(id):
    reserva = repo_reservas.obtener_reserva_por_id(id)

    if reserva is None:
        return error(
            'NOT_FOUND',
            'Reserva no encontrada',
            404,
        )

    return jsonify(reserva), 200


@reservas_bp.route('/reservas/<int:id>/estado', methods=['PUT'])
def put_estado_reserva(id):
    datos = request.get_json(silent=True)

    es_valido, mensaje = valid_reservas.validar_estado_PUT(
        datos
    )

    if not es_valido:
        return error('BAD_REQUEST', mensaje, 400)

    reserva, problema = serv_reservas.cambiar_estado_reserva(
        id,
        datos['estado'],
    )

    if problema == 'RESERVA_NO_ENCONTRADA':
        return error(
            'NOT_FOUND',
            'Reserva no encontrada',
            404,
        )

    if problema == 'TRANSICION_INVALIDA':
        return error(
            'CONFLICT',
            'La transición de estado no está permitida',
            409,
        )

    if problema == 'CANCELACION_FUERA_DE_TERMINO':
        return error(
            'CONFLICT',
            'La reserva ya comenzó y no puede cancelarse',
            409,
        )

    if problema == 'FINALIZACION_ANTICIPADA':
        return error(
            'CONFLICT',
            'La reserva todavía no finalizó',
            409,
        )

    return jsonify(reserva), 200
