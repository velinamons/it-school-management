courses = [
    {
        "age_group": "6-8",
        "courses": [
            {
                "name": "Robot Explorers",
                "experience": ["Beginner", "Learner"],
                "goals": ["Creative Fun", "Future Education", "Innovation Exploration"]
            }
        ]
    },
    {
        "age_group": "9-12",
        "courses": [
            {
                "name": "Junior Robotics Innovators",
                "experience": ["Beginner", "Learner"],
                "goals": ["Creative Fun", "Innovation Exploration"]
            },
            {
                "name": "Robotics Project Designers",
                "experience": ["Learner", "Builder"],
                "goals": ["Future Education", "Innovation Exploration"]
            }
        ]
    },
    {
        "age_group": "13-15",
        "courses": [
            {
                "name": "Teen Robotics Fundamentals",
                "experience": ["Learner", "Builder"],
                "goals": ["Creative Fun"]
            },
            {
                "name": "Robotics Engineering Essentials",
                "experience": ["Builder", "Inventor"],
                "goals": ["Future Education", "Innovation Exploration"]
            }
        ]
    },
    {
        "age_group": "16-18",
        "courses": [
            {
                "name": "Advanced Robotics and AI",
                "experience": ["Inventor", "Builder"],
                "goals": ["Creative Fun", "Innovation Exploration"]
            },
            {
                "name": "Robotics Innovations and Careers",
                "experience": ["Inventor", "Builder"],
                "goals": ["Future Education"]
            }
        ]
    }
]


def filter_courses_by_age(courses, age_group):
    for group in courses:
        if group["age_group"] == age_group:
            return group["courses"]
    return []


def filter_courses_by_experience(courses, experience):
    return [course for course in courses if experience in course["experience"]]


def filter_courses_by_goals(courses, learning_goals):
    return [course for course in courses if any(goal in course["goals"] for goal in learning_goals)]


def select_course(courses, age_group, experience, learning_goals):
    age_filtered_courses = filter_courses_by_age(courses, age_group)
    experience_filtered_courses = filter_courses_by_experience(age_filtered_courses, experience)
    goal_matched_courses = filter_courses_by_goals(experience_filtered_courses, learning_goals)

    if goal_matched_courses:
        return goal_matched_courses[0]["name"]
    return "No suitable course found."
