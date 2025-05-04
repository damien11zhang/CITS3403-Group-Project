from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
users = {}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_random_secret_key'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import *

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
        rankings = {
            'engineering': int(request.form['engineering']),
            'tech': int(request.form['tech']),
            'social': int(request.form['social']),
            'creative': int(request.form['creative']),
            'business': int(request.form['business']),
            'science': int(request.form['science']),
            'admin': int(request.form['admin']),
            'health': int(request.form['health']),
            'trades': int(request.form['trades']),
            'law': int(request.form['law']),
        }

        if len(set(rankings.values())) < 10:
            return "Please assign a unique rank to each statement!"

        return redirect(url_for('quiz2'))

    return render_template("quiz.html")

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
                    session_id=session.sid,
                    question_type='subgroup',
                    target_id=subgroup_id,
                    score=score
                )
                db.session.add(response)
        db.session.commit()

        return redirect(url_for('quiz3'))

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
