import sqlite3
import streamlit as st

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

# Fetch data from SQLite database
def fetch_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM studentTable")
    students = cursor.fetchall()
    conn.close()
    return students

# Fetch branches for the dropdown
def fetch_branches():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT branch_code, branch_name FROM branchTable")
    branches = cursor.fetchall()
    conn.close()
    return branches

# Add new student
def add_student():
    st.subheader("Add New Student")

    # Input fields for student details
    username = st.text_input("Username", key="add_username")
    email = st.text_input("Email", key="add_email")
    password = st.text_input("Password", type="password", key="add_password")
    full_name = st.text_input("Full Name", key="add_full_name")
    mobile_number = st.text_input("Mobile Number", key="add_mobile_number")
    address = st.text_area("Address", key="add_address")
    year_of_joining = st.number_input("Year of Joining", min_value=1900, max_value=2100, step=1, key="add_year_of_joining")
    current_semester = st.number_input("Current Semester", min_value=1, max_value=8, step=1, key="add_current_semester")
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1, key="add_cgpa")

    # Branch dropdown
    branches = fetch_branches()
    branch_options = [branch[0] for branch in branches]
    branch_names_dict = {branch[0]: branch[1] for branch in branches}
    branch_code = st.selectbox("Branch", branch_options, key="add_branch_code")

    # Save button logic
    if st.button("Save New Student"):
        if username.strip() == "":
            st.error("Username is required!")
        elif email.strip() == "":
            st.error("Email is required!")
        elif password.strip() == "":
            st.error("Password is required!")
        elif full_name.strip() == "":
           st.error("Full Name is required!")
        elif mobile_number.strip() == "":
           st.error("Mobile Number is required!")
        elif address.strip() == "":
           st.error("Address is required!")
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO studentTable (username, email, password, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, email, password, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa))
                conn.commit()
                conn.close()
                st.success("New student added successfully!")
                st.session_state.show_add_form = False  # Hide the form
                st.session_state.page = "main"
                st.rerun()
            except sqlite3.IntegrityError as e:
                st.error(f"Error adding student: {e}")

# Edit existing student
def edit_student(username):
    st.subheader("Edit Student")

    # Fetch student details
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM studentTable WHERE username = ?", (username,))
    student = cursor.fetchone()
    conn.close()

    if student:
        # Input fields for editing
        email = st.text_input("Email", value=student[1], key=f"edit_email_{username}")
        password = st.text_input("Password", type="password", value=student[2], key=f"edit_password_{username}")
        full_name = st.text_input("Full Name", value=student[3], key=f"edit_full_name_{username}")
        mobile_number = st.text_input("Mobile Number", value=student[4], key=f"edit_mobile_number_{username}")
        address = st.text_area("Address", value=student[5], key=f"edit_address_{username}")
        year_of_joining = st.number_input("Year of Joining", min_value=1900, max_value=2100, step=1, value=student[6], key=f"edit_year_of_joining_{username}")
        current_semester = st.number_input("Current Semester", min_value=1, max_value=8, step=1, value=student[8], key=f"edit_current_semester_{username}")
        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1, value=student[9], key=f"edit_cgpa_{username}")


        # Branch dropdown
        branches = fetch_branches()
        branch_options = [branch[0] for branch in branches]
        branch_names_dict = {branch[0]: branch[1] for branch in branches}
        branch_code = st.selectbox("Branch", branch_options, index=branch_options.index(student[7]) if student[7] in branch_options else 0, key=f"edit_branch_code_{username}")

        # Save button logic
        if st.button("Save Changes"):
            if email.strip() == "":
                st.error("Email is required!")
            elif password.strip() == "":
                st.error("Password is required!")
            elif full_name.strip() == "":
               st.error("Full Name is required!")
            elif mobile_number.strip() == "":
               st.error("Mobile Number is required!")
            elif address.strip() == "":
               st.error("Address is required!")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE studentTable SET email = ?, password = ?, full_name = ?, mobile_number = ?, address = ?, year_of_joining = ?, branch_code = ?, current_semester = ?, cgpa = ?
                        WHERE username = ?
                    """, (email, password, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa, username))
                    conn.commit()
                    conn.close()
                    st.success("Student updated successfully!")
                    st.session_state.show_edit_form = False
                    st.session_state.page = "main"
                    st.rerun()
                except sqlite3.Error as e:
                    st.error(f"Error updating student: {e}")
    else:
        st.error("Student not found!")


# Delete student from the database
def delete_student(username):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM studentTable WHERE username = ?", (username,))
        conn.commit()
        st.success(f"Student with username '{username}' deleted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error deleting student with username '{username}': {e}")
    finally:
        conn.close()
    st.session_state.page = "main"
    st.rerun()


# Main app function
def app():
    st.subheader("Student Management Page")
    st.write("Manage your students and their details here.")

    if st.button("Add New Student", key="add_student_button"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.rerun()

    # Fetch and display students
    students = fetch_students()
    st.write("### Students Table")
    # Table Header
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1.5, 2, 1.5, 2, 2, 1.5, 1.5, 1.5, 1.5, 1])
    with col1:
        st.write("**Username**")
    with col2:
        st.write("**Full Name**")
    with col3:
        st.write("**Email**")
    with col4:
        st.write("**Mobile Number**")
    with col5:
        st.write("**Address**")
    with col6:
        st.write("**Year of Joining**")
    with col7:
         st.write("**Branch**")
    with col8:
         st.write("**Semester**")
    with col9:
        st.write("**CGPA**")
    with col10:
        st.write("**Actions**")

    if students:
        for student in students:
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1.5, 2, 1.5, 2, 2, 1.5, 1.5, 1.5, 1.5, 1])
            with col1:
                st.write(student[0])  # Username
            with col2:
                st.write(student[3])  # Full Name
            with col3:
                st.write(student[1])  # Email
            with col4:
                st.write(student[4])  # Mobile Number
            with col5:
                st.write(student[5])  # Address
            with col6:
                 st.write(student[6]) # Year of Joining
            with col7:
                 st.write(student[7]) #Branch code
            with col8:
                 st.write(student[8]) #current semester
            with col9:
                st.write(student[9]) # cgpa
            with col10:
                if st.button("✏️", key=f"edit_{student[0]}"):
                    st.session_state.show_edit_form = True
                    st.session_state.student_username = student[0]
                    st.session_state.show_add_form = False
                    st.rerun()
                if st.button("🗑️", key=f"delete_{student[0]}"):
                    delete_student(student[0])
    else:
        st.write("No students available.")

    if st.session_state.get("show_add_form", False):
        add_student()

    if st.session_state.get("show_edit_form", False):
        edit_student(st.session_state.student_username)


# Page routing
if "page" not in st.session_state:
    st.session_state.page = "main"
if "student_username" not in st.session_state:
    st.session_state.student_username = None
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "show_edit_form" not in st.session_state:
    st.session_state.show_edit_form = False


# Routing logic
if st.session_state.page == "main":
    app()