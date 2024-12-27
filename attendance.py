import sqlite3
import streamlit as st
from datetime import date

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

# Fetch data from SQLite database
def fetch_attendance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendanceTable")
    attendance_records = cursor.fetchall()
    conn.close()
    return attendance_records

# Fetch students for dropdown
def fetch_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, full_name FROM studentTable")
    students = cursor.fetchall()
    conn.close()
    return students

# Fetch courses for dropdown
def fetch_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT course_code, course_name FROM courseTable")
    courses = cursor.fetchall()
    conn.close()
    return courses

# Add new attendance record
def add_attendance():
    st.subheader("Add New Attendance Record")

    # Student dropdown
    students = fetch_students()
    student_options = [student[0] for student in students]
    student_names_dict = {student[0]: student[1] for student in students}
    student_username = st.selectbox("Student", student_options, key="add_student_username")

    # Course dropdown
    courses = fetch_courses()
    course_options = [course[0] for course in courses]
    course_names_dict = {course[0]: course[1] for course in courses}
    course_code = st.selectbox("Course", course_options, key="add_course_code")

    attendance_status = st.radio("Attendance", ["Present", "Absent"], key="add_attendance_status")
    attendance_date = st.date_input("Date", value=date.today(), key="add_attendance_date")


    # Save button logic
    if st.button("Save New Attendance"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attendanceTable (username, course_code, attendance, date)
                VALUES (?, ?, ?, ?)
            """, (student_username, course_code, attendance_status, attendance_date))
            conn.commit()
            conn.close()
            st.success("New attendance record added successfully!")
            st.session_state.show_add_form = False
            st.session_state.page = "main"
            st.rerun()
        except sqlite3.IntegrityError as e:
            st.error(f"Error adding attendance record: {e}")

# Edit existing attendance record
def edit_attendance(username, course_code, attendance_date):
    st.subheader("Edit Attendance Record")

    # Fetch attendance details
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendanceTable WHERE username = ? AND course_code = ? AND date = ?", (username, course_code, attendance_date))
    attendance_record = cursor.fetchone()
    conn.close()


    if attendance_record:
        # Input fields for editing
        attendance_status = st.radio("Attendance", ["Present", "Absent"], key=f"edit_attendance_status_{username}_{course_code}_{attendance_date}", index = 0 if attendance_record[2] == "Present" else 1)
        attendance_date = st.date_input("Date", value=attendance_record[3], key=f"edit_attendance_date_{username}_{course_code}")

         # Student dropdown
        students = fetch_students()
        student_options = [student[0] for student in students]
        student_names_dict = {student[0]: student[1] for student in students}
        student_username = st.selectbox("Student", student_options, key=f"edit_student_username_{username}_{course_code}_{attendance_date}", index = student_options.index(username) if username in student_options else 0)

        # Course dropdown
        courses = fetch_courses()
        course_options = [course[0] for course in courses]
        course_names_dict = {course[0]: course[1] for course in courses}
        course_code = st.selectbox("Course", course_options, key=f"edit_course_code_{username}_{course_code}_{attendance_date}", index = course_options.index(course_code) if course_code in course_options else 0)

        # Save button logic
        if st.button("Save Changes"):
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE attendanceTable SET attendance = ?, date = ? , username = ?, course_code = ?
                        WHERE username = ? AND course_code = ? AND date = ?
                    """, (attendance_status, attendance_date, student_username, course_code, username, course_code, attendance_date))
                    conn.commit()
                    conn.close()
                    st.success("Attendance record updated successfully!")
                    st.session_state.show_edit_form = False
                    st.session_state.page = "main"
                    st.rerun()
                except sqlite3.Error as e:
                        st.error(f"Error updating attendance record: {e}")
    else:
        st.error("Attendance record not found!")

# Delete attendance record from the database
def delete_attendance(username, course_code, attendance_date):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM attendanceTable WHERE username = ? AND course_code = ? AND date = ?", (username, course_code, attendance_date))
        conn.commit()
        st.success(f"Attendance record for student '{username}', course '{course_code}' on '{attendance_date}' deleted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error deleting attendance record: {e}")
    finally:
        conn.close()
    st.session_state.page = "main"
    st.rerun()

# Main app function
def app():
    st.subheader("Attendance Management Page")
    st.write("Manage student attendance records here.")

    if st.button("Add New Attendance", key="add_attendance_button"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.rerun()

    # Table Header
    st.write("### Attendance Table")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    with col1:
        st.write("**Student**")
    with col2:
        st.write("**Course**")
    with col3:
        st.write("**Attendance**")
    with col4:
        st.write("**Date**")
    with col5:
        st.write("**Actions**")


    # Fetch and display attendance records
    attendance_records = fetch_attendance()
    if attendance_records:
        for record in attendance_records:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
            with col1:
                # Display student name instead of username
                students = fetch_students()
                student_names_dict = {student[0]: student[1] for student in students}
                st.write(student_names_dict.get(record[0], "N/A"))
            with col2:
                # Display course name instead of course code
                courses = fetch_courses()
                course_names_dict = {course[0]: course[1] for course in courses}
                st.write(course_names_dict.get(record[1], "N/A"))
            with col3:
                st.write(record[2])
            with col4:
                st.write(record[3])
            with col5:
                if st.button("✏️", key=f"edit_{record[0]}_{record[1]}_{record[3]}"):
                    st.session_state.show_edit_form = True
                    st.session_state.edit_username = record[0]
                    st.session_state.edit_course_code = record[1]
                    st.session_state.edit_attendance_date = record[3]
                    st.session_state.show_add_form = False
                    st.rerun()
                if st.button("🗑️", key=f"delete_{record[0]}_{record[1]}_{record[3]}"):
                    delete_attendance(record[0], record[1], record[3])
    else:
        st.write("No attendance records available.")

    if st.session_state.get("show_add_form", False):
        add_attendance()

    if st.session_state.get("show_edit_form", False):
        edit_attendance(st.session_state.edit_username, st.session_state.edit_course_code, st.session_state.edit_attendance_date)


# Page routing
if "page" not in st.session_state:
    st.session_state.page = "main"
if "edit_username" not in st.session_state:
    st.session_state.edit_username = None
if "edit_course_code" not in st.session_state:
    st.session_state.edit_course_code = None
if "edit_attendance_date" not in st.session_state:
     st.session_state.edit_attendance_date = None
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "show_edit_form" not in st.session_state:
    st.session_state.show_edit_form = False


# Routing logic
if st.session_state.page == "main":
    app()