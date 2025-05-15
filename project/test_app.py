import unittest
import uuid
from app import app, db, User
from flask import session
from datetime import datetime

class CareerCompassTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        self.username = f"user_{uuid.uuid4().hex[:8]}"
        self.email = f"{self.username}@test.com"
        self.password = "testpass123"

        # Register user
        self.client.post('/signup', data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'confirm_password': self.password
        }, follow_redirects=True)

        # Manually set join_date if needed
        with app.app_context():
            user = User.query.filter_by(username=self.username).first()
            user.join_date = datetime.utcnow()
            db.session.commit()

    def test_signup(self):
        new_email = f"{uuid.uuid4().hex[:8]}@test.com"
        response = self.client.post('/signup', data={
            'username': 'testuser',
            'email': new_email,
            'password': 'abc123',
            'confirm_password': 'abc123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_signup_existing_email(self):
        response = self.client.post('/signup', data={
            'username': 'anyuser',
            'email': self.email,  # already used
            'password': 'abc123',
            'confirm_password': 'abc123'
        }, follow_redirects=True)
        self.assertIn(b'Email already registered', response.data)

    def test_login(self):
        response = self.client.post('/login', data={
            'username': self.username,
            'password': self.password
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CareerCompass', response.data)

    def test_login_wrong_password(self):
        response = self.client.post('/login', data={
            'username': self.username,
            'password': 'wrongpass'
        }, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_quiz_stage1_flow(self):
        self.client.post('/login', data={
            'username': self.username,
            'password': self.password
        }, follow_redirects=True)

        # Access quiz stage 1
        response = self.client.get('/quiz', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select your interests', response.data)

        # Submit 3 clusters
        response = self.client.post('/quiz', data={
            'selected_clusters': ['Health & Care', 'Social & People', 'Science & Tech']
        }, follow_redirects=True)
        self.assertIn(b'Quiz Stage 2', response.data)

    def test_full_quiz_flow(self):
        self.client.post('/login', data={
            'username': self.username,
            'password': self.password
        }, follow_redirects=True)

        # Stage 1
        self.client.post('/quiz', data={
            'selected_clusters': ['Health & Care', 'Social & People', 'Science & Tech']
        }, follow_redirects=True)

        # Stage 2
        self.client.post('/quiz2', data={
            'question_1': '5',
            'question_2': '4',
            'question_3': '3',
            'question_4': '2',
            'question_5': '1'
        }, follow_redirects=True)

        # Stage 3
        self.client.post('/quiz3', data={
            'question_6': '4',
            'question_7': '3',
            'question_8': '2',
            'question_9': '5',
            'question_10': '1'
        }, follow_redirects=True)

        # Stage 4
        response = self.client.post('/quiz4', data={
            'question_11': '3',
            'question_12': '2',
            'question_13': '1',
            'question_14': '4',
            'question_15': '5'
        }, follow_redirects=True)

        self.assertIn(b'Results', response.data)

if __name__ == '__main__':
    unittest.main()
