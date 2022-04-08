from flask import abort
from app.models.user import User

def authenticated(session):
    return session.get("user")

def check_permission(user_id, permission):
    return User.has_permission(user_id, permission)

def assert_permission(session, permission):
    if not authenticated(session):
        abort(401)
    if not check_permission(session["user2"].id, permission):
        abort(401)
    if  User.esta_bloqueado(session["user2"].id):
        abort(401)
    if  User.esta_en_espera(session["user2"].id):
        abort(401)