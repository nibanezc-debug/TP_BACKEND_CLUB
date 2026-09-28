from flask import Blueprint, jsonify, request

from src.repositorios import canchas as repo_canchas
from src.servicios import canchas as serv_canchas
from src.servicios.paginacion import construir_links
from src.validaciones import canchas as valid_canchas

canchas_bp = Blueprint('canchas_bp', __name__)


def error(code, message, status):
    return jsonify({
        'errors': [{'code': code, 'message': message, 'level': 'error'}]
    }), status


def _bool_query(nombre):
    valor = request.args.get(nombre)
    return None if valor is None else valor == 'true'


def _id_deporte_query():
    valor = request.args.get('id_deporte')
    return None if valor is None else int(valor)


def _filtros_para_links():
    return {
        k: v for k, v in request.args.items()
        if k not in ('_limit', '_offset')
    }


@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():
    es_valido, mensaje = valid_canchas.validar_cancha_GET(request.args)
    if not es_valido:
        return error('BAD_REQUEST', mensaje, 400)

    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))

    canchas, total = repo_canchas.buscar_canchas(
        _id_deporte_query(),
        request.args.get('nombre'),
        _bool_query('techada'),
        _bool_query('activa'),
        limit,
        offset,
    )

    if not canchas:
        return '', 204

    return jsonify({
        'canchas': canchas,
        '_links': construir_links(
            request.base_url, _filtros_para_links(), total, limit, offset
        ),
    }), 200


@canchas_bp.route('/canchas', methods=['POST'])
def post_cancha():
    datos = request.get_json(silent=True)

    es_valido, mensaje = valid_canchas.validar_cancha_POST(datos)
    if not es_valido:
        return error('BAD_REQUEST', mensaje, 400)

    id_cancha, problema = serv_canchas.crear_cancha(datos)
    if problema == 'DEPORTE_NO_ENCONTRADO':
        return error('NOT_FOUND', 'Deporte no encontrado', 404)

    return jsonify({'id': id_cancha}), 201


@canchas_bp.route('/canchas/<int:id>', methods=['GET'])
def get_cancha(id):
    cancha = repo_canchas.obtener_cancha_por_id(id)
    if not cancha:
        return error('NOT_FOUND', 'Cancha no encontrada', 404)
    return jsonify(cancha), 200


@canchas_bp.route('/canchas/<int:id>', methods=['PATCH'])
def patch_cancha(id):
    if repo_canchas.obtener_cancha_por_id(id) is None:
        return error('NOT_FOUND', 'Cancha no encontrada', 404)

    datos = request.get_json(silent=True)

    es_valido, mensaje = valid_canchas.validar_cancha_PATCH(datos)
    if not es_valido:
        return error('BAD_REQUEST', mensaje, 400)

    cancha, problema = serv_canchas.actualizar_cancha(id, datos)
    if problema == 'CANCHA_NO_ENCONTRADA':
        return error('NOT_FOUND', 'Cancha no encontrada', 404)

    return jsonify(cancha), 200


@canchas_bp.route('/canchas/<int:id>', methods=['DELETE'])
def delete_cancha(id):
    problema = serv_canchas.eliminar_cancha(id)

    if problema == 'CANCHA_NO_ENCONTRADA':
        return error('NOT_FOUND', 'Cancha no encontrada', 404)

    if problema == 'CANCHA_CON_RESERVAS':
        return error(
            'CONFLICT',
            'La cancha tiene reservas asociadas; puede desactivarse con PATCH',
            409,
        )

    return '', 204


@canchas_bp.route('/canchas/disponibles', methods=['GET'])
def get_canchas_disponibles():
    es_valido, mensaje = valid_canchas.validar_disponibles_GET(request.args)
    if not es_valido:
        return error('BAD_REQUEST', mensaje, 400)

    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))

    inicio_iso, fin_iso = valid_canchas.armar_intervalo_iso(
        request.args['fecha'],
        request.args['hora_inicio'],
        request.args['hora_fin'],
    )

    canchas, total = repo_canchas.buscar_canchas_libres(
        inicio_iso,
        fin_iso,
        _id_deporte_query(),
        _bool_query('techada'),
        limit,
        offset,
    )

    
    return jsonify({
        'canchas': canchas,
        '_links': construir_links(
            request.base_url, _filtros_para_links(), total, limit, offset
        ),
    }), 200
