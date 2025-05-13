import unittest
import uuid
from app import app, db, User
from datetime import datetime

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        unique_id = str(uuid.uuid4())[:8]
        self.username = f"testuser_{unique_id}"
        self.password = "testpass"
        self.email = f"{self.username}@example.com"

        self.client.post('/signup', data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'confirm_password': self.password
        }, follow_redirects=True)

        with app.app_context():
            user = User.query.filter_by(username=self.username).first()
            user.join_date = datetime.utcnow()
            db.session.commit()

    def login(self):
        return self.client.post('/login', data={
            'username': self.username,
            'password': self.password
        }, follow_redirects=True)

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login to Your Account", response.data)

    def test_homepage_redirects_to_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b"Login", response.data)

    def test_select_3_clusters(self):
        self.login()
        response = self.client.post('/quiz', data={
            'selected_clusters': ['1', '2', '3']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"slider", response.data.lower())

    def test_profile_page_loads(self):
        self.login()
        response = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b"Welcome", response.data)
        self.assertIn(self.username.encode(), response.data)

if __name__ == '__main__':
    unittest.main()
