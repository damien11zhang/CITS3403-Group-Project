from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from uuid import uuid4
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_wtf import CSRFProtect
from collections import defaultdict
from forms import LoginForm, SignupForm
from extensions import db  # <--- new way
from models import User, JobCluster, Subgroup, Job, UserResponse, QuizSession, Suggestion, FriendRequest, SharedResult
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_random_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app) 

db.init_app(app)  
migrate = Migrate(app, db)

def validate_quiz_session():
    """Helper function to validate if a quiz session exists."""
    if 'session_id' not in session:
        flash("Please start the quiz first.", "warning")
        return False
    return True

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    if request.method == 'POST':
        suggestion = Suggestion(
            user_id=session.get('user_id', 'guest'),
            job_title=request.form['job_title'],
            description=request.form.get('description'),
            question_1=request.form.get('question_1'),
            question_2=request.form.get('question_2')
        )
        db.session.add(suggestion)
        db.session.commit()
        flash("Thanks for your suggestion!")
        return redirect(url_for('suggest'))

    return render_template('suggest.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            print("Password matched!")
            login_user(user)
            session['user_id'] = user.id

            if 'session_id' in session:
                return redirect(url_for('quiz4'))
            else:
                return redirect(url_for('profile'))
        else:
            print("Login failed.")
            flash('Invalid username or password.')

    return render_template('login.html', form=form)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered')
            return render_template('signup.html', form=form)

        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    recent_session = QuizSession.query.filter_by(user_id=current_user.id).order_by(QuizSession.created_at.desc()).first()

    top_jobs = []
    if recent_session:
        user_responses = UserResponse.query.filter_by(session_id=recent_session.session_id, question_type='second').all()
        job_scores = {response.target_id: response.score for response in user_responses}
        sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        top_jobs = [(Job.query.get(job_id), score) for job_id, score in sorted_jobs]

    friend_requests = FriendRequest.query.filter_by(to_user_id=current_user.id).all()

    shared_results = SharedResult.query.filter_by(shared_with_id=current_user.id).all()
    shared_sessions = [
        QuizSession.query.get(shared.quiz_session_id) for shared in shared_results
    ]
    return render_template(
        'profile.html',
        user=current_user,
        top_jobs=top_jobs,
        friend_requests=friend_requests,
        quiz_sessions=current_user.quiz_sessions,
        shared_sessions=shared_sessions
    )

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_profile_pic', methods=['POST'])
@login_required
def upload_profile_pic():
    if 'profile_pic' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('profile'))

    file = request.files['profile_pic']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('profile'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Update the user's profile picture in the database
        current_user.profile_pic = filename
        db.session.commit()

        flash('Profile picture updated successfully!', 'success')
        return redirect(url_for('profile'))

    flash('Invalid file type. Please upload an image file.', 'danger')
    return redirect(url_for('profile'))

import uuid

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Clear all previous quiz-related session data
        for key in ['session_id', 'selected_clusters', 'asked_subgroups',
                    'job_scores', 'passing_jobs', 'top_jobs']:
            session.pop(key, None)

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
    if not validate_quiz_session():
        return redirect(url_for('quiz'))

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
        return redirect(url_for('quiz3'))

    # Load all subgroups for selected clusters
    subgroups = Subgroup.query.filter(Subgroup.job_cluster_id.in_(selected_ids)).all()
    return render_template('quiz2.html', subgroups=subgroups)

@app.route('/quiz3', methods=['GET', 'POST'])
def quiz3():
    if not validate_quiz_session():
        return redirect(url_for('quiz'))

    session_id = session.get('session_id')

    # Filter valid subgroups (score >= 5)
    subgroup_responses = UserResponse.query.filter_by(
        session_id=session_id,
        question_type='subgroup'
    ).all()

    passing_subgroup_ids = [res.target_id for res in subgroup_responses if res.score >= 5]

    if request.method == 'POST':
        job_scores = {}
        passing_jobs = []

        for key, value in request.form.items():
            if key.startswith('job_q1_'):
                job_id = int(key.split('_')[2])
                score = int(value)

                db.session.add(UserResponse(
                    session_id=session_id,
                    question_type='first',
                    target_id=job_id,
                    score=score
                ))

                job = Job.query.get(job_id)

                if job.subgroup_id in passing_subgroup_ids:
                    subgroup_score = next(
                        (res.score for res in subgroup_responses if res.target_id == job.subgroup_id),
                        0
                    )
                    total_score = subgroup_score + score
                    job_scores[str(job_id)] = total_score

                    if score >= 4:
                        passing_jobs.append(job_id)

        db.session.commit()
        session['job_scores'] = job_scores
        session['passing_jobs'] = passing_jobs

        return redirect(url_for('quiz4'))

    # On GET: Show only jobs from passing subgroups
    jobs = Job.query.filter(Job.subgroup_id.in_(passing_subgroup_ids)).all()
    return render_template('quiz3.html', jobs=jobs)

@app.route('/quiz4', methods=['GET', 'POST'])
def quiz4():
    if not validate_quiz_session():
        return redirect(url_for('quiz'))

    session_id = session.get('session_id')
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None  # Or use a dummy ID if needed


    passing_jobs = session.get('passing_jobs', [])
    if not passing_jobs:
        flash("No valid jobs found. Please restart the quiz.", "warning")
        return redirect(url_for('quiz'))

    if request.method == 'POST':
        job_scores = session.get('job_scores', {})  # job_id: subgroup + Q1 score
        final_scores = {}

        # Create a new QuizSession for this user
        quiz_session = QuizSession(session_id=session_id, user_id=user_id)
        db.session.add(quiz_session)
        db.session.commit()

        for key, value in request.form.items():
            if key.startswith('job_q2_'):
                job_id = int(key.split('_')[2])
                q2_score = int(value)

                # Add UserResponse for this question
                response = UserResponse(
                    session_id=session_id,
                    question_type='second',
                    target_id=job_id,
                    score=q2_score
                )
                db.session.add(response)

                # Calculate the total score for the job
                total = job_scores.get(str(job_id), 0) + q2_score
                final_scores[job_id] = total

        db.session.commit()

        # Store scores in session so /results can use them
        session['job_scores'] = final_scores 
        top_jobs = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        session['top_jobs'] = [job_id for job_id, score in top_jobs]

        return redirect(url_for('results', session_id=session_id))

    # GET method
    jobs = Job.query.filter(Job.id.in_(passing_jobs)).all()
    return render_template('quiz4.html', jobs=jobs)

@app.route('/results', methods=['GET'])
def results():
    session_id = request.args.get('session_id')
    if not session_id:
        flash("No quiz results found. Please complete a quiz first.", "warning")
        return redirect(url_for('quiz'))

    quiz_session = QuizSession.query.filter_by(session_id=session_id).first()
    if not quiz_session:
        flash("Invalid session ID.", "danger")
        return redirect(url_for('profile'))
    
    if quiz_session.user_id != current_user.id:
        shared = SharedResult.query.filter_by(
            quiz_session_id=quiz_session.id,
            shared_with_id=current_user.id
        ).first()
        if not shared:
            flash("You do not have permission to view this result.", "danger")
            return redirect(url_for('profile'))

    user_responses = UserResponse.query.filter_by(session_id=session_id).all()
    job_scores = {response.target_id: response.score for response in user_responses if response.question_type == 'second'}
    sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)

    # Get the top 5 jobs and accumulate weighted attributes
    top_jobs = []
    attribute_totals = defaultdict(int)

    for job_id, score in sorted_jobs[:5]:
        job = Job.query.get(job_id)
        if job:
            top_jobs.append((job, score))
            cluster = job.subgroup.job_cluster
            attribute_totals['social']     += cluster.social     * score
            attribute_totals['physical']   += cluster.physical   * score
            attribute_totals['leadership'] += cluster.leadership * score
            attribute_totals['creativity'] += cluster.creativity * score
            attribute_totals['logic']      += cluster.logic      * score

    # Normalize scores to a 0–100 scale
    max_val = max(attribute_totals.values(), default=1)
    normalized_scores = {
        key: int((value / max_val) * 100) for key, value in attribute_totals.items()
    }

    # Calculate scores per subgroup
    subgroup_scores = defaultdict(int)
    for job_id, score in sorted_jobs[:5]:
        job = Job.query.get(job_id)
        if job:
            subgroup_name = job.subgroup.name
            subgroup_scores[subgroup_name] += score

    return render_template(
        'results.html',
        top_jobs=top_jobs,
        attribute_totals=dict(attribute_totals),
        normalized_scores=normalized_scores,
        subgroup_scores=dict(subgroup_scores),
        quiz_session=quiz_session
    )

