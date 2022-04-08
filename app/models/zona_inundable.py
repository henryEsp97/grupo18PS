from sqlalchemy import Column, String, SmallInteger, Boolean, Text
from sqlalchemy import exc
from app.db import db
from app.helpers.codificador import decodificar

class ZonaInundable(db.Model):
    """Define una entidad de zona inundable"""

    __tablename__ = "Zonas_inundables"
    id = Column(SmallInteger, primary_key=True)
    codigo = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(30), unique=True, nullable=False)
    coordenadas = Column(Text,nullable=False)
    estado = Column(Boolean)
    color = Column(String(15))

    def __init__(self, codigo=None, nombre=None, coordenadas=None, estado=None, color=None):
        self.codigo = codigo
        self.nombre = nombre
        self.coordenadas = coordenadas
        self.estado = estado
        self.color = color

    def coordenadas_tolist(self):
        return decodificar(self.coordenadas)

    @classmethod
    def get_cantidad(self):
        return ZonaInundable.query.count()
    @classmethod
    def get_zonas(self):
        """Devuelve una lista de todas las zonas en la db"""
        return ZonaInundable.query.all()

    @classmethod
    def get_zonas_paginadas(self, page, per_page):
        """Devuelve un paginate object con zonas"""
        return ZonaInundable.query.paginate(page=page, per_page=per_page)

    @classmethod
    def get_zona(self, id_zona):
        """Devuelve, si existe, el objeto zona con id=id_zona"""
        return ZonaInundable.query.get(id_zona)

    @classmethod
    def get_zonas_busqueda(self, q, criterio_orden, pagina, cant_pagina):
        """Devuelve un objeto paginate con las zonas filtradas por búsqueda de nombre"""
        return ZonaInundable\
        .query\
        .filter(ZonaInundable.nombre.contains(q))\
        .order_by(criterio_orden)\
        .paginate(page=pagina, per_page=cant_pagina)

    @classmethod
    def get_zonas_ordenados_paginados(
        self,
        criterio_orden,
        pagina,
        cant_pagina
        ):
        """Devuelve un objeto paginate con las zonas ordenadas por el criterio pasado como parámetro"""
        return ZonaInundable\
        .query\
        .order_by(criterio_orden)\
        .paginate(page=pagina, per_page=cant_pagina)

    @classmethod
    def get_zonas_con_filtro(
        self,
        filter_option,
        criterio_orden,
        pagina,
        cant_pagina
    ):
        """Devuelve un objeto paginate con las zonas filtradas por estado"""
        if filter_option == '1':
            zonas = ZonaInundable\
            .query\
            .filter(ZonaInundable.estado == True)\
            .order_by(criterio_orden)\
            .paginate(page=pagina, per_page=cant_pagina)
        else:
            zonas = ZonaInundable\
            .query\
            .filter(ZonaInundable.estado == False)\
            .order_by(criterio_orden)\
            .paginate(page=pagina, per_page=cant_pagina)
        return zonas

    @classmethod
    def check_codigo(self, cod):
        """Devuelve false si ya existe una zona con el codigo=cod"""
        if ZonaInundable.query.filter_by(codigo=cod).first():
            return False
        else:
            return True

    @classmethod
    def check_zona(self, nombre):
        """Devuelve False si ya existe una zona con el nombre=nombre"""
        if ZonaInundable.query.filter_by(nombre=nombre).first():
            return False
        else:
            return True

    @classmethod
    def create_zona(self, codigo=None, nombre=None, coordenadas=None, estado=0, color="#fb3715"):
        """Crea una zona"""
        new_zona = ZonaInundable(codigo, nombre, coordenadas, estado, color)
        db.session.add(new_zona)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            return e

    @classmethod
    def update_zona(self, codigo=None, nombre=None, coordenadas=None, estado=None, color=None):
        """Actualiza la zona con nombre=nombre"""
        zona = ZonaInundable.query.filter_by(nombre=nombre).first()
        if zona:
            if codigo:
                zona.codigo = codigo
            if nombre:
                zona.nombre = nombre
            if coordenadas:
                zona.coordenadas = coordenadas
            if estado:
                zona.estado = estado
            if color:
                zona.color = color
            try:
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                return e

    @classmethod
    def delete_zona(self, id_zona):
        """Elimina la zona con id=id_zona"""
        zona = ZonaInundable.get_zona(id_zona)
        db.session.delete(zona)
        db.session.commit()