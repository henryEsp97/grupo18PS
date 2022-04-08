from datetime import datetime
from sqlalchemy import Column, String, exc
from sqlalchemy.sql.sqltypes import SMALLINT,  DateTime
from sqlalchemy import Column, ForeignKey
from app.db import db
from app.helpers.codificador import decodificar, codificar


class Denuncia(db.Model):
    """Define una entidad de tipo Denuncia"""

    __tablename__ = "denuncias"
    id = Column(SMALLINT, primary_key=True)
    titulo = Column(String(40), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_cierre = Column(DateTime)
    descripcion = Column(String(500), nullable=False)
    coordenadas = Column(String(200), nullable=False)
    categoria_id = Column(SMALLINT, ForeignKey("categories.id"))
    estado_id = Column(SMALLINT, ForeignKey("statuses.id"))
    asignado_a = Column(SMALLINT, ForeignKey("users.id"))
    apellido_denunciante = Column(String(20), nullable=False)
    nombre_denunciante = Column(String(20), nullable=False)
    telefono_denunciante = Column(String(20), nullable=False)
    email_denunciante = Column(String(30), nullable=False)


    def __init__(
        self, titulo=None,
        fecha_cierre=None,
        descripcion=None,
        coordenadas=None,
        categoria_id=None,
        asignado_a=None,
        apellido_denunciante=None,
        nombre_denunciante=None,
        telefono_denunciante=None,
        email_denunciante=None
        ):
        self.titulo = titulo
        self.fecha_cierre = fecha_cierre
        self.descripcion = descripcion
        self.coordenadas = coordenadas
        self.categoria_id = categoria_id
        self.estado_id = 3
        self.asignado_a = asignado_a
        self.apellido_denunciante = apellido_denunciante
        self.nombre_denunciante = nombre_denunciante
        self.telefono_denunciante = telefono_denunciante
        self.email_denunciante = email_denunciante

    @classmethod
    def create_denuncia(self,
        titulo=None,
        fecha_cierre=None,
        descripcion=None,
        coordenadas=None,
        categoria_id=None,
        asignado_a=None,
        apellido_denunciante=None,
        nombre_denunciante=None,
        telcel_denunciante=None,
        email_denunciante=None
        ):
        coords=codificar(coordenadas)
        new_denuncia = Denuncia(titulo,
            fecha_cierre,
            descripcion,
            coords,
            categoria_id,
            asignado_a,
            apellido_denunciante,
            nombre_denunciante,
            telcel_denunciante,
            email_denunciante
            )
        db.session.add(new_denuncia)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            return e
        return new_denuncia
        
    @classmethod
    def get_cantidad(self):
        return Denuncia.query.count()
    def as_dict(self):
        return {attr.name: getattr(self, attr.name) for attr in self.__table__.columns}

    def coordenadas_tolist(self):
        return decodificar(self.coordenadas) 

    @classmethod
    def get_denuncia(self, denuncia_id):
        return Denuncia.query.get(denuncia_id)

    @classmethod
    def denuncias_por_busqueda(self, q, orden, pagina, cant_paginas):
        return Denuncia.query.filter(Denuncia.titulo.contains(q)).order_by(orden.orderBy).paginate(page=pagina,per_page=cant_paginas,error_out=False)  

    @classmethod
    def denuncias_por_fechas(self, fecha1, fecha2, orden, pagina, cant_paginas):
        return Denuncia.query.filter(Denuncia.fecha_creacion.between(fecha1, fecha2)).order_by(orden.orderBy).paginate(page=pagina,per_page=cant_paginas,error_out=False)

    @classmethod
    def paginacion(self,orden,pagina,cant_paginas):
        return Denuncia.query.order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)

    @classmethod
    def get_denuncias_all(self):
        """Devuelve una lista de todas las denuncias en la db"""
        return Denuncia.query.all()

    @classmethod
    def get_denuncias_sinConfirmar(self,orden,pagina,cant_paginas):
        return Denuncia.query.filter(Denuncia.estado_id == 3).order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)

    @classmethod
    def get_denuncias_enCurso(self,orden,pagina,cant_paginas):
        return Denuncia.query.filter(Denuncia.estado_id == 4).order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)

    @classmethod
    def get_denuncias_resuelta(self,orden,pagina,cant_paginas):
        return Denuncia.query.filter(Denuncia.estado_id == 5).order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)
        
    @classmethod
    def get_denuncias_cerrada(self,orden,pagina,cant_paginas):
        return Denuncia.query.filter(Denuncia.estado_id == 6).order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)

    @classmethod
    def check_titulo(self, titulo):
        """Devuelve False si ya existe una denuncia con el titulo=titulo"""
        if Denuncia.query.filter_by(titulo=titulo).first():
            return False
        else:
            return True


class Seguimiento(db.Model):
    """Define una entidad de tipo Seguimiento"""

    __tablename__ = 'seguimientos'
    id = Column(SMALLINT, primary_key=True)
    denuncia_id = Column(SMALLINT, ForeignKey('denuncias.id', ondelete='CASCADE'))
    descripcion = Column(String(80))
    autor = Column(SMALLINT, ForeignKey("users.id"))
    fecha = Column(DateTime, default=datetime.utcnow)

    def __init__(
        self, descripcion=None,
        denuncia_id=None,
        autor=None,
        ):
        self.descripcion = descripcion
        self.denuncia_id = denuncia_id
        self.autor = autor

    @classmethod
    def get_seguimientos(self, denuncia_id):
        return Seguimiento.query.filter(Seguimiento.denuncia_id==denuncia_id)
    
    @classmethod
    def get_seguimiento(self, seguimiento_id):
        return Seguimiento.query.get(seguimiento_id)
        
