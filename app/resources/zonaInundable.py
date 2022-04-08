from flask import redirect, render_template, request, url_for, session, abort
import string
import random

import pandas as pd

from app.models.ordenacion import Ordenacion
from app.helpers.auth import assert_permission
from app.models.elementos import Elementos
from app.models.zona_inundable import ZonaInundable
from app.helpers.codificador import codificar
from app.helpers.zonas_forms import ImportForm

def index():
    """Controlador para listar las zonas inundables"""
    #Chequea autenticación y permisos
    assert_permission(session,'zona_inundable_index')

    #variables para paginación
    cant_paginas = Elementos.get_elementos()
    page = request.args.get('page', 1, type=int)

    #variable para opción de ordenación
    ordenacion = Ordenacion.get_ordenacion_zonas()

    #variable para opción de filtrado por estado: publicado o despublicado
    filter_option = request.args.get("filter_option")

    q = request.args.get("q") #query de búsqueda por nombre
    if q:
        zonas = ZonaInundable.get_zonas_busqueda(q, ordenacion.orderBy, page, cant_paginas)
    elif filter_option:
        zonas = ZonaInundable.get_zonas_con_filtro(filter_option, ordenacion.orderBy, page, cant_paginas)
    else:
        zonas = ZonaInundable.get_zonas_ordenados_paginados(ordenacion.orderBy, page, cant_paginas)
    return render_template("zona_inundable/index.html", zonas=zonas)

def show(id_zona):
    zona = ZonaInundable.get_zona(id_zona)
    return render_template("zona_inundable/show.html",zona=zona)

def update(id_zona):
    #Chequea autenticación y permisos
    assert_permission(session,'zona_inundable_update')
    error=''
    zona = ZonaInundable.get_zona(id_zona)
    if not zona:
        abort(404)
    else:
        if request.method=="POST":
            e = ZonaInundable.update_zona(nombre=zona.nombre,codigo=request.form['codigo'],estado=int(request.form['estado']), color=request.form['color'])
            if e:
                if 'codigo' in e.orig.args[1]:
                    error = "Ya existe una zona con ese codigo"
                return render_template("zona_inundable/update.html", zona=zona, error_message=error)
            else:
                return redirect(url_for("zonaInundable_index"))
        return render_template("zona_inundable/update.html", zona=zona)

def importar():
    """Controlador para importar archivo csv de zonas"""

    #Chequea autenticación y permisos
    assert_permission(session,'zona_inundable_importar')

    form = ImportForm()
    if request.method=="POST":
        if form.validate_on_submit():

            filestream =  form.file.data 
            filestream.seek(0)
            csvData = pd.read_csv( filestream  )

            S = 10  # cantidad de caracteres del codigo.  

            # Recorre las filas
            for i,row in csvData.iterrows():
                #saltea primer fila: nombre, area
                if i > 0:
                    #agrega la zona si no se encuentra ya cargada
                    if ZonaInundable.check_zona(row['name']):
                        #genera código random que no se encuentre ya en la db
                        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
                        while not ZonaInundable.check_codigo(ran):
                            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
                        ZonaInundable.create_zona(codigo=ran, nombre=row['name'],coordenadas=codificar(row['area']))
                    else:
                        #si ya está cargada, actualiza el nombre y el area
                        ZonaInundable.update_zona(nombre=row['name'],coordenadas=codificar(row['area']))

            return redirect(url_for('zonaInundable_index'))
    return render_template("zona_inundable/import.html", form=form)

def destroy(id_zona):
    """Controlador para eliminar una zona inundable"""

    #Chequea autenticación y permisos
    assert_permission(session, 'zona_inundable_destroy')

    #busca y elimina
    ZonaInundable.delete_zona(id_zona)

    return redirect(url_for("zonaInundable_index"))