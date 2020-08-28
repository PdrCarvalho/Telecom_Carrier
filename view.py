from flask import Flask, request, jsonify, Response, json
import decimal

from models import PhoneNumber
from app import db, app


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
        db.session.add(number)
        db.session.commit()
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
