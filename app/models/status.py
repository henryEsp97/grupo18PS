from sqlalchemy import Column, String, SMALLINT
from app.db import db

class Status(db.Model):
    """Define una entidad de tipo Status que se corresponde con el table statuses"""

    __tablename__ = "statuses"
    id = Column(SMALLINT, primary_key=True)
    name = Column(String(30), unique=True)

    def __init__(self, name=None):
        self.name = name

    @classmethod
    def get_all(self):
        return Status.query.all()

    @classmethod
    def get_status(self, id_status):
        """Devuelve, si existe, el objeto status con id=id_status"""
        return Status.query.get(id_status)