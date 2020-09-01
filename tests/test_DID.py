import unittest
from app import app, db


class TestHomeView(unittest.TestCase):
    app = app.test_client()
    did_exemplo = {
        "value": "+55 84 91234-4321",
        "monthyPrice": 0.039,
        "setupPrice": 3.40,
        "currency": "U$"
    }

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.register('manager', 'manager', 'manager')
        self.response = self.login('manager', 'manager')
        self.headers_manager = {'Authorization': 'Bearer ' + self.response.json['access_token']}
        self.register('user', 'user', 'user')
        self.response = self.login('user', 'user')
        self.headers_user = {'Authorization': 'Bearer ' + self.response.json['access_token']}

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

    def create_DID(self, DID, headers):
        return self.app.post(
            '/',
            json=dict(value=DID['value'], monthyPrice=DID['monthyPrice'], setupPrice=DID['setupPrice'],
                      currency=DID['currency']),
            headers=headers
        )

    def update_DID(self, DID_id, update_dic, headers):
        return self.app.put(
            f'/{DID_id}',
            json=update_dic,
            headers=headers
        )

    def delete_DID(self, DID_id, headers):
        return self.app.delete(
            f'/{DID_id}',
            headers=headers
        )

    def test_create_authorized_did(self):
        self.response = self.create_DID(DID=self.did_exemplo, headers=self.headers_manager)
        self.assertTrue(isinstance(self.response.json['id'], int))

    def test_create_did_unauthorized(self):
        self.response = self.create_DID(DID=self.did_exemplo, headers=self.headers_user)
        self.assertEqual(self.response.status_code, 401)

    def test_update_authorized_did(self):
        self.response = self.create_DID(DID=self.did_exemplo, headers=self.headers_manager)
        self.response = self.update_DID(DID_id=self.response.json['id'], update_dic=dict(monthyPrice=1.11),
                                        headers=self.headers_manager)
        self.assertEqual(self.response.status_code, 200)

    def test_delete_authorized_did(self):
        self.response = self.create_DID(DID=self.did_exemplo, headers=self.headers_manager)
        self.response = self.delete_DID(DID_id=self.response.json['id'], headers=self.headers_manager)
        self.assertEqual(self.response.status_code, 200)

    def test_update_unauthorized_did(self):
        self.response = self.create_DID(DID=self.did_exemplo, headers=self.headers_manager)
        self.response = self.update_DID(DID_id=self.response.json['id'], update_dic=dict(monthyPrice=1.11),
                                        headers=self.headers_user)
        self.assertEqual(self.response.status_code, 401)

    def test_delete_unauthorized_did(self):
        self.response = self.create_DID(DID=self.did_exemplo, headers=self.headers_manager)
        self.response = self.delete_DID(DID_id=self.response.json['id'], headers=self.headers_user)
        self.assertEqual(self.response.status_code, 401)

    def test_get_authorized_did(self):
        self.response = self.app.get('/', headers=self.headers_user)
        self.assertEqual(self.response.status_code, 200)

    def test_create_negative_money(self):
        did = {
            "value": "+55 84 91234-4321",
            "monthyPrice": -1,
            "setupPrice": -1,
            "currency": "U$"
        }
        self.response = self.create_DID(DID=did, headers=self.headers_manager)
        self.assertEqual(self.response.status_code, 500)

    def test_create_text_money(self):
        did = {
            "value": "+55 84 91234-4321",
            "monthyPrice": 'test',
            "setupPrice": 'test',
            "currency": "U$"
        }
        self.response = self.create_DID(DID=did, headers=self.headers_manager)
        self.assertEqual(self.response.status_code, 500)

    def test_around_money(self):
        did = {
            "value": "+55 84 91234-4321",
            "monthyPrice": 0.0399,
            "setupPrice": 3.401,
            "currency": "U$"
        }
        self.response = self.create_DID(DID=did, headers=self.headers_manager)
        self.assertListEqual([0.04, 3.40], [self.response.json['monthyPrice'], self.response.json['setupPrice']])
