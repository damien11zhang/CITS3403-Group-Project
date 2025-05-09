from extensions import db
from datetime import datetime, timezone

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
    job_cluster_id = db.Column(db.Integer, db.ForeignKey('job_clusters.id'), nullable=False)
    subgroup_question = db.Column(db.String(300), nullable=False)
    jobs = db.relationship('Job', backref='subgroup', lazy=True)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroups.id'), nullable=False)
    question_1 = db.Column(db.String(300), nullable=False)
    question_2 = db.Column(db.String(300), nullable=False)

class UserSelectedCluster(db.Model):
    __tablename__ = 'user_selected_clusters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)  # email or guest
    cluster_id = db.Column(db.Integer, db.ForeignKey('job_clusters.id'), nullable=False)

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # 'subgroup', 'first', 'second'
    target_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=True)  # Optional, or link to User
    job_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    question_1 = db.Column(db.String(300), nullable=True)
    question_2 = db.Column(db.String(300), nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class QuizSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(255), unique=True)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)
