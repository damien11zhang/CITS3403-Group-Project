from app import app, db
from models import JobCluster, Subgroup, Job

def seed_law():
    with app.app_context():
        # Cluster: Law and Public Service
        law = JobCluster(
                         name="Law, Government & Safety",
                         description="Protect public interests, enforce laws, and promote justice in communities.",
                                social=7,
                                physical=2,
                                leadership=9,
                                creativity=4,
                                logic=8)
        db.session.add(law)

        # Subgroup 1: Support Roles
        support_roles = Subgroup(
            name="Support Roles",
            subgroup_question="Do behind the scene roles that help important sectors function appeal to you?",
            job_cluster=law
        )
        db.session.add(support_roles)

        jobs_support_roles = [
            Job(title="Paralegal", question_1="Does researching, organizing, and preparing legal documents appeal to you?",
                question_2="How much would you enjoy being the backbone for high profile lawyers?", subgroup=support_roles),
            Job(title="Public Servant", question_1="Are you interested in working for the government to support community services or policies?",
                question_2="Do you enjoy administrative work that contributes to the public good?", subgroup=support_roles)
        ]

        # Subgroup 2: Law and Justice
        law_justice = Subgroup(
            name="Law and Justice",
            subgroup_question="Do you have a strong interest in courtroom settings and influencing legal outcomes through argument or decision-making?",
            job_cluster=law
        )
        db.session.add(law_justice)

        jobs_law_justice = [
            Job(title="Prosecutor", question_1="Are you motivated by holding individuals accountable for criminal behavior?",
                question_2="Would you enjoy presenting legal arguments in court to represent the government?", subgroup=law_justice),
            Job(title="Judge", question_1="Do you like making decisions based on rules, logic, and fairness?",
                question_2="Are you interested in maintaining order and ensuring justice in a courtroom?", subgroup=law_justice),
            Job(title="Criminal Lawyer", question_1="Does defending the innocent appeal to you?",
                question_2="Do you enjoy building arguments and challenging opposing viewpoints?", subgroup=law_justice),
            Job(title="Civil Lawyer", question_1="Are you drawn to solving disputes over property, contracts, or personal rights?",
                question_2="Would you enjoy representing clients in lawsuits that don't involve criminal charges?", subgroup=law_justice),
        ]

        # Subgroup 3: Public Protection
        public_protection = Subgroup(
            name="Public Protection",
            subgroup_question="Are you excited by active, high-stakes roles where you serve and protect others during emergencies?",
            job_cluster=law
        )
        db.session.add(public_protection)

        jobs_public_protection = [
            Job(title="Detective", question_1="Do you enjoy out of the box thinking?",
                question_2="Do you enjoy solving mysteries and uncovering the truth through investigation?", subgroup=public_protection),
            Job(title="Firefighter", question_1="Do you enjoy being physically active and helping people during dangerous situations?",
                question_2="Would you enjoy working as part of a team to respond to fires and emergencies?", subgroup=public_protection),
            Job(title="Paramedic", question_1="Are you interested in medical care and helping people in crisis situations?",
                question_2="Can you see yourself staying calm while providing emergency treatment in unpredictable environments?", subgroup=public_protection),
            Job(title="Police Officer", question_1="Do you feel drawn to protecting communities and enforcing laws?",
                question_2="Are you comfortable responding to emergencies and making quick decisions under pressure?", subgroup=public_protection)
        ]
        
  
        db.session.add_all(jobs_support_roles + jobs_law_justice + jobs_public_protection)
        db.session.commit()
        print("Law & Public Service cluster with subgroups seeded successfully.")

seed_law()