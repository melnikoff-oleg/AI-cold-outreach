import streamlit as st

def initialize_session_state():
    if 'generated_messages' not in st.session_state:
        st.session_state.generated_messages = []
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = None
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = None
        st.session_state.company_data = None
    if 'linkedin_url' not in st.session_state:
        st.session_state.linkedin_url = ""
    if 'goal' not in st.session_state:
        st.session_state.goal = ""
    if 'example_message' not in st.session_state:
        st.session_state.example_message = ""
    if 'submit_button' not in st.session_state:
        st.session_state.submit_button = False
    if 'is_generate_more' not in st.session_state:
        st.session_state.is_generate_more = False

def extract_messages(ai_response):
    if '---Best Options---' in ai_response:
        options_section = ai_response.split('---Best Options---')[1]
        messages = options_section.strip().split('\n\n')
        return messages
    else:
        return [ai_response.strip()]

def update_progress(progress_text, progress_bar, progress, message):
    progress_text.text(message)
    progress_bar.progress(progress)

def reset_session_state():
    st.session_state.generated_messages = []
    st.session_state.profile_data = None
    st.session_state.company_data = None
    st.session_state.is_generate_more = False
    st.session_state.submit_button = False
