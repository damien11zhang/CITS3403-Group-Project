from app import app, db
from models import JobCluster, Subgroup, Job

def seed_social():
    with app.app_context():
        # Cluster: Social & People
        social = JobCluster(
                            name="Social & Community Services",
                            description="Support and empower individuals and communities through care, guidance, and engagement.",
                                social=10,
                                physical=3,
                                leadership=7,
                                creativity=4,
                                logic=4)
        db.session.add(social)

        # Subgroup 1: Education & Guidance
        education_guidance = Subgroup(
            name="Education & Guidance",
            subgroup_question="Do you enjoy teaching, advising, or helping others grow in their personal or professional life?",
            job_cluster=social
        )
        db.session.add(education_guidance)

        jobs_education_guidance = [
            Job(title="Teacher", question_1="Do you enjoy explaining concepts to others in an engaging way?",
                question_2="Can you manage a group while keeping everyone engaged and learning?", subgroup=education_guidance),
            Job(title="Career Advisor", question_1="Do you like helping others figure out their career paths and future goals?",
                question_2="Do you enjoy researching different job options and market trends to help others decide?", subgroup=education_guidance),
            Job(title="Training & Development Officer", question_1="Do you like leading workshops or training sessions to help others grow?",
                question_2="Can you adjust your teaching style for different people and learning speeds?", subgroup=education_guidance)
        ]

        # Subgroup 2: Emotional & Social Support
        emotional_support = Subgroup(
            name="Emotional & Social Support",
            subgroup_question="Do you enjoy supporting others through emotional or social challenges in their lives?",
            job_cluster=social
        )
        db.session.add(emotional_support)

        jobs_emotional_support = [
            Job(title="Social Worker", question_1="Are you passionate about helping people overcome life challenges?",
                question_2="Are you able to stay emotionally strong when working with people in crisis?", subgroup=emotional_support),
            Job(title="Counselor / Therapist", question_1="Do you feel comfortable listening deeply and offering support without judgment?",
                question_2="Do you enjoy helping people navigate personal growth over time?", subgroup=emotional_support),
            Job(title="Youth Worker", question_1="Do you enjoy mentoring and empowering young people?",
                question_2="Are you creative in designing programs or activities to inspire youth?", subgroup=emotional_support)
        ]

        # Subgroup 3: Community & Coordination
        community_coordination = Subgroup(
            name="Community & Coordination",
            subgroup_question="Do you enjoy organizing people or events, and working closely with teams or the public?",
            job_cluster=social
        )
        db.session.add(community_coordination)

        jobs_community_coordination = [
            Job(title="Volunteer Coordinator", question_1="Do you enjoy organizing teams and motivating people to contribute?",
                question_2="Are you good at keeping people organized, motivated, and on-task?", subgroup=community_coordination),
            Job(title="Event Coordinator", question_1="Do you enjoy planning and managing events from start to finish?",
                question_2="Do you enjoy managing multiple details and logistics under tight deadlines?", subgroup=community_coordination),
            Job(title="HR Specialist", question_1="Do you enjoy working with people to build a positive workplace culture?",
                question_2="Do you enjoy resolving conflicts and promoting fairness in the workplace?", subgroup=community_coordination),
            Job(title="Community Outreach Officer", question_1="Do you enjoy engaging with communities and promoting social programs?",
                question_2="Are you confident representing an organization in public settings?", subgroup=community_coordination)
        ]

        db.session.add_all(jobs_education_guidance + jobs_emotional_support + jobs_community_coordination)
        db.session.commit()
        print("Social & People cluster with subgroups seeded successfully.")

seed_social()