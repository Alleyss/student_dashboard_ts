import sqlite3
import streamlit as st
from datetime import date

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

# Fetch students for dropdown
def fetch_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, full_name FROM studentTable")
    students = cursor.fetchall()
    conn.close()
    return students

# Fetch notifications
def fetch_notifications():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notificationStudentTable")
    notifications = cursor.fetchall()
    conn.close()
    return notifications

# Send a notification to student
def send_notification(recipient_username, message, date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
           INSERT INTO notificationStudentTable (recipient_username, message, date)
           VALUES (?, ?, ?)
        """, (recipient_username, message, date))
        conn.commit()
        conn.close()
        st.success("Notification sent successfully!")
    except sqlite3.Error as e:
        st.error(f"Error sending notification: {e}")

# Clear oldest 5 notifications
def clear_old_notifications():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM notificationStudentTable
            WHERE id IN (SELECT id FROM notificationStudentTable ORDER BY date, id ASC LIMIT 5)
        """)
        conn.commit()
        conn.close()
        st.success("Oldest 5 notifications cleared successfully!")
    except sqlite3.Error as e:
        st.error(f"Error clearing notifications: {e}")


# Main app function
def app():
    st.subheader("Notify Students")
    st.write("Send notifications to students here.")

    # Checkbox for Specific Student
    specific_student_selected = st.checkbox("Send to Specific Student", key="specific_student_checkbox")
    
    recipient_username = None  # Initialize for specific student selection

    if specific_student_selected:
           students = fetch_students()
           student_options = [student[0] for student in students]
           student_names_dict = {student[0]: student[1] for student in students}
           recipient_username = st.selectbox("Select Student", student_options, key="student_select_student")


    with st.form("notify_student_form"):
        message = st.text_area("Message", key="student_message")
        notification_date = st.date_input("Date", value=date.today(), key="student_notification_date")

        submitted = st.form_submit_button("Send Notification")

        if submitted:
            if message.strip() == "":
                st.error("Message cannot be empty!")
            else:
                if specific_student_selected and recipient_username:
                    send_notification(recipient_username, message, notification_date)
                elif not specific_student_selected:
                    students = fetch_students()
                    for student in students:
                        send_notification(student[0], message, notification_date)
                else:
                    st.error("Select a student to send the notification!")
    # Clear Old Notifications Button
    if st.button("Clear Old Notifications"):
         clear_old_notifications()
         st.rerun()


    # Display Notifications
    st.write("### Notifications")

    # Table Header
    col1, col2, col3, col4 = st.columns([2, 4, 3, 2])
    with col1:
       st.write("**Recipient**")
    with col2:
       st.write("**Message**")
    with col3:
        st.write("**Date**")
    with col4:
         st.empty()

    notifications = fetch_notifications()
    if notifications:
        for notification in notifications:
            col1, col2, col3, col4 = st.columns([2, 4, 3, 2])
            with col1:
               students = fetch_students()
               student_names_dict = {student[0]: student[1] for student in students}
               st.write(student_names_dict.get(notification[1], "N/A")) #Recipient
            with col2:
                st.write(notification[2])  # Message
            with col3:
                st.write(notification[3]) # Date
            with col4:
                st.empty()
    else:
        st.write("No notifications available.")

# Main routing logic
if "page" not in st.session_state:
    st.session_state.page = "main"