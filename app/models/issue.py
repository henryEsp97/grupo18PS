from sqlalchemy import Column, Integer, String, ForeignKey, SMALLINT
from sqlalchemy.orm import relationship

from app.db import db
from app.models.category import Category
from app.models.status import Status
class Issue(db.Model):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True)
    email = Column(String(30), unique=True)
    description = Column(String(30), unique=True)
    category_id = Column(SMALLINT, ForeignKey("categories.id"))
    category = relationship(Category)
    status_id = Column(SMALLINT, ForeignKey("statuses.id"))
    status = relationship(Status)

    def __init__(self, email=None, description=None, status_id=None, category_id=None): 
        self.email = email
        self.description = description
        self.status_id = status_id
        self.category_id = category_id
