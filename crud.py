import sqlite3

# Establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('instance/students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Utility to execute a query and fetch results
def execute_query(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Utility to fetch data
def fetch_query(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Student CRUD
def add_student(username, email, password, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa):
    #hashed_password = generate_password_hash(password)
    query = """INSERT INTO students (username, email, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa, password)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    execute_query(query, (username, email, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa, password))

def get_all_students():
    return fetch_query("SELECT * FROM students")

def get_student_by_id(username):
    return fetch_query("SELECT * FROM students WHERE username = ?", (username,))

def update_student_login(username, password):
    #hashed_password = generate_password_hash(password)
    execute_query("UPDATE students SET password = ? WHERE username = ?", (password, username))

def update_student(username, email, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa):
    query = """UPDATE students SET email = ?, full_name = ?, mobile_number = ?, address = ?, year_of_joining = ?, branch_code = ?, current_semester = ?, cgpa = ? WHERE username = ?"""
    execute_query(query, (email, full_name, mobile_number, address, year_of_joining, branch_code, current_semester, cgpa, username))

def delete_student(username):
    execute_query("DELETE FROM students WHERE username = ?", (username,))

# Course CRUD
def add_course(course_code, course_name, credits, course_instructor_code, branch_code):
    query = """INSERT INTO courses (course_code, course_name, credits, course_instructor_code, branch_code)
               VALUES (?, ?, ?, ?, ?)"""
    execute_query(query, (course_code, course_name, credits, course_instructor_code, branch_code))

def update_course(course_code, course_name, credits, course_instructor_code, branch_code):
    query = """UPDATE courses SET course_name = ?, credits = ?, course_instructor_code = ?, branch_code = ? WHERE course_code = ?"""
    execute_query(query, (course_name, credits, course_instructor_code, branch_code, course_code))

def delete_course(course_code):
    execute_query("DELETE FROM courses WHERE course_code = ?", (course_code,))

def get_course_by_id(course_code):
    return fetch_query("SELECT * FROM courses WHERE course_code = ?", (course_code,))

def get_all_courses():
    return fetch_query("SELECT * FROM courses")

# Faculty CRUD
def add_faculty(faculty_code, full_name, email, password, cabin_number, specialization):
    #hashed_password = generate_password_hash(password)
    query = """INSERT INTO faculty (faculty_code, full_name, email, password, cabin_number, specialization)
               VALUES (?, ?, ?, ?, ?, ?)"""
    execute_query(query, (faculty_code, full_name, email, hashed_password, cabin_number, specialization))

def update_faculty(faculty_code, name, email, cabin_number, specialization):
    query = """UPDATE faculty SET name = ?, email = ?, cabin_number = ?, specialization = ? WHERE faculty_code = ?"""
    execute_query(query, (name, email, cabin_number, specialization, faculty_code))

def delete_faculty(faculty_code):
    execute_query("DELETE FROM faculty WHERE faculty_code = ?", (faculty_code,))

def get_faculty_by_id(faculty_code):
    return fetch_query("SELECT * FROM faculty WHERE faculty_code = ?", (faculty_code,))

def get_all_faculty():
    return fetch_query("SELECT * FROM faculty")

# Marks CRUD
def add_marks(username, course_code, ExamType, marks_obtained, max_marks):
    query = """INSERT INTO marks (username, course_code, ExamType, marks_obtained, max_marks)
               VALUES (?, ?, ?, ?, ?)"""
    execute_query(query, (username, course_code, ExamType, marks_obtained, max_marks))

def update_marks(username, course_code, ExamType, marks_obtained, max_marks):
    query = """UPDATE marks SET ExamType = ?, marks_obtained = ?, max_marks = ? WHERE username = ? AND course_code = ?"""
    execute_query(query, (ExamType, marks_obtained, max_marks, username, course_code))

def delete_marks(username, course_code):
    execute_query("DELETE FROM marks WHERE username = ? AND course_code = ?", (username, course_code))

def get_marks_by_username(username):
    return fetch_query("SELECT * FROM marks WHERE username = ?", (username,))

def get_marks_by_course(course_code):
    return fetch_query("SELECT * FROM marks WHERE course_code = ?", (course_code,))

def get_all_marks():
    return fetch_query("SELECT * FROM marks")

# Attendance CRUD
def add_attendance(username, course_code, attendance, date):
    query = """INSERT INTO attendance (username, course_code, attendance, date)
               VALUES (?, ?, ?, ?)"""
    execute_query(query, (username, course_code, attendance, date))

def update_attendance(username, course_code, attendance, date):
    query = """UPDATE attendance SET attendance = ?, date = ? WHERE username = ? AND course_code = ?"""
    execute_query(query, (attendance, date, username, course_code))

def delete_attendance(username, course_code):
    execute_query("DELETE FROM attendance WHERE username = ? AND course_code = ?", (username, course_code))

def get_attendance_by_username(username):
    return fetch_query("SELECT * FROM attendance WHERE username = ?", (username,))

def get_attendance_by_coursecode(course_code):
    return fetch_query("SELECT * FROM attendance WHERE course_code = ?", (course_code,))

def get_all_attendance():
    return fetch_query("SELECT * FROM attendance")

# Branch CRUD
def add_branch(branch_code, branch_name):
    query = """INSERT INTO branches (branch_code, branch_name)
               VALUES (?, ?)"""
    execute_query(query, (branch_code, branch_name))

def get_branch_by_id(branch_code):
    return fetch_query("SELECT * FROM branches WHERE branch_code = ?", (branch_code,))

def update_branch(branch_code, branch_name):
    query = """UPDATE branches SET branch_name = ? WHERE branch_code = ?"""
    execute_query(query, (branch_name, branch_code))

def delete_branch(branch_code):
    execute_query("DELETE FROM branches WHERE branch_code = ?", (branch_code,))

def get_all_branches():
    return fetch_query("SELECT * FROM branches")
