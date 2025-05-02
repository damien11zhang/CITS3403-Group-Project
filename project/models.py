from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy
from app import db

class JobCluster(db.Model):
    __tablename__ = 'job_clusters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    subgroups = db.relationship('Subgroup', backref='job_cluster', lazy=True)

class Subgroup(db.Model):
    __tablename__ = 'subgroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(300), nullable=False)
    job_cluster_id = db.Column(db.Integer, db.ForeignKey('job_clusters.id'), nullable=False)
    jobs = db.relationship('Job', backref='subgroup', lazy=True)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    question_1 = db.Column(db.String(300), nullable=False)
    question_2 = db.Column(db.String(300), nullable=False)
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroups.id'), nullable=False)

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)  # To track users anonymously
    question_type = db.Column(db.String(50), nullable=False)  # e.g., 'subgroup', 'job_q1', 'job_q2'
    target_id = db.Column(db.Integer, nullable=False)  # ID of the subgroup/job
    score = db.Column(db.Integer, nullable=False)  # Score out of 10
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
