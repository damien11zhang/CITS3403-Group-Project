from app import app, db
from models import JobCluster, Subgroup, Job

def seed_creative_data():
    with app.app_context():
        creative_data = JobCluster(
                                   name="Creative & Design",
                                   description="Express ideas and emotions through visuals, storytelling, and imaginative design.")
        db.session.add(creative_data)

        design_roles = Subgroup(
            name="Digital Design & Interaction",
            subgroup_question="How interested are you in designing digital visuals or environments that are clear, useful, or interactive?",
            job_cluster=creative_data
        )
        db.session.add(design_roles)

        jobs_design = [
            Job(title="UI/UX Designer",
                question_1="How interested are you in improving how people interact with websites or apps?",
                question_2="How appealing is it to you to create designs that are both beautiful and easy to use?",
                subgroup=design_roles),
            Job(title="Graphic Designer",
                question_1="How interested are you in creating visual designs like posters, logos, or social media graphics?",
                question_2="How appealing is it to you to communicate ideas through images and design?",
                subgroup=design_roles),
            Job(title="3D Modeler",
                question_1="How curious are you about designing 3D objects for games, animation, or virtual environments?",
                question_2="How appealing is it to turn ideas into realistic or stylized 3D visuals?",
                subgroup=design_roles)
        ]
        motion_roles = Subgroup(
            name="Motion & Media",
            subgroup_question="How appealing is it to you to create dynamic content like videos, animations, or media for entertainment or education?",
            job_cluster=creative_data
        )
        db.session.add(motion_roles)

        jobs_motion = [
            Job(title="Animator",
                question_1="How curious are you about bringing characters or visuals to life through motion?",
                question_2="How interested are you in using tools to create animations for games, ads, or films?",
                subgroup=motion_roles),
            Job(title="Video Editor",
                question_1="How appealing is it to take raw video footage and shape it into a polished final product?",
                question_2="How interested are you in using editing tools to tell a story or convey emotion?",
                subgroup=motion_roles),
            Job(title="Content Creator",
                question_1="How interested are you in expressing ideas through videos, writing, or other digital media?",
                question_2="How appealing is the idea of building an audience by sharing creative content online?",
                subgroup=motion_roles)
        ]

        visual_roles = Subgroup(
            name="Visual Arts & Storytelling",
            subgroup_question="How interested are you in using art or photography to tell stories or convey a message?",
            job_cluster=creative_data
        )
        db.session.add(visual_roles)

        jobs_visual = [
            Job(title="Illustrator",
                question_1="How interested are you in creating art for books, branding, or digital media?",
                question_2="How appealing is it to draw or paint ideas that help bring a message or story to life?",
                subgroup=visual_roles),
            Job(title="Photographer",
                question_1="How interested are you in capturing moments, scenes, or people through a camera lens?",
                question_2="How appealing is it to you to edit and enhance photos to create visual impact?",
                subgroup=visual_roles)
        ]

        leadership_roles = Subgroup(
            name="Creative Leadership",
            subgroup_question="How appealing is it to you to lead creative projects and guide the vision behind visuals or campaigns?",
            job_cluster=creative_data
        )
        db.session.add(leadership_roles)

        jobs_leadership = [
            Job(title="Art Director",
                question_1="How interested are you in guiding the visual style and feel of creative projects?",
                question_2="How appealing is it to lead a team of designers or artists toward a shared creative vision?",
                subgroup=leadership_roles),
            Job(title="Creative Director",
                question_1="How interested are you in overseeing the overall look, tone, and message of creative campaigns?",
                question_2="How appealing is the idea of combining business goals with visual storytelling?",
                subgroup=leadership_roles)
        ]

        db.session.add_all(jobs_design + jobs_motion + jobs_visual + jobs_leadership)
        db.session.commit()
        print("Creative & Visual cluster seeded successfully.")

seed_creative_data()