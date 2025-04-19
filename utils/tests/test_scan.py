import unittest
from app import app

class ScanTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_scan_nmap(self):
        response = self.app.post('/scan/nmap', json={'target': '127.0.0.1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.json)
