import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_homepage_redirects_to_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b"Login", response.data)

    @unittest.skip("Login belum selesai, skip dulu")
    def test_access_quiz(self):
        response = self.client.get('/quiz', follow_redirects=True)
        self.assertIn(b"Select 3 Statements", response.data)

if __name__ == '__main__':
    unittest.main() 