from flask import render_template, request, jsonify


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return make_response(kwargs,404)

def bad_request(e):
    kwargs = {
        "error_name": "400 Bad Request",
        "error_description": "Error en la consulta HTTP",
    }
    return make_response(kwargs,400)


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return make_response(kwargs,401)

def server_error(e):
    kwargs = {
        "error_name": "500 Internal Server error",
        "error_description": "Ocurrió un error en el servidor",
    }
    return make_response(kwargs, 500)

def created(e):
    kwargs = {
        "error_name": "201 Created",
        "error_description": "El objeto se creó exitosamente",
    }
    return make_response(kwargs, 201)

def make_response(data, status):
    if request.path.startswith("/api/"):
        return jsonify(data), status
    else:
        return render_template("error.html", **data), status
