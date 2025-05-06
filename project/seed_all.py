from app import app
from extensions import db
from models import JobCluster, Subgroup, Job
from sqlalchemy import text
import os

SEED_FILES = [
    "seed_engineering.py",
    "seed_science.py",
    "seed_health.py",
    "seed_business.py",
    "seed_admin.py",
    "seed_social.py",
    "seed_trade.py",
    "seed_tech_data.py",
    "seed_creative.py",
    "seed_law.py"
]

with app.app_context():
    print("🧹 Wiping all tables...")
    db.session.execute(text('DELETE FROM jobs;'))
    db.session.execute(text('DELETE FROM subgroups;'))
    db.session.execute(text('DELETE FROM job_clusters;'))
    db.session.commit()
    print("✅ Wipe complete.\n")

    for filename in SEED_FILES:
        path = os.path.join(os.getcwd(), filename)
        print(f"📥 Executing: {filename}")
        try:
            exec(open(path).read())
            cluster_count = JobCluster.query.count()
            print(f"✅ {filename} completed. Total clusters: {cluster_count}")
        except Exception as e:
            print(f"❌ ERROR in {filename}: {e}")

    print("\n🔍 Final Cluster Check:")
    for cluster in JobCluster.query.all():
        print(f"- {cluster.id} – {cluster.name}")
