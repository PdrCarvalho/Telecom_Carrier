import os
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from config import Config
import decimal
app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import url

if __name__ == '__main__':
    app.run()
