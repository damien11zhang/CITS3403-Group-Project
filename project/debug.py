from app import app, db
from models import JobCluster

with app.app_context():
    clusters = JobCluster.query.all()
    for cluster in clusters:
        print(f"{cluster.id} – {cluster.name}")
