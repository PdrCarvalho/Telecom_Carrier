import unittest
from app import app, db


class TestHomeView(unittest.TestCase):
    app = app.test_client()

    def setUp(self):
        db.drop_all()
        db.create_all()

    def register(self, username, password, role='user'):
        return self.app.post(
            '/register',
            json=dict(username=username, password=password, role=role)
        )

    def login(self, username, password):
        return self.app.post(
            '/login',
            json=dict(username=username, password=password),
        )

    def test_get_unauthorized(self):
        self.response = self.app.get('/')
        self.assertEqual(401, self.response.status_code)

    def test_create_user(self):
        self.response = self.register('test', 'test')
        self.assertTrue(isinstance(self.response.json['id'], int))

    def test_create_same_username(self):
        self.register('same_username', 'same_username')
        self.response = self.register('same_username', 'same_username')
        self.assertEqual(self.response.status_code, 500)

    def test_login(self):
        self.register('user_login', 'user_login')
        self.response = self.login('user_login', 'user_login')
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(bool(self.response.json['access_token']))

    def test_user_authentication(self):
        self.register('authentication', 'authentication')
        self.response = self.login('authentication', 'authentication')
        headers = {'Authorization': 'Bearer ' + self.response.json['access_token']}
        self.response = self.app.get('/', headers=headers)
        self.assertEqual(self.response.status_code, 200)

