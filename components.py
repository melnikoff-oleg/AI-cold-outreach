import streamlit as st
from config import TEMPLATES
from utils import reset_session_state

def display_header():
    st.markdown(
        """
        <div style='text-align: center;'>
            <h2 style='font-size: 36px; font-weight: bold; color: #333333;'>💡 Generate Personalized Outbound Messages Instantly</h2>
            <p style='font-size: 20px; color: #666666;'>Enter a LinkedIn profile and your goal, get a tailored message ready to send.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

def display_template_selection():
    st.markdown(
        """
        <style>
        .template-button {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #CCCCCC;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            font-size: 16px;
            width: 100%;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .template-button:hover {
            border-color: #4A90E2;
            color: #4A90E2;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h3 style='text-align: center;'>Select a Template</h3>", unsafe_allow_html=True)

    template_names = list(TEMPLATES.keys())
    num_templates = len(template_names)
    cols = st.columns(num_templates, gap="small")

    for idx, col in enumerate(cols):
        with col:
            if st.button(template_names[idx], key=TEMPLATES[template_names[idx]]["key"]):
                selected_template = TEMPLATES[template_names[idx]]["key"]
                st.session_state.selected_template = selected_template
                # Populate input fields
                st.session_state.linkedin_url = TEMPLATES[template_names[idx]]["linkedin_url"]
                st.session_state.goal = TEMPLATES[template_names[idx]]["goal"]
                st.session_state.example_message = TEMPLATES[template_names[idx]]["example"]
    st.write("")
    st.write("")
    return TEMPLATES

def display_input_form(templates):
    st.markdown("<h3 style='text-align: center;'>Input Details</h3>", unsafe_allow_html=True)
    with st.form(key='input_form'):
        linkedin_url = st.text_input(
            "LinkedIn Profile URL",
            value=st.session_state.linkedin_url,
            placeholder="e.g., https://www.linkedin.com/in/johndoe/"
        )

        goal = st.text_area(
            "Your Goal",
            value=st.session_state.goal,
            placeholder="Describe what you want to achieve with this message..."
        )

        example_message = st.text_area(
            "Example of a Good Message (Optional)",
            value=st.session_state.example_message,
            placeholder="Paste an example message here or leave blank..."
        )

        st.session_state.submit_button = st.form_submit_button(label='Generate Messages')

    # Update session state with inputs
    st.session_state.linkedin_url = linkedin_url
    st.session_state.goal = goal
    st.session_state.example_message = example_message

    return linkedin_url, goal, example_message

def display_generated_messages():
    if st.session_state.generated_messages:
        st.markdown("<h3 style='text-align: center; color: #333333;'>Your Personalized Message Options</h3>", unsafe_allow_html=True)
        for idx, message in enumerate(st.session_state.generated_messages, 1):
            message_content = message.replace('\n', '<br>')
            st.markdown(f"""
            <div style='background-color: #F5F5F5; padding: 20px; border: 1px solid #DDDDDD; border-radius: 5px; margin-bottom: 20px;'>
                <p style='font-size: 16px; color: #333333;'>{message_content}</p>
                <div style='clear: both;'></div>
            </div>""", unsafe_allow_html=True)

def display_next_actions():
    if st.session_state.generated_messages:
        st.write("")
        st.markdown("<h3 style='text-align: center;'>What would you like to do next?</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Generate More Messages"):
                st.session_state.is_generate_more = True
                st.session_state.submit_button = True
        with col2:
            if st.button("📝 Start New Message"):
                reset_session_state()
                # Inputs remain the same; no need to reset them
                st.experimental_rerun()

def display_footer():
    st.write("")
    st.write("")
    st.markdown(
        """
        <hr style='border:1px solid #DDDDDD'>
        <div style='text-align: center; font-size: 14px; color: #999999;'>
            <p>We respect your privacy. No data is stored.</p>
            <p>Questions? Contact me at <a href='mailto:oleg@evolva.ai'>oleg@evolva.ai</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
