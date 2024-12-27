import sqlite3
import streamlit as st

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

# Fetch data from SQLite database
def fetch_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courseTable")
    courses = cursor.fetchall()
    conn.close()
    return courses

# Fetch branches for the dropdown
def fetch_branches():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT branch_code, branch_name FROM branchTable")
    branches = cursor.fetchall()
    conn.close()
    return branches

# Fetch faculties for dropdown
def fetch_faculties():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT faculty_code, full_name FROM facultyTable")
    faculties = cursor.fetchall()
    conn.close()
    return faculties


# Add new course
def add_course():
    st.subheader("Add New Course")

    # Input fields for course details
    course_code = st.text_input("Course Code", key="add_course_code")
    course_name = st.text_input("Course Name", key="add_course_name")
    credits = st.number_input("Credits", min_value=1, max_value=10, step=1, key="add_credits")

    # Branch dropdown
    branches = fetch_branches()
    branch_options = [branch[0] for branch in branches]
    branch_names_dict = {branch[0]: branch[1] for branch in branches} # For displaying purposes only.
    branch_code = st.selectbox("Branch", branch_options, key="add_branch_code")

    # Faculty dropdown
    faculties = fetch_faculties()
    faculty_options = [faculty[0] for faculty in faculties]
    faculty_names_dict = {faculty[0]: faculty[1] for faculty in faculties}# For displaying purposes only.
    faculty_code = st.selectbox("Course Instructor", faculty_options, key="add_faculty_code")

    # Save button logic
    if st.button("Save New Course"):
        if course_code.strip() == "":
            st.error("Course Code is required!")
        elif course_name.strip() == "":
            st.error("Course Name is required!")
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO courseTable (course_code, course_name, credits, course_instructor_code, branch_code) VALUES (?, ?, ?, ?, ?)",
                    (course_code, course_name, credits, faculty_code, branch_code),
                )
                conn.commit()
                conn.close()
                st.success("New course added successfully!")
                st.session_state.show_add_form = False  # Hide the form
                st.session_state.page = "main"
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Course Code already exists! Please use a unique code.")

# Edit existing course
def edit_course(course_code):
    st.subheader("Edit Course")

    # Fetch course details
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courseTable WHERE course_code = ?", (course_code,))
    course = cursor.fetchone()
    conn.close()

    if course:
        # Input fields for editing
        course_name = st.text_input("Course Name", value=course[1], key=f"edit_course_name_{course_code}")
        credits = st.number_input("Credits", min_value=1, max_value=10, step=1, value=course[2], key=f"edit_credits_{course_code}")

        # Branch dropdown
        branches = fetch_branches()
        branch_options = [branch[0] for branch in branches]
        branch_names_dict = {branch[0]: branch[1] for branch in branches}
        branch_code = st.selectbox("Branch", branch_options, index=branch_options.index(course[4]) if course[4] in branch_options else 0, key=f"edit_branch_code_{course_code}")

        # Faculty dropdown
        faculties = fetch_faculties()
        faculty_options = [faculty[0] for faculty in faculties]
        faculty_names_dict = {faculty[0]: faculty[1] for faculty in faculties}
        faculty_code = st.selectbox("Course Instructor", faculty_options, index=faculty_options.index(course[3]) if course[3] in faculty_options else 0, key=f"edit_faculty_code_{course_code}")


        # Save button logic
        if st.button("Save Changes"):
            if course_name.strip() == "":
                st.error("Course Name is required!")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE courseTable SET course_name = ?, credits = ?, course_instructor_code = ?, branch_code = ? WHERE course_code = ?",
                        (course_name, credits, faculty_code, branch_code, course_code),
                    )
                    conn.commit()
                    conn.close()
                    st.success("Course updated successfully!")
                    st.session_state.show_edit_form = False  # Hide the form
                    st.session_state.page = "main"
                    st.rerun()

                except sqlite3.Error as e:
                     st.error(f"An error occurred while updating the course: {e}")
    else:
        st.error("Course not found!")


# Delete course from the database
def delete_course(course_code):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM courseTable WHERE course_code = ?", (course_code,))
        conn.commit()
        st.success(f"Course with code '{course_code}' deleted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error deleting course with code '{course_code}': {e}")
    finally:
        conn.close()
    st.session_state.page = "main"
    st.rerun()


# Main app function
def app():
    st.subheader("Course Management Page")
    st.write("Manage your courses and their details here.")

    if st.button("Add New Course", key="add_course_button"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.rerun()

    # Table Header
    st.write("### Courses Table")
    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 2, 3, 1])
    with col1:
        st.write("**Course Code**")
    with col2:
        st.write("**Course Name**")
    with col3:
        st.write("**Credits**")
    with col4:
        st.write("**Branch**")
    with col5:
        st.write("**Instructor**")
    with col6:
        st.write("**Actions**")

    # Fetch and display courses
    courses = fetch_courses()
    if courses:
        for course in courses:
             col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 2, 3, 1])
             with col1:
                st.write(course[0])  # Course Code
             with col2:
                st.write(course[1])  # Course Name
             with col3:
                st.write(course[2])  # Credits
             with col4:
                # Display branch name instead of branch code
                branches = fetch_branches()
                branch_names_dict = {branch[0]: branch[1] for branch in branches}
                st.write(branch_names_dict.get(course[4], "N/A"))
             with col5:
                #Display faculty name instead of faculty code
                faculties = fetch_faculties()
                faculty_names_dict = {faculty[0]: faculty[1] for faculty in faculties}
                st.write(faculty_names_dict.get(course[3], "N/A"))
             with col6:
                if st.button("✏️", key=f"edit_{course[0]}"):
                    st.session_state.show_edit_form = True
                    st.session_state.course_code = course[0]
                    st.session_state.show_add_form = False
                    st.rerun()
                if st.button("🗑️", key=f"delete_{course[0]}"):
                    delete_course(course[0])

    else:
        st.write("No courses available.")

    if st.session_state.get("show_add_form", False):
        add_course()

    if st.session_state.get("show_edit_form", False):
        edit_course(st.session_state.course_code)


# Page routing
if "page" not in st.session_state:
    st.session_state.page = "main"
if "course_code" not in st.session_state:
    st.session_state.course_code = None
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "show_edit_form" not in st.session_state:
    st.session_state.show_edit_form = False

# Routing logic
if st.session_state.page == "main":
    app()