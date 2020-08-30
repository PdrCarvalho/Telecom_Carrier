import hashlib

from flask import request, json
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, \
    fresh_jwt_required
import decimal

from src.models import PhoneNumber, User
from app import db, app
from . import constants
from .permissions import manager_required

# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     return {
#         'hello': identity,
#         'foo': ['bar', 'baz']
#     }


@manager_required
def add_phone_number():
    value = request.json.get('value', None)
    monthyPrice = decimal.Decimal(request.json.get('monthyPrice', None))
    setupPrice = decimal.Decimal(request.json.get('setupPrice', None))
    currency = request.json.get('currency', None)
    if not bool(value and monthyPrice and setupPrice and currency):
        response = app.response_class(
            response=json.dumps({'error': 'validation error'}),
            status=500,
            mimetype='application/json'
        )
        return response
    try:
        number = PhoneNumber(
            value=value,
            monthyPrice=monthyPrice,
            setupPrice=setupPrice,
            currency=currency
        )
        number.save_to_db()
        data = json.dumps(number.serialize())
        response = app.response_class(
            response=data,
            status=201,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        response = app.response_class(
            response=json.dumps({'error': e}),
            status=500,
            mimetype='application/json'
        )
        return response


def get_all():
    try:
        numbers = PhoneNumber.query.filter_by(active=True)
        data = json.dumps([e.serialize() for e in numbers])
        response = app.response_class(
            response=data,
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        response = app.response_class(
            response=json.dumps({'error': e}),
            status=500,
            mimetype='application/json'
        )
        return response


@fresh_jwt_required
def get_by_id(id_):
    try:
        number = PhoneNumber.query.filter_by(id=id_, active=True).first()
        if number:
            data = json.dumps(number.serialize())
            response = app.response_class(
                response=data,
                status=200,
                mimetype='application/json'
            )
            return response
        response = app.response_class(
            response=json.dumps({'error': 'Number not exist'}),
            status=404,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        response = app.response_class(
            response=json.dumps({'error': e}),
            status=500,
            mimetype='application/json'
        )
        return response


@manager_required
def delete_phone_number(id_):
    try:
        number = PhoneNumber.query.filter_by(id=id_, active=True).first()
        if number:
            number.active = False
            db.session.commit()
            response = app.response_class(
                response=json.dumps({'msg': 'Deleted'}),
                status=200,
                mimetype='application/json'
            )
            return response
        response = app.response_class(
            response=json.dumps({'error': 'Number not exist'}),
            status=404,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        response = app.response_class(
            response=json.dumps({'error': e}),
            status=500,
            mimetype='application/json'
        )
        return response


@manager_required
def update_phone_number(id_):
    update_labels = ['value', 'monthyPrice', 'setupPrice', 'currency']
    update = {}
    for label in update_labels:
        item = request.json.get(label, None)
        if item:
            update[label] = item
    try:
        number = PhoneNumber.query.filter_by(id=id_, active=True).first()
        if number:
            for label, item in update.items():
                setattr(number, label, item)
            db.session.commit()
            data = json.dumps(number.serialize())
            response = app.response_class(
                response=data,
                status=200,
                mimetype='application/json'
            )
            return response
        response = app.response_class(
            response=json.dumps({'error': 'Number not exist'}),
            status=404,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        response = app.response_class(
            response=json.dumps({'error': e}),
            status=500,
            mimetype='application/json'
        )
        return response


def register_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    role = request.json.get('role', None)
    if not role:
        role = constants.ROLES_TYPE[constants.USER]
    if not username or not password or role not in constants.ROLES_TYPE.values():
        response = app.response_class(
            response=json.dumps({'error': 'validation error'}),
            status=500,
            mimetype='application/json'
        )
        return response
    if bool(User.query.filter_by(username=username).first()):
        response = app.response_class(
            response=json.dumps({'error': 'User already exists'}),
            status=500,
            mimetype='application/json'
        )
        return response
    try:
        user = User(username=username, password=hashlib.sha256(password.encode("utf-8")).hexdigest(), role=role)
        user.save_to_db()
        data = json.dumps(user.serialize())
        response = app.response_class(
            response=data,
            status=201,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        response = app.response_class(
            response=json.dumps({'error': e.__str__()}),
            status=500,
            mimetype='application/json'
        )
        return response


def login_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        response = app.response_class(
            response=json.dumps({'error': 'Send username and password.'}),
            status=500,
            mimetype='application/json'
        )
        return response
    user = User.query.filter_by(username=username).first()
    if user and user.password == hashlib.sha256(password.encode("utf-8")).hexdigest():
        access_token = create_access_token(identity=user.id, fresh=True)  # Puts User ID as Identity in JWT
        refresh_token = create_refresh_token(identity=user.id)
        data = json.dumps({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.serialize()
        })
        response = app.response_class(
            response=data,
            status=200,
            mimetype='application/json'
        )
        return response
    response = app.response_class(
        response=json.dumps({'error': 'The password entered is incorrect.'}),
        status=500,
        mimetype='application/json'
    )
    return response


@jwt_refresh_token_required
def refresh():
    current_user_id = get_jwt_identity()  # Gets Identity from JWT
    new_token = create_access_token(identity=current_user_id, fresh=False)
    data = json.dumps({
        'access_token': new_token,
    })
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response
