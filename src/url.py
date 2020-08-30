from flask import json

from app import app, jwt
from . import view


@jwt.expired_token_loader
def expired_token_callback():
    response = app.response_class(
        response=json.dumps({
            "description": "Token has expired!",
            "error": "token_expired"
        }),
        status=401,
        mimetype='application/json'
    )
    return response


@jwt.invalid_token_loader
def invalid_token_callback():
    return app.response_class(
        response=json.dumps({
            "description": "Signature verification failed!",
            "error": "invalid_token"
        }),
        status=401,
        mimetype='application/json'
    )


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return app.response_class(
        response=json.dumps({
            "description": "Access token not found!",
            "error": "unauthorized_loader"
        }),
        status=401,
        mimetype='application/json'
    )


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback():
    return app.response_class(
        response=json.dumps({
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token"
        }),
        status=401,
        mimetype='application/json'
    )


app.add_url_rule('/register', 'register_user', view.register_user, methods=['POST'])
app.add_url_rule('/login', 'login_user', view.login_user, methods=['POST'])
app.add_url_rule('/', 'getAll', view.get_all)
app.add_url_rule('/<id_>', 'getid', view.get_by_id)
app.add_url_rule('/', 'add', view.add_phone_number, methods=['POST'])
app.add_url_rule('/<id_>', 'delete', view.delete_phone_number, methods=['DELETE'])
app.add_url_rule('/<id_>', 'update', view.update_phone_number, methods=['PUT'])
