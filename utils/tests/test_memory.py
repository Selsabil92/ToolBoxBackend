import unittest
from app import app

class MemoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_analyze_memory(self):
        response = self.app.get('/memory/analyze')
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.json)
