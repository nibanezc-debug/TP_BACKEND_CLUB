from datetime import datetime, time
from src import constantes


def validar_horario_disponibilidad(fecha_str, hora_inicio_str, hora_fin_str):

  try:
    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
  except (ValueError, TypeError):
    return False, "La fecha debe tener el formato YYYY-MM-DD válido"

  try:
    s_ini = (
        f"{hora_inicio_str}:00"
        if len(hora_inicio_str) == 5
        else str(hora_inicio_str)
    )
    hora_ini_obj = datetime.strptime(s_ini, "%H:%M:%S").time()
  except (ValueError, TypeError, AttributeError):
    return False, "La hora_inicio debe tener el formato HH:MM:SS o HH:MM"

  try:
    s_fin = (
        f"{hora_fin_str}:00" if len(hora_fin_str) == 5 else str(hora_fin_str)
    )
    hora_fin_obj = datetime.strptime(s_fin, "%H:%M:%S").time()
  except (ValueError, TypeError, AttributeError):
    return False, "La hora_fin debe tener el formato HH:MM:SS o HH:MM"

  if hora_ini_obj.minute != 0 or hora_ini_obj.second != 0:
    return False, "La hora_inicio debe ser en punto (minutos y segundos en 00)"

  if hora_fin_obj.minute != 0 or hora_fin_obj.second != 0:
    return False, "La hora_fin debe ser en punto (minutos y segundos en 00)"

  hora_apertura = time(constantes.HORA_INICIO, 0, 0)
  hora_cierre = time(constantes.HORA_FINAL, 0, 0)

  if hora_ini_obj < hora_apertura or hora_fin_obj > hora_cierre:
    return False, "El horario de reserva debe estar entre las 08:00 y las 23:00"

  if hora_ini_obj >= hora_fin_obj:
    return False, "La hora_inicio debe ser anterior a la hora_fin"

  duracion_horas = hora_fin_obj.hour - hora_ini_obj.hour
  if duracion_horas not in [1, 2, 3]:
    return False, "La duración de la reserva debe ser de 1, 2 o 3 horas"

  inicio_dt = datetime.combine(fecha_obj, hora_ini_obj)
  if inicio_dt < datetime.now():
    return (
        False,
        "No se pueden consultar o reservar horarios pasados",
    )

  return True, None