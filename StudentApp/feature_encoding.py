import pandas as pd
import os

# Dictionary containing the file paths to each encoding CSV
ENCODING_FILES = {
    'Previous_Achievements': 'D:\ProjectHaji\HajiProject\EncodedFeatures\Previous_Achievements.csv',
    'Certifications': 'D:\ProjectHaji\HajiProject\EncodedFeatures\Certifications.csv',
    'Hard_Skills': 'D:\ProjectHaji\HajiProject\EncodedFeatures\Hard Skill 1.csv',
    'Soft_Skills': 'D:\ProjectHaji\HajiProject\EncodedFeatures\Soft Skill 1.csv',
    'Previous_Work_Experience_Type': 'D:\ProjectHaji\HajiProject\EncodedFeatures\Experience Type.csv',
    'Previous_JobProfile': 'D:\ProjectHaji\HajiProject\EncodedFeatures\PreviousJobProfile.csv',
    'Keywords': 'D:\ProjectHaji\HajiProject\EncodedFeatures\Keywords.csv',
    'Current_Job_Profile': 'D:\ProjectHaji\HajiProject\EncodedFeatures\CurrentJobProfile.csv',  
    'Interests': 'D:\ProjectHaji\HajiProject\EncodedFeatures\Interests.csv',
    'Career Goal': 'D:\ProjectHaji\HajiProject\EncodedFeatures\Career Goal.csv'    
}

def load_encoding(file_path):
    """Load the CSV file as a dictionary for quick lookup."""
    if file_path and os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            
            # Drop duplicates from 'value' column to avoid unhashable Series
            df = df.drop_duplicates(subset=['value'])
            
            # Convert the dataframe into a dictionary: {'value': 'code'}
            encoding_dict = df.set_index('value').to_dict()['code']
            return encoding_dict
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return {}
    else:
        print(f"File path {file_path} does not exist or is invalid.")
        return {}

def update_encoding(file_path, value, code):
    """Update the CSV file with a new value and code."""
    if file_path:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=['value', 'code'])

        new_row = pd.DataFrame({'value': [value], 'code': [code]})

        # Use pd.concat instead of append
        df = pd.concat([df, new_row], ignore_index=True)

        # Remove any duplicate 'value' rows to avoid Series issue
        df = df.drop_duplicates(subset=['value'])

        # Save the updated dataframe back to the CSV file
        df.to_csv(file_path, index=False)
    else:
        print(f"Invalid file path provided for {value}, could not update encoding.")

def get_encoded_value(column, value):
    """Get the numeric code for a value, or assign a new one if it doesn't exist."""
    file_path = ENCODING_FILES.get(column)
    
    if file_path is None:
        print(f"File path for column {column} not found in ENCODING_FILES.")
        return None

    # Load existing encodings
    encodings = load_encoding(file_path)

    # Ensure value is scalar (single element), not a Series
    if isinstance(value, pd.Series):
        # Convert Series to scalar by taking the first value
        value = value.iloc[0]

    # Check if the value already has an encoding
    if value in encodings:
        return encodings[value]
    else:
        # Assign a new code
        new_code = len(encodings) + 1  # Next available code
        update_encoding(file_path, value, new_code)
        return new_code

def apply_encodings(input_data_dict):
    """Apply encodings to the input data dictionary and return a DataFrame."""
    encoded_data = {}

    # Iterate through each key-value pair in the dictionary
    for column, value in input_data_dict.items():
        # Get the encoded value
        encoded_value = get_encoded_value(column, value)
        if encoded_value is not None:
            encoded_data[column] = encoded_value
    
    # Convert the encoded dictionary back to a DataFrame
    encoded_df = pd.DataFrame([encoded_data])
    return encoded_df

def get_Course_Data(student, skill_details, experience, grade_score):
    input_data = {
        'CGPA': float(student.cgpa),
        'Previous_Achievements': student.previous_achievements,
        'Certifications': skill_details.certifications,
        'Hard_Skills': skill_details.hard_skills_1,
        'Soft_Skills': skill_details.soft_skills_1,
        'Previous_Work_Experience_Type': experience.previous_work_experience_type,
        'Previous_JobProfile': experience.previous_job_profile,
        'Current_Work_Experience_Years': int(experience.current_work_experience_years),
        'Keywords': experience.keywords,
        'Current_Job_Profile': experience.current_job_profile,
        'Interests': experience.interests,
        'Career Goal': experience.career_goal,
        'Total_Grades': int(grade_score)
    }

    return apply_encodings(input_data)