@app.route('/add_friend/<int:friend_id>', methods=['POST'])
@login_required
def add_friend(friend_id):
    friend = User.query.get(friend_id)
    if friend and friend != current_user and friend not in current_user.friends:
        current_user.friends.append(friend)
        db.session.commit()
        flash(f"You are now friends with {friend.username}")
    else:
        flash("Cannot add this user.")
    return redirect(url_for('profile'))

@app.route('/friend/<int:friend_id>')
@login_required
def view_friend(friend_id):
    friend = User.query.get(friend_id)
    if friend not in current_user.friends:
        flash("You're not friends with this user.")
        return redirect(url_for('profile'))

    quiz_sessions = QuizSession.query.filter_by(user_id=friend.id).all()
    return render_template('friend_profile.html', friend=friend, quiz_sessions=quiz_sessions)

@app.route('/send_friend_request/<int:to_user_id>', methods=['POST'])
@login_required
def send_friend_request(to_user_id):
    to_user = User.query.get_or_404(to_user_id)

    if to_user in current_user.friends:
        flash("You're already friends with this user.", "info")
        return redirect(url_for('profile'))

    existing_request = FriendRequest.query.filter_by(
        from_user_id=current_user.id, to_user_id=to_user_id
    ).first()
    if existing_request:
        flash("Friend request already sent.", "info")
        return redirect(url_for('profile'))
    
    reverse_request = FriendRequest.query.filter_by(
        from_user_id=to_user_id, to_user_id=current_user.id
    ).first()
    if reverse_request:
        flash("This user already sent you a friend request.", "info")
        return redirect(url_for('profile'))

    friend_request = FriendRequest(from_user_id=current_user.id, to_user_id=to_user_id)
    db.session.add(friend_request)
    db.session.commit()

    flash("Friend request sent!", "success")
    return redirect(url_for('profile'))

