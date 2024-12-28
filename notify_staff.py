import sqlite3
import streamlit as st
from datetime import date

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

# Fetch faculties for dropdown
def fetch_faculties():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT faculty_code, full_name FROM facultyTable")
    faculties = cursor.fetchall()
    conn.close()
    return faculties

# Fetch notifications
def fetch_notifications():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notificationFacultyTable")
    notifications = cursor.fetchall()
    conn.close()
    return notifications

# Send a notification to faculty
def send_notification(recipient_username, message, date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
           INSERT INTO notificationFacultyTable (recipient_username, message, date)
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
            DELETE FROM notificationFacultyTable
            WHERE id IN (SELECT id FROM notificationFacultyTable ORDER BY date, id ASC LIMIT 5)
        """)
        conn.commit()
        conn.close()
        st.success("Oldest 5 notifications cleared successfully!")
    except sqlite3.Error as e:
        st.error(f"Error clearing notifications: {e}")

# Main app function
def app():
    st.subheader("Notify Staff")
    st.write("Send notifications to faculty members here.")

    # Checkbox for Specific Faculty
    specific_faculty_selected = st.checkbox("Send to Specific Faculty", key="specific_faculty_checkbox")

    # Initialize for specific faculty selection
    recipient_username = None
    if specific_faculty_selected:
          faculties = fetch_faculties()
          faculty_options = [faculty[0] for faculty in faculties]
          faculty_names_dict = {faculty[0]: faculty[1] for faculty in faculties}
          recipient_username = st.selectbox("Select Faculty", list(faculty_names_dict.values()), key="faculty_select_faculty")
          recipient_username = list(faculty_names_dict.keys())[list(faculty_names_dict.values()).index(recipient_username)]

    with st.form("notify_faculty_form"):
        message = st.text_area("Message", key="faculty_message")
        notification_date = st.date_input("Date", value=date.today(), key="faculty_notification_date")
        
        submitted = st.form_submit_button("Send Notification")

        if submitted:
            if message.strip() == "":
                st.error("Message cannot be empty!")
            else:
                if specific_faculty_selected and recipient_username:
                     send_notification(recipient_username, message, notification_date)
                elif not specific_faculty_selected:
                     faculties = fetch_faculties()
                     for faculty in faculties:
                          send_notification(faculty[0], message, notification_date)
                else:
                     st.error("Select a faculty to send the notification!")


    # Clear Old Notifications Button
    if st.button("Clear Old Notifications"):
         clear_old_notifications()
         st.rerun()

    # Display notifications
    st.write("### Notifications")
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
        faculties = fetch_faculties()
        faculty_names_dict = {faculty[0]: faculty[1] for faculty in faculties}
        for notification in notifications:
            col1, col2, col3, col4 = st.columns([2, 4, 3, 2])
            with col1:
                st.write(faculty_names_dict.get(notification[1], "N/A"))  # Recipient
            with col2:
                st.write(notification[2])  # Message
            with col3:
                st.write(notification[3])  # Date
            with col4:
                st.empty()
    else:
        st.write("No notifications available.")

# Main routing logic
if "page" not in st.session_state:
    st.session_state.page = "main"

if __name__ == '__main__':
    app()