from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegistrationForm
from .forms import StudentLoginForm
from .models import Student

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'registration.html', {'form': form})

#==========================================LOGIN

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentLoginForm

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            # Get student_id from the form
            student_id = form.cleaned_data['student_id']
            try:
                # Fetch the student object
                student = Student.objects.get(student_id=student_id)
                
                # Set student_id in the session
                request.session['student_id'] = student.student_id
                request.session.modified = True  # Ensure the session is saved
                
                messages.success(request, 'Login successful.')
                return redirect('fill_details')  # Redirect to FillDetails.html
            except Student.DoesNotExist:
                messages.error(request, 'Student ID not found.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid login credentials.')
    else:
        form = StudentLoginForm()
    
    return render(request, 'login.html', {'form': form})

#======================================================================

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student


def dashboard(request):
    # Check if student_id exists in session
    student_id = request.session.get('student_id')
    print("Student ID from session:", student_id)

    if student_id:
        try:
            # Fetch the student details using student_id
            student = Student.objects.get(student_id=student_id)
            print("Student fetched:", student)
        except Student.DoesNotExist:
            print("Student does not exist.")
            messages.error(request, 'Student not found.')
            return redirect('login')
        
        # Pass the student information to the template
        return render(request, 'dashboard.html', {'student': student})
    else:
        print("No student ID found in session.")
        # If student_id is not found in session, redirect to login
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('login')

    
def logout_view(request):
    # Clear the session
    request.session.flush()
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')



#===========================FEEDBACK===============================================================

# views.py
from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback

# views.py
from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback

def give_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Get the student object from the cleaned data
            student = form.cleaned_data.get('student_id')

            # Use update_or_create to either update an existing feedback or create a new one
            feedback, created = Feedback.objects.update_or_create(
                student=student,  # Matching condition (student_id)
                defaults={
                    'counselor_name': form.cleaned_data.get('counselor_name'),
                    'counselor_number': form.cleaned_data.get('counselor_number'),
                    'feedback_text': form.cleaned_data.get('feedback_text'),
                }
            )

            # Redirect to success page with student information
            return redirect('feedback_success', student_id=student.student_id, student_name=student.student_name)
        else:
            # Clear the student_id field only if the form is not valid
            form.fields['student_id'].initial = ''

    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})


# feedback_success view to handle passed data
def feedback_success(request, student_id, student_name):
    return render(request, 'feedback_success.html', {
        'student_id': student_id,
        'student_name': student_name
    })



#---------------------------SENTIMENT------------------------------------
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Feedback
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer
url="https:\\github.com\Kadirjpn\ProMa\blob\main\HajiProject\PKL_Files\model_feedback_analyzer.pkl"
# Load the sentiment analyzer model from the pickle file
with open(f'model_feedback_analyzer.pkl', 'rb') as f:
    loaded_analyzer = pickle.load(f)

def get_sentiment_score_and_label(text):
    scores = loaded_analyzer.polarity_scores(text)
    if scores['compound'] >= 0.670500:
        sentiment = 'Excellent Progress'
    elif 0.510600 <= scores['compound'] <= 0.670500:
        sentiment = 'Very Good Progress'
    elif 0.077200 <= scores['compound'] <= 0.510600:
        sentiment = 'Good Progress'
    elif scores['compound'] < 0.00000:
        sentiment = 'No Progress'
    else:
        sentiment = 'Neutral'
    return scores['compound'], sentiment

def predict_feedback_sentiment(feedback_text):
    score, sentiment = get_sentiment_score_and_label(feedback_text)
    message = f"Progress Percentage: {score*100:.2f}%, Remark: {sentiment}"
    return message

# View to get counselor feedback and display sentiment analysis
def get_counselor_feedback(request):
    # Get the student_id from the session
    student_id = request.session.get('student_id')
    sentiment_message=""
    try:
        # Fetch the feedback for the given student_id
        feedback = Feedback.objects.get(student__student_id=student_id)
        feedback_text = feedback.feedback_text

        # Analyze the sentiment of the feedback text
        sentiment_message = predict_feedback_sentiment(feedback_text)
        sentiment_parts = sentiment_message.split(", ")
        score = sentiment_parts[0]  # First part: Progress Percentage
        remark = sentiment_parts[1]  # Second part: Remark
        
        context={
            
            'c_id':feedback.counselor_number,
            'c_name':feedback.counselor_name,
            'f_date':feedback.feedback_date,
            'f_time':feedback.feedback_time,
            'f_text':feedback.feedback_text,
            'score':score,
            'remark':remark
        }
        # If feedback exists, render the feedback_result.html template
        return render(request, 'feedback_result.html', context)

    except Feedback.DoesNotExist:
        # If no feedback is found, display message on the dashboard
        context = {'message': "Feedback Not Yet Provided"}
       
        # Render the dashboard with the message
        return render(request, 'dashboard.html', context)

