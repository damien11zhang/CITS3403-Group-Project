from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/quiz')
def quiz():
    return render_template("quiz.html")

@app.route('/results')
def results():
    return render_template("results.html")

if __name__ == '__main__':
    app.run(debug=True)