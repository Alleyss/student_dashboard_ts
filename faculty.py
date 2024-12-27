import sqlite3
import streamlit as st

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

# Fetch data from SQLite database
def fetch_faculties():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facultyTable")
    faculties = cursor.fetchall()
    conn.close()
    return faculties

# Add new faculty
def add_faculty():
    st.subheader("Add New Faculty")

    # Input fields for faculty details
    faculty_code = st.text_input("Faculty Code", key="add_faculty_code")
    full_name = st.text_input("Full Name", key="add_full_name")
    email = st.text_input("Email", key="add_email")
    password = st.text_input("Password", type="password", key="add_password")
    cabin_number = st.text_input("Cabin Number", key="add_cabin_number")
    specialization = st.text_input("Specialization", key="add_specialization")

    # Save button logic
    if st.button("Save New Faculty"):
        if faculty_code.strip() == "":
            st.error("Faculty Code is required!")
        elif full_name.strip() == "":
            st.error("Full Name is required!")
        elif email.strip() == "":
            st.error("Email is required!")
        elif password.strip() == "":
             st.error("Password is required!")
        elif specialization.strip() == "":
            st.error("Specialization is required!")
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO facultyTable (faculty_code, full_name, email, password, cabin_number, specialization)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (faculty_code, full_name, email, password, cabin_number, specialization))
                conn.commit()
                conn.close()
                st.success("New faculty member added successfully!")
                st.session_state.show_add_form = False
                st.session_state.page = "main"
                st.rerun()
            except sqlite3.IntegrityError as e:
                st.error(f"Error adding faculty: {e}")

# Edit existing faculty
def edit_faculty(faculty_code):
    st.subheader("Edit Faculty")

    # Fetch faculty details
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facultyTable WHERE faculty_code = ?", (faculty_code,))
    faculty = cursor.fetchone()
    conn.close()

    if faculty:
        # Input fields for editing
        full_name = st.text_input("Full Name", value=faculty[1], key=f"edit_full_name_{faculty_code}")
        email = st.text_input("Email", value=faculty[2], key=f"edit_email_{faculty_code}")
        password = st.text_input("Password", type="password", value=faculty[3], key=f"edit_password_{faculty_code}")
        cabin_number = st.text_input("Cabin Number", value=faculty[4], key=f"edit_cabin_number_{faculty_code}")
        specialization = st.text_input("Specialization", value=faculty[5], key=f"edit_specialization_{faculty_code}")

        # Save button logic
        if st.button("Save Changes"):
            if full_name.strip() == "":
               st.error("Full Name is required!")
            elif email.strip() == "":
                st.error("Email is required!")
            elif password.strip() == "":
                 st.error("Password is required!")
            elif specialization.strip() == "":
                st.error("Specialization is required!")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE facultyTable SET full_name = ?, email = ?, password = ?, cabin_number = ?, specialization = ?
                        WHERE faculty_code = ?
                    """, (full_name, email, password, cabin_number, specialization, faculty_code))
                    conn.commit()
                    conn.close()
                    st.success("Faculty updated successfully!")
                    st.session_state.show_edit_form = False
                    st.session_state.page = "main"
                    st.rerun()
                except sqlite3.Error as e:
                    st.error(f"Error updating faculty: {e}")
    else:
        st.error("Faculty not found!")

# Delete faculty from the database
def delete_faculty(faculty_code):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM facultyTable WHERE faculty_code = ?", (faculty_code,))
        conn.commit()
        st.success(f"Faculty with code '{faculty_code}' deleted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error deleting faculty with code '{faculty_code}': {e}")
    finally:
        conn.close()
    st.session_state.page = "main"
    st.rerun()


# Main app function
def app():
    st.subheader("Faculty Management Page")
    st.write("Manage faculty members and their details here.")

    if st.button("Add New Faculty", key="add_faculty_button"):
        st.session_state.show_add_form = True
        st.session_state.show_edit_form = False
        st.rerun()

    # Table header
    st.write("### Faculty Table")
    col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 2, 2, 2, 1])
    with col1:
        st.write("**Faculty Code**")
    with col2:
        st.write("**Full Name**")
    with col3:
        st.write("**Email**")
    with col4:
        st.write("**Cabin Number**")
    with col5:
        st.write("**Specialization**")
    with col6:
         st.write("**Actions**")

    # Fetch and display faculties
    faculties = fetch_faculties()
    if faculties:
        for faculty in faculties:
            col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 2, 2, 2, 1])
            with col1:
                st.write(faculty[0])  # Faculty Code
            with col2:
                st.write(faculty[1])  # Full Name
            with col3:
                st.write(faculty[2])  # Email
            with col4:
                 st.write(faculty[4]) # Cabin Number
            with col5:
                st.write(faculty[5]) # Specialization
            with col6:
                if st.button("✏️", key=f"edit_{faculty[0]}"):
                    st.session_state.show_edit_form = True
                    st.session_state.faculty_code = faculty[0]
                    st.session_state.show_add_form = False
                    st.rerun()
                if st.button("🗑️", key=f"delete_{faculty[0]}"):
                    delete_faculty(faculty[0])
    else:
        st.write("No faculty members available.")

    if st.session_state.get("show_add_form", False):
        add_faculty()

    if st.session_state.get("show_edit_form", False):
        edit_faculty(st.session_state.faculty_code)


# Page routing
if "page" not in st.session_state:
    st.session_state.page = "main"
if "faculty_code" not in st.session_state:
    st.session_state.faculty_code = None
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "show_edit_form" not in st.session_state:
    st.session_state.show_edit_form = False


# Routing logic
if st.session_state.page == "main":
    app()