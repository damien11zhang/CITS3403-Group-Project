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
    job_cluster_id = db.Column(db.Integer, db.ForeignKey('job_clusters.id'), nullable=False)
    jobs = db.relationship('Job', backref='subgroup', lazy=True)
    subgroup_question = db.Column(db.String(300), nullable=False)  # Shared subgroup question

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroups.id'), nullable=False)
    first_question = db.Column(db.String(300), nullable=False)  # First job-specific question
    second_question = db.Column(db.String(300), nullable=False)  # Second job-specific question

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # 'subgroup', 'first', 'second'
    target_id = db.Column(db.Integer, nullable=False)  # ID of the job or subgroup
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
