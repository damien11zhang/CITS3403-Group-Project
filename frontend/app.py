from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/quiz')
def quiz():
    return render_template("quiz.html")

# Add other routes like login, signup, results, etc.
