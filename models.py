from app import db


class PhoneNumber(db.Model):
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