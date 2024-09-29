import streamlit as st
from config import PAGE_CONFIG, HIDE_STREAMLIT_STYLE
from components import (
    display_header,
    display_template_selection,
    display_input_form,
    display_generated_messages,
    display_next_actions,
    display_footer,
)
from utils import initialize_session_state
from api import fetch_profile_data, generate_messages

# Set page configuration
st.set_page_config(
    page_title=PAGE_CONFIG['page_title'],
    page_icon=PAGE_CONFIG['page_icon'],
    layout=PAGE_CONFIG['layout'],
    initial_sidebar_state=PAGE_CONFIG['initial_sidebar_state']
)

# Hide Streamlit's default menu and footer
st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

def main():
    # Display Header
    display_header()

    # Template Selection
    templates = display_template_selection()

    # Input Form
    linkedin_url, goal, example_message = display_input_form(templates)

    # Handle form submission
    if st.session_state.submit_button:
        if not linkedin_url.strip() or not goal.strip():
            st.error("Please provide both a LinkedIn Profile URL and your goal.")
        else:
            fetch_profile = not st.session_state.is_generate_more or st.session_state.profile_data is None
            fetch_company = not st.session_state.is_generate_more or st.session_state.company_data is None
            fetch_profile_data(fetch_profile, fetch_company)
            generate_messages()

    # Display Generated Messages
    display_generated_messages()

    # Display Next Actions
    display_next_actions()

    # Display Footer
    display_footer()

if __name__ == "__main__":
    main()
