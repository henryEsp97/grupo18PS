from flask import redirect, render_template, request, url_for, session
from sqlalchemy import exc

from app.models.ordenacion import Ordenacion
from app.models.recorrido import Recorrido
from app.helpers.auth import assert_permission
from app.db import db
from app.models.elementos import Elementos
from app.helpers.codificador import codificar

def index():
    """Controlador para mostrar el listado de recorridos de evacuación"""

    #Chequea autenticación y permisos
    assert_permission(session, 'recorrido_index')

    #variables para paginación
    cant_paginas = Elementos.get_elementos()
    page = request.args.get('page', 1, type=int)

    #variable para opción de ordenación
    ordenacion = Ordenacion.get_ordenacion_recorridos()#agregar metodo a la clase ordenación

    #variable para opción de filtrado por estado: publicado o despublicado
    filter_option = request.args.get("filter_option")

    q = request.args.get("q") #query de búsqueda por nombre
    if q:
        recorridos = Recorrido.get_recorridos_busqueda(q, ordenacion.orderBy, page, cant_paginas)
    elif filter_option:
        recorridos = Recorrido.get_recorridos_con_filtro(filter_option, ordenacion.orderBy, page, cant_paginas)
    else:
        recorridos = Recorrido.get_recorridos_ordenados_paginados(ordenacion.orderBy, page, cant_paginas)

    return render_template("recorrido/index.html", recorridos=recorridos)

def show(id_recorrido):
    recorrido = Recorrido.get_recorrido(id_recorrido)
    return render_template("recorrido/show.html",recorrido=recorrido)

def new():
    """Controlador para mostrar el formulario para crear recorridos de evacuación"""
    #Chequea autenticación y permisos
    assert_permission(session, 'recorrido_new')

    return render_template("recorrido/new.html")

def create():
    """Controlador para crear un recorrido de evacuación"""

    #Chequea autenticación y permisos
    assert_permission(session, 'recorrido_create')

    #catchea todos los errores que levantan los validadores de campos
    estado = int(request.form['estado'])
    if len(request.form['coord'])>0:
        coordenadas = codificar(request.form['coord'])
    else:
        error= "Marque un recorrido en el mapa"
        return render_template("recorrido/new.html", error_message=error)
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    try:
        new_recorrido = Recorrido(nombre, descripcion, coordenadas, estado)
    except ValueError as e:
        return render_template("recorrido/new.html", error_message=e)
    else:
        db.session.add(new_recorrido)

    #si el nombre ingresado o direccion ya se encuentra registrado en la db se produce maneja las excepciones
    try:
        db.session.commit()
    except exc.IntegrityError as e:
        if 'nombre' in e.orig.args[1]:
            error = "Ya existe un recorrido con ese nombre"
        db.session.rollback()
        return render_template("recorrido/new.html", error_message=error)

    return redirect(url_for("recorrido_index"))

def update(id_recorrido):
    """Controlador para editar un punto de encuentro"""

    #Chequea autenticación y permisos
    assert_permission(session, 'recorrido_update')

    recorrido = Recorrido.get_recorrido(id_recorrido)
    if request.method == 'POST':
        if len(request.form['coord'])>0:
            recorrido.coordenadas = codificar(request.form['coord'])
        recorrido.estado = int(request.form['estado'])
        try:
            recorrido.nombre = request.form['nombre']
            recorrido.descripcion = request.form['descripcion']
            db.session.commit()
        except exc.IntegrityError as e: #maneja las excepciones de datos ya ingresados en db
            if 'direccion' in e.orig.args[1]:
                error = "Ya existe un punto con esa direccion"
            elif 'nombre' in e.orig.args[1]:
                error = "Ya existe un punto con ese nombre"
            db.session.rollback()
            return render_template("recorrido/edit.html", recorrido=recorrido, error_message=error) 
        except ValueError as e: #maneja la validación de los campos
            db.session.rollback()
            return render_template("recorrido/edit.html", recorrido=recorrido, error_message=e)
        return redirect(url_for("recorrido_index")) 
    return render_template('recorrido/edit.html', recorrido=recorrido)

def destroy(id_recorrido):
    """Controlador para eliminar un punto de encuentro"""

    #Chequea autenticación y permisos
    assert_permission(session, 'recorrido_destroy')
    
    #busca y elimina
    recorrido = Recorrido.get_recorrido(id_recorrido)
    db.session.delete(recorrido)
    db.session.commit()
    return redirect(url_for("recorrido_index"))