#==================================================================
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentSkillForm
from .models import SkillDetails, Student

'''def fill_details(request):
    # Check if student_id exists in the session
    student_id = request.session.get('student_id')
    
    if not student_id:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('login')

    # Check if skill details exist for the student using filter and exists
    if SkillDetails.objects.filter(student_id=student_id).exists():
        show_fill_button = False  # Skill details already exist
    else:
        show_fill_button = True  # No skill details, show the button

    # Check if experience details exist for the student using filter and exists
    if StudentExperience.objects.filter(student_id=student_id).exists():
        show_experience_button = False  # Skill details already exist
    else:
        show_experience_button = True  # No skill details, show the button

    # Check if both buttons should be hidden and dashboard button should be shown
    if not show_fill_button and not show_experience_button:
        show_dashboard_button = True  # Show dashboard button
    else:
        show_dashboard_button = False  # Do not show dashboard button

    context = {
        'show_fill_button': show_fill_button,
        'show_experience_button': show_experience_button,
        'show_dashboard_button': show_dashboard_button,  # Pass to template
        'student_id':student_id,
    }
    print("hello",student_id)
    # Render FillDetails.html with the show_fill_button context
    return render(request, 'fill_details.html', context)
    '''


def fill_details(request):
    # Retrieve student_id from session
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('login')  # Redirect to login if session expired or no student_id

    error_message = None  # Initialize the error message to None

    try:
        # Fetch the Student object using student_id
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        error_message = 'No student found with the given ID.'

    if not error_message:
        # Check if SkillDetails exist for the student
        skill_exists = SkillDetails.objects.filter(student=student).exists()

        # Check if StudentExperience exists for the student
        experience_exists = StudentExperience.objects.filter(student=student).exists()

        # Determine which buttons to show
        show_fill_skill_button = not skill_exists
        show_fill_experience_button = not experience_exists
        show_dashboard_button = skill_exists and experience_exists
    else:
        # If there's an error, hide all buttons
        show_fill_skill_button = show_fill_experience_button = show_dashboard_button = False

    return render(request, 'fill_details.html', {
        'student_id': student_id,
        'show_fill_button': show_fill_skill_button,
        'show_experience_button': show_fill_experience_button,
        'show_dashboard_button': show_dashboard_button,
        'error_message': error_message  # Pass the error message to the template
    })
#==============================

from django.shortcuts import render, redirect
from .models import SkillDetails
from .forms import StudentSkillForm
from django.contrib.auth.decorators import login_required

#@login_required
def student_skill_form_view(request):
    # Retrieve student_id from session or other logic
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('login')  # Ensure the user is redirected to login if session is expired or invalid

    # Fetch the Student object using student_id
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        messages.error(request, 'No student found with the given ID.')
        return redirect('error_page')  # Redirect to an error page if no student is found

    if request.method == 'POST':
        form = StudentSkillForm(request.POST)
        if form.is_valid():
            skill_details = form.save(commit=False)
            skill_details.student = student  # Assign the student object based on the student_id
            skill_details.save()
            return redirect('fill_details')  # Redirect to the fill details page or another success page
    else:
        form = StudentSkillForm()

    return render(request, 'student_skill_form.html', {'form': form})


from .forms import StudentExperienceForm
from .models import StudentExperience

def fill_experience_details(request):
    # Get the student_id from the session
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('login')  # Redirect to login if session expired or no student_id

    # Fetch the Student object using student_id
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        messages.error(request, 'No student profile found for the given ID.')
        return redirect('error_page')  # Redirect to an error page if no student is found

    if request.method == 'POST':
        form = StudentExperienceForm(request.POST)
        if form.is_valid():
            experience_details = form.save(commit=False)
            experience_details.student = student  # Assign the student object
            experience_details.save()
            return redirect('fill_details')  # Redirect to the fill details page or another success page
    else:
        form = StudentExperienceForm()

    return render(request, 'student_experience_form.html', {'form': form})

#======================================COURSE RECOMMENDATION=====================================

