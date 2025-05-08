from app import app, db
from models import JobCluster, Subgroup, Job

def seed_health():
    with app.app_context():
        # Cluster: Health & Care
        health = JobCluster(
                           name="Health & Wellbeing",
                           description="Care for people's physical and mental health through treatment, support, and rehabilitation.")
        db.session.add(health)

        # Subgroup 1: Clinical & Emergency
        clinical_emergency = Subgroup(
            name="Clinical & Emergency",
            subgroup_question="Do you enjoy providing immediate, hands-on care in dynamic or high-pressure situations?",
            job_cluster=health
        )
        db.session.add(clinical_emergency)

        jobs_clinical_emergency = [
            Job(title="Registered Nurse", question_1="Are you comfortable providing hands-on medical care in fast-paced situations?",
                question_2="Are you willing to work long shifts, including nights and weekends?", subgroup=clinical_emergency),
            Job(title="Paramedic", question_1="Can you stay calm and act quickly during emergencies?",
                question_2="Do you feel excited by fast decision-making and hands-on action?", subgroup=clinical_emergency),
            Job(title="Midwife", question_1="Are you passionate about supporting women through pregnancy and childbirth?",
                question_2="Do you enjoy building trust and emotional support during highly personal life events?", subgroup=clinical_emergency)
        ]

        # Subgroup 2: Therapy & Rehabilitation
        therapy_rehab = Subgroup(
            name="Therapy & Rehabilitation",
            subgroup_question="Do you enjoy helping others recover or improve their physical and mental abilities?",
            job_cluster=health
        )
        db.session.add(therapy_rehab)

        jobs_therapy_rehab = [
            Job(title="Psychologist", question_1="Do you enjoy helping people work through emotional and mental challenges?",
                question_2="Do you enjoy analyzing behavior to find patterns and solutions?", subgroup=therapy_rehab),
            Job(title="Physiotherapist", question_1="Do you enjoy guiding people through physical recovery exercises?",
                question_2="Do you enjoy one-on-one work helping others improve physically over time?", subgroup=therapy_rehab),
            Job(title="Occupational Therapist", question_1="Do you enjoy helping people regain independence in everyday tasks?",
                question_2="Do you enjoy problem-solving daily tasks for people with physical or cognitive challenges?", subgroup=therapy_rehab),
            Job(title="Speech Pathologist", question_1="Do you enjoy helping people improve how they speak and communicate?",
                question_2="Do you feel confident working with clients who need slow, repetitive support?", subgroup=therapy_rehab)
        ]

        # Subgroup 3: Nutrition & Medication
        nutrition_medication = Subgroup(
            name="Nutrition & Medication",
            subgroup_question="Do you enjoy advising people on nutrition, wellness, or medication use?",
            job_cluster=health
        )
        db.session.add(nutrition_medication)

        jobs_nutrition_medication = [
            Job(title="Dietitian / Nutritionist", question_1="Do you like giving personalized nutrition advice to help people improve their health?",
                question_2="Do you enjoy creating meal or diet plans tailored to someone's goals?", subgroup=nutrition_medication),
            Job(title="Pharmacist", question_1="Do you enjoy giving advice about medication and ensuring it is used safely?",
                question_2="Are you confident explaining complex medical information in simple terms?", subgroup=nutrition_medication)
        ]

        # Subgroup 4: Diagnostics
        diagnostics = Subgroup(
            name="Diagnostics",
            subgroup_question="Do you enjoy analyzing medical samples or data to assist in diagnoses?",
            job_cluster=health
        )
        db.session.add(diagnostics)

        jobs_diagnostics = [
            Job(title="Medical Lab Technician", question_1="Do you like performing lab tests and working behind the scenes in healthcare?",
                question_2="Do you enjoy following structured procedures with high attention to detail?", subgroup=diagnostics)
        ]

        db.session.add_all(jobs_clinical_emergency + jobs_therapy_rehab + jobs_nutrition_medication + jobs_diagnostics)
        db.session.commit()
        print("Health & Care cluster with subgroups seeded successfully.")

seed_health()