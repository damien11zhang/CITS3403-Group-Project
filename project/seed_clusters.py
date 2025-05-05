from extensions import db
from models import JobCluster
from app import app

clusters = [
    {
        "name": "Health & Care",
        "description": "You enjoy helping others and working in healthcare or wellbeing."
    },
    {
        "name": "Team & Leadership",
        "description": "You enjoy teamwork, leadership, and connecting with others."
    },
    {
        "name": "Curiosity & Logic",
        "description": "You're curious, logical, and enjoy solving problems."
    },
    {
        "name": "Business & Data",
        "description": "You enjoy analyzing data, managing resources, or entrepreneurship."
    },
    {
        "name": "Creativity & Expression",
        "description": "You like expressing yourself through arts, design, or storytelling."
    },
    {
        "name": "Hands-on & Practical",
        "description": "You prefer practical, hands-on work and building or fixing things."
    }
]

with app.app_context():
    db.session.query(JobCluster).delete()  # optional: bersihin dulu
    for cluster in clusters:
        db.session.add(JobCluster(name=cluster["name"], description=cluster["description"]))
    db.session.commit()
    print("✅ Clusters successfully seeded!")
