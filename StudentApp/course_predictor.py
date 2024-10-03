import json
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# Helper function for numpy encoding in JSON
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
        
cm_path = Path(__file__).parents[1] / 'HajiProject/Data/class_mapping.txt'
# Function to save updated class_mappings back to class_mapping.txt
def save_updated_mappings(class_mappings):
    with open('cm_path', 'w') as f:
        modified_mappings = {
            k: {str(k2): v2 for k2, v2 in v.items()} if isinstance(v, dict) else v 
            for k, v in class_mappings.items()
        }
        f.write(json.dumps(modified_mappings, cls=NpEncoder))
        
ct_path = Path(__file__).parents[1] / 'HajiProject/Data/course_taken.txt'
cm_path = Path(__file__).parents[1] / 'HajiProject/Data/class_mapping.txt'
# Function to load predefined course_taken and class_mappings from text files
def load_predefined_mappings():
    # Load course_taken mapping from course_taken.txt
    with open('ct_path', 'r') as f:
        course_taken = json.load(f)
    
    # Load class_mappings from class_mapping.txt
    try:
        with open('cm_path', 'r') as f:
            class_mappings = json.load(f)
    except json.JSONDecodeError:
        class_mappings = {}
    
    return course_taken, class_mappings

# Function to map new student data using class_mappings (and update if new values are found)
def map_and_update_mappings(new_data, class_mappings):
    mapped_values = {}
    updated = False  # Flag to track if any new mappings were added

    for column in new_data:
        # Skip numeric columns like CGPA and Current_Work_Experience_Years
        if column in ['CGPA', 'Current_Work_Experience_Years']:
            mapped_values[column] = new_data[column][0] if isinstance(new_data[column], list) else new_data[column]
            continue  # Skip mapping for these numeric columns

        # Handle scalar values like int, float, or string
        value = new_data[column] if isinstance(new_data[column], (int, float, str)) else new_data[column][0]

        if column in class_mappings:
            if value in class_mappings[column]:
                mapped_values[column] = class_mappings[column][value]
            else:
                # Assign a new value for the unmapped entry
                new_value_index = len(class_mappings[column])
                class_mappings[column][value] = new_value_index
                mapped_values[column] = new_value_index
                updated = True  # Mark that the mapping was updated
        else:
            # If the column does not exist in class_mappings, create it
            class_mappings[column] = {value: 0}
            mapped_values[column] = 0
            updated = True  # Mark that the mapping was updated

    if updated:
        save_updated_mappings(class_mappings)  # Save only if new mappings are added

    # Ensure numeric values like Total_Grades are used as-is
    mapped_values['Total_Grades'] = new_data['Total_Grades'][0] if isinstance(new_data['Total_Grades'], list) else new_data['Total_Grades']
    
    return mapped_values, class_mappings

# Function to encode target using course_taken mapping
def encode_df_target(df_target, course_taken):
    df_target_encoded = df_target['CourseTaken'].map(course_taken)
    
    if df_target_encoded.isnull().any():
        raise ValueError("Some target values could not be encoded. Please check if all course names are covered in the course_taken.txt.")
    
    return df_target_encoded

# Function to apply class mappings and ensure all categorical columns are encoded as numeric
def apply_class_mappings(df, class_mappings):
    df_encoded = df.copy()
    updated = False  # Flag to track if we need to save updated mappings

    for column in df.columns:
        # Skip numeric columns like CGPA and Current_Work_Experience_Years
        if column in ['CGPA', 'Current_Work_Experience_Years']:
            continue

        if column in class_mappings:
            for i, value in df[column].items():
                if value in class_mappings[column]:
                    df_encoded.at[i, column] = class_mappings[column][value]
                else:
                    # Create new mapping for new values
                    new_value_index = len(class_mappings[column])
                    class_mappings[column][value] = new_value_index
                    df_encoded.at[i, column] = new_value_index
                    updated = True  # Mark that mappings were updated
        else:
            # Create a new mapping for the column if it doesn't exist
            class_mappings[column] = {}
            for i, value in df[column].items():
                new_value_index = len(class_mappings[column])
                class_mappings[column][value] = new_value_index
                df_encoded.at[i, column] = new_value_index
                updated = True

    # Save updated mappings back to file if changes occurred
    if updated:
        save_updated_mappings(class_mappings)

    return df_encoded

# Function to ensure all columns are numeric
def ensure_numeric(df):
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

# Function to predict the course taken based on new student data and historic data
def Predict_CourseTaken(df_features_encoded, df_target, new_data_encoded):
    # Ensure all columns are numeric
    df_features_encoded = ensure_numeric(df_features_encoded)
    new_data_encoded = ensure_numeric(new_data_encoded)

    # Separate features (X) and target (y)
    X = df_features_encoded
    y = df_target

    # Ensure all columns are numeric
    print("Data types before passing to XGBoost:")
    print(X.dtypes)  # Debugging to check dtypes

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train XGBoost model
    model = XGBClassifier()

    # Train the model
    model.fit(X_train, y_train)

    # Predict the course for new_data
    predicted_course_encoded = model.predict(new_data_encoded)

    print('Predicted Course Taken for new data:', predicted_course_encoded)

    return predicted_course_encoded  # Return the predicted encoded course value

# Main function to predict the course based on new data
def predict_course(new_data):
    # Load predefined mappings
    course_taken, class_mappings = load_predefined_mappings()

    # Load the historic data (this will contain df_features and df_target)
    df = pd.read_csv('D:\ProjectHaji\HajiProject\Data\epic1data.csv')

    # Select relevant features
    df_features = df[['CGPA', 'Previous_Achievements', 'Certifications', 'Hard_Skills',
                      'Soft_Skills', 'Previous_Work_Experience_Type', 'Previous_JobProfile',
                      'Current_Work_Experience_Years', 'Keywords', 'Current_Job_Profile',
                      'Interests', 'Career Goal', 'Total_Grades']]

    df_target = df[['CourseTaken']]

    # Encode df_target using the course_taken dictionary
    df_target_encoded = encode_df_target(df_target, course_taken)

    # Apply class mappings to encode categorical features in df_features
    df_features_encoded = apply_class_mappings(df_features, class_mappings)

    # Ensure all features are numeric
    print("Data types after encoding:")
    print(df_features_encoded.dtypes)  # Debugging to ensure all columns are numeric

    # Map new student data and update class_mappings if new values are found
    mapped_values, updated_class_mappings = map_and_update_mappings(new_data, class_mappings)

    # Save the updated class mappings back to class_mapping.txt
    save_updated_mappings(updated_class_mappings)

    # Prepare the new data for prediction
    new_data_encoded = pd.DataFrame([mapped_values])

    # Predict the course based on new data and historic data
    predicted_course_encoded = Predict_CourseTaken(df_features_encoded, df_target_encoded, new_data_encoded)

    # Reverse the course_taken dictionary to map encoded values to course names
    reversed_course_taken = {v: k for k, v in course_taken.items()}

    # Decode the predicted_course_encoded using the reversed dictionary
    predicted_course_name = reversed_course_taken.get(predicted_course_encoded[0], "Course Not Found")

    return predicted_course_name
