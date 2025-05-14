from extensions import db
from datetime import datetime, timezone
from flask_login import UserMixin

friendships = db.Table(
'friendships',
db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    friends = db.relationship(
        'User',
        secondary=friendships,
        primaryjoin=(id == friendships.c.user_id),
        secondaryjoin=(id == friendships.c.friend_id),
        backref='friend_of'
    )

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name='fk_friend_request_from_user'),
        nullable=False
    )
    to_user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name='fk_friend_request_to_user'),
        nullable=False
    )
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined

    from_user = db.relationship('User', foreign_keys=[from_user_id])
    to_user = db.relationship('User', foreign_keys=[to_user_id])

class JobCluster(db.Model):
    __tablename__ = 'job_clusters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    subgroups = db.relationship('Subgroup', backref='job_cluster', lazy=True)

class Subgroup(db.Model):
    __tablename__ = 'subgroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    job_cluster_id = db.Column(
        db.Integer,
        db.ForeignKey('job_clusters.id', name='fk_subgroup_job_cluster'),
        nullable=False
    )
    subgroup_question = db.Column(db.String(300), nullable=False)
    jobs = db.relationship('Job', backref='subgroup', lazy=True)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subgroup_id = db.Column(
        db.Integer,
        db.ForeignKey('subgroups.id', name='fk_job_subgroup'),
        nullable=False
    )
    question_1 = db.Column(db.String(300), nullable=False)
    question_2 = db.Column(db.String(300), nullable=False)

class UserSelectedCluster(db.Model):
    __tablename__ = 'user_selected_clusters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)  # email or guest
    cluster_id = db.Column(
        db.Integer,
        db.ForeignKey('job_clusters.id', name='fk_user_selected_cluster_job_cluster'),
        nullable=False
    )

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.String(100),
        db.ForeignKey('quiz_sessions.session_id', name='fk_user_response_quiz_session'),
        nullable=False
    )
    question_type = db.Column(db.String(50), nullable=False)  # 'subgroup', 'first', 'second'
    target_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class QuizSession(db.Model):
    __tablename__ = 'quiz_sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name='fk_quiz_session_user'),
        nullable=True
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='quiz_sessions')
    responses = db.relationship('UserResponse', backref='quiz_session', lazy=True)