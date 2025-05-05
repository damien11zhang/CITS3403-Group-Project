from app import app, db
from models import JobCluster, Subgroup, Job

with app.app_context():
    # Clear existing data (optional for isolated testing)
    db.drop_all()
    db.create_all()

    # Create JobCluster
    science = JobCluster(name="Science and Research")
    db.session.add(science)

    # Subgroup 1: Laboratory & Medical Research
    lab_med_subgroup = Subgroup(
        name="Laboratory & Medical Research",
        job_cluster=science,
        subgroup_question="Do you enjoy working in lab settings to develop medical or biological advancements?"
    )
    db.session.add(lab_med_subgroup)

    # Jobs
    db.session.add_all([
        Job(
            title="Biomedical Scientist",
            subgroup=lab_med_subgroup,
            question_1="Do you find it rewarding to study human biology to advance medical treatments?",
            question_2="Are you interested in using lab-based techniques to diagnose or prevent disease?"
        ),
        Job(
            title="Clinical Research Associate",
            subgroup=lab_med_subgroup,
            question_1="Are you interested in overseeing clinical trials to ensure safe and ethical testing of new treatments?",
            question_2="Do you enjoy working at the intersection of science, medicine, and regulatory compliance?"
        ),
        Job(
            title="Biotechnologist",
            subgroup=lab_med_subgroup,
            question_1="Are you passionate about using living organisms to develop new products or technologies?",
            question_2="Do you enjoy working with genetic engineering, microbiology, or biochemical processes?"
        ),
    ])

    # Subgroup 2: Environmental & Earth Sciences
    env_earth_subgroup = Subgroup(
        name="Environmental & Earth Sciences",
        job_cluster=science,
        subgroup_question="Are you passionate about studying natural systems to promote environmental sustainability?"
    )
    db.session.add(env_earth_subgroup)

    db.session.add_all([
        Job(
            title="Environmental Scientist",
            subgroup=env_earth_subgroup,
            question_1="Are you passionate about understanding and solving environmental issues like pollution or climate change?",
            question_2="Do you enjoy working with data and ecosystems to promote sustainability?"
        ),
        Job(
            title="Agricultural Scientist",
            subgroup=env_earth_subgroup,
            question_1="Are you curious about improving crop yields and sustainable farming practices?",
            question_2="Do you enjoy applying biology and chemistry to improve food production?"
        ),
        Job(
            title="Geoscientist",
            subgroup=env_earth_subgroup,
            question_1="Are you drawn to studying the Earth’s physical structure, processes, and resources?",
            question_2="Do you enjoy analyzing rock, soil, and environmental samples to understand our planet?"
        ),
    ])

    # Subgroup 3: Materials & Applied Sciences
    materials_subgroup = Subgroup(
        name="Materials & Applied Sciences",
        job_cluster=science,
        subgroup_question="Do you like applying scientific techniques to real-world problems through material or evidence analysis?"
    )
    db.session.add(materials_subgroup)

    db.session.add_all([
        Job(
            title="Materials Scientist",
            subgroup=materials_subgroup,
            question_1="Are you fascinated by studying and creating new materials to solve engineering or industrial problems?",
            question_2="Do you enjoy experimenting with physical and chemical properties at the microscopic level?"
        ),
        Job(
            title="Forensic Scientist",
            subgroup=materials_subgroup,
            question_1="Are you interested in analyzing evidence to assist in criminal investigations?",
            question_2="Do you enjoy applying scientific methods to uncover the truth in legal cases?"
        ),
    ])

    # Subgroup 4: Scientific Communication & Strategy
    sci_comm_subgroup = Subgroup(
        name="Scientific Communication & Strategy",
        job_cluster=science,
        subgroup_question="Are you motivated by connecting scientific discovery with broader societal impact?"
    )
    db.session.add(sci_comm_subgroup)

    db.session.add_all([
        Job(
            title="Researcher",
            subgroup=sci_comm_subgroup,
            question_1="Do you enjoy forming hypotheses and testing them through structured investigations?",
            question_2="Are you motivated by discovering new knowledge and contributing to scientific understanding?"
        ),
        Job(
            title="Science Policy Analyst",
            subgroup=sci_comm_subgroup,
            question_1="Are you interested in shaping public policy based on scientific evidence and trends?",
            question_2="Do you enjoy evaluating research to inform decision-makers and the public?"
        ),
    ])

    # Commit all data
    db.session.commit()
    print("Science and Research cluster seeded successfully!")
