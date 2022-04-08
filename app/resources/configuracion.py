from flask import redirect, render_template, request, url_for, session

from app.models.elementos import Elementos
from app.models.ordenacion import Ordenacion
from app.models.colores import Colores
from app.helpers.auth import assert_permission
# Public resources

def conf():
    assert_permission(session,'configuracion_index')
    #return a la vista
    elem = Elementos.get_elementos()
    ordenPuntos = Ordenacion.get_ordenacion_puntos()
    ordenUsuarios = Ordenacion.get_ordenacion_usuarios()
    ordenDenuncias = Ordenacion.get_ordenacion_denuncias()
    colores = Colores.get_colores()
    color = colores.privado
    return render_template("config.html", cant = elem, ordenP = ordenPuntos.orderBy, ordenU = ordenUsuarios.orderBy, ordenD = ordenDenuncias.orderBy, coloresPriv = colores.privado, coloresPub = colores.publico, color = color)


def configurado():
    assert_permission(session,'configuracion_update')
    #Acá actualizo en la bd los nuevos valores ingresados
    Colores.configurar(request.form.get('colorPri'),request.form.get('colorPub'))
    Ordenacion.configurarOrdenUsuarios(request.form.get('orden_usuarios'))
    Ordenacion.configurarOrdenPuntos(request.form.get('orden_puntos'))    
    Ordenacion.configurarOrdenDenuncias(request.form.get('orden_denuncias'))
    Elementos.configurar(request.form.get('numero'))
    return redirect(url_for("home"))     