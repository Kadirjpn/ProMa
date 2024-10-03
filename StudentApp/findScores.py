def get_grade_score(skill_details):
    total=skill_details.grades_1+skill_details.grades_2+skill_details.grades_3
    percentage=total/3
    if percentage==1:
        grade_score=5
    elif percentage==2:
        grade_score=3
    elif percentage==3:
        grade_score=2
    else:
        grade_score=1
    return grade_score


def get_hard_skill_score(student):
# Logic to calculate hard skills score
    hard_skills = [student.hard_skills_1, student.hard_skills_2, student.hard_skills_3]
    if hard_skills[0] == hard_skills[1] == hard_skills[2]:
        hard_skill_score = 1  # All hard skills are the same
    elif hard_skills[0] != hard_skills[1] and hard_skills[0] != hard_skills[2] and hard_skills[1] != hard_skills[2]:
        hard_skill_score = 5  # All hard skills are different
    else:
        hard_skill_score = 3  # Two hard skills are the same, one is different
    return hard_skill_score


def get_soft_skill_score(student):
    # Logic to calculate soft skills score
    soft_skills = [student.soft_skills_1, student.soft_skills_2, student.soft_skills_3]
    if soft_skills[0] == soft_skills[1] == soft_skills[2]:
        soft_skill_score = 1  # All soft skills are the same
    elif soft_skills[0] != soft_skills[1] and soft_skills[0] != soft_skills[2] and soft_skills[1] != soft_skills[2]:
        soft_skill_score = 5  # All soft skills are different
    else:
        soft_skill_score = 2  # Two soft skills are the same, one is different
    return soft_skill_score

def get_profile_score(overall_score):
    if overall_score >= 15:
        profile_score = 'A+'
    elif 10 <= overall_score < 15:
        profile_score = 'A'
    elif 8 <= overall_score < 10:
        profile_score = 'B'
    elif 5 <= overall_score < 8:
        profile_score = 'C'
    else:
        profile_score = 'D'
    return profile_score