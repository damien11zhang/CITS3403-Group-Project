from app import db
from models import JobCluster

clusters = [
    ("Engineering", "I enjoy figuring out how systems or machines work."),
    ("Technology", "I like working with tech, logic, and data."),
    ("Social", "I find joy in helping or guiding others."),
    ("Creative", "I love expressing ideas visually or creatively."),
    ("Business", "I am good at planning or solving business problems."),
    ("Science", "I'm curious and enjoy investigating how things work."),
    ("Administration", "I like organizing tasks and keeping systems structured."),
    ("Health", "I feel fulfilled when caring for others’ well-being."),
    ("Trades", "I enjoy hands-on, practical work and seeing results."),
    ("Law", "I'm passionate about fairness, rules, and justice.")
]

def seed_clusters():
    for name, desc in clusters:
        cluster = JobCluster(name=name, description=desc)
        db.session.add(cluster)
    db.session.commit()

if __name__ == '__main__':
    seed_clusters()
    print("Job clusters seeded.")