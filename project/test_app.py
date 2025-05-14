'''import unittest
import uuid
from app import app, db, User, FriendRequest
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
            user.join_date = datetime.utcnow  # This will now work
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

    def test_send_friend_request(self):
        # Create two users
        user1 = User(id=1, username="user1", email="user1@example.com", password="password")
        user2 = User(id=2, username="user2", email="user2@example.com", password="password")
        with app.app_context():
            db.session.add_all([user1, user2])
            db.session.commit()

        # Log in as user1
        self.client.post('/login', data={'username': 'user1', 'password': 'password'}, follow_redirects=True)

        # Send a friend request to user2
        response = self.client.post(f'/send_friend_request/{user2.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the friend request exists
        with app.app_context():
            friend_request = FriendRequest.query.filter_by(from_user_id=user1.id, to_user_id=user2.id).first()
            self.assertIsNotNone(friend_request)
            self.assertEqual(friend_request.status, 'pending')

    def test_accept_friend_request(self):
        # Create two users
        user1 = User(id=1, username="user1", email="user1@example.com", password="password")
        user2 = User(id=2, username="user2", email="user2@example.com", password="password")
        with app.app_context():
            db.session.add_all([user1, user2])
            db.session.commit()

            # Create a friend request from user1 to user2
            friend_request = FriendRequest(from_user_id=user1.id, to_user_id=user2.id, status='pending')
            db.session.add(friend_request)
            db.session.commit()

        # Log in as user2
        self.client.post('/login', data={'username': 'user2', 'password': 'password'}, follow_redirects=True)

        # Accept the friend request
        response = self.client.post(f'/accept_friend_request/{friend_request.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the friendship exists
        with app.app_context():
            self.assertIn(user1, user2.friends)
            self.assertIn(user2, user1.friends)

if __name__ == '__main__':
    unittest.main()'''

#Only for testing the friend request functionality
import unittest
from app import app, db, User, FriendRequest
from datetime import datetime

class FriendRequestTestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for tests
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        # Create the database schema
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_send_friend_request(self):
        # Create two users
        user1 = User(id=1, username="user1", email="user1@example.com", password="password")
        user2 = User(id=2, username="user2", email="user2@example.com", password="password")
        with app.app_context():
            db.session.add_all([user1, user2])
            db.session.commit()

        # Log in as user1
        self.client.post('/login', data={'username': 'user1', 'password': 'password'}, follow_redirects=True)

        # Send a friend request to user2
        response = self.client.post(f'/send_friend_request/{user2.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the friend request exists
        with app.app_context():
            friend_request = FriendRequest.query.filter_by(from_user_id=user1.id, to_user_id=user2.id).first()
            self.assertIsNotNone(friend_request)
            self.assertEqual(friend_request.status, 'pending')

    def test_accept_friend_request(self):
        # Create two users
        user1 = User(id=1, username="user1", email="user1@example.com", password="password")
        user2 = User(id=2, username="user2", email="user2@example.com", password="password")
        with app.app_context():
            db.session.add_all([user1, user2])
            db.session.commit()

            # Create a friend request from user1 to user2
            friend_request = FriendRequest(from_user_id=user1.id, to_user_id=user2.id, status='pending')
            db.session.add(friend_request)
            db.session.commit()

        # Log in as user2
        self.client.post('/login', data={'username': 'user2', 'password': 'password'}, follow_redirects=True)

        # Accept the friend request
        response = self.client.post(f'/accept_friend_request/{friend_request.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Re-query the users to ensure they are bound to the current session
    with app.app_context():
        user1 = User.query.get(1)
        user2 = User.query.get(2)
        self.assertIn(user1, user2.friends)
        self.assertIn(user2, user1.friends)

if __name__ == '__main__':
    unittest.main()