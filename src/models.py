from app import db

import sqlalchemy.types as types
from . import constants


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class BaseModel:
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()


class PhoneNumber(db.Model, BaseModel):
    __tablename__ = 'phone numbers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(), nullable=False)
    monthyPrice = db.Column(db.Float(), nullable=False)
    setupPrice = db.Column(db.Float(), nullable=False)
    currency = db.Column(db.String(), nullable=False)
    saleDate = db.Column(db.Date(), default=None)
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, value, monthyPrice, setupPrice, currency):
        self.value = value
        self.monthyPrice = monthyPrice
        self.setupPrice = setupPrice
        self.currency = currency

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'value': self.value,
            'monthyPrice': self.monthyPrice,
            'setupPrice': self.setupPrice,
            'currency': self.currency
        }


class User(db.Model, BaseModel):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(ChoiceType(choices=constants.ROLES_TYPE), nullable=False, default=constants.ROLES_TYPE.get(1, 1))

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
