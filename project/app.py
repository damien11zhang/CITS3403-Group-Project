from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from uuid import uuid4

from extensions import db  # <--- new way
from models import *

app = Flask(__name__)
users = {}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_random_secret_key'

db.init_app(app)  # <--- wajib!
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/support')
def support():
    return render_template("support.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users and check_password_hash(users[email]['password'], password):
            session['user_id'] = email
            session['username'] = users[email]['username']
            flash('Login successful!')
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password')
    
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('All fields are required')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('signup.html')
        
        if email in users:
            flash('Email already registered')
            return render_template('signup.html')
        
        users[email] = {
            'username': username,
            'password': generate_password_hash(password)
        }
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    
    return render_template("signup.html")

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile')
        return redirect(url_for('login'))
    
    return render_template("profile.html", username=session.get('username'))

import uuid

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        selected = request.form.getlist('selected_clusters')
        if len(selected) != 3:
            return "Please select exactly 3 clusters."

        # Generate a unique session ID for this user if not already present
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            print(f"=== NEW SESSION ID CREATED: {session['session_id']} ===")

        # Save selected clusters to session
        session['selected_clusters'] = selected
        return redirect(url_for('quiz2'))

    clusters = JobCluster.query.all()
    print("=== DEBUG: CLUSTERS LOADED ===")
    for c in clusters:
        print(f"{c.id} - {c.name} - {c.description}")
    print("==============================")

    return render_template("quiz.html", clusters=clusters)

@app.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    selected_ids = session.get('selected_clusters', [])

    if not selected_ids:
        return redirect(url_for('quiz'))

    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('score_'):
                subgroup_id = int(key.split('_')[1])
                score = int(value)

                response = UserResponse(
                    session_id=session['session_id'],
                    question_type='subgroup',
                    target_id=subgroup_id,
                    score=score
                )
                db.session.add(response)

        db.session.commit()
        return redirect(url_for('quiz_stage3'))

    subgroups = Subgroup.query.filter(Subgroup.job_cluster_id.in_(selected_ids)).all()
    return render_template('quiz2.html', subgroups=subgroups)

@app.route('/quiz3', methods=['GET', 'POST'])
def quiz_stage3():
    if request.method == 'POST':
        passing_jobs = []
        job_scores = {}

        for key, value in request.form.items():
            if key.startswith('job_q1_'):
                job_id = int(key.split('_')[2])
                score = int(value)

                # Save Q1 response
                db.session.add(UserResponse(
                    session_id=session['session_id'],
                    question_type='first',
                    target_id=job_id,
                    score=score
                ))

                # Get subgroup score from previous stage
                job = Job.query.get(job_id)
                subgroup_score = db.session.query(UserResponse).filter_by(
                    session_id=session['session_id'],
                    question_type='subgroup',
                    target_id=job.subgroup_id
                ).first()

                total_score = score + (subgroup_score.score if subgroup_score else 0)
                job_scores[str(job_id)] = total_score  # Must store str keys in session

                if score >= 4:
                    passing_jobs.append(job_id)

        db.session.commit()
        session['job_scores'] = job_scores
        session['passing_jobs'] = passing_jobs

        return redirect(url_for('quiz_stage4'))

    # Get subgroups that passed stage 2
    subgroup_responses = UserResponse.query.filter_by(
        session_id=session['session_id'],
        question_type='subgroup'
    ).all()

    passing_subgroup_ids = [res.target_id for res in subgroup_responses if res.score >= 5]
    jobs = Job.query.filter(Job.subgroup_id.in_(passing_subgroup_ids)).all()

    return render_template('quiz3.html', jobs=jobs)
@app.route('/quiz4', methods=['GET', 'POST'])
def quiz_stage4():
    if request.method == 'POST':
        job_scores = session.get('job_scores', {})  # job_id: subgroup + Q1 score
        final_scores = {}

        for key, value in request.form.items():
            if key.startswith('job_q2_'):
                job_id = int(key.split('_')[2])
                q2_score = int(value)

                db.session.add(UserResponse(
                    session_id=session['session_id'],
                    question_type='second',
                    target_id=job_id,
                    score=q2_score
                ))

                total = job_scores.get(str(job_id), 0) + q2_score
                final_scores[job_id] = total

        db.session.commit()

        # Store top 5 jobs
        top_jobs = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        session['top_jobs'] = [job_id for job_id, score in top_jobs]

        return redirect(url_for('results'))

    passing_jobs = session.get('passing_jobs', [])
    jobs = Job.query.filter(Job.id.in_(passing_jobs)).all()

    return render_template('quiz4.html', jobs=jobs)

@app.route('/results')
def results():
    return render_template("results.html")

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
