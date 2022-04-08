from sqlalchemy import Column, Integer

from app.db import db


class Elementos(db.Model):
    """Define una entidad de tipo Elementos que se corresponde con el table elementos"""


    __tablename__ = "elementos"
    id = Column(Integer, primary_key=True)
    cant = Column(Integer)

    def __init__(self, cant=None):
        self.cant = cant

    def configurar(numero):
        elem = Elementos.query.first()
        if elem is not None:
            if numero:
                elem.cant = numero
        else:
            elem = Elementos(4)
        db.session.commit()
 
    @classmethod
    def get_elementos(self):
        elem = Elementos.query.first()
        if elem:
            cant_paginas = elem.cant 
        else: #si no hay nada cargado en la db asigna 4 por defecto
            cant_paginas = 4
        return cant_paginas
