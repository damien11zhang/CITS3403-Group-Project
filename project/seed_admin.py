from app import app, db
from models import JobCluster, Subgroup, Job

def seed_admin():
    with app.app_context():
        # Cluster: Admin & Organisation
        admin = JobCluster(
            name="Admin & Organisation",
            description="Organize, support, and coordinate systems",
            social=4,
            physical=1,
            leadership=6,
            creativity=3,
            logic=8)

        db.session.add(admin)

        # Subgroup 1: Frontline Support
        frontline_support = Subgroup(
            name="Frontline Support",
            subgroup_question="How much do you enjoy helping people solve problems in real-time and being the first point of contact for questions or concerns?",
            job_cluster=admin
        )
        db.session.add(frontline_support)

        jobs_frontline_support = [
            Job(title="Customer Support", question_1="How much do you find satisfaction in solving small problems that improve someones day?",
                question_2="How comfortable are you with repetitive tasks while continuing to be friendly in tone?", subgroup=frontline_support),
            Job(title="Receptionist", question_1="How much do you enjoy helping people feel welcome in new environments?",
                question_2="How much do you enjoy roles that include phone, in-person and email communication?", subgroup=frontline_support),
            Job(title="Platform Moderator", question_1="How comfortable are you with making serious judgement calls on what is/isn't appropriate?",
                question_2="How much do you enjoy working behind the scenes and keeping things running smoothly?", subgroup=frontline_support)
        ]

        # Subgroup 2: Information Management
        information_management = Subgroup(
            name="Information Management",
            subgroup_question="Do you find satisfaction in keeping things organized and making sure nothing gets overlooked?",
            job_cluster=admin
        )
        db.session.add(information_management)

        jobs_information_management = [
            Job(title="Data Entry", question_1="Do you enjoy working independently on tasks that require strict accuracy?",
                question_2="How much do you enjoy repetitive tasks when they involve important information?", subgroup=information_management),
            Job(title="Archivist", question_1="How much do you like preserving and organizing documents?",
                question_2="How comfortable are you with handling sensitive information?", subgroup=information_management)
        ]

        # Subgroup 3: People & Events
        people_events = Subgroup(
            name="People & Events",
            subgroup_question="How much do you like bringing people together and making sure everything runs smoothly behind the scenes?",
            job_cluster=admin
        )
        db.session.add(people_events)

        jobs_people_events = [
            Job(title="Human Resources", question_1="How much do you enjoy supporting others throughout their workplace career?",
                question_2="How comfortable are you with balancing empathy and workplace policy?", subgroup=people_events),
            Job(title="Event Planner", question_1="How do you like creating experiences that others will enjoy or remember?",
                question_2="How comfortable are you managing small details on a tight deadline?", subgroup=people_events)
        ]
        
        #Subgroup 4: Internal Operations
        internal_operations = Subgroup(
            name="Internal Operations",
            subgroup_question="Do you enjoy keeping things on track and making sure day-to-day tasks are handled smoothly?",
            job_cluster=admin
        )
        db.session.add(internal_operations)

        jobs_internal_operations = [
            Job(title="Administrative Assistant", question_1="How much do you enjoy helping others work efficiently?", 
                question_2="How much do you enjoy roles that are routine with occasional unexpected tasks?", subgroup=internal_operations),
            Job(title="Scheduling Assistant", question_1="How much does coordinating appointments appeal you?",
                question_2="How much do you enjoy managing logistics and ensuring plans run smoothly?", subgroup=internal_operations),
            Job(title="Personal Assistant", question_1="How comfortable are you juggling multiple priorities for someone else?",
                question_2="How much do you enjoy being in a role where anticipation and proactivity matter?", subgroup=internal_operations)
        ]

        db.session.add_all(jobs_frontline_support + jobs_information_management + jobs_people_events + jobs_internal_operations)
        db.session.commit()
        print("Admin & Organisation cluster with subgroups seeded successfully.")

seed_admin()
