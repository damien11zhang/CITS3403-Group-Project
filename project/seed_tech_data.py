from app import app, db
from models import JobCluster, Subgroup, Job

def seed_tech_data():
    with app.app_context():
        tech_data = JobCluster(name="Tech & Data")
        db.session.add(tech_data)

        data_roles = Subgroup(
            name="Data-Centric Roles",
            question="How interested are you in using data to make decisions, uncover insights, or power smart systems?",
            job_cluster=tech_data
        )
        db.session.add(data_roles)

        jobs_data = [
            Job(title="Data Analyst", question_1="How interested are you in discovering patterns and insights hidden in data?",
                question_2="How curious are you about using tools like spreadsheets or coding to solve real-world problems?", subgroup=data_roles),
            Job(title="Data Scientist", question_1="How interested are you in making predictions or understanding trends using data and algorithms?",
                question_2="How curious are you about combining math, tech, and critical thinking to solve complex problems?", subgroup=data_roles),
            Job(title="Machine Learning Engineer", question_1="How excited are you by the idea of creating smart systems that can learn and improve over time?",
                question_2="How interested are you in exploring how machines can make predictions based on data?", subgroup=data_roles)
        ]

        dev_roles = Subgroup(
            name="Software Development Roles",
            question="How appealing is the idea of building digital tools or apps that people use every day?",
            job_cluster=tech_data
        )
        db.session.add(dev_roles)

        jobs_dev = [
            Job(title="Software Developer", question_1="How appealing do you find the idea of building apps or websites by writing code?",
                question_2="How intrigued are you by solving puzzles or logical challenges with programming?", subgroup=dev_roles),
            Job(title="Frontend Developer", question_1="Do you enjoy turning designs into interactive, user-friendly web interfaces?",
                question_2="Are you skilled at making websites responsive and accessible across devices?", subgroup=dev_roles),
            Job(title="Backend Developer", question_1="How interested are you in building the behind-the-scenes logic that powers apps and websites?",
                question_2="How appealing is the idea of managing how data moves between users and systems?", subgroup=dev_roles)
        ]
        infra_cloud_roles = Subgroup(
            name="Infrastructure and Cloud Roles",
            question="How interested are you in setting up and maintaining the technology that keeps apps running reliably?",
            job_cluster=tech_data
        )
        db.session.add(infra_cloud_roles)

        jobs_infra_cloud = [
            Job(title="DevOps Engineer", question_1="How appealing is the idea of helping systems run smoothly through automation?",
                question_2="How interested are you in managing the tools that help developers build and deploy software?", subgroup=infra_cloud_roles),
            Job(title="Cloud Architect", question_1="How curious are you about designing online systems that can scale to support lots of users?",
                question_2="How interested are you in learning how services like AWS or Google Cloud power modern tech?", subgroup=infra_cloud_roles)
        ]
        security_storage_roles = Subgroup(
            name="Security and Storage Roles",
            question="How appealing is the idea of protecting information and making sure it’s organized and accessible?",
            job_cluster=tech_data
        )
        db.session.add(security_storage_roles)

        jobs_security_storage = [
            Job(title="Cybersecurity Analyst", question_1="How interested are you in protecting digital information from threats or hackers?",
                question_2="How curious are you about spotting weaknesses in systems and fixing them before something goes wrong?", subgroup=security_storage_roles),
            Job(title="Database Administrator", question_1="How interested are you in organizing and managing large collections of data?",
                question_2="How appealing is the idea of ensuring data is stored securely and works efficiently?", subgroup=security_storage_roles)
        ]
        db.session.add_all(jobs_data + jobs_dev + jobs_infra_cloud + jobs_security_storage)
        db.session.commit()
        print("Tech & Data cluster seeded successfully.")