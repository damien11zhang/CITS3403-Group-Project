from app import app, db
from models import JobCluster, Subgroup, Job


def seed_engineering():
    with app.app_context():
        # Create Job Cluster
        engineering = JobCluster(
                                 name="Engineering & Systems",
                                 description="Design and improve machines, structures, and systems that solve real-world problems.")
        db.session.add(engineering)

        # Subgroup 1: Infrastructure & Environment (Civil, Mining, Project)
        infra_env = Subgroup(
            name="Infrastructure & Environment",
            subgroup_question="Do you enjoy planning and managing large-scale physical projects that shape environments and communities?",
            job_cluster=engineering
        )
        db.session.add(infra_env)

        jobs_infra_env = [
            Job(title="Civil", question_1="Do you enjoy designing and planning infrastructure like bridges, roads, or buildings?",
                question_2="Are you motivated by creating solutions that improve public safety and city functionality?", subgroup=infra_env),
            Job(title="Mining", question_1="Are you interested in the extraction of natural resources in a safe and efficient way?",
                question_2="Do you enjoy working in outdoor or remote environments with heavy machinery?", subgroup=infra_env),
            Job(title="Project", question_1="Do you enjoy managing engineering tasks and coordinating across different teams?",
                question_2="Are you skilled at balancing time, budget, and technical quality?", subgroup=infra_env)
        ]

        # Subgroup 2: Mechanical Systems & Design (Mechanical, Electrical, Automation & Robotics, Aeronautical)
        mech_design = Subgroup(
            name="Mechanical Systems & Design",
            subgroup_question="Are you drawn to designing and refining complex physical systems and machines?",
            job_cluster=engineering
        )
        db.session.add(mech_design)

        jobs_mech_design = [
            Job(title="Mechanical", question_1="Do you like working with machines and understanding how physical systems operate?",
                question_2="Are you comfortable using physics and math to solve practical problems?", subgroup=mech_design),
            Job(title="Electrical", question_1="Do you enjoy designing or working with electrical circuits and power systems?",
                question_2="Are you interested in how electronics impact modern infrastructure?", subgroup=mech_design),
            Job(title="Automation & Robotics", question_1="Are you fascinated by designing intelligent systems that can perform repetitive or precise tasks?",
                question_2="Do you enjoy integrating mechanical, electronic, and software systems?", subgroup=mech_design),
            Job(title="Aeronautical", question_1="Are you excited by the design and performance of aircraft and spacecraft?",
                question_2="Do you have a strong interest in aerodynamics, propulsion, and structural mechanics?", subgroup=mech_design)
        ]

        # Subgroup 3: Process & Production (Chemical, Industrial)
        process_prod = Subgroup(
            name="Process & Production",
            subgroup_question="Do you enjoy improving production efficiency and ensuring processes run smoothly and safely?",
            job_cluster=engineering
        )
        db.session.add(process_prod)

        jobs_process_prod = [
            Job(title="Chemical", question_1="Do you enjoy applying chemistry and process design to transform materials?",
                question_2="Are you interested in working on large-scale production systems like refineries or pharmaceuticals?", subgroup=process_prod),
            Job(title="Industrial", question_1="Do you enjoy optimizing systems to improve efficiency and productivity?",
                question_2="Are you interested in improving workflows in manufacturing or logistics?", subgroup=process_prod)
        ]

        # Subgroup 4: Software & Systems (Software)
        software_sys = Subgroup(
            name="Software & Systems",
            subgroup_question="Do you enjoy building digital systems that help solve real-world problems?",
            job_cluster=engineering
        )
        db.session.add(software_sys)

        jobs_software_sys = [
            Job(title="Software", question_1="Do you enjoy writing code and developing software solutions?",
                question_2="Are you passionate about solving problems through technology and logical thinking?", subgroup=software_sys)
        ]

        # Add all jobs to the session
        db.session.add_all(jobs_infra_env + jobs_mech_design + jobs_process_prod + jobs_software_sys)

        # Commit changes
        db.session.commit()
        print("Engineering & Systems cluster seeded successfully.")

seed_engineering()