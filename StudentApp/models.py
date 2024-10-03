from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    STATE_CHOICES = [
        ('Johor', 'Johor'),
        ('Kedah', 'Kedah'),
        ('Melaka', 'Melaka'),
        ('Negeri Sembilan', 'Negeri Sembilan'),
        ('Pahang', 'Pahang'),
        ('Penang', 'Penang'),
        ('Perak', 'Perak'),
        ('Selangor', 'Selangor'),
        ('Perlis', 'Perlis'),
        ('Sabah', 'Sabah'),
        ('Sarawak', 'Sarawak'),
        ('Kuala Lumpur', 'Kuala Lumpur'),
        ('Terengganu', 'Terengganu'),
        ('Labuan', 'Labuan'),
        ('Putrajaya', 'Putrajaya'),
    ]

    EXPERIENCE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Freelance', 'Freelance'),
    ]

    GRADE_CHOICES = [(i, str(i)) for i in range(101)]

    student_id = models.CharField(max_length=10, unique=True)
    student_name = models.CharField(max_length=100,null=True)
    age = models.IntegerField(choices=[(i, i) for i in range(18, 41)])
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    race = models.CharField(max_length=50)
    location = models.CharField(max_length=20, choices=STATE_CHOICES)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    previous_achievements = models.TextField(blank=True)

    def __str__(self):
        return self.student_id
 
#===============================================
from django.db import models

# Define grade choices as required
GRADE_CHOICES = [
    (1, 'A'),
    (2, 'B'),
    (3, 'C'),
    (4, 'D'),

]


class StudentDetails(models.Model):
    pass  # You can just delete this model definition.

class SkillDetails(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 
    
    # Courses and grades
    course_taken_1 = models.CharField(max_length=100)
    grades_1 = models.IntegerField(choices=GRADE_CHOICES)
    
    course_taken_2 = models.CharField(max_length=100, blank=True)# Optional
    grades_2 = models.IntegerField(choices=GRADE_CHOICES, blank=True)# Optional
    
    course_taken_3 = models.CharField(max_length=100, blank=True)# Optional
    grades_3 = models.IntegerField(choices=GRADE_CHOICES, blank=True)# Optional
    
    # Certifications
    certifications = models.TextField(blank=True)
    
    # Hard skills
    hard_skills_1 = models.CharField(max_length=100)  # Required
    hard_skills_2 = models.CharField(max_length=100, blank=True)  # Optional
    hard_skills_3 = models.CharField(max_length=100, blank=True)  # Optional
    
    # Soft skills
    soft_skills_1 = models.CharField(max_length=100)  # Required
    soft_skills_2 = models.CharField(max_length=100, blank=True)  # Optional
    soft_skills_3 = models.CharField(max_length=100, blank=True)  # Optional

    def __str__(self):
        return self.student.name


from django.db import models

EXPERIENCE_CHOICES = [
    ('Internship', 'Internship'),
    ('Full-time', 'Full-time'),
    ('Part-time', 'Part-time'),
    ('Freelance', 'Freelance')
]

class StudentExperience(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    
    # Previous Work Experience
    previous_work_experience_type = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, verbose_name="Previous Work Experience Type")
    previous_work_experience_years = models.IntegerField(choices=[(i, i) for i in range(0, 10)], verbose_name="Previous Work Experience Years")
    previous_job_profile = models.CharField(max_length=100, verbose_name="Previous Job Profile")
    previous_work_experience_at = models.CharField(max_length=100, verbose_name="Previous Work Experience At")
    
    # Current Work Experience
    current_work_experience_type = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, verbose_name="Current Work Experience Type")
    current_work_experience_years = models.IntegerField(choices=[(i, i) for i in range(0, 10)], verbose_name="Current Work Experience Years")
    current_job_profile = models.CharField(max_length=100, verbose_name="Current Job Profile")
    current_work_experience_at = models.CharField(max_length=100, verbose_name="Current Work Experience At")
    
    # Other Fields
    interests = models.TextField(blank=True, verbose_name="Interests")
    keywords = models.TextField(blank=True, verbose_name="Keywords")
    career_goal = models.TextField(blank=True, verbose_name="Career Goal")

    def __str__(self):
        return f"Experience of {self.student}"



   
class Feedback(models.Model):
    counselor_name = models.CharField(max_length=100)
    counselor_number = models.CharField(max_length=15)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Assuming you have a Student model
    feedback_text = models.TextField()
    feedback_date = models.DateField(auto_now_add=True)  # Automatically capture date
    feedback_time = models.TimeField(auto_now_add=True)  # Automatically capture time

    def __str__(self):
        return f"Feedback from {self.counselor_name} for : {self.student.student_id} Feedback Text {self.feedback_text}"


class Recruiter(models.Model):
    recruiter_id = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.recruiter_id