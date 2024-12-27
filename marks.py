import sqlite3
import streamlit as st

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

# Fetch data from SQLite database
def fetch_marks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM marksTable")
    marks_records = cursor.fetchall()
    conn.close()
    return marks_records

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


# Add new marks record
def add_marks():
    st.subheader("Add New Marks Record")

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

    exam_type = st.text_input("Exam Type", key="add_exam_type")
    marks_obtained = st.number_input("Marks Obtained", min_value=0.0, key="add_marks_obtained")
    max_marks = st.number_input("Max Marks", min_value=1.0, key="add_max_marks")


    # Save button logic
    if st.button("Save New Marks"):
        if exam_type.strip() == "":
            st.error("Exam Type is required!")
        elif marks_obtained > max_marks:
            st.error("Marks obtained should not be greater than max marks.")
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO marksTable (username, course_code, ExamType, marks_obtained, max_marks)
                    VALUES (?, ?, ?, ?, ?)
                """, (student_username, course_code, exam_type, marks_obtained, max_marks))
                conn.commit()
                conn.close()
                st.success("New marks record added successfully!")
                st.session_state.show_add_form = False
                st.session_state.page = "main"
                st.rerun()
            except sqlite3.IntegrityError as e:
                 st.error(f"Error adding marks record: {e}")

# Edit existing marks record
def edit_marks(username, course_code, exam_type):
    st.subheader("Edit Marks Record")

    # Fetch marks details
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM marksTable WHERE username = ? AND course_code = ? AND ExamType = ?", (username, course_code, exam_type))
    marks_record = cursor.fetchone()
    conn.close()

    if marks_record:
        # Input fields for editing
        marks_obtained = st.number_input("Marks Obtained", min_value=0.0, value=marks_record[3], key=f"edit_marks_obtained_{username}_{course_code}_{exam_type}")
        max_marks = st.number_input("Max Marks", min_value=1.0, value=marks_record[4], key=f"edit_max_marks_{username}_{course_code}_{exam_type}")

        # Student dropdown
        students = fetch_students()
        student_options = [student[0] for student in students]
        student_names_dict = {student[0]: student[1] for student in students}
        student_username = st.selectbox("Student", student_options, key=f"edit_student_username_{username}_{course_code}_{exam_type}", index = student_options.index(username) if username in student_options else 0)

        # Course dropdown
        courses = fetch_courses()
        course_options = [course[0] for course in courses]
        course_names_dict = {course[0]: course[1] for course in courses}
        course_code = st.selectbox("Course", course_options, key=f"edit_course_code_{username}_{course_code}_{exam_type}", index = course_options.index(course_code) if course_code in course_options else 0)

        exam_type = st.text_input("Exam Type", value = marks_record[2], key=f"edit_exam_type_{username}_{course_code}_{exam_type}")


        # Save button logic
        if st.button("Save Changes"):
            if exam_type.strip() == "":
               st.error("Exam Type is required!")
            elif marks_obtained > max_marks:
                st.error("Marks obtained should not be greater than max marks.")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE marksTable SET marks_obtained = ?, max_marks = ?, username = ?, course_code = ?, ExamType = ?
                        WHERE username = ? AND course_code = ? AND ExamType = ?
                    """, (marks_obtained, max_marks, student_username, course_code, exam_type, username, course_code, exam_type))
                    conn.commit()
                    conn.close()
                    st.success("Marks record updated successfully!")
                    st.session_state.show_edit_form = False
                    st.session_state.page = "main"
                    st.rerun()
                except sqlite3.Error as e:
                    st.error(f"Error updating marks record: {e}")
    else:
        st.error("Marks record not found!")


# Delete marks record from the database
def delete_marks(username, course_code, exam_type):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM marksTable WHERE username = ? AND course_code = ? AND ExamType = ?", (username, course_code, exam_type))
        conn.commit()
        st.success(f"Marks record for student '{username}', course '{course_code}', exam type '{exam_type}' deleted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error deleting marks record: {e}")
    finally:
        conn.close()
    st.session_state.page = "main"
    st.rerun()


# Main app function
def app():
    st.subheader("Marks Management Page")
    st.write("Manage student marks records here.")

    if st.button("Add New Marks", key="add_marks_button"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.rerun()

    # Table Header
    st.write("### Marks Table")
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
    with col1:
        st.write("**Student**")
    with col2:
        st.write("**Course**")
    with col3:
        st.write("**Exam Type**")
    with col4:
        st.write("**Marks Obtained**")
    with col5:
        st.write("**Max Marks**")
    with col6:
        st.write("**Actions**")


    # Fetch and display marks records
    marks_records = fetch_marks()
    if marks_records:
        for record in marks_records:
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
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
                st.write(record[4])
            with col6:
                if st.button("✏️", key=f"edit_{record[0]}_{record[1]}_{record[2]}"):
                    st.session_state.show_edit_form = True
                    st.session_state.edit_username = record[0]
                    st.session_state.edit_course_code = record[1]
                    st.session_state.edit_exam_type = record[2]
                    st.session_state.show_add_form = False
                    st.rerun()
                if st.button("🗑️", key=f"delete_{record[0]}_{record[1]}_{record[2]}"):
                    delete_marks(record[0], record[1], record[2])
    else:
        st.write("No marks records available.")

    if st.session_state.get("show_add_form", False):
        add_marks()

    if st.session_state.get("show_edit_form", False):
         edit_marks(st.session_state.edit_username, st.session_state.edit_course_code, st.session_state.edit_exam_type)

# Page routing
if "page" not in st.session_state:
    st.session_state.page = "main"
if "edit_username" not in st.session_state:
    st.session_state.edit_username = None
if "edit_course_code" not in st.session_state:
    st.session_state.edit_course_code = None
if "edit_exam_type" not in st.session_state:
    st.session_state.edit_exam_type = None
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "show_edit_form" not in st.session_state:
    st.session_state.show_edit_form = False


# Routing logic
if st.session_state.page == "main":
    app()