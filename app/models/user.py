from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import Column, ForeignKey

from app.db import db

""" se corresponde con el table users_roles"""
users_roles= db.Table ('users_roles',
    Column('id_users_roles', db.Integer, primary_key=True),
    Column('user_id' ,db.SmallInteger, ForeignKey('users.id')),
    Column('rol_id', db.SmallInteger, ForeignKey('roles.id')) 
    )

""" se corresponde con el table roles_permisos"""
roles_permisos= db.Table ('roles_permisos',
    Column('id_roles_permisos', db.Integer, primary_key=True),
    Column('rol_id' , db.SmallInteger, ForeignKey('roles.id')),
    Column('permiso_id', db.SmallInteger, ForeignKey('permisos.id')) )

class User(db.Model):
    """Define una entidad de tipo User que se corresponde con el table users"""

    __tablename__ = "users"
    id = Column(SmallInteger, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(30), unique=True)
    password = Column(String(300))
    bloqueado = Column(Boolean, default= False)
    username = Column(String(39),unique = True)
    roles = relationship( "Rol", secondary='users_roles', lazy='subquery', backref=db.backref('users',lazy='subquery'))
    espera= Column(Boolean, default= False)
    
    def __init__(self, username=None,first_name=None, last_name=None, email=None, password=None, espera =False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.bloqueado = False
        self.espera = espera
        self.username = username
    

    @staticmethod
    def get(user_email):
        return User.query.filter(User.email == user_email).first()

    
    @classmethod
    def has_permission(self,user_id, permission):
        user = User.query.filter(User.id==user_id).first()
        permisos = []
        nombres_permisos = []
        for rol in user.roles:
            permisos.append(rol.permisos)
        for a in permisos:
            for permiso in a:
                nombres_permisos.append(permiso.name)

        return permission in nombres_permisos

    @classmethod
    def esta_bloqueado(self, user_id):
        user= User.query.filter(User.id == user_id).first()
        return user.bloqueado

    @classmethod
    def esta_en_espera(self, user_id):
        user= User.query.filter(User.id == user_id).first()
        return user.espera

    @classmethod
    def get_email(self,email):
        return User.query.filter(User.email == email).first()

    @classmethod
    def get_username(self, username):
        return User.query.filter(User.username == username).first()

    @classmethod
    def es_admin(self,user_id):
        user= User.get_user_de_id(user_id)
        for rol in user.roles:
            if rol.name == "administrador":
                return True
        return False
    
    @classmethod
    def get_user_de_id(self, user_id):
        return User.query.filter(User.id == user_id).first()
        
    @classmethod
    def users_por_busqueda(self, q, orden, pagina, cant_paginas):
        return User.query.filter(User.username.contains(q)).order_by(orden.orderBy).paginate(page=pagina,per_page=cant_paginas,error_out=False)  

    @classmethod
    def paginacion(self,orden,pagina,cant_paginas):
        return User.query.order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)

    @classmethod
    def get_users_bloqueados(self,orden,pagina,cant_paginas):
        return User.query.filter(User.bloqueado== True).order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)

    @classmethod
    def get_users_no_bloqueados(self,orden,pagina,cant_paginas):
        return User.query.filter(User.bloqueado== False).order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)

    @classmethod
    def get_users_en_espera(self,orden,pagina,cant_paginas):
        return User.query.filter(User.espera== True).order_by(orden.orderBy).paginate(page=pagina, per_page=cant_paginas)

    @classmethod    
    def allUsers(asd):
        return db.session.query(User).all()

    @classmethod
    def create(cls, conn, data):
        sql = """
            INSERT INTO users (email, password, first_name, last_name)
            VALUES (%s, %s, %s, %s)
        """

        cursor = conn.cursor()
        cursor.execute(sql, list(data.values()))
        conn.commit()
        

        return True

       
                
class Rol(db.Model):
    """Define una entidad de tipo Rol que se corresponde con el table roles"""

    __tablename__ = 'roles'
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(30), unique=True)
    permisos = relationship( "Permiso", secondary='roles_permisos',lazy='subquery', backref=db.backref('roles',lazy='subquery'))


    @classmethod
    def get_roles(self):
        return Rol.query.all()

    @classmethod
    def get_rol(self,rol_id):
        return Rol.query.get(rol_id)

    @classmethod
    def get_rol_admin(self):
        return Rol.query.filter(Rol.name =="administrador").first()

class Permiso(db.Model):
    """Define una entidad de tipo Permiso que se corresponde con el table permisos"""

    __tablename__ = "permisos"
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(30), unique=True)