from sqlalchemy import Column, String, SMALLINT
from app.db import db

class Category(db.Model):
    """Define una entidad de tipo Category que se corresponde con el table categories"""

    __tablename__ = "categories"
    id = Column(SMALLINT, primary_key=True)
    name = Column(String(30), unique=True)

    def __init__(self, name=None):
        self.name = name


    @classmethod
    def get_all(self):
        return Category.query.all()

    @classmethod
    def get_categoria(self,categoria_name):
        return Category.query.filter(Category.name == categoria_name).first()
    
    @classmethod
    def get_categoria_id(self, id_categoria):
        """Devuelve, si existe, el objeto categoria con id=id_categoria"""
        return Category.query.get(id_categoria)

    @classmethod
    def check_id(self, id):
        """Devuelve False si existe una categoria con el id=id"""
        if Category.query.filter_by(id=id).first():
            return False
        else:
            return True