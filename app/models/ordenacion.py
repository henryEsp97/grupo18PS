from sqlalchemy import Column, Integer, String

from app.db import db


class Ordenacion(db.Model):
    """Define una entidad de tipo Ordenacion que se corresponde con el table ordenacion"""


    __tablename__ = "ordenacion"
    id = Column(Integer, primary_key=True)
    orderBy = Column(String(50))
    lista = Column(String(50))

    def __init__(self, orderBy=None, lista = None):
        self.orderBy = orderBy
        self.lista = lista

    def configurarOrdenUsuarios(ordenUsers):
        ordenU = Ordenacion.query.filter_by(lista = 'usuarios').first()
        if ordenU is not None: 
            ordenU.orderBy = ordenUsers
        else:
            ordenU = Ordenacion('first_name','usuarios')
            db.session.add(ordenU)
        db.session.commit()

    def configurarOrdenPuntos(ordenPuntos):
        ordenP = Ordenacion.query.filter_by(lista = 'puntos').first()
        if ordenP is not None: 
            ordenP.orderBy = ordenPuntos
        else:
            ordenP = Ordenacion('nombre','puntos')
            db.session.add(ordenP)
        db.session.commit()

    def configurarOrdenDenuncias(ordenDenuncias):
        ordenD = Ordenacion.query.filter_by(lista = 'denuncias').first()
        if ordenD is not None: 
            ordenD.orderBy = ordenDenuncias
        else:
            ordenD = Ordenacion('titulo','denuncias')
            db.session.add(ordenD)
        db.session.commit()    

    @classmethod
    def get_ordenacion_puntos(self):
        orden =  Ordenacion.query.filter_by(lista='puntos').first()
        if not orden:
            orden = Ordenacion('nombre','puntos')
        return orden

    @classmethod
    def get_ordenacion_usuarios(self):
        orden =  Ordenacion.query.filter_by(lista='usuarios').first()
        if not orden:
            orden = Ordenacion('first_name','usuarios')
        return orden    
    @classmethod
    def get_ordenacion_recorridos(self):
        orden =  Ordenacion.query.filter_by(lista='recorridos').first()
        if not orden:
            orden = Ordenacion('nombre','puntos')
        return orden
    @classmethod    
    def get_ordenacion_denuncias(self):
        orden =  Ordenacion.query.filter_by(lista='denuncias').first()
        if not orden:
            orden = Ordenacion('titulo','denuncias')
        return orden

    @classmethod
    def get_ordenacion_zonas(self):
        orden =  Ordenacion.query.filter_by(lista='zonas').first()
        if not orden:
            orden = Ordenacion('nombre','zonas')
        return orden
