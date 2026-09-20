from flask import Blueprint, jsonify, request
from src.repositorios import canchas as repo_canchas

canchas_bp = Blueprint("canchas_bp", __name__)

@canchas_bp.route("/canchas", methods=["GET"])
def get_canchas():
  limit = request.args.get("_limit", default=10, type=int)
  offset = request.args.get("_offset", default=0, type=int)
  id_deporte = request.args.get("id_deporte", type=int)
  nombre = request.args.get("nombre")
  techada_str = request.args.get("techada")
  activa_str = request.args.get("activa")

  techada = (
      True
      if techada_str and techada_str.lower() == "true"
      else (False if techada_str and techada_str.lower() == "false" else None)
  )
  activa = (
      True
      if activa_str and activa_str.lower() == "true"
      else (False if activa_str and activa_str.lower() == "false" else None)
  )

  lista, _ = repo_canchas.buscar_canchas(
      id_deporte, nombre, techada, activa, limit, offset
  )
  return jsonify({"canchas": lista}), 200


@canchas_bp.route("/canchas", methods=["POST"])
def post_cancha():
  datos = request.get_json(silent=True) or {}

  nombre = datos.get("nombre", "")
  id_deporte = datos.get("id_deporte")
  precio_hora = datos.get("precio_hora", 0)
  techada = bool(datos.get("techada", False))
  activa = bool(datos.get("activa", True))

  # Guarda directamente en MySQL
  cancha_id = repo_canchas.guardar_cancha(
      nombre, id_deporte, precio_hora, techada, activa
  )
  return jsonify({"id": cancha_id}), 201


@canchas_bp.route("/canchas/<int:id>", methods=["GET"])
def get_cancha_by_id(id):
  cancha = repo_canchas.obtener_cancha_por_id(id)
  if not cancha:
    return (
        jsonify(
            {"errors": [{"code": "NOT_FOUND", "message": "Cancha no encontrada"}]}
        ),
        404,
    )
  return jsonify(cancha), 200


@canchas_bp.route("/canchas/<int:id>", methods=["PATCH"])
def patch_cancha(id):
  datos = request.get_json(silent=True) or {}
  repo_canchas.actualizar_cancha_db(id, datos)
  return "", 200


@canchas_bp.route("/canchas/<int:id>", methods=["DELETE"])
def delete_cancha(id):
  repo_canchas.eliminar_cancha_db(id)
  return "", 204


@canchas_bp.route("/canchas/disponibles", methods=["GET"])
def get_canchas_disponibles():
  fecha = request.args.get("fecha")
  hora_inicio = request.args.get("hora_inicio")
  hora_fin = request.args.get("hora_fin")
  id_deporte = request.args.get("id_deporte", type=int)
  techada_str = request.args.get("techada")
  limit = request.args.get("_limit", default=10, type=int)
  offset = request.args.get("_offset", default=0, type=int)

  techada = (
      True
      if techada_str and techada_str.lower() == "true"
      else (False if techada_str and techada_str.lower() == "false" else None)
  )

  start_iso = f"{fecha}T{hora_inicio}.000000-03:00"
  end_iso = f"{fecha}T{hora_fin}.000000-03:00"

  lista, _ = repo_canchas.buscar_canchas_libres(
      start_iso, end_iso, id_deporte, techada, limit, offset
  )
  return jsonify({"canchas": lista}), 200
