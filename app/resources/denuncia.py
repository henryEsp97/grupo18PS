from datetime import datetime
from flask import redirect, render_template, request, url_for, session
from flask.helpers import flash
from app.models.category import Category
from app.models.status import Status
from app.models.user import User
from app.helpers.codificador import codificar

from app.models.ordenacion import Ordenacion
from app.models.denuncia import Denuncia, Seguimiento
from app.helpers.auth import assert_permission
from app.db import db
from app.models.elementos import Elementos


def index():
    """ Muestra las denuncias del sistema """
    assert_permission(session,'denuncia_index')

    #paginacion
    page  = int(request.args.get('page', 1,type=int))

    cant_paginas = Elementos.get_elementos()

    #variable para opción de ordenación
    ordenacion = Ordenacion.get_ordenacion_denuncias()
    users = User.allUsers()
    categorias = Category.get_all()
    estados = Status.get_all()
    fecha1 = request.args.get("date1")
    fecha2 = request.args.get("date2")
    q = request.args.get("q")
    if q:
        denuncias= Denuncia.denuncias_por_busqueda(q,ordenacion ,page,cant_paginas)
    elif fecha1 and fecha2:
        if fecha1 < fecha2:
            denuncias= Denuncia.denuncias_por_fechas(fecha1,fecha2,ordenacion,page,cant_paginas)
        else:
            flash("Las fechas ingresadas son incorrectas")
            return redirect(url_for("denuncia_index"))
    else:
        denuncias = Denuncia.paginacion(ordenacion, page, cant_paginas)
    return render_template("denuncia/index.html", denuncias=denuncias, users=users, categorias=categorias, estados=estados)


def info(denuncia_id):
    """ Muestra la informacion adicional de la denuncia"""
    assert_permission(session,'denuncia_index')
    denuncia = Denuncia.get_denuncia(denuncia_id)
    seguimientos = Seguimiento.get_seguimientos(denuncia_id)
    users = User.allUsers()
    return render_template("denuncia/masInfo.html", denuncia=denuncia, seguimientos=seguimientos, users=users)


def sinConfirmar():
    """ Muestra las denuncias sin confirmar """
    assert_permission(session,'denuncia_sinConfirmar') 

    #chequeo si habia un orden creado
    ordenacion = Ordenacion.get_ordenacion_denuncias()
    users = User.allUsers()
    cant_paginas = Elementos.get_elementos()

    page  = int(request.args.get('page', 1,type=int))
    q = request.args.get("q")
    if q:
        denuncias= Denuncia.users_por_busqueda(q,ordenacion ,page,cant_paginas)
    else:
        denuncias = Denuncia.get_denuncias_sinConfirmar(ordenacion, page, cant_paginas)
    return render_template("denuncia/index.html", denuncias=denuncias, users=users)


def enCurso():
    """ Muestra las denuncias en curso """
    assert_permission(session,'denuncia_index') 

    #chequeo si habia un orden creado
    ordenacion = Ordenacion.get_ordenacion_denuncias()
    users = User.allUsers()
    cant_paginas = Elementos.get_elementos()

    page  = int(request.args.get('page', 1,type=int))
    q = request.args.get("q")
    if q:
        denuncias= Denuncia.users_por_busqueda(q,ordenacion ,page,cant_paginas)
    else:
        denuncias = Denuncia.get_denuncias_enCurso(ordenacion, page, cant_paginas)
    return render_template("denuncia/index.html", denuncias=denuncias, users=users)

def resuelta():
    """ Muestra las denuncias resueltas """
    assert_permission(session,'denuncia_index') 

    #chequeo si habia un orden creado
    ordenacion = Ordenacion.get_ordenacion_denuncias()
    users = User.allUsers()
    cant_paginas = Elementos.get_elementos()

    page  = int(request.args.get('page', 1,type=int))
    q = request.args.get("q")
    if q:
        denuncias= Denuncia.users_por_busqueda(q,ordenacion ,page,cant_paginas)
    else:
        denuncias = Denuncia.get_denuncias_resuelta(ordenacion, page, cant_paginas)
    return render_template("denuncia/index.html", denuncias=denuncias, users=users)

