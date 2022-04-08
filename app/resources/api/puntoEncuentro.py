from flask import jsonify, Blueprint,request
from app.models.puntoEncuentro import PuntoEncuentro
from app.helpers.codificador import decodificar
from app.models.elementos import Elementos


puntoEncuentro_api = Blueprint("puntos", __name__, url_prefix="/puntos-encuentro")

@puntoEncuentro_api.get("/")
def index():
    lista_puntos = []
    cant_per_page = Elementos.get_elementos()
    page = request.args.get('page',1,type=int)
    puntos = PuntoEncuentro.get_puntos_paginados(page,cant_per_page)

    for punto in puntos.items:
        lista_puntos.append(
            {
                'id':punto.id, 
                'nombre':punto.nombre, 
                'direccion': punto.direccion,
                'coordenadas':decodificar(punto.coordenadas),
                'estado': punto.estado,
                'telefono': punto.telefono,
                'email': punto.email
            }

        )
    return jsonify(total=len(lista_puntos), pagina=page, puntos=lista_puntos)