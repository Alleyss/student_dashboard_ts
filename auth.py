import sqlite3
import streamlit as st
from database import create_tables
from multiapp import MultiApp
import home
import branch
import course
import student
import faculty
import marks
import attendance
import notify_staff
import notify_student
import chatbot
from api_client import get_streaming_chat_response
from utils import load_sections, save_sections, add_new_section, get_section_conversation, add_message_to_section

# Initialize session state for tracking login
def authenticate_student(username, password):
    conn = sqlite3.connect('instance/students.db')  # Path to your SQLite DB
    cur = conn.cursor()
    cur.execute("SELECT * FROM studentTable WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

# Register new user
def register_student(username, email, password, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa):
    try:
        conn = sqlite3.connect('instance/students.db')  # Ensure the correct database name is used
        cur = conn.cursor()
        
        # Insert into studentTable
        cur.execute("""
            INSERT INTO studentTable (username, email, password, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, email, password, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Registration failed: {e}")  # For debugging, print the error message
        return False

def main():
    
    # Initialize session state for tracking login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Display Login/Signup or Dashboard based on session state
    if not st.session_state.logged_in:
        menu = ["Login", "Sign Up"]
        # Initialize the database
        create_tables()
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if authenticate_student(username, password):
                    st.session_state.logged_in = True
                    st.success(f"Welcome {username}!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

        elif choice == "Sign Up":
            st.subheader("Sign Up")
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            full_name = st.text_input("Full Name")
            mobile_number = st.text_input("Mobile Number")
            address = st.text_area("Address")
            year_of_joining = st.number_input("Year of Joining", min_value=1900, max_value=2100, step=1)
            branch_code = st.text_input("Branch Code")
            current_semester = st.number_input("Current Semester", min_value=1, max_value=8, step=1, value=1)
            cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)

            if st.button("Register"):
                if register_student(username, email, password, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa):
                    st.success("Registration successful! You can now log in.")

    else:  # If logged in, show the app dashboard
        # Now instantiate and run the MultiApp
        app = MultiApp()  # Instantiate the MultiApp class

        # Add all pages to the app
        app.add_app("Home", home.app)
        app.add_app("Branch", branch.app)
        app.add_app("Courses", course.app)
        app.add_app("Student", student.app)
        app.add_app("Faculty", faculty.app)
        app.add_app("Marks", marks.app)
        app.add_app("Attendance", attendance.app)
        app.add_app("Notify Staff", notify_staff.app)
        app.add_app("Notify Student", notify_student.app)
        app.add_app("Open Chatbot", chatbot.app)

        app.add_app("Log Out", MultiApp.logout)

        # Run the app with the selected page
        app.run()
        
        
# Run the app
if __name__ == "__main__":
    main()