def cerrada():
    """ Muestra las denuncias cerradas """
    assert_permission(session,'denuncia_index') 

    #chequeo si habia un orden creado
    ordenacion = Ordenacion.get_ordenacion_denuncias()
    users = User.allUsers()
    cant_paginas = Elementos.get_elementos()

    page  = int(request.args.get('page', 1,type=int))
    q = request.args.get("q")
    if q:
        denuncias= Denuncia.users_por_busqueda(q,ordenacion ,page,cant_paginas)
    else:
        denuncias = Denuncia.get_denuncias_cerrada(ordenacion, page, cant_paginas)
    return render_template("denuncia/index.html", denuncias=denuncias, users=users)




def create():
    """Controlador para crear una denuncia"""

    #Chequea autenticación y permisos
    assert_permission(session, 'denuncia_create')
    if request.method == "GET":
        return render_template("denuncia/new.html")

    #catchea todos los errores que levantan los validadores de campos
    if request.method == "POST":
        params = request.form   
        error = None
        if not params["titulo"]:
            error = 'Titulo es requerido'
        if not params["descripcion"]:
            error = 'Descripcion es requerido'
        elif not params["apellido_denunciante"]:
            error = 'Apellido del denunciante es requerido'
        elif not params["nombre_denunciante"]:
            error = 'Nombre del denunciante es requerido'
        elif not params["telefono_denunciante"]:
            error = 'Telefono del denunciante es requerido'
        elif not params["categoria"]:
            error = 'Categoria de la denuncia es requerido'
        elif '@' not in params["email_denunciante"]:
            error = 'Ingrese un email valido'

        if error is None:
            category= Category.get_categoria(params["categoria"])
            coordenadas = codificar(str([[request.form['lat'],request.form['lng']]]))
            new_denuncia = Denuncia(titulo=params["titulo"],descripcion=params["descripcion"], coordenadas=coordenadas, categoria_id=category.id, apellido_denunciante=params["apellido_denunciante"], nombre_denunciante=params["nombre_denunciante"], telefono_denunciante=params["telefono_denunciante"], email_denunciante=params["email_denunciante"] )    
            db.session.add(new_denuncia)
            db.session.commit()
            flash("Denuncia agregada con exito")
            return redirect(url_for("denuncia_index"))
        else:
            flash(error)
            return redirect(url_for("denuncia_create"))

def update(denuncia_id):
    """Controlador para editar una denuncia"""

    #Chequea autenticación y permisos
    assert_permission(session, 'denuncia_update')

    denuncia = Denuncia.get_denuncia(denuncia_id)
    if request.method == 'POST':
        params = request.form   
        error = None
        if not params["titulo"]:
            error = 'Titulo es requerido'
        if not params["descripcion"]:
            error = 'Descripcion es requerido'
        elif not params["apellido_denunciante"]:
            error = 'Apellido del denunciante es requerido'
        elif not params["nombre_denunciante"]:
            error = 'Nombre del denunciante es requerido'
        elif not params["telefono_denunciante"]:
            error = 'Telefono del denunciante es requerido'
        elif not params["categoria"]:
            error = 'Categoria de la denuncia es requerido'
        elif '@' not in params["email_denunciante"]:
            error = 'Ingrese un email valido'

        if error is None:
            category= Category.get_categoria(params["categoria"])
            denuncia.titulo = params["titulo"]
            denuncia.descripcion = params["descripcion"]
            denuncia.coordenadas = codificar(str([[request.form['lat'],request.form['lng']]]))
            denuncia.apellido_denunciante = params["apellido_denunciante"]
            denuncia.nombre_denunciante = params["nombre_denunciante"]
            denuncia.email_denunciante = params["email_denunciante"]
            denuncia.telefono_denunciante = params["telefono_denunciante"]
            denuncia.categoria_id = category.id
            db.session.commit()
        else:
            flash(error)
            return redirect(url_for("denuncia_edit", denuncia_id=denuncia_id))   
        return redirect(url_for("denuncia_index"))
    return render_template('denuncia/edit.html', denuncia=denuncia)

