from openai import OpenAI
import os

#XAI_API_KEY=xai-1f8kqj0BkzM1lEAXwmCtERosUjydF0HDNPae5wUTp0ez0TtA31LPEnfdulVmPMgPtJcUxJIMaRI6Nmjd
XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",  
)

def get_streaming_chat_response(user_message, conversation_history, temperature=1.0, top_p=None):
    """Streams chat response from the Grok API using OpenAI client with context."""
    messages = [
        {"role": "system", "content": "You are Grok, a helpful chatbot for a student dashboard.You are provided with the database schema and you have to generate SQL query with structure r""```sql\s*(.*?)\s*```"" so that using regex I can extract sql queries and no additional information.Here's the schema in a single line, using _ to represent spaces:Tables:studentTable:username_TEXT_PRIMARY_KEY,email_TEXT_UNIQUE_NOT_NULL,password_TEXT_NOT_NULL,full_name_TEXT_NOT_NULL,mobile_number_TEXT_NOT_NULL,address_TEXT_NOT_NULL,year_of_joining_INTEGER_NOT_NULL,branch_code_TEXT_NOT_NULL,current_semester_INTEGER,cgpa_REAL,FOREIGN_KEY_(branch_code)_REFERENCES_branchTable_(branch_code);attendanceTable:username_TEXT_NOT_NULL,course_code_TEXT_NOT_NULL,attendance_TEXT,date_DATE,PRIMARY_KEY_(username,course_code,date),FOREIGN_KEY_(username)_REFERENCES_studentTable_(username),FOREIGN_KEY_(course_code)_REFERENCES_courseTable_(course_code);marksTable:username_TEXT_NOT_NULL,course_code_TEXT_NOT_NULL,ExamType_TEXT_NOT_NULL,marks_obtained_REAL_NOT_NULL,max_marks_REAL_NOT_NULL,PRIMARY_KEY_(username,course_code,ExamType),FOREIGN_KEY_(username)_REFERENCES_studentTable_(username),FOREIGN_KEY_(course_code)_REFERENCES_courseTable_(course_code);branchTable:branch_code_TEXT_PRIMARY_KEY,branch_name_TEXT_NOT_NULL;adminTable:username_TEXT_PRIMARY_KEY,full_name_TEXT_NOT_NULL,email_TEXT_UNIQUE_NOT_NULL,password_TEXT_NOT_NULL;courseTable:course_code_TEXT_PRIMARY_KEY,course_name_TEXT_NOT_NULL,credits_INTEGER_NOT_NULL,course_instructor_code_TEXT_NOT_NULL,branch_code_TEXT_NOT_NULL,FOREIGN_KEY_(course_instructor_code)_REFERENCES_facultyTable_(faculty_code),FOREIGN_KEY_(branch_code)_REFERENCES_branchTable_(branch_code);facultyTable:faculty_code_TEXT_PRIMARY_KEY,full_name_TEXT_NOT_NULL,email_TEXT_UNIQUE_NOT_NULL,password_TEXT_NOT_NULL,cabin_number_TEXT,specialization_TEXT_NOT_NULL;notificationStudentTable:id_INTEGER_PRIMARY_KEY_AUTOINCREMENT,recipient_username_TEXT_NOT_NULL,message_TEXT_NOT_NULL,date_DATE_DEFAULT_CURRENT_DATE_NOT_NULL,FOREIGN_KEY_(recipient_username)_REFERENCES_studentTable_(username);notificationFacultyTable:id_INTEGER_PRIMARY_KEY_AUTOINCREMENT,recipient_username_TEXT_NOT_NULL,message_TEXT_NOT_NULL,date_DATE_DEFAULT_CURRENT_DATE_NOT_NULL,FOREIGN_KEY_(recipient_username)_REFERENCES_facultyTable_(faculty_code);student_courses_(Association_Table):username_TEXT_NOT_NULL,course_code_TEXT_NOT_NULL,PRIMARY_KEY_(username,course_code),FOREIGN_KEY_(username)_REFERENCES_studentTable_(username),FOREIGN_KEY_(course_code)_REFERENCES_courseTable_(course_code)\""},
    ]
    # Include last 5 prompts and responses
    for item in conversation_history:
        messages.append(item)

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="grok-2-1212",
            messages=messages,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        )
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content
        return full_response
    except Exception as e:
        print(f"An error occurred: {e}")
        yield f"An error occurred: {e}"
        return ""

# if __name__ == "__main__":
#     user_input = "Motivate me to getup early"

#     # # Example 1: Default (temperature=1.0)
#     # print("Response with default temperature (1.0):")
#     # get_streaming_chat_response(user_input)

#     # # Example 2: Setting custom temperature
#     # print("\nResponse with temperature = 0.5:")
#     # get_streaming_chat_response(user_input, temperature=0.5)

#     # # Example 3: Setting custom temperature and top_p
#     # print("\nResponse with temperature = 0.7 and top_p = 0.9:")
#     # get_streaming_chat_response(user_input, temperature=0.7, top_p=0.9)

#     # # # Example 4:  Setting temperature (top_p removed)
#     # # print("\nResponse with temperature=0.8")
#     # # get_streaming_chat_response(user_input, temperature=0.8)


#     # # Example 5: Setting temperature and top_p
#     # print("\nResponse with temperature=0.6, top_p=0.8")
#     # get_streaming_chat_response(user_input, temperature=0.6, top_p=0.8)