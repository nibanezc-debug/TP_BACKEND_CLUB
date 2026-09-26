from urllib.parse import urlencode


def construir_links(base_url, filtros, total, limit, offset):
    """Arma el objeto _links (HATEOAS) que pide el enunciado.

    Sirve para cualquier listado: socios, canchas o reservas.
    'filtros' son los parámetros de búsqueda, para que se mantengan al navegar.
    """
    def link(nuevo_offset):
        query = dict(filtros, _limit=limit, _offset=nuevo_offset)
        return {'href': f'{base_url}?{urlencode(query)}'}

    ultimo_offset = ((total - 1) // limit) * limit if total > 0 else 0

    return {
        '_first': link(0),
        '_prev': link(max(offset - limit, 0)) if offset > 0 else None,
        '_next': link(offset + limit) if offset + limit < total else None,
        '_last': link(ultimo_offset),
    }
