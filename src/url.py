from flask import json

from app import app, jwt
from . import view


app.add_url_rule('/register', 'register_user', view.register_user, methods=['POST'])
app.add_url_rule('/login', 'login_user', view.login_user, methods=['POST'])
app.add_url_rule('/', 'getAll', view.get_all)
app.add_url_rule('/<id_>', 'getid', view.get_by_id)
app.add_url_rule('/', 'add', view.add_phone_number, methods=['POST'])
app.add_url_rule('/<id_>', 'delete', view.delete_phone_number, methods=['DELETE'])
app.add_url_rule('/<id_>', 'update', view.update_phone_number, methods=['PUT'])
