import pandas as pdcd
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64
import numpy as np
import pandas as pd
# Use the non-interactive Agg backend
matplotlib.use('Agg')

def plot_grade_comparison_view(request, student_id):
    # Load the CSV file

    # df_path = Path(__file__).parents[1] / 'HajiProject/Data/epic1data.csv' 
    df = pd.read_csv('HajiProject/Data/epic1data.csv')
    print("------------", int(student_id))
    
    # Plot 1: Grade comparison
    # Check if a student with the given ID exists
    student_df = df[df['Student_id'] == int(student_id)]
    
    if student_df.empty:
        print(f"No student found with ID {student_id}")
        return None
    else:
        # Get the final grade of the student
        selected_student_grade = student_df['Final_Grade'].values[0]        
        print("Selected Grade", selected_student_grade)
        
        
        same_grade_count = df[df['Final_Grade'] == selected_student_grade].shape[0]
        grade_hierarchy = ['A', 'B', 'C', 'D']
        above_grades = grade_hierarchy[:grade_hierarchy.index(selected_student_grade)]
        below_grades = grade_hierarchy[grade_hierarchy.index(selected_student_grade) + 1:]
        above_count = df[df['Final_Grade'].isin(above_grades)]['Final_Grade'].value_counts()
        below_count = df[df['Final_Grade'].isin(below_grades)]['Final_Grade'].value_counts()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='#f5f5f5')

        # Plotting students with grades above
        color_palette_above = plt.cm.Blues(np.linspace(0.3, 0.7, len(above_count)))
        bars_above = ax1.bar(above_count.index, above_count.values, color=color_palette_above, edgecolor='black', linewidth=1.5, width=0.6)
        ax1.set_title(f'Students with Grades Above Your Grade = {selected_student_grade}', fontsize=14, weight='bold', backgroundcolor='#cfe2f3', pad=20)
        ax1.set_xlabel('Grades', fontsize=12)
        ax1.set_ylabel('Number of Students', fontsize=12, labelpad=10)
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax1.legend(['Grades Above'], loc='upper right')  # Legend placement

        # Add counts on top of bars for above grades
        for bar in bars_above:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(height)}', ha='center', va='bottom', fontsize=10, color='black')

        # Plotting students with grades below
        color_palette_below = plt.cm.Reds(np.linspace(0.3, 0.7, len(below_count)))
        bars_below = ax2.bar(below_count.index, below_count.values, color=color_palette_below, edgecolor='black', linewidth=1.5, width=0.6)
        ax2.set_title(f'Students with Grades Below Your Grade = {selected_student_grade}', fontsize=14, weight='bold', backgroundcolor='#f4cccc', pad=20)
        ax2.set_xlabel('Grades', fontsize=12)
        ax2.set_ylabel('Number of Students', fontsize=12, labelpad=10)
        ax2.grid(True, linestyle='--', alpha=0.5)
        ax2.legend(['Grades Below'], loc='upper right')  # Legend placement

        # Add counts on top of bars for below grades
        for bar in bars_below:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(height)}', ha='center', va='bottom', fontsize=10, color='black')

        plt.tight_layout(pad=3.0)

        # Save plot to a buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png_grade_comparison = buffer.getvalue()
        buffer.close()

        # Close the plot to avoid memory leaks
        plt.close(fig)

        # Encode the image in base64
        encoded_image_grade_comparison = base64.b64encode(image_png_grade_comparison).decode('utf-8')

        
        # Plot 2: Course comparison (same as before)
        selected_student_course = student_df['CourseTaken'].values[0]

        same_course_count = df[df['CourseTaken'] == selected_student_course].shape[0]
        other_courses_count = df[df['CourseTaken'] != selected_student_course]['CourseTaken'].value_counts()

        fig, (ax3, ax4) = plt.subplots(2, 1, figsize=(8, 10), facecolor='#f5f5f5')  # Two rows (stacked)

        color_palette_same_course = plt.cm.Greens(np.linspace(0.3, 0.7, 1))
        color_palette_other_courses = plt.cm.Oranges(np.linspace(0.3, 0.7, len(other_courses_count)))

        # Plot same course
        bars_same_course = ax3.bar([selected_student_course], [same_course_count], color=color_palette_same_course, edgecolor='black', linewidth=1.5, width=0.6)
        ax3.set_title(f'Students with Same Course: {selected_student_course}', fontsize=14, weight='bold', backgroundcolor='#d9ead3', pad=20)
        ax3.set_ylabel('Number of Students', fontsize=12, labelpad=10)
        ax3.grid(True, linestyle='--', alpha=0.5)
            
            # Annotate the count on the bars for same course
        for bar in bars_same_course:
            yval = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=12, weight='bold')

            # Plot other courses
        bars_other_courses = ax4.bar(other_courses_count.index, other_courses_count.values, color=color_palette_other_courses, edgecolor='black', linewidth=1.5, width=0.6)
        ax4.set_title('Students with Other Courses', fontsize=14, weight='bold', backgroundcolor='#fce5cd', pad=20)
        ax4.set_ylabel('Number of Students', fontsize=12, labelpad=10)
        ax4.grid(True, linestyle='--', alpha=0.5)

            # Annotate the count on the bars for other courses
        for bar in bars_other_courses:
            yval = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=12, weight='bold')

            # Adding legends at the bottom
        ax3.legend(['Same Course'], loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1, fontsize=10)
        ax4.legend(bars_other_courses, other_courses_count.index, title="Courses", loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=len(other_courses_count), fontsize=10)

            # Remove x-axis labels for both subplots
        ax3.set_xticklabels([''])
        ax4.set_xticklabels([''] * len(other_courses_count.index))

        plt.tight_layout(pad=3.0)
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png_course_comparison = buffer.getvalue()
        buffer.close()
            #plt.show()
        plt.close(fig)

        encoded_image_course_comparison = base64.b64encode(image_png_course_comparison).decode('utf-8')
     
        # Plot 3: Separate plots for each hard skill
        # Hard Skill 1
        selected_skill_1 = student_df['Hard_Skills'].values[0] #df.loc[df['Student_id'] == student_id, 'Hard_Skills'].values[0]
        same_skill_1_count = df[df['Hard_Skills'] == selected_skill_1].shape[0]
        different_skill_1_count = df[df['Hard_Skills'] != selected_skill_1].shape[0]

        fig, ax5 = plt.subplots(figsize=(8, 6), facecolor='#f5f5f5')
        bars_skill_1 = ax5.bar(
            ['Same Skill 1', 'Different Skill 1'],
            [same_skill_1_count, different_skill_1_count],
            color=['#5cb85c', '#d9534f'],
            edgecolor='black',
            linewidth=1.5,
            width=0.6
        )
        ax5.set_title(f'Students with Same and Different Hard Skill ({selected_skill_1})', fontsize=14, weight='bold', pad=20)
        ax5.set_ylabel('Number of Students', fontsize=12, labelpad=10)
        ax5.grid(True, linestyle='--', alpha=0.5)

        # Annotate counts
        for bar in bars_skill_1:
            yval = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=12, weight='bold')

        # Legend at bottom
        ax5.legend(bars_skill_1, ['Same Skill 1', 'Different Skill 1'], loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=10)

        plt.tight_layout(pad=3.0)
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png_skill_1 = buffer.getvalue()
        buffer.close()
        #plt.show()
        plt.close(fig)

        encoded_image_skill_1 = base64.b64encode(image_png_skill_1).decode('utf-8')


        # Prepare the result to render in the template
        result = {
            'same_grade_count': same_grade_count,
            'encoded_image_grade_comparison': encoded_image_grade_comparison,
            'student_id': student_id,
            'final_grade': selected_student_grade,
            'encoded_image_course_comparison': encoded_image_course_comparison,
            'same_course_count': same_course_count,
            'selected_student_course': selected_student_course,
            'encoded_image_skill_1': encoded_image_skill_1,
        }

        return result