@app.route('/friend_requests')
@login_required
def friend_requests():
    requests = FriendRequest.query.filter_by(to_user_id=current_user.id, status='pending').all()
    return render_template('friend_requests.html', requests=requests)

@app.route('/accept_friend_request/<int:request_id>', methods=['POST'])
@login_required
def accept_friend_request(request_id):
    friend_request = FriendRequest.query.get(request_id)
    if not friend_request or friend_request.to_user_id != current_user.id:
        flash("Invalid friend request.", "danger")
        return redirect(url_for('friend_requests'))

    # Add the friendship
    current_user.friends.append(friend_request.from_user)
    friend_request.from_user.friends.append(current_user)

    db.session.delete(friend_request)
    db.session.commit()

    flash("Friend request accepted!", "success")
    return redirect(url_for('profile'))

@app.route('/decline_friend_request/<int:request_id>', methods=['POST'])
@login_required
def decline_friend_request(request_id):
    friend_request = FriendRequest.query.get(request_id)
    if not friend_request or friend_request.to_user_id != current_user.id:
        flash("Invalid friend request.", "danger")
        return redirect(url_for('friend_requests'))

    # Update the request status
    friend_request.status = 'declined'
    db.session.commit()
    flash("Friend request declined.", "info")
    return redirect(url_for('friend_requests'))

@app.route('/users')
@login_required
def users():
    query = request.args.get('q', '')
    if query:
        users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    else:
        users = []
    return render_template('users.html', users=users, query=query)

@app.route('/share_result', methods=['POST'])
@login_required
def share_result():
    session_id = request.form.get('session_id')
    friend_id = request.form.get('friend_id')

    if not session_id or not friend_id:
        flash('Missing data to share result.', 'danger')
        return redirect(url_for('profile'))

    quiz_session = QuizSession.query.filter_by(session_id=session_id).first()
    if not quiz_session:
        flash('Quiz session not found.', 'danger')
        return redirect(url_for('profile'))

    friend = User.query.get(friend_id)
    if not friend or friend not in current_user.friends or friend.id == current_user.id:
        flash('Invalid friend selection.', 'danger')
        return redirect(url_for('profile'))

    already_shared = SharedResult.query.filter_by(
        quiz_session_id=quiz_session.id,
        shared_with_id=friend.id
    ).first()

    if already_shared:
        flash(f'You’ve already shared this result with {friend.username}.', 'info')
        return redirect(url_for('profile'))

    shared_result = SharedResult(
        quiz_session_id=quiz_session.id, 
        shared_with_id=friend.id
    )
    db.session.add(shared_result)
    db.session.commit()

    flash(f'Result shared with {friend.username}!', 'success')
    return redirect(url_for('profile'))

@app.route('/logout')
@login_required
def logout():

    for key in ['session_id', 'selected_clusters', 'asked_subgroups', 'job_scores', 'passing_jobs', 'top_jobs']:
        session.pop(key, None)
    
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
