# filepath: /Users/dame/Desktop/CITS3403-Group-Project/project/tests/test_friends.py
import pytest
from project.models import User, FriendRequest
from project.extensions import db

def test_send_friend_request(client, db):
    # Create two users
    user1 = User(username="user1", email="user1@example.com", password="password")
    user2 = User(username="user2", email="user2@example.com", password="password")
    db.session.add_all([user1, user2])
    db.session.commit()

    # Log in as user1
    client.post('/login', data={'email': 'user1@example.com', 'password': 'password'})

    # Send a friend request to user2
    response = client.post(f'/send_friend_request/{user2.id}', follow_redirects=True)
    assert response.status_code == 200

    # Check that the friend request exists
    friend_request = FriendRequest.query.filter_by(from_user_id=user1.id, to_user_id=user2.id).first()
    assert friend_request is not None
    assert friend_request.status == 'pending'