import sqlite3
import streamlit as st
import plotly.express as px
import pandas as pd


# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')


# --- Helper functions to Fetch Data ---
def fetch_student_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM studentTable")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def fetch_faculty_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM facultyTable")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def fetch_attendance_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
         SELECT st.full_name, ct.course_name, at.attendance, at.date
            FROM attendanceTable at
            JOIN studentTable st ON at.username = st.username
            JOIN courseTable ct ON at.course_code = ct.course_code
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_marks_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
         SELECT st.full_name, ct.course_name, mt.marks_obtained, mt.max_marks, mt.ExamType, ft.full_name
            FROM marksTable mt
            JOIN studentTable st ON mt.username = st.username
            JOIN courseTable ct ON mt.course_code = ct.course_code
            JOIN facultyTable ft ON ct.course_instructor_code = ft.faculty_code
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT course_code, course_name FROM courseTable")
    courses = cursor.fetchall()
    conn.close()
    return courses

def fetch_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, full_name FROM studentTable")
    students = cursor.fetchall()
    conn.close()
    return students


def fetch_faculties():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT faculty_code, full_name FROM facultyTable")
    faculties = cursor.fetchall()
    conn.close()
    return faculties

def fetch_branch_student_distribution():
     conn = get_connection()
     cursor = conn.cursor()
     cursor.execute("""
        SELECT bt.branch_name, count(st.username)
        FROM studentTable st
        JOIN branchTable bt ON st.branch_code = bt.branch_code
        GROUP BY bt.branch_name
     """)
     data = cursor.fetchall()
     conn.close()
     return data

def fetch_faculty_specialization_distribution():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT specialization, count(faculty_code)
        FROM facultyTable
        GROUP BY specialization
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_course_credits_distribution():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT credits, count(course_code)
        FROM courseTable
        GROUP BY credits
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def fetch_faculty_course_distribution():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
       SELECT ft.full_name, COUNT(ct.course_code)
        FROM facultyTable ft
        LEFT JOIN courseTable ct ON ft.faculty_code = ct.course_instructor_code
        GROUP BY ft.full_name

    """)
    data = cursor.fetchall()
    conn.close()
    return data


# --- Main app function ---
def app():
    st.subheader("Dashboard")
    st.write("Welcome to the dashboard. Here's an overview of your data:")

    # --- Cards for counts ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Students", fetch_student_count())
    with col2:
        st.metric("Number of Faculty Members", fetch_faculty_count())

    # --- Visualizations ---

    # Attendance Visualization
    st.write("### Attendance Visualization")
    attendance_data = fetch_attendance_data()
    if attendance_data:
        df_attendance = pd.DataFrame(attendance_data, columns=["Student Name", "Course Name", "Attendance Status", "Date"])
        fig_attendance = px.histogram(df_attendance, x="Student Name", color="Attendance Status", barmode="group", title="Attendance Status of Students")
        st.plotly_chart(fig_attendance)
    else:
        st.write("No attendance data available.")

    # Marks Visualization
    st.write("### Marks Visualization")

    marks_data = fetch_marks_data()

    if marks_data:
        df_marks = pd.DataFrame(marks_data, columns=["Student Name", "Course Name", "Marks Obtained", "Max Marks", "Exam Type", "Faculty Name"])

    # Select student for specific student graph
        students = fetch_students()
        student_options = [student[0] for student in students]
        student_names_dict = {student[0]: student[1] for student in students}
        selected_student = st.selectbox("Select a student", student_options, key="student_marks_dropdown", format_func=lambda x: student_names_dict.get(x))
        df_student_marks = df_marks[df_marks["Student Name"] == student_names_dict.get(selected_student)]
        if not df_student_marks.empty:
            fig_student_marks = px.bar(df_student_marks, x="Course Name", y="Marks Obtained", color="Exam Type", title=f"Marks for student {student_names_dict.get(selected_student)}")
            st.plotly_chart(fig_student_marks)
        else:
            st.write("No marks available for the selected student.")


        # Average Marks by Faculty Visualization
        st.write("#### Average Marks by Faculty (Percentage)")
        df_marks["Percentage"] = (df_marks["Marks Obtained"] / df_marks["Max Marks"]) * 100
        df_faculty_average_marks = df_marks.groupby("Faculty Name").agg({"Percentage": "mean"}).reset_index()
        fig_faculty_average_marks = px.bar(df_faculty_average_marks, x="Faculty Name", y="Percentage", title = "Average marks percentage of students under each faculty")
        st.plotly_chart(fig_faculty_average_marks)
    else:
         st.write("No marks data available.")

    # --- Additional Visualizations ---
    st.write("### Additional Visualizations")

    # Branch student distribution
    branch_student_data = fetch_branch_student_distribution()
    if branch_student_data:
        df_branch_student = pd.DataFrame(branch_student_data, columns = ["Branch Name", "Number of Students"])
        fig_branch_student = px.pie(df_branch_student, names="Branch Name", values="Number of Students", title = "Number of Students in each Branch")
        st.plotly_chart(fig_branch_student)
    else:
        st.write("No branch data available.")


    # Faculty Specialization Distribution
    faculty_specialization_data = fetch_faculty_specialization_distribution()
    if faculty_specialization_data:
         df_faculty_specialization = pd.DataFrame(faculty_specialization_data, columns = ["Specialization", "Number of Faculties"])
         fig_faculty_specialization = px.pie(df_faculty_specialization, names="Specialization", values="Number of Faculties", title = "Number of Faculties in each specialization")
         st.plotly_chart(fig_faculty_specialization)
    else:
         st.write("No specialization data available.")

    # Course credits distribution
    course_credits_data = fetch_course_credits_distribution()
    if course_credits_data:
        df_course_credits = pd.DataFrame(course_credits_data, columns = ["Credits", "Number of Courses"])
        fig_course_credits = px.bar(df_course_credits, x="Credits", y="Number of Courses", title = "Distribution of courses for different credit values")
        st.plotly_chart(fig_course_credits)
    else:
        st.write("No course credit data available")

    # Faculty Course Distribution
    faculty_course_distribution_data = fetch_faculty_course_distribution()
    if faculty_course_distribution_data:
        df_faculty_course = pd.DataFrame(faculty_course_distribution_data, columns = ["Faculty Name", "Number of Courses"])
        fig_faculty_course = px.bar(df_faculty_course, x="Faculty Name", y="Number of Courses", title = "Number of courses under each faculty")
        st.plotly_chart(fig_faculty_course)
    else:
        st.write("No faculty course data available.")


# Main routing logic
if "page" not in st.session_state:
    st.session_state.page = "main"