from .models import Student, SkillDetails, StudentExperience
from .findScores import get_profile_score, get_hard_skill_score, get_soft_skill_score,get_grade_score
from .feature_encoding import apply_encodings,get_Course_Data
from sklearn.preprocessing import LabelEncoder
from .course_predictor import predict_course

def student_recommendation_view(request):
    # Retrieve student_id from session
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('login')

    # Fetch the Student, SkillDetails, and StudentExperience based on student_id
    try:
        student = Student.objects.get(student_id=student_id)
        skill_details = SkillDetails.objects.filter(student=student).first()  # Assuming one set of skill details per student
        experience_details = StudentExperience.objects.filter(student=student).first()  # Assuming one set of experience details per student

        if not skill_details or not experience_details:
            messages.error(request, 'No skill or experience details found for this student.')
            return redirect('dashboard')  # Redirect back to the dashboard if no data is found

    except Student.DoesNotExist:
        messages.error(request, 'No student profile found for the given ID.')
        return redirect('dashboard')  # Redirect to the dashboard if no student is found

    # Perform Calculation to Find Profile Score
    hard_skill_score=get_hard_skill_score(skill_details)
    soft_skill_score=get_soft_skill_score(skill_details)
    grade_score=get_grade_score(skill_details)
    overall_score=int(hard_skill_score)+int(soft_skill_score)+int(grade_score)+float(student.cgpa)
    profile_score=get_profile_score(overall_score)

    hard_skills=skill_details.hard_skills_1+", "+skill_details.hard_skills_2 +", "+skill_details.hard_skills_3
    soft_skills=skill_details.soft_skills_1+", "+skill_details.soft_skills_1+", "+skill_details.soft_skills_3
    
    input_data = {
        'CGPA': [float(student.cgpa)],
        'Previous_Achievements': [student.previous_achievements],
        'Certifications': [skill_details.certifications],
        'Hard_Skills': hard_skills,
        'Soft_Skills': soft_skills,
        'Previous_Work_Experience_Type': [experience_details.previous_work_experience_type],
        'Previous_JobProfile': [experience_details.previous_job_profile],
        'Current_Work_Experience_Years': [int(experience_details.current_work_experience_years)],
        'Keywords': [experience_details.keywords],
        'Current_Job_Profile': [experience_details.current_job_profile],
        'Interests': [experience_details.interests],
        'Career Goal': [experience_details.career_goal],
        'Total_Grades': int(overall_score)  
    }
   
   
    print("@@@@ In Viewws.py **** BEFORE PREDICTING input_data",input_data)
    
    # Predict the course
     # Predict the course
    predicted_course_name = predict_course(input_data)

    if not predicted_course_name:
        messages.error(request, 'There was an issue with the course prediction. Please try again later.')
        return redirect('dashboard')
   
    print("****** Predicted Course Name=",predicted_course_name)

    # Pass all the data to the recommendation template
    context = {
        'student': student,
        'skill_details': skill_details,
        'experience_details': experience_details,
        'hard_skill_score':hard_skill_score,
        'soft_skill_score':soft_skill_score,
        'grade_score':grade_score,
        'profile_score':profile_score,
        'overall_score':overall_score,
        'course_name': predicted_course_name,
        #'grade_comparison':result_grade_comparison
    }

    return render(request, 'recommendation.html', context)

#-----------------------GRAPH PLOT---------------------------
from django.shortcuts import render
from .plot_grade import plot_grade_comparison_view  # Import the method you provided

def student_track_progress_view(request):
    student_id = request.session.get('student_id')  # Assuming `student_id` is stored in session
    print("Student Id Here",student_id)
    # If student_id is not found in session, redirect to an error page
    if not student_id:
        return render(request, 'student_track_progress.html', {'message': 'Student ID not found in session.'})

    # Call the plot_grade_comparison_view function to generate the plots
    result = plot_grade_comparison_view(request, student_id)

    # If no result was returned (student not found in CSV)
    if result is None:
        return render(request, 'student_track_progress.html', {'message': 'Student data not found.'})

    # Render the template with the plot data
    return render(request, 'student_track_progress.html', result)

#=====================================Recruiter=================================
from .models import Recruiter

def recruiter_login(request):
    if request.method == 'POST':
        recruiter_id = request.POST['recruiter_id']
        password = request.POST['password']

        try:
            recruiter = Recruiter.objects.get(recruiter_id=recruiter_id)
            if recruiter.password == password:
                request.session['recruiter_id'] = recruiter.recruiter_id
                return redirect('recruiter_dashboard')
            else:
                messages.error(request, 'Invalid password')
        except Recruiter.DoesNotExist:
            messages.error(request, 'Recruiter ID not found')
    
    return render(request, 'recruiter_login.html')

def recruiter_register(request):
    if request.method == 'POST':
        recruiter_id = request.POST['recruiter_id']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('recruiter_register')

        # Check if recruiter ID or email already exists
        if Recruiter.objects.filter(recruiter_id=recruiter_id).exists():
            messages.error(request, 'Recruiter ID already exists')
        elif Recruiter.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            # Save new recruiter
            recruiter = Recruiter(recruiter_id=recruiter_id, email=email, password=password)
            recruiter.save()
            messages.success(request, 'Recruiter registered successfully!')
            return redirect('recruiter_login')
    
    return render(request, 'recruiter_register.html')

from django.shortcuts import render
from .models import SkillDetails, Student, StudentExperience
from django.contrib import messages

from django.shortcuts import render
from .models import SkillDetails, Student, StudentExperience
from django.contrib import messages

from django.shortcuts import render
from .models import SkillDetails, Student, StudentExperience
from django.contrib import messages

def recruiter_dashboard(request):
    recruiter_id = request.session.get('recruiter_id')

    # Fetch unique hard skills
    hard_skills_1 = SkillDetails.objects.values_list('hard_skills_1', flat=True).distinct()
    hard_skills_2 = SkillDetails.objects.values_list('hard_skills_2', flat=True).distinct()
    hard_skills_3 = SkillDetails.objects.values_list('hard_skills_3', flat=True).distinct()

    # Combine and deduplicate the list of hard skills
    unique_hard_skills = sorted(set(hard_skills_1) | set(hard_skills_2) | set(hard_skills_3))

    students_with_details = []

    if request.method == 'POST':
        hard_skill = request.POST.get('hard_skills')
        recommendations = request.POST.get('recommendations')

        if not hard_skill:
            messages.error(request, 'Please select a hard skill.')
        else:
            try:
                recommendations = int(recommendations)

                # Fetch students with the selected hard skill from SkillDetails
                skill_filtered_students = SkillDetails.objects.filter(
                    hard_skills_1=hard_skill
                ).values_list('student__student_id', flat=True)

                print(f"Filtered student IDs: {skill_filtered_students}")

                # Include hard_skills_2 and hard_skills_3 in filtering
                skill_filtered_students |= SkillDetails.objects.filter(
                    hard_skills_2=hard_skill
                ).values_list('student__student_id', flat=True)
                skill_filtered_students |= SkillDetails.objects.filter(
                    hard_skills_3=hard_skill
                ).values_list('student__student_id', flat=True)

                # Ensure IDs are strings (for CharField student_id)
                skill_filtered_students = list(map(str, skill_filtered_students))

                # Fetch the required number of students from Student model
                students = Student.objects.filter(student_id__in=skill_filtered_students)[:recommendations]
                print(f"Student queryset: {students}")

                if not students.exists():
                    messages.error(request, 'No students found for the selected hard skill.')
                
                # Fetch corresponding skill details and experience for students
                for student in students:
                    try:
                        skill_details = SkillDetails.objects.get(student=student)
                        experience = StudentExperience.objects.get(student=student)
                        students_with_details.append({
                            'student_name': student.student_name,
                            'email': student.email,
                            'cgpa': student.cgpa,
                            'certifications': skill_details.certifications,
                            'coursetaken': skill_details.course_taken_1 +" , "+ skill_details.course_taken_2 +" , "+ skill_details.course_taken_3,
                            'totexperience': int(experience.current_work_experience_years)+ int(experience.previous_work_experience_years),
                        })
                    except (SkillDetails.DoesNotExist, StudentExperience.DoesNotExist):
                        # Handle cases where experience or skill details are missing
                        students_with_details.append({
                            'student_name': student.student_name,
                            'email': student.email,
                            'cgpa': student.cgpa,
                            'certifications': 'N/A',
                            'course_taken_1': 'N/A',
                            'experience': 'N/A',
                        })

               # messages.success(request, f'Requesting {recommendations} recommendations for {hard_skill} skill.')

            except ValueError:
                messages.error(request, 'Please enter a valid number for recommendations.')

    return render(request, 'recruiter_dashboard.html', {
        'unique_hard_skills': unique_hard_skills,
        'students_with_details': students_with_details,
    })

from django.contrib.auth import logout
def recruiter_logout(request):
    logout(request)
    return redirect('recruiter_login')  # Redirect to the login page after logout
