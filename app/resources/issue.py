from flask import redirect, render_template, request, url_for

from app.models.elementos import Elementos
from app.models.ordenacion import Ordenacion
from app.models.colores import Colores
from app.models.issue import Issue
from app.db import db
# Public resources
def index():
        color = "default"
        colores = Colores.query.first()
        if colores is not None:
            color = colores.publico
        orden = Ordenacion.query.filter_by(lista='issues').first()
        elem = Elementos.get_elementos()
        if elem is not None:
            per_page = int(elem.cant)
        else:
            per_page = 2 #si todavía no se creo el objeto asigna 2 por defecto
        page  = int(request.args.get('page', 1))
        #aca defino por default 2 crioterios de ordenacion, por mail o descripcion
        issues = Issue.query.order_by(orden.orderBy).paginate(page,per_page,error_out=False)
        return render_template("issue/index.html", issues=issues,color = color)
    
def new():
    return render_template("issue/new.html")


def create():
    new_issue = Issue(**request.form)

    db.session.add(new_issue)
    db.session.commit()

    return redirect(url_for("issue_index"))
def config():

    return render_template("issue/config.html")
