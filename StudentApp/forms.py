from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    class Meta:
        model = Student
        fields = ['student_id', 'student_name', 'age', 'gender', 'race', 'location', 'email', 'password', 'cgpa', 'previous_achievements']
        labels = {
            'student_id': 'Student ID',
            'student_name': 'Full Name',
            'age': 'Age',
            'gender': 'Gender',
            'race': 'Race',
            'location': 'Location (State)',
            'email': 'Email Address',
            'cgpa': 'CGPA',
            'previous_achievements': 'Highest Qualification',
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("A student with this ID already exists.")
        return student_id

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


from django import forms
from .models import Student

class StudentLoginForm(forms.Form):
    student_id = forms.CharField(max_length=10, label='Student ID')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        password = cleaned_data.get('password')

        if not Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError('Student ID does not exist.')

        student = Student.objects.filter(student_id=student_id).first()
        if student and student.password != password:
            raise forms.ValidationError('Incorrect password.')

        return cleaned_data


#======================================================================================
from django import forms
from .models import Student, Feedback

class FeedbackForm(forms.ModelForm):
    student_id = forms.CharField(max_length=10, label="Student ID")

    class Meta:
        model = Feedback
        fields = [
            'student_id',  # Adding this to capture Student ID manually
            'counselor_name',
            'counselor_number',
            'feedback_text',
        ]
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4}),
        }

    # Custom validation for checking if Student ID exists
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        try:
            # Check if the student with the provided ID exists
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            raise forms.ValidationError(f"Student with ID {student_id} does not exist.")
        return student

#========================================================================
from django import forms
from .models import SkillDetails

class StudentSkillForm(forms.ModelForm):
    class Meta:
        model = SkillDetails
        fields = [
            'course_taken_1', 'grades_1',
            'course_taken_2', 'grades_2',
            'course_taken_3', 'grades_3',
            'certifications', 'hard_skills_1', 'hard_skills_2', 'hard_skills_3',
            'soft_skills_1', 'soft_skills_2', 'soft_skills_3'
        ]

    # You can add custom validation here if needed

from django import forms
from .models import StudentExperience

class StudentExperienceForm(forms.ModelForm):
    class Meta:
        model = StudentExperience
        fields = [
            'previous_work_experience_type', 
            'previous_work_experience_years',
            'previous_job_profile', 
            'previous_work_experience_at',
            'current_work_experience_type', 
            'current_work_experience_years',
            'current_job_profile', 
            'current_work_experience_at',
            'interests', 
            'keywords', 
            'career_goal'
        ]
        labels = {
            'previous_work_experience_type': 'Previous Work Experience Type',
            'previous_work_experience_years': 'Previous Work Experience Years',
            'previous_job_profile': 'Previous Job Profile',
            'previous_work_experience_at': 'Previous Work Experience At',
            'current_work_experience_type': 'Current Work Experience Type',
            'current_work_experience_years': 'Current Work Experience Years',
            'current_job_profile': 'Current Job Profile',
            'current_work_experience_at': 'Current Work Experience At',
            'interests': 'Interests',
            'keywords': 'Keywords',
            'career_goal': 'Career Goal',
        }

