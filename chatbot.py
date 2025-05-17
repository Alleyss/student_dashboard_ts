import streamlit as st
from api_client import get_streaming_chat_response
from utils import load_sections, save_sections, add_new_section, get_section_conversation, add_message_to_section
import sqlite3
import pandas as pd
import re

# Database connection and setup
def get_connection():
    return sqlite3.connect('instance/students.db')

def app():
    st.title("Grok-Powered Chatbot")
    
    # Load existing sections
    sections = load_sections()

    # Ensure 'main' section exists
    if "main" not in sections:
        sections = add_new_section(sections, "main")
        save_sections(sections)
    
    # Initialize selected section to 'main'
    if "selected_section" not in st.session_state:
        st.session_state.selected_section = "main"

    # Display conversation
    if st.session_state.selected_section:
        conversation = get_section_conversation(sections, st.session_state.selected_section)
        for message in conversation:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask me about Streamlit"):
            # Get last 5 conversation turns
            last_5_messages = conversation[-5:]
            message_user = {"role": "user", "content": prompt}
            sections = add_message_to_section(sections, st.session_state.selected_section, message_user)
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                # Call the get_streaming_chat_response function with user input
                response_stream = get_streaming_chat_response(prompt, last_5_messages,0.5,0.9)
                # Use a generator to enable streaming
                response = st.write_stream(response_stream)
            
            sql_match = re.search(r"```sql\s*(.*?)\s*```", response, re.DOTALL)
            
            if sql_match:
              sql_query = sql_match.group(1).strip()
              try:
                  conn = get_connection()
                  cursor = conn.cursor()
                  cursor.execute(sql_query)
                  results = cursor.fetchall()
                  conn.commit()
                  conn.close()
                  
                #   conn.commit()

                  if results:
                      df = pd.DataFrame(results, columns=[description[0] for description in cursor.description])
                      st.dataframe(df)
                      message_assistant = {"role": "assistant", "content": df.to_markdown()}
                      sections = add_message_to_section(sections, st.session_state.selected_section, message_assistant)
                      save_sections(sections)

                  else:
                      st.write("No results found")
                      message_assistant = {"role": "assistant", "content": "No results found"}
                      sections = add_message_to_section(sections, st.session_state.selected_section, message_assistant)
                      save_sections(sections)

              except sqlite3.Error as e:
                  st.error(f"Error executing the query: {e}")
                  message_assistant = {"role": "assistant", "content": f"Error executing the query: {e}"}
                  sections = add_message_to_section(sections, st.session_state.selected_section, message_assistant)
                  save_sections(sections)

            else:
               message_assistant = {"role": "assistant", "content": response}
               sections = add_message_to_section(sections, st.session_state.selected_section, message_assistant)
               save_sections(sections)