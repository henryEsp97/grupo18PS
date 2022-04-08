
from app.models.category import Category
from app.models.denuncia import Denuncia


def validate_denuncia(categoria_id, coordenadas, apellido_denunciante, nombre_denunciante, telcel_denunciante, email_denunciante, titulo, descripcion):
    if not Denuncia.check_titulo(titulo):
        return "Ya existe una denuncia con ese titulo"
    if Category.check_id(categoria_id):
        return "No existe categoría con ese id"
    if not coordenadas:
        return "Las coordenadas no pueden estar en blanco"
    if not apellido_denunciante:
        return "El apellido del denunciante no puede estar en blanco"
    if not nombre_denunciante:
        return "El nombre del denunciante no puede estar en blanco"
    if not telcel_denunciante:
        return "El telefono del denunciante no puede estar en blanco"
    if not email_denunciante:
        return "El email del denunciante no puede estar en blanco"
    if not descripcion:
        return "La descripción no puede estar en blanco"
    return ""