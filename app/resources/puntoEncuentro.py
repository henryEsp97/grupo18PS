from flask import redirect, render_template, request, url_for, session
from sqlalchemy import exc

from app.models.ordenacion import Ordenacion
from app.models.puntoEncuentro import PuntoEncuentro
from app.helpers.auth import assert_permission
from app.db import db
from app.models.elementos import Elementos
from app.helpers.codificador import codificar

def index():
    """Controlador para mostrar el listado de puntos de encuentro"""

    #Chequea autenticación y permisos
    assert_permission(session, 'punto_encuentro_index')

    #variables para paginación
    cant_paginas = Elementos.get_elementos()
    page = request.args.get('page', 1, type=int)

    #variable para opción de ordenación
    ordenacion = Ordenacion.get_ordenacion_puntos()

    #variable para opción de filtrado por estado: publicado o despublicado
    filter_option = request.args.get("filter_option")

    q = request.args.get("q") #query de búsqueda por nombre
    if q:
        puntos = PuntoEncuentro.get_puntos_busqueda(q, ordenacion.orderBy, page, cant_paginas)
    elif filter_option:
        puntos = PuntoEncuentro.get_puntos_con_filtro(filter_option, ordenacion.orderBy, page, cant_paginas)
    else:
        puntos = PuntoEncuentro.get_puntos_ordenados_paginados(ordenacion.orderBy, page, cant_paginas)

    return render_template("puntoEncuentro/index.html", puntos=puntos)

def show(id_punto):
    punto = PuntoEncuentro.get_punto(id_punto)
    return render_template("puntoEncuentro/show.html",punto=punto)

def new():
    """Controlador para mostrar el formulario para crear puntos de encuentro"""
    #Chequea autenticación y permisos
    assert_permission(session, 'punto_encuentro_new')

    return render_template("puntoEncuentro/new.html")

def create():
    """Controlador para crear un punto de encuentro"""

    #Chequea autenticación y permisos
    assert_permission(session, 'punto_encuentro_create')

    #catchea todos los errores que levantan los validadores de campos
    coordenadas = codificar(str([[request.form['lat'],request.form['lng']]]))
    estado = int(request.form['estado'])
    telefono = request.form['telefono']
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    email = request.form['email']
    try:
        new_punto = PuntoEncuentro(nombre, direccion, coordenadas, estado, telefono, email)
    except ValueError as e:
        return render_template("puntoEncuentro/new.html", error_message=e)
    else:
        db.session.add(new_punto)

    #si el nombre ingresado o direccion ya se encuentra registrado en la db se produce maneja las excepciones
    try:
        db.session.commit()
    except exc.IntegrityError as e:
        if 'direccion' in e.orig.args[1]:
            error = "Ya existe un punto con esa direccion"
        elif 'nombre' in e.orig.args[1]:
            error = "Ya existe un punto con ese nombre"
        db.session.rollback()
        return render_template("puntoEncuentro/new.html", error_message=error)

    return redirect(url_for("puntoEncuentro_index"))

def update(id_punto):
    """Controlador para editar un punto de encuentro"""

    #Chequea autenticación y permisos
    assert_permission(session, 'punto_encuentro_update')

    punto = PuntoEncuentro.get_punto(id_punto)
    if request.method == 'POST':
        punto.coordenadas = codificar(str([[request.form['lat'],request.form['lng']]]))
        punto.estado = int(request.form['estado'])
        punto.telefono = request.form['telefono']
        try:
            punto.nombre = request.form['nombre']
            punto.direccion = request.form['direccion']
            punto.email = request.form['email']
            db.session.commit()
        except exc.IntegrityError as e: #maneja las excepciones de datos ya ingresados en db
            if 'direccion' in e.orig.args[1]:
                error = "Ya existe un punto con esa direccion"
            elif 'nombre' in e.orig.args[1]:
                error = "Ya existe un punto con ese nombre"
            db.session.rollback()
            return render_template("puntoEncuentro/edit.html", puntoEncuentro=punto, error_message=error) 
        except ValueError as e: #maneja la validación de los campos
            db.session.rollback()
            return render_template("puntoEncuentro/edit.html", puntoEncuentro=punto, error_message=e)
        return redirect(url_for("puntoEncuentro_index")) 
    return render_template('puntoEncuentro/edit.html', puntoEncuentro=punto)

def destroy(id_punto):
    """Controlador para eliminar un punto de encuentro"""

    #Chequea autenticación y permisos
    assert_permission(session, 'punto_encuentro_destroy')
    
    #busca y elimina
    punto = PuntoEncuentro.get_punto(id_punto)
    db.session.delete(punto)
    db.session.commit()
    return redirect(url_for("puntoEncuentro_index"))

