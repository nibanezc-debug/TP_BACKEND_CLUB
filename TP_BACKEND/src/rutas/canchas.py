from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import Error as MySQLError
from src.repositorios import canchas as repo_canchas
from src.validaciones import canchas as valid_canchas
from src.servicios import canchas as serv_canchas

canchas_bp = Blueprint("canchas_bp", __name__)

@canchas_bp.route("/canchas", methods=["GET"]) #verificado
def get_canchas():
    limit = request.args.get("_limit", default=10, type=int)
    offset = request.args.get("_offset", default=0, type=int)
    id_deporte_str = request.args.get("id_deporte")
    nombre = request.args.get("nombre")
    techada_str = request.args.get("techada")
    activa_str = request.args.get("activa")



    if not valid_canchas.datos_validos_cancha_GET(nombre, id_deporte_str, techada_str, activa_str):
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Datos de entrada inválidos o faltantes"}]}), 400

    techada = True if techada_str and techada_str.lower() == "true" else (False if techada_str and techada_str.lower() == "false" else None)
    activa = True if activa_str and activa_str.lower() == "true" else (False if activa_str and activa_str.lower() == "false" else None)
    id_deporte = int(id_deporte_str) if id_deporte_str is not None else None

    lista, _ = repo_canchas.buscar_canchas(id_deporte, nombre, techada, activa, limit, offset)

    if not lista:
        return "", 204

    return jsonify({"canchas": lista}), 200


@canchas_bp.route("/canchas", methods=["POST"]) #verificado
def post_cancha():
    datos = request.get_json(silent=True) or {}
    nombre = datos.get("nombre")
    id_deporte = datos.get("id_deporte")
    precio_hora = datos.get("precio_hora")
    techada = datos.get("techada", False)
    activa = datos.get("activa", True)
    
    if not valid_canchas.datos_validos_cancha_POST_PATCH(nombre, id_deporte, precio_hora, techada, activa):
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Datos de entrada inválidos o faltantes"}]}), 400

    try:
        cancha_id = repo_canchas.guardar_cancha(nombre, id_deporte, precio_hora, techada, activa)
        return jsonify({"id": cancha_id}), 201
    except MySQLError:
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": "Deporte no encontrado"}]}), 404


@canchas_bp.route("/canchas/<int:id>", methods=["GET"])
def obtener_cancha_por_id(id):
    cancha = repo_canchas.obtener_cancha_por_id(id)
    if not cancha:
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": "Cancha no encontrada"}]}), 404
    return jsonify(cancha), 200


@canchas_bp.route("/canchas/<int:id>", methods=["PATCH"]) #verificado
def patch_cancha(id):
    cancha = repo_canchas.obtener_cancha_por_id(id)
    
    if not cancha:
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": "Cancha no encontrada"}]}), 404
    
    datos = request.get_json(silent=True) or {}
    
    if not datos:
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Cuerpo de la petición vacío"}]}), 400
    
    nombre = datos.get("nombre", cancha["nombre"])
    precio_hora = datos.get("precio_hora", cancha["precio_hora"])
    techada = datos.get("techada", cancha["techada"])
    activa = datos.get("activa", cancha["activa"])

    if "nombre" in datos and isinstance(nombre, str):
        nombre = nombre.strip()

    if not valid_canchas.datos_validos_cancha_POST_PATCH(nombre ,None , precio_hora, techada, activa):
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Datos de entrada inválidos"}]}), 400

    repo_canchas.actualizar_cancha_db(id, datos)
    return "", 204


@canchas_bp.route("/canchas/<int:id>", methods=["DELETE"]) #verificado
def delete_cancha(id):
    cancha = repo_canchas.obtener_cancha_por_id(id)
    if not cancha:
        return jsonify({"errors": [{"code": "NOT_FOUND", "message": "Cancha no encontrada"}]}), 404

    try:
        repo_canchas.eliminar_cancha_db(id)
        return "", 204
    except MySQLError:
        return jsonify({"errors": [{"code": "CONFLICT", "message": "La cancha posee reservas asociadas"}]}), 409


@canchas_bp.route("/canchas/disponibles", methods=["GET"]) #verificada
def get_canchas_disponibles():
    fecha = request.args.get("fecha")
    hora_inicio = request.args.get("hora_inicio")
    hora_fin = request.args.get("hora_fin")
    id_deporte_str = request.args.get("id_deporte")
    techada_str = request.args.get("techada")
    limit = request.args.get("_limit", default=10, type=int)
    offset = request.args.get("_offset", default=0, type=int)

    
    if not fecha or not hora_inicio or not hora_fin:
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Faltan parámetros requeridos: fecha, hora_inicio, hora_fin"}]}), 400

    if not valid_canchas.datos_validos_cancha_GET(None, id_deporte_str, techada_str, None):
        return jsonify({"errors": [{"code": "BAD_REQUEST", "message": "Datos de entrada inválidos o faltantes"}]}), 400    

    es_valido, mensaje_error = serv_canchas.validar_horario_disponibilidad(fecha, hora_inicio, hora_fin)
    
    if not es_valido:
        return (jsonify({"errors": [{"code": "BAD_REQUEST", "message": mensaje_error}]}),400,)

    techada = True if techada_str and techada_str.lower() == "true" else (False if techada_str and techada_str.lower() == "false" else None)
    id_deporte = int(id_deporte_str) if id_deporte_str is not None else None

    hora_ini_limpio = hora_inicio if len(hora_inicio) == 8 else f"{hora_inicio}:00"
    hora_fin_limpio = hora_fin if len(hora_fin) == 8 else f"{hora_fin}:00"

    start_iso = f"{fecha}T{hora_ini_limpio}.000000-03:00"
    end_iso = f"{fecha}T{hora_fin_limpio}.000000-03:00"

    lista, _ = repo_canchas.buscar_canchas_libres(start_iso, end_iso, id_deporte, techada, limit, offset)

    if not lista:
        return "", 200

    return jsonify({"canchas": lista}), 200
