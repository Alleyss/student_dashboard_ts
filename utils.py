import json
import os

SECTIONS_FILE = "sections_data.json"

def load_sections():
    """Loads sections from the JSON file."""
    if not os.path.exists(SECTIONS_FILE):
        return {}
    with open(SECTIONS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError: # if there is an error parsing the json
          return {}

def save_sections(sections):
    """Saves sections to the JSON file."""
    with open(SECTIONS_FILE, 'w') as f:
        json.dump(sections, f, indent=4)

def add_new_section(sections, section_title):
    """Adds a new section to the sections dict"""
    if section_title and section_title not in sections:
      sections[section_title] = []
      save_sections(sections)
    return sections

def get_section_conversation(sections, selected_section):
    """Retrieve the conversation history from a specific section."""
    if selected_section in sections:
      return sections[selected_section]
    return []

def add_message_to_section(sections, selected_section, message):
      """Adds a new message to the section"""
      if selected_section in sections:
          sections[selected_section].append(message)
          save_sections(sections)
      return sections