from app import app, db
from models import JobCluster, Subgroup, Job, Question

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create JobCluster
    engineering = JobCluster(name="Engineering and Systems")
    db.session.add(engineering)
    
    # Create Subgroup
    mechanical_subgroup = Subgroup(name="Design & Infrastructure", job_cluster=engineering)
    db.session.add(mechanical_subgroup)

    # Add subgroup-level question
    subgroup_q = Question(
        text="Do you enjoy designing and optimizing complex systems or structures?",
        question_type='subgroup',
        subgroup=mechanical_subgroup
    )
    db.session.add(subgroup_q)

    # Create a Job
    mechanical_engineer = Job(title="Mechanical Engineer", subgroup=mechanical_subgroup)
    db.session.add(mechanical_engineer)

    # Add job-specific questions
    job_q1 = Question(
        text="Do you enjoy working with mechanical systems and solving real-world engineering problems?",
        question_type='first',
        job=mechanical_engineer
    )
    job_q2 = Question(
        text="Do you find thermodynamics and material science interesting?",
        question_type='second',
        job=mechanical_engineer
    )
    db.session.add_all([job_q1, job_q2])

    # Commit everything
    db.session.commit()
    print("Database seeded successfully!")
