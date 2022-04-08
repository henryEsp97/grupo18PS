
from sqlalchemy import Column, String, SmallInteger, Boolean, Text
from sqlalchemy.orm import validates
from app.db import db
from app.helpers.codificador import decodificar


class PuntoEncuentro(db.Model):
    """Define una entidad de tipo Punto de Encuentro"""

    __tablename__ = "puntos_de_encuentro"
    id = Column(SmallInteger, primary_key=True)
    nombre = Column(String(40), unique=True, nullable=False)
    direccion = Column(String(30), unique=True, nullable=False)
    coordenadas = Column(Text)
    estado = Column(Boolean)
    telefono = Column(String(30))
    email = Column(String(40))

    def __init__(
        self, nombre=None,
        direccion=None,
        coordenadas=None,
        estado=None,
        telefono=None,
        email=None
        ):
        self.nombre = nombre
        self.direccion = direccion
        self.coordenadas = coordenadas
        self.estado = estado
        self.telefono = telefono
        self.email = email

    def coordenadas_tolist(self):
        return decodificar(self.coordenadas)

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

    @validates('email')
    def validate_email(self, key, email):
        """Valida el campo email"""

        if email and '@' not in email:
            raise ValueError("Ingrese un mail válido")
        return email

    @classmethod
    def get_cantidad(self):
        return PuntoEncuentro.query.count()
    @classmethod
    def get_punto(self, punto_id):
        return PuntoEncuentro.query.get(punto_id)

    @classmethod
    def get_puntos_busqueda(self, q, criterio_orden, pagina, cant_pagina):
        return PuntoEncuentro\
        .query\
        .filter(PuntoEncuentro.nombre.contains(q))\
        .order_by(criterio_orden)\
        .paginate(page=pagina, per_page=cant_pagina)

    @classmethod
    def get_puntos_ordenados_paginados(
        self,
        criterio_orden,
        pagina,
        cant_pagina
        ):
        return PuntoEncuentro\
        .query\
        .order_by(criterio_orden)\
        .paginate(page=pagina, per_page=cant_pagina)

    @classmethod
    def get_puntos_con_filtro(
        self,
        filter_option,
        criterio_orden,
        pagina,
        cant_pagina
    ):
        if filter_option == '1':
            puntos = PuntoEncuentro\
            .query\
            .filter(PuntoEncuentro.estado == True)\
            .order_by(criterio_orden)\
            .paginate(page=pagina, per_page=cant_pagina)
        else:
            puntos = PuntoEncuentro\
            .query\
            .filter(PuntoEncuentro.estado == False)\
            .order_by(criterio_orden)\
            .paginate(page=pagina, per_page=cant_pagina)
        return puntos

    @classmethod
    def get_puntos_paginados(self, page, per_page):
        """Devuelve un paginate object con zonas"""
        return PuntoEncuentro.query.paginate(page=page, per_page=per_page)

    def as_dict(self):
        return {
            attr.name: getattr(self, attr.name) for attr in self.__table__.columns
         }