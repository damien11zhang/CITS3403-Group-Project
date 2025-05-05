from app import app, db
from models import JobCluster, Subgroup, Job

def seed_trade():
    with app.app_context():
        # Cluster: Trade & Skilled work
        trade = JobCluster(name="Trade & Skilled Work")
        db.session.add(trade)

        # Subgroup 1: Construction
        construction = Subgroup(
            name="Construction",
            question="Do you enjoy physical work on a project that could last multiple months?",
            job_cluster=trade
        )
        db.session.add(construction)

        jobs_construction = [
            Job(title="Concreter", question_1="Are you comfortable with handling heavy materials?",
                question_2="Do you enjoy a highly physical, hands on job?", subgroup=construction),
            Job(title="Scaffolder", question_1="How comfortable are you with working at heights?",
                question_2="Does the idea of creating physical things that others will build off of appeal to you?", subgroup=construction),
            Job(title="Machinery Operator", question_1="Does the idea of operating heavy machinery appeal to you?",
                question_2="How do you feel about working on large-scale construction sites?", subgroup=construction),
            Job(title="Truck Driver", question_1="How comfortable are you with potentially long hours while remaining alert?",
                question_2="Does the idea of managing logistics & handling cargo appeal to you?", subgroup=construction)
        ]

        # Subgroup 2: Residential Trades
        residential_trades = Subgroup(
            name="Residential Trades",
            question="Does helping people with some issues directly on their property appeal to you?",
            job_cluster=trade
        )
        db.session.add(residential_trades)

        jobs_residential_trades = [
            Job(title="Locksmith", question_1="How do you feel about problem solving in a hands-on environment?",
                question_2="Do you find the workings of locks/keys to be interesting?", subgroup=residential_trades),
            Job(title="Electrician", question_1="Does troubleshooting electrical issues in both residential and commercial buildings appeal to you?",
                question_2="Are you comfortable working near high-voltage equipment?", subgroup=residential_trades),
            Job(title="Plumber", question_1="Would you enjoy handling house piping?", 
                question_2="How comfortable are you with working in tight spaces or underground?", subgroup=residential_trades)
        ]

        # Subgroup 3: Workshop Trades
        workshop_trades = Subgroup(
            name="Workshop Trades",
            question="Does working from a workshop as opposed to on a site appeal to you?",
            job_cluster=trade
        )
        db.session.add(workshop_trades)

        jobs_workshop_trades = [
            Job(title="Welder", question_1="Are you comfortable working near high temperature/dangerous equipment?",
                question_2="Do you enjoy making new metallic things?", subgroup=workshop_trades),
            Job(title="Carpenter", question_1="Do you enjoy working with wood and making new things?",
                question_2="Does working with precision tools to create physical objects appeal to you?", subgroup=workshop_trades),
            Job(title="Mechanic", question_1="Do you enjoy diagnosing & repairing mechanical faults?",
                question_2="How comfortable are you when working on complex mechanical systems?", subgroup=workshop_trades)
        ]
        

        db.session.add_all(jobs_construction + jobs_residential_trades + jobs_workshop_trades)
        db.session.commit()
        print("Trade & Skilled Work cluster with subgroups seeded successfully.")
