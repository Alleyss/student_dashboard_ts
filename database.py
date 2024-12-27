import sqlite3

def create_connection(db_file):
    """Create a database connection to SQLite."""
    conn = sqlite3.connect(db_file)
    return conn

def create_tables():
    """Create the necessary tables if they don't exist."""
    conn = create_connection('instance/students.db')  # Path to your SQLite DB
    cursor = conn.cursor()

    # Student table
    cursor.execute('''
        -- Association table for many-to-many relationship between Student and Course
        CREATE TABLE IF NOT EXISTS student_courses  (
            username TEXT NOT NULL,
            course_code TEXT NOT NULL,
            PRIMARY KEY (username, course_code),
            FOREIGN KEY (username) REFERENCES studentTable (username),
            FOREIGN KEY (course_code) REFERENCES courseTable (course_code)
        );
                 ''')
    cursor.execute('''
        -- Table for Student
        CREATE TABLE IF NOT EXISTS studentTable (
            username TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            address TEXT NOT NULL,
            year_of_joining INTEGER NOT NULL,
            branch_code TEXT NOT NULL,
            current_semester INTEGER,
            cgpa REAL,
            FOREIGN KEY (branch_code) REFERENCES branchTable (branch_code)
        );
                 ''')
    cursor.execute('''
        -- Table for Attendance
        CREATE TABLE IF NOT EXISTS attendanceTable (
            username TEXT NOT NULL,
            course_code TEXT NOT NULL,
            attendance TEXT,
            date DATE,
            PRIMARY KEY (username, course_code, date),
            FOREIGN KEY (username) REFERENCES studentTable (username),
            FOREIGN KEY (course_code) REFERENCES courseTable (course_code)
        );
                 ''')
    cursor.execute('''
        -- Table for Marks
        CREATE TABLE IF NOT EXISTS marksTable (
            username TEXT NOT NULL,
            course_code TEXT NOT NULL,
            ExamType TEXT NOT NULL,
            marks_obtained REAL NOT NULL,
            max_marks REAL NOT NULL,
            PRIMARY KEY (username, course_code, ExamType),
            FOREIGN KEY (username) REFERENCES studentTable (username),
            FOREIGN KEY (course_code) REFERENCES courseTable (course_code)
        );
                 ''')
    cursor.execute('''
        -- Table for Branch
        CREATE TABLE IF NOT EXISTS branchTable (
            branch_code TEXT PRIMARY KEY,
            branch_name TEXT NOT NULL
        );
                 ''')
    cursor.execute('''
        -- Table for Admin
        CREATE TABLE IF NOT EXISTS adminTable (
            username TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
                 ''')
    cursor.execute('''
        -- Table for Course
        CREATE TABLE IF NOT EXISTS courseTable (
            course_code TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            course_instructor_code TEXT NOT NULL,
            branch_code TEXT NOT NULL,
            FOREIGN KEY (course_instructor_code) REFERENCES facultyTable (faculty_code),
            FOREIGN KEY (branch_code) REFERENCES branchTable (branch_code)
        );
                 ''')
    cursor.execute('''
        -- Table for Faculty
        CREATE TABLE IF NOT EXISTS facultyTable (
            faculty_code TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            cabin_number TEXT,
            specialization TEXT NOT NULL
        );
                 ''')
    cursor.execute('''
        -- Table for NotificationStudent
        CREATE TABLE IF NOT EXISTS notificationStudentTable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_username TEXT NOT NULL,
            message TEXT NOT NULL,
            date DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (recipient_username) REFERENCES studentTable (username)
        );
                 ''')
    cursor.execute('''
        -- Table for NotificationFaculty
        CREATE TABLE IF NOT EXISTS notificationFacultyTable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_username TEXT NOT NULL,
            message TEXT NOT NULL,
            date DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (recipient_username) REFERENCES facultyTable (faculty_code)
        );

    ''')


    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
