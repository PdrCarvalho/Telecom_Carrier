from functools import wraps

from flask import json
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

from app import jwt, app
from .models import User


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


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    try:
        user = User.query.filter_by(id=identity).first()
        return {'role': user.serialize()['role']}
    except Exception:
        return {'role': 'user'}


def manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'manager':
            return app.response_class(
                response=json.dumps({
                    "description": "Access token not found!"+claims['role'],
                    "error": "unauthorized_loader"
                }),
                status=401,
                mimetype='application/json'
            )
        else:
            return fn(*args, **kwargs)

    return wrapper
