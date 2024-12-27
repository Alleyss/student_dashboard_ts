import sqlite3
import streamlit as st

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

# Fetch data from SQLite database
def fetch_branches():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM branchTable")
    branches = cursor.fetchall()
    conn.close()
    return branches


# Add new branch
def add_branch():
    st.subheader("Add New Branch")

    # Input fields for branch code and name
    branch_code = st.text_input("Branch Code", key="add_branch_code")
    branch_name = st.text_input("Branch Name", key="add_branch_name")

    # Save button logic
    if st.button("Save New Branch"):
        if branch_code.strip() == "":
            st.error("Branch Code is required!")
        elif branch_name.strip() == "":
            st.error("Branch Name is required!")
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO branchTable (branch_code, branch_name) VALUES (?, ?)",
                               (branch_code, branch_name))
                conn.commit()
                conn.close()
                st.success("New branch added successfully!")
                st.session_state.show_add_form = False  # Hide the form
                st.session_state.page = "main"
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Branch Code already exists! Please use a unique code.")
def edit_branch(branch_code):
    st.subheader("Edit Branch")

    # Fetch branch details
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT branch_name FROM branchTable WHERE branch_code = ?", (branch_code,))
    branch = cursor.fetchone()
    conn.close()
    if branch:
        # Pre-fill the branch name for editing
        branch_name = st.text_input("Branch Name", value=branch[0], key=f"edit_branch_name_{branch_code}")

        # Save button logic
        if st.button("Save Changes"):
            if branch_name.strip() == "":
                st.error("Branch Name is required!")
            else:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE branchTable SET branch_name = ? WHERE branch_code = ?",
                               (branch_name, branch_code))
                conn.commit()
                conn.close()
                st.success("Branch updated successfully!")
                st.session_state.show_edit_form = False # Hide the form
                st.session_state.page = "main"
                st.rerun()

    else:
        st.error("Branch not found!")
# Delete branch from the database
def delete_branch(branch_code):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM branchTable WHERE branch_code = ?", (branch_code,))
        conn.commit()
        st.success(f"Branch with code '{branch_code}' deleted successfully!")
    except sqlite3.Error as e:
        st.error(f"Error deleting branch with code '{branch_code}': {e}")
    finally:
        conn.close()
    st.session_state.page = "main"
    st.rerun()

# Main app function
def app():
    st.subheader("Branch Management Page")
    st.write("Manage your branches and their details here.")

    if st.button("Add New Branch", key="add_branch_button"):
         st.session_state.show_add_form = True
         st.session_state.show_edit_form = False
         st.rerun()

    # Table Header
    st.write("### Branches Table")
    col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
    with col1:
        st.write("**Branch Code**")
    with col2:
        st.write("**Branch Name**")
    with col3:
        st.write("**Actions**")
    with col4:
        st.empty()

    # Fetch and display branches
    branches = fetch_branches()
    if branches:
        for branch in branches:
            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                st.write(branch[0])  # Branch code
            with col2:
                st.write(branch[1])  # Branch Name
            with col3:
                 if st.button("✏️", key=f"edit_{branch[0]}"):
                    st.session_state.show_edit_form = True
                    st.session_state.branch_code = branch[0]
                    st.session_state.show_add_form = False
                    st.rerun()
                 if st.button("🗑️", key=f"delete_{branch[0]}"):
                    delete_branch(branch[0])

    else:
        st.write("No branches available.")

    if st.session_state.get("show_add_form", False):
        add_branch()

    if st.session_state.get("show_edit_form", False):
         edit_branch(st.session_state.branch_code)

# Page routing
if "page" not in st.session_state:
    st.session_state.page = "main"
if "branch_code" not in st.session_state:
    st.session_state.branch_code = None
if "show_add_form" not in st.session_state:
     st.session_state.show_add_form = False
if "show_edit_form" not in st.session_state:
    st.session_state.show_edit_form = False

# Routing logic
if st.session_state.page == "main":
    app()