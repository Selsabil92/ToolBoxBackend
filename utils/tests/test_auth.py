import unittest
from app import app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_login(self):
        response = self.app.post('/auth/login', json={'email': 'selsabil.guennouni@supdevinci_edu.fr', 'password': 'ProjetCyber'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
