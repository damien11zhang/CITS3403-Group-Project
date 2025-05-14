from app import app, db
from models import JobCluster, Subgroup, Job

def seed_business_strategy_data():
    with app.app_context():
        biz_strategy = JobCluster(
                                  name="Business & Strategy",
                                  description="Lead teams, solve business challenges, and drive organizational growth through planning and analysis.",
                                social=5,
                                physical=2,
                                leadership=9,
                                creativity=6,
                                logic=7)
        db.session.add(biz_strategy)

        strategy_roles = Subgroup(
            name="Strategy and Analysis Roles",
            subgroup_question="How interested are you in solving complex problems using data, logic, or long-term planning?",
            job_cluster=biz_strategy
        )
        db.session.add(strategy_roles)

        jobs_strategy = [
            Job(title="Consultant",
                question_1="How interested are you in solving business problems by analyzing data and offering advice?",
                question_2="How appealing is it to work with different companies to help improve their performance?",
                subgroup=strategy_roles),
            Job(title="Business Analyst",
                question_1="How interested are you in finding patterns in data to help businesses make smarter decisions?",
                question_2="How appealing is it to explore how companies can work more efficiently?",
                subgroup=strategy_roles),
            Job(title="Strategic Planner",
                question_1="How interested are you in setting long-term goals and figuring out how to achieve them?",
                question_2="How appealing is it to work behind the scenes to map out the big picture?",
                subgroup=strategy_roles)
        ]

        leadership_roles = Subgroup(
            name="Leadership & Management Roles",
            subgroup_question="How appealing is it to you to guide teams and projects to meet goals efficiently and effectively?",
            job_cluster=biz_strategy
        )
        db.session.add(leadership_roles)

        jobs_leadership = [
            Job(title="Product Manager",
                question_1="How interested are you in shaping how a product is built and brought to market?",
                question_2="How appealing is the idea of working between design, engineering, and business teams?",
                subgroup=leadership_roles),
            Job(title="Operations Manager",
                question_1="How interested are you in making sure things run smoothly in a business setting?",
                question_2="How appealing is it to find better ways to manage people, time, or resources?",
                subgroup=leadership_roles),
            Job(title="HR Business Partner",
                question_1="How interested are you in supporting teams and helping people thrive in their roles?",
                question_2="How appealing is it to be a link between people and company strategy?",
                subgroup=leadership_roles)
        ]

        marketing_roles = Subgroup(
            name="Marketing & Brand Roles",
            subgroup_question="How interested are you in creating and managing how products or companies connect with their audience?",
            job_cluster=biz_strategy
        )
        db.session.add(marketing_roles)

        jobs_marketing = [
            Job(title="Marketing Strategist",
                question_1="How curious are you about understanding what makes people buy things or pay attention to brands?",
                question_2="How appealing is it to create strategies that help businesses connect with their audience?",
                subgroup=marketing_roles),
            Job(title="Brand Manager",
                question_1="How curious are you about shaping how a product or company is seen by the public?",
                question_2="How appealing is it to manage a brand message across social media, ads, and packaging?",
                subgroup=marketing_roles)
        ]

        entrepreneurship_roles = Subgroup(
            name="Entrepreneurship & Finance Roles",
            subgroup_question="How appealing is the idea of managing money, taking risks, or starting your own venture?",
            job_cluster=biz_strategy
        )
        db.session.add(entrepreneurship_roles)

        jobs_entrepreneurship = [
            Job(title="Entrepreneur",
                question_1="How interested are you in starting and growing your own business or venture?",
                question_2="How appealing is it to take risks and bring new ideas to life?",
                subgroup=entrepreneurship_roles),
            Job(title="Financial Analyst",
                question_1="How interested are you in analyzing numbers to evaluate business performance or investment decisions?",
                question_2="How appealing is the idea of helping companies make smart financial choices?",
                subgroup=entrepreneurship_roles)
        ]

        db.session.add_all(jobs_strategy + jobs_leadership + jobs_marketing + jobs_entrepreneurship)

        db.session.commit()
        print("Business & Strategy cluster seeded successfully.")

if __name__ == "__main__":
    seed_business_strategy_data()