def destroy(denuncia_id):
    """Controlador para eliminar una denuncia"""
    #Chequea autenticación y permisos
    assert_permission(session, 'denuncia_destroy')
    
    #busca seguimientos si es que tiene, los eliminar
    seguimientos = Seguimiento.get_seguimientos(denuncia_id)
    if seguimientos is not None:
        for x in seguimientos:
            seguimiento = Seguimiento.get_seguimiento(x.id)
            db.session.delete(seguimiento)
    #busca y elimina denuncia        
    denuncia = Denuncia.get_denuncia(denuncia_id)
    db.session.delete(denuncia)
    db.session.commit()
    return redirect(url_for("denuncia_index"))


def confirmar(denuncia_id):
    """Controlador para confirmar una denuncia"""
    #Chequea autenticación y permisos
    assert_permission(session, 'denuncia_confirmar')
    #busca y confirma
    denuncia = Denuncia.get_denuncia(denuncia_id)
    denuncia.estado_id=4
    denuncia.asignado_a=session["user2"].id
    db.session.commit()
    return redirect(url_for("denuncia_index"))

def cerrar(denuncia_id):
    """Controlador para cerrar una denuncia"""
    #Chequea autenticación y permisos
    assert_permission(session, 'denuncia_cerrar')
    #busca y confirma
    denuncia = Denuncia.get_denuncia(denuncia_id)
    if denuncia.estado_id != 3 :
        if denuncia.asignado_a != session["user2"].id :
            return redirect(url_for("denuncia_index"))
    denuncia.estado_id=6
    denuncia.fecha_cierre=datetime.now()
    new_seguimiento = Seguimiento(descripcion="No fue posible contactar al denunciante", denuncia_id=denuncia_id, autor=session["user2"].id)    
    db.session.add(new_seguimiento)
    db.session.commit()
    return redirect(url_for("denuncia_index"))

def resolver(denuncia_id):
    """Controlador para resolver una denuncia"""
    #Chequea que el user sea el que esta a cargo
    denuncia = Denuncia.get_denuncia(denuncia_id)
    if denuncia.asignado_a == session["user2"].id :
        denuncia.estado_id=5
        denuncia.fecha_cierre=datetime.now()
        db.session.commit()
    return redirect(url_for("denuncia_index"))

def seguimiento(denuncia_id):
    """Controlador para realizar un seguimiento"""
    denuncia = Denuncia.get_denuncia(denuncia_id)
    if request.method == 'POST':
        params = request.form   
        error = None
        if not params["descripcion"]:
            error = 'Descripcion es requerido'
        if error is None:
            new_seguimiento = Seguimiento(descripcion=params["descripcion"], denuncia_id=denuncia_id, autor=session["user2"].id)    
            db.session.add(new_seguimiento)
            db.session.commit()
            flash("Seguimiento realizado con exito")
            return redirect(url_for("denuncia_index"))
        else:
            flash(error)
            return redirect(url_for("denuncia_index"))
    return render_template('denuncia/seguimiento.html', denuncia=denuncia)

def seguimiento_destroy(seguimiento_id):
    """Controlador para eliminar un seguimiento"""
    #Chequea autenticación y permisos
    assert_permission(session, 'seguimiento_destroy')
    #busca y elimina
    seguimiento = Seguimiento.get_seguimiento(seguimiento_id)
    db.session.delete(seguimiento)
    db.session.commit()
    return redirect(url_for("denuncia_index"))

def seguimiento_update(seguimiento_id):
    """Controlador para editar un seguimiento"""

    #Chequea autenticación y permisos
    assert_permission(session, 'seguimiento_update')

    seguimiento = Seguimiento.get_seguimiento(seguimiento_id)
    if request.method == 'POST':
        params = request.form   
        error = None
        if not params["descripcion"]:
            error = 'Descripcion es requerido'
        if error is None:
            seguimiento.descripcion = params["descripcion"]
            db.session.commit()
        else:
            flash(error)
            return redirect(url_for("seguimiento_edit", seguimiento_id=seguimiento_id))   
        return redirect(url_for("denuncia_index"))
    return render_template('denuncia/editSeguimiento.html', seguimiento=seguimiento)