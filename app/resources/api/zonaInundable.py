from flask import jsonify, Blueprint, request
from flask import abort
from app.models.zona_inundable import ZonaInundable
from app.helpers.codificador import decodificar
from app.models.elementos import Elementos

zona_api = Blueprint("zonas", __name__, url_prefix="/zonas-inundables")

@zona_api.get("/")
def get_zonas():
    lista_zonas = []
    cant_per_page = Elementos.get_elementos()
    page = request.args.get('page',1,type=int)
    zonas = ZonaInundable.get_zonas_paginadas(page,cant_per_page)
    for zona in zonas.items:
        lista_zonas.append(
            {
                'id':zona.id, 
                'nombre':zona.nombre, 
                'coordenadas':decodificar(zona.coordenadas),
                'color':zona.color
            }
        )
    return jsonify(total=len(lista_zonas), pagina=page, zonas=lista_zonas)

@zona_api.get("/all")
def get_zonas_all():
    lista_zonas = []
    zonas = ZonaInundable.get_zonas()
    for zona in zonas:
        lista_zonas.append(
            {
                'id':zona.id, 
                'nombre':zona.nombre, 
                'coordenadas':decodificar(zona.coordenadas),
                'color':zona.color
            }
        )
    return jsonify(total=len(lista_zonas), zonas=lista_zonas)

@zona_api.get("/<id_zona>")
def get_zona(id_zona):
    zona = ZonaInundable.get_zona(id_zona)
    if not zona:
        abort(404) 
    return jsonify('atributos',
            {
                'id':zona.id, 
                'nombre':zona.nombre, 
                'coordenadas':decodificar(zona.coordenadas),
                'color':zona.color
            }
    )