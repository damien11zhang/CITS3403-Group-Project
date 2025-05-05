from app import db
from models import Question

def seed_section1_questions():
    questions = [
        Question(text="Do you enjoy helping others in need?", cluster_id=1),
        Question(text="Are you interested in how the human body works?", cluster_id=1),
        Question(text="Do you enjoy organizing events or teams?", cluster_id=2),
        Question(text="Do you see yourself managing a company one day?", cluster_id=2),
        Question(text="Do you like solving technical problems?", cluster_id=3),
        Question(text="Are you curious about how machines work?", cluster_id=3),
        Question(text="Do you enjoy drawing or storytelling?", cluster_id=4),
        Question(text="Do you often get creative ideas?", cluster_id=4),
        Question(text="Do you enjoy helping people learn?", cluster_id=5),
        Question(text="Are you a good communicator?", cluster_id=5),
    ]
    db.session.add_all(questions)
    db.session.commit()
    print("Section 1 Questions seeded.")