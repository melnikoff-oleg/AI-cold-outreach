import streamlit as st
import time
from openai import OpenAI
import requests
import os
import threading

# Set OpenAI API key
openai_client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

# Set page configuration
st.set_page_config(
    page_title="Personalized Outreach Messages",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

hide_running_indicator = """
<style>
[data-testid="stStatusWidget"] {display: none;}
</style>
"""
st.markdown(hide_running_indicator, unsafe_allow_html=True)

# Hide Streamlit's default menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize session state variables
if 'generated_messages' not in st.session_state:
    st.session_state.generated_messages = []
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None
    st.session_state.company_data = None

# Main container
def main():
    # Headline and Subheadline
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

    # Template Selection
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

    # Define templates with emojis
    templates = {
        "🔍 Recruiter Outreach": {
            "linkedin_url": "https://www.linkedin.com/in/nycgareth/",
            "goal": "Convince the candidate to join our innovative startup working on AI for healthcare.",
            "example": "Hi [Name], I was impressed by your work in machine learning and think you'd be a great fit for our team at [Company].",
            "key": "Recruiter Outreach"
        },
        "💼 B2B Sales Outreach": {
            "linkedin_url": "https://www.linkedin.com/in/nycgareth/",
            "goal": "Introduce our new SaaS platform that can help optimize their business processes and propose a demo meeting.",
            "example": "Hello [Name], our platform has helped companies like yours increase efficiency by 30%. I'd love to show you how.",
            "key": "B2B Sales Outreach"
        },
        "🤝 Customer Development": {
            "linkedin_url": "https://www.linkedin.com/in/nycgareth/",
            "goal": "Understand customer needs to improve our product offerings.",
            "example": "Hi [Name], as someone experienced in [industry], your insights would be invaluable for our product development.",
            "key": "Customer Development"
        },
        "✏️ Custom Message": {
            "linkedin_url": "",
            "goal": "",
            "example": "",
            "key": "Custom Message"
        },
    }

    # Template buttons in one line
    template_names = list(templates.keys())
    num_templates = len(template_names)
    cols = st.columns(num_templates, gap="small")

    for idx, col in enumerate(cols):
        with col:
            if st.button(template_names[idx], key=templates[template_names[idx]]["key"]):
                selected_template = templates[template_names[idx]]["key"]
                st.session_state.selected_template = selected_template
                # When a template is selected, populate the input fields
                st.session_state.linkedin_url = templates[template_names[idx]]["linkedin_url"]
                st.session_state.goal = templates[template_names[idx]]["goal"]
                st.session_state.example_message = templates[template_names[idx]]["example"]

    st.write("")
    st.write("")

    # Input Fields
    st.markdown("<h3 style='text-align: center;'>Input Details</h3>", unsafe_allow_html=True)
    with st.form(key='input_form'):
        # Get template data
        if 'linkedin_url' not in st.session_state:
            st.session_state.linkedin_url = ""
        if 'goal' not in st.session_state:
            st.session_state.goal = ""
        if 'example_message' not in st.session_state:
            st.session_state.example_message = ""

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

        submit_button = st.form_submit_button(label='Generate Messages')

    # Update session state with inputs
    st.session_state.linkedin_url = linkedin_url
    st.session_state.goal = goal
    st.session_state.example_message = example_message

    # Handle form submission
    if submit_button:
        if not linkedin_url.strip() or not goal.strip():
            st.error("Please provide both a LinkedIn Profile URL and your goal.")
        else:
            generate_messages(False)  # False indicates it's not a "Generate More Messages" action

    # Display generated messages
    if st.session_state.generated_messages:
        st.markdown("<h3 style='text-align: center; color: #333333;'>Your Personalized Message Options</h3>", unsafe_allow_html=True)
        for idx, message in enumerate(st.session_state.generated_messages, 1):
            message_content = message.replace('\n', '<br>')
            st.markdown(f"""
            <div style='background-color: #F5F5F5; padding: 20px; border: 1px solid #DDDDDD; border-radius: 5px; margin-bottom: 20px;'>
                <p style='font-size: 16px; color: #333333;'>{message_content}</p>
                <div style='clear: both;'></div>
            </div>""", unsafe_allow_html=True)

    # Provide clear actions
    if st.session_state.generated_messages:
        st.write("")
        st.markdown("<h3 style='text-align: center;'>What would you like to do next?</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Generate More Messages"):
                generate_messages(True)  # True indicates it's a "Generate More Messages" action
        with col2:
            if st.button("📝 Start New Message"):
                st.session_state.generated_messages = []
                # Inputs remain the same; no need to reset them
                st.experimental_rerun()

    # Footer
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

# Function to generate messages using OpenAI and Proxycurl
def generate_messages(is_generate_more):
    # Show dynamic progress updates
    try:
        progress_text = st.empty()
        progress_bar = st.progress(0)

        # Check if profile data is already fetched
        if not is_generate_more or st.session_state.profile_data is None:
            # Step 1: Fetching LinkedIn profile
            progress_text.text("🔍 Fetching LinkedIn profile...")
            progress_bar.progress(5)
            headers = {'Authorization': 'Bearer ' + os.getenv("PROXYCURL_TOKEN")}
            api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
            params = {'url': st.session_state.linkedin_url}
            response = requests.get(api_endpoint, params=params, headers=headers)
            if response.status_code != 200:
                st.error("Error fetching LinkedIn profile data.")
                return
            person_profile = response.json()
            st.session_state.profile_data = person_profile
            time.sleep(1)  # Reduced sleep time for first step
        else:
            person_profile = st.session_state.profile_data

        # Step 2: Analyzing your goal
        progress_text.text("🎯 Analyzing your goal...")
        progress_bar.progress(20)
        time.sleep(0.5)

        # Step 3: Fetching company information
        if not is_generate_more or st.session_state.company_data is None:
            progress_text.text("🏢 Fetching company information...")
            progress_bar.progress(35)
            company_profile = {}
            if 'experiences' in person_profile and person_profile['experiences']:
                experiences = person_profile['experiences']
                current_company = None
                for exp in experiences:
                    if exp.get('currently') is True:
                        current_company = exp
                        break
                if not current_company:
                    current_company = experiences[0]
                company_url = current_company.get('company_linkedin_profile_url')
                if company_url:
                    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company'
                    params = {'url': company_url}
                    headers = {'Authorization': 'Bearer ' + os.getenv("PROXYCURL_TOKEN")}
                    response = requests.get(api_endpoint, params=params, headers=headers)
                    if response.status_code == 200:
                        company_profile = response.json()
            else:
                company_profile = {}
            st.session_state.company_data = company_profile
            time.sleep(1)
        else:
            company_profile = st.session_state.company_data

        # Step 4: Brainstorming ideas
        progress_text.text("💡 Brainstorming ideas...")
        progress_bar.progress(50)
        time.sleep(1)

        # Step 5: Generating messages
        progress_text.text("✍️ Generating messages...")
        progress_bar.progress(65)

        # Build the prompt
        prompt = ""
        prompt += f"You are a professional with expertise in crafting cold outreach messages that convert.\n"
        prompt += "Help me write a cold outreach message to a potential partner that will make them interested in conversation.\n"
        prompt += "---\n"
        prompt += "Here is a description of my intention:\n"
        prompt += f"{st.session_state.goal}\n"
        prompt += "---\n"
        prompt += "Here is the profile of the lead you are reaching out to:\n"
        prompt += f"Name: {person_profile.get('full_name', 'N/A')}.\n"
        prompt += f"Occupation: {person_profile.get('occupation', 'N/A')}.\n"
        summary = person_profile.get('summary', '')
        if summary:
            prompt += f"Summary: {summary}\n"
        if company_profile:
            prompt += "Information about their company:\n"
            prompt += f"Name: {company_profile.get('name', 'N/A')}.\n"
            industry = company_profile.get('industry', '')
            if industry:
                prompt += f"Industry: {industry}.\n"
            description = company_profile.get('description', '')
            if description:
                prompt += f"Description: {description}\n"
        prompt += "---\n"
        prompt += "Help me write a message for this lead that resonates with them and makes them want to reply. Keep in mind my requirements:\n"
        prompt += "- Keep it short and to the point, at max 100 words.\n"
        prompt += "- Make an attention-grabbing opening.\n"
        prompt += "- Write naturally, like a human. Avoid sounding like a bot.\n"
        prompt += "- Use simple, common English words.\n"
        prompt += "- Go straight to the point, avoid any compliments or saying that I followed them for a long time.\n"
        if st.session_state.example_message:
            prompt += "---\n"
            prompt += "Here is an example message that I like; imitate the style as closely as possible:\n"
            prompt += f"{st.session_state.example_message}\n"
        prompt += "---\n"
        prompt += "Now brainstorm about how to write a catchy subject and opening line, then brainstorm personalization ideas specifically to this lead.\n"
        prompt += "Then write 6 highly diverse options for the message.\n"
        prompt += "Gauge each of them in terms of how likely they will get a response and how human they sound. Then choose the top 3 of them and print them in the following format: ---Best Options---'newline x2'Option 1'newline'Subject: ...'newline'Body: ... 'newline x2'Option 2... And nothing else after the last option.\n"
        prompt += "Start working:\n"

        # Call OpenAI API to get the messages
        def call_openai_api():
            nonlocal ai_response
            completion = openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-4",
            )
            ai_response = completion.choices[0].message.content

        ai_response = ""
        api_thread = threading.Thread(target=call_openai_api)
        api_thread.start()

        # While the API call is processing, update progress
        progress = 65
        messages_during_wait = [
            "🔄 Refining language and tone...",
            "🔄 Tailoring content to the recipient...",
            "🔄 Finalizing message drafts..."
        ]
        message_index = 0
        while api_thread.is_alive():
            progress += 1
            progress_bar.progress(progress)
            progress_text.text(messages_during_wait[message_index % len(messages_during_wait)])
            time.sleep(3)
            message_index +=1
            if progress >= 95:
                progress = 95
        api_thread.join()

        progress_text.text("✅ Completed!")
        progress_bar.progress(100)
        time.sleep(0.5)
        progress_text.empty()
        progress_bar.empty()

        # Extract messages from AI response
        messages = extract_messages(ai_response)

        # Append new messages to session state
        st.session_state.generated_messages.extend(messages)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to extract messages from AI response
def extract_messages(ai_response):
    if '---Best Options---' in ai_response:
        options_section = ai_response.split('---Best Options---')[1]
        messages = options_section.strip().split('\n\n')
        return messages
    else:
        return [ai_response.strip()]

if __name__ == "__main__":
    main()
