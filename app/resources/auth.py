from flask import redirect, render_template, request, url_for, session, flash
from app.db import db
from app.models.user import User
from app.models.colores import Colores
from werkzeug.security import check_password_hash
from app.helpers.auth import assert_permission
# Import our oauth object from our app

import requests
from oauthlib.oauth2 import WebApplicationClient

import json

# Configuration
GOOGLE_CLIENT_ID = '44050287165-rcvai5a3fmnmgv7tuu1ok4kegj62ut1e.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def login_with_google():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://admin-grupo18.proyecto2021.linti.unlp.edu.ar/login/callback-google",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

# @app.route("/login/callback_google")
def callback_google():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    

    # Doesn't exist? Add it to the database.
    user =User.get(users_email)
    if  user is None:
        new_user = User(
         username=users_name, email=users_email, espera=True
        )
        db.session.add(new_user)
        db.session.commit()

        if User.esta_en_espera(new_user.id):
            error= "Se registro el usuario exitosamente, espere a que el administrador habilite su cuenta"
            flash(error)
            return redirect(url_for("auth_login"))
        else:
             #login
            session.clear()
            session["user"] = new_user.email
            session["user2"] = new_user
    else:
        
        if  User.esta_bloqueado(user.id):
            error= "Usuario bloqueado no puede iniciar sesion"
            flash(error)
            return redirect(url_for("auth_login"))
        elif  User.esta_en_espera(user.id):
            error= "Usuario en espera no puede iniciar sesion"
            flash(error)
            return redirect(url_for("auth_login"))
        else:
            #login
            session.clear()
            session["user"] = user.email
            session["user2"] = user


    # Send user back to homepage
    return redirect(url_for("home"))



def espera():
    return render_template("espera.html")


def login():
    colores = Colores.query.first()
    color = "default"
    if colores is not None:
        color = colores.publico
    return render_template("auth/login.html", color = color)


def authenticate():
    
    params = request.form

    user = db.session.query(User).filter(
        User.email==params["email"]
    ).first()
    error = None
    if not user:
        user = db.session.query(User).filter(
            User.username==params["email"]
        ).first()
        if not user:
            error= "Usuario y/o clave incorrecto."
            flash(error)
            return redirect(url_for("auth_login"))

    if not check_password_hash(user.password, params["password"]):
        error= "Usuario y/o clave incorrecto."
        flash(error)
        return redirect(url_for("auth_login"))  
             
    if user.bloqueado == True:
        error= "Usuario bloqueado no puede iniciar sesion"
        flash(error)
        return redirect(url_for("auth_login"))   

    if error is None:
        session.clear()
        session["user"] = user.email
        session["user2"] = user
        flash("La sesión se inició correctamente.")
        return redirect(url_for("home"))
    


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))


