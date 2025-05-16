# careerCompass - Career Quiz App

A personalized career discovery platform built with Flask. Users can take quizzes, view career matches, track their quiz history, manage their profile, send and accept friend requests, and share results with friends.

---

## Group Members:
1. 23669907 - Damien Zhang
2. 23136223 - Jules Van Melle-Park
3. 23951196 - Sam Hunt
4. 24195369 - Agnes Renatha Sihombing

## Features

- **User Registration & Login**
- **Career Quiz System** with multiple question types
- **Result Scoring** using job clusters and attributes
- **Profile Page** with:
  - Editable user info
  - Quiz history
  - Shared results from friends
  - Friend request notifications
- **Friend System** to connect with other users
- **Result Sharing** via session ID
- **Flask-based backend** with Jinja2 templates
---

## Technologies Used

- **Python 3**
- **Flask**
- **Flask-Login** 
- **SQLAlchemy** 
- **SQLite** 
- **Jinja2** 

---

## Setup Instructions
1. Clone the repository
    git clone https://github.com/damien11zhang/CITS3403-Group-Project
    cd project
2. Create virtual environment
    python3 -m venv venv
    venv\Scripts\activate.bat on Windows, venv/bin/activate on Mac
4. Install dependencies
    pip install -r requirements.txt
5. Run the application
    flask run
6. Visit http://127.0.0.1:5000 on browser.

---

## Main Project Structure

1. `app.py` - main application file
2. `templates/` - all HTML templates
3. `test/` - test files
4. `models.py` - database models

---

## Testing
Once in the project directory, please run the following to test:
1. python test_app.py
2. python test_selenium.py
