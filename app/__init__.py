from os import path, environ
from flask import Flask, render_template, Blueprint, session,url_for, redirect
from os import environ
from flask import Flask, render_template, Blueprint, session
from flask_session import Session
from flask_cors import CORS
from config import config

from app import db
from app.models.colores import Colores

from app.resources import user, puntoEncuentro, configuracion, zonaInundable, issue, denuncia, recorrido

import logging

from app.resources import auth
from app.resources.api.issue import issue_api
from app.resources.api.zonaInundable import zona_api
from app.resources.api.denuncia import denuncia_api
from app.resources.api.puntoEncuentro import puntoEncuentro_api
from app.resources.api.recorridos_evacuacion import recorridos_evacuacion_api
from app.resources.api.estadisticas import estadisticas_api

from app.helpers import handler
from app.helpers import auth as helper_auth
from flask_login import (LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    )

from oauthlib.oauth2 import WebApplicationClient


# GOOGLE Configuration
GOOGLE_CLIENT_ID = '44050287165-rcvai5a3fmnmgv7tuu1ok4kegj62ut1e.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    
    app.secret_key = 'randomsecretkey'

    # OAuth 2 client setup
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    
    login_manager = LoginManager()
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return user.get(user_id)

    env = environ.get("FLASK_ENV", environment)
    if env == 'development':
        app.debug = True
    else:
        app.debug = False

    # Carga de la configuración
    app.config.from_object(config[env])

    #configuración de CORS
    CORS(app)

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=helper_auth.check_permission)
    app.jinja_env.globals.update(get_color_privado=Colores.get_color_privado)
    app.jinja_env.globals.update(get_color_publico=Colores.get_color_publico)

    # Autenticación
    app.add_url_rule("/login-google", "auth_login_with_google", auth.login_with_google)
    app.add_url_rule(
        "/login/callback-google", "auth_callback-google", auth.callback_google, methods=["GET"]
    )
    app.add_url_rule("/espera", "auth_espera", auth.espera)   
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Consultas
    
    app.add_url_rule("/consultas", "issue_index", issue.index, methods=["GET"])
    app.add_url_rule("/consultas", "issue_create", issue.create, methods=["POST"])
    app.add_url_rule("/consultas/nueva", "issue_new", issue.new)

    # Rutas de Admin
    app.add_url_rule("/Configuracion", "config_index", configuracion.conf)
    app.add_url_rule("/Configurado", "configurado", configuracion.configurado, methods=["POST"])
    
    # Rutas de Denuncia
    app.add_url_rule("/denuncias", "denuncia_index", denuncia.index, methods=["POST", "GET"])
    app.add_url_rule("/denuncias/info<int:denuncia_id>", "denuncia_info", denuncia.info, methods=["GET"])
    app.add_url_rule("/denuncias/enCurso", "denuncia_enCurso", denuncia.enCurso, methods=["GET"])
    app.add_url_rule("/denuncias/resuelta", "denuncia_resuelta", denuncia.resuelta, methods=["GET"])
    app.add_url_rule("/denuncias/sinConfirmar", "denuncia_sinConfirmar", denuncia.sinConfirmar, methods=["GET"])
    app.add_url_rule("/denuncias/cerrada", "denuncia_cerrada", denuncia.cerrada, methods=["GET"])
    app.add_url_rule("/denuncias/nuevo", "denuncia_create", denuncia.create, methods=["POST", "GET"])
    app.add_url_rule("/denuncia/confirmar/<int:denuncia_id>", "denuncia_confirmar", denuncia.confirmar, methods=["POST","GET"])
    app.add_url_rule("/denuncia/cerrar/<int:denuncia_id>", "denuncia_cerrar", denuncia.cerrar, methods=["POST","GET"])
    app.add_url_rule("/denuncia/resolver/<int:denuncia_id>", "denuncia_resolver", denuncia.resolver, methods=["POST","GET"])
    app.add_url_rule("/denuncia/delete<int:denuncia_id>", "denuncia_destroy", denuncia.destroy, methods=["POST","GET"])
    app.add_url_rule("/denuncias/editar<int:denuncia_id>", "denuncia_edit", denuncia.update, methods=["POST","GET"])
    app.add_url_rule("/denuncias/seguimiento<int:denuncia_id>", "denuncia_seguimiento", denuncia.seguimiento, methods=["POST","GET"])
    app.add_url_rule("/denuncia/seguimiento_delete<int:seguimiento_id>", "seguimiento_destroy", denuncia.seguimiento_destroy, methods=["POST","GET"])
    app.add_url_rule("/denuncias/seguimiento_editar<int:seguimiento_id>", "seguimiento_edit", denuncia.seguimiento_update, methods=["POST","GET"])

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/espera", "users_espera", user.espera, methods=["GET"])
    app.add_url_rule("/usuarios/bloqueados", "user_bloqueados", user.bloqueados, methods=["GET"])
    app.add_url_rule("/usuarios/nobloqueados", "user_no_bloqueados", user.no_bloqueados, methods=["GET"])
    app.add_url_rule("/usuarios/nuevo", "user_create", user.create, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/delete<int:user_id>", "user_delete", user.delete,methods=["POST","GET"])
    app.add_url_rule("/usuarios/editar<int:user_id>", "user_edit", user.edit,methods=["POST","GET"])
    
    # Rutas de PuntosEncuentro
    app.add_url_rule("/puntosEncuentro", "puntoEncuentro_index", puntoEncuentro.index)
    app.add_url_rule("/puntosEncuentro/ver/<int:id_punto>", "puntoEncuentro_show", puntoEncuentro.show)
    app.add_url_rule("/puntosEncuentro", "puntoEncuentro_create", puntoEncuentro.create, methods=["POST"])
    app.add_url_rule("/puntosEncuentro/nuevo", "puntoEncuentro_new", puntoEncuentro.new)
    app.add_url_rule("/puntosEncuentro/editar/<int:id_punto>", "puntoEncuentro_update", puntoEncuentro.update, methods=["POST","GET"])
    app.add_url_rule("/puntosEncuentro/eliminar/<int:id_punto>", "puntoEncuentro_destroy", puntoEncuentro.destroy, methods=["POST", "GET"])

    # Rutas de Recorridos
    app.add_url_rule("/recorrido", "recorrido_index", recorrido.index)
    app.add_url_rule("/recorrido", "recorrido_create", recorrido.create, methods=["POST"])
    app.add_url_rule("/recorrido/nuevo", "recorrido_new", recorrido.new)
    app.add_url_rule("/recorrido/editar/<int:id_recorrido>", "recorrido_update", recorrido.update, methods=["POST","GET"])
    app.add_url_rule("/recorrido/eliminar/<int:id_recorrido>", "recorrido_destroy", recorrido.destroy, methods=["POST", "GET"])
    app.add_url_rule("/recorrido/ver/<int:id_recorrido>", "recorrido_show", recorrido.show)
    # Rutas de zonas inundables
    app.add_url_rule("/zonasInundables", "zonaInundable_index", zonaInundable.index)
    app.add_url_rule("/zonasInundables/ver/<int:id_zona>", "zonaInundable_show", zonaInundable.show)
    app.add_url_rule("/zonasInundables/importar", "zonaInundable_importar", zonaInundable.importar, methods=["POST","GET"])
    app.add_url_rule("/zonasInundables/eliminar/<int:id_zona>", "zonaInundable_destroy", zonaInundable.destroy, methods=["POST", "GET"])
    app.add_url_rule("/zonasInundables/editar/<int:id_zona>", "zonaInundable_update", zonaInundable.update, methods=["POST", "GET"])


    

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        if helper_auth.authenticated(session):
            color = Colores.get_color_privado()    
            return render_template("home.html",color = color)
        else:
            color = Colores.get_color_publico()    
            return render_template("home.html",color = color)






    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(issue_api)
    api.register_blueprint(zona_api)
    api.register_blueprint(denuncia_api)
    api.register_blueprint(puntoEncuentro_api)
    api.register_blueprint(recorridos_evacuacion_api)
    api.register_blueprint(estadisticas_api)

    app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500
    app.register_error_handler(500, handler.server_error)

    # Retornar la instancia de app configurada
    return app
