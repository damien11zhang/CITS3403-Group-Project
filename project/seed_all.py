from app import app
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
    for filename in SEED_FILES:
        path = os.path.join(os.getcwd(), filename)
        print(f"Running: {filename}")
        try:
            exec(open(path).read())
            print(f"✅ {filename} completed successfully.")
        except Exception as e:
            print(f"❌ Error running {filename}: {e}")
