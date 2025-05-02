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
    questions = db.relationship('Question', backref='subgroup', lazy=True)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroups.id'), nullable=False)
    questions = db.relationship('Question', backref='job', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'first', 'second', or 'subgroup'
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)
    subgroup_id = db.Column(db.Integer, db.ForeignKey('subgroups.id'), nullable=True)

class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)  # ID of job or subgroup
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
