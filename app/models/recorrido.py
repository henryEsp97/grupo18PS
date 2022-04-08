
from sqlalchemy import Column, String, SmallInteger, Boolean, Text

from sqlalchemy.orm import validates

from app.db import db
from app.helpers.codificador import decodificar


class Recorrido(db.Model):
    """Define una entidad de tipo Recorridos de evacuación"""

    __tablename__ = "recorridos"
    id = Column(SmallInteger, primary_key=True)
    nombre = Column(String(40), unique=True, nullable=False)
    descripcion = Column(Text)
    coordenadas = Column(Text)
    estado = Column(Boolean)

    def __init__(
        self, nombre=None,
        descripcion=None,
        coordenadas=None,
        estado=None,
        ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.coordenadas = coordenadas
        self.estado = estado

    @validates('direccion')
    def validate_direccion(self, key, direccion):
        """Valida el campo dirección"""

        if not direccion:
            raise ValueError("Debe ingresar una direccion")
        return direccion

    @validates('nombre')
    def validate_nombre(self, key, nombre):
        """Valida el campo nombre"""

        if not nombre:
            raise ValueError("Debe ingresar un nombre")
        return nombre

    def coordenadas_tolist(self):
        return decodificar(self.coordenadas)
    @classmethod    
    def get_cantidad(self):
        return Recorrido.query.count()
    @classmethod
    def get_recorrido(self, recorrido_id):
        return Recorrido.query.get(recorrido_id)

    @classmethod
    def get_recorridos_busqueda(self, q, criterio_orden, pagina, cant_pagina):
        return Recorrido\
        .query\
        .filter(Recorrido.nombre.contains(q))\
        .order_by(criterio_orden)\
        .paginate(page=pagina, per_page=cant_pagina)

    @classmethod
    def get_recorridos_ordenados_paginados(
        self,
        criterio_orden,
        pagina,
        cant_pagina
        ):
        return Recorrido\
        .query\
        .order_by(criterio_orden)\
        .paginate(page=pagina, per_page=cant_pagina)

    @classmethod
    def get_recorridos_con_filtro(
        self,
        filter_option,
        criterio_orden,
        pagina,
        cant_pagina
    ):
        if filter_option == '1':
            puntos = Recorrido\
            .query\
            .filter(Recorrido.estado == True)\
            .order_by(criterio_orden)\
            .paginate(page=pagina, per_page=cant_pagina)
        else:
            puntos = Recorrido\
            .query\
            .filter(Recorrido.estado == False)\
            .order_by(criterio_orden)\
            .paginate(page=pagina, per_page=cant_pagina)
        return puntos

    @classmethod
    def get_recorridos_paginados(self, page, per_page):
        """Devuelve un paginate object con zonas"""
        return Recorrido.query.paginate(page=page, per_page=per_page)