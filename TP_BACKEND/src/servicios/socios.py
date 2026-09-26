from src.repositorios import socios as repo_socios


def normalizar_email(email):
    # El enunciado pide guardarlo en minúsculas y sin espacios en los extremos
    return email.strip().lower()


def crear_socio(datos):
    """Devuelve (id_nuevo, None) o (None, 'EMAIL_DUPLICADO')."""
    nombre = datos['nombre'].strip()
    email = normalizar_email(datos['email'])

    # 409 aunque el socio que ya tiene ese mail esté inactivo
    if repo_socios.obtener_socio_por_email(email):
        return None, 'EMAIL_DUPLICADO'

    return repo_socios.guardar_socio(nombre, email), None


def actualizar_socio(id_socio, datos):
    """Devuelve None si salió bien, o 'NO_ENCONTRADO' / 'EMAIL_DUPLICADO'."""
    if not repo_socios.obtener_socio_por_id(id_socio):
        return 'NO_ENCONTRADO'

    campos = {}
    if 'nombre' in datos:
        campos['nombre'] = datos['nombre'].strip()
    if 'activo' in datos:
        campos['activo'] = datos['activo']
    if 'email' in datos:
        email = normalizar_email(datos['email'])
        otro = repo_socios.obtener_socio_por_email(email)
        # Si el mail lo tiene OTRO socio, es conflicto. Si es el mismo, no pasa nada.
        if otro and otro['id'] != id_socio:
            return 'EMAIL_DUPLICADO'
        campos['email'] = email

    repo_socios.actualizar_socio_db(id_socio, campos)
    return None
