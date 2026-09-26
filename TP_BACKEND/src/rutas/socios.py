from flask import Blueprint, jsonify, request
from src.repositorios import socios as repo_socios
from src.validaciones import socios as valid_socios
from src.servicios import socios as serv_socios
from src.servicios.paginacion import construir_links

socios_bp = Blueprint("socios_bp", __name__)


def error(code, message, status):
    return jsonify({"errors": [{"code": code, "message": message, "level": "error"}]}), status


@socios_bp.route("/socios", methods=["GET"])
def get_socios():
    es_valido, mensaje = valid_socios.validar_socio_GET(request.args)
    if not es_valido:
        return error("BAD_REQUEST", mensaje, 400)

    limit = int(request.args.get("_limit", 10))
    offset = int(request.args.get("_offset", 0))
    nombre = request.args.get("nombre")
    activo_str = request.args.get("activo")
    activo = None if activo_str is None else activo_str == "true"

    socios, total = repo_socios.buscar_socios(nombre, activo, limit, offset)

    if not socios:
        return "", 204

    filtros = {k: v for k, v in request.args.items() if k not in ("_limit", "_offset")}
    return jsonify({
        "socios": socios,
        "_links": construir_links(request.base_url, filtros, total, limit, offset),
    }), 200


@socios_bp.route("/socios", methods=["POST"])
def post_socio():
    datos = request.get_json(silent=True)

    es_valido, mensaje = valid_socios.validar_socio_POST(datos)
    if not es_valido:
        return error("BAD_REQUEST", mensaje, 400)

    id_socio, problema = serv_socios.crear_socio(datos)
    if problema == "EMAIL_DUPLICADO":
        return error("CONFLICT", "El email ya está registrado", 409)

    return jsonify({"id": id_socio}), 201


@socios_bp.route("/socios/<int:id>", methods=["GET"])
def get_socio(id):
    socio = repo_socios.obtener_socio_por_id(id)
    if not socio:
        return error("NOT_FOUND", "Socio no encontrado", 404)
    return jsonify(socio), 200


@socios_bp.route("/socios/<int:id>", methods=["PATCH"])
def patch_socio(id):
    datos = request.get_json(silent=True)

    es_valido, mensaje = valid_socios.validar_socio_PATCH(datos)
    if not es_valido:
        return error("BAD_REQUEST", mensaje, 400)

    problema = serv_socios.actualizar_socio(id, datos)
    if problema == "NO_ENCONTRADO":
        return error("NOT_FOUND", "Socio no encontrado", 404)
    if problema == "EMAIL_DUPLICADO":
        return error("CONFLICT", "El email ya está registrado", 409)

    return "", 204
