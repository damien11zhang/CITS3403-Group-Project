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

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        selected = request.form.getlist('selected_clusters')
        if len(selected) != 3:
            flash("Please select exactly 3 clusters.")
            return redirect(url_for('quiz'))

        user_id = session.get('user_id') or "guest"

        for cid in selected:
            db.session.add(UserSelectedCluster(user_id=user_id, cluster_id=int(cid)))
        db.session.commit()

        session['selected_clusters'] = [int(cid) for cid in selected]
        session['session_id'] = str(uuid4())

        return redirect(url_for('quiz2'))

    clusters = JobCluster.query.all()
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

        return redirect(url_for('results'))

    subgroups = Subgroup.query.filter(Subgroup.job_cluster_id.in_(selected_ids)).all()
    return render_template('quiz2.html', subgroups=subgroups)

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
