from flask import jsonify, Blueprint,request
from app.models.recorrido import Recorrido
from app.helpers.codificador import decodificar
from app.models.elementos import Elementos


recorridos_evacuacion_api = Blueprint("recorridos", __name__, url_prefix="/recorridos-evacuacion")

@recorridos_evacuacion_api.get("/")
def index():
    lista_recorridos = []
    cant_per_page = Elementos.get_elementos()
    page = request.args.get('page',1,type=int)
    recorridos = Recorrido.get_recorridos_paginados(page,cant_per_page)

    for recorrido in recorridos.items:
        lista_recorridos.append(
            {
                'id':recorrido.id, 
                'nombre':recorrido.nombre, 
                'descripcion': recorrido.descripcion,
                'coordenadas':decodificar(recorrido.coordenadas),
                'estado': recorrido.estado
            }

        )
    return jsonify(total=len(lista_recorridos), pagina=page, recorridos=lista_recorridos)