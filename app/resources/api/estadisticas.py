from flask import jsonify, Blueprint,request
from app.models.puntoEncuentro import PuntoEncuentro
from app.models.zona_inundable import ZonaInundable
from app.models.denuncia import Denuncia
from app.models.recorrido import Recorrido
from app.helpers.codificador import decodificar
from app.models.elementos import Elementos
import sys


estadisticas_api = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")

@estadisticas_api.get("/")
def index():
    lista = []
    cant_puntos = PuntoEncuentro.get_cantidad()
    cant_recorridos = Recorrido.get_cantidad()
    cant_denuncias = Denuncia.get_cantidad()
    cant_zonasInundables = ZonaInundable.get_cantidad()

    lista.append(
        {
            'cantidad_puntos':cant_puntos, 
            'cantidad_recorridos':cant_recorridos, 
            'cantidad_denuncias':cant_denuncias,
            'cantidad_zonas_inundables':cant_zonasInundables,
        }

    )
    print(lista, file=sys.stderr)
    return jsonify(lista)