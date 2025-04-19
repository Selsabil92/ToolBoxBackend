import unittest
from app import app

class TrafficTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_analyze_traffic(self):
        response = self.app.get('/traffic/analyze')
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.json)
