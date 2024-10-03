import streamlit as st
from openai import OpenAI
import requests
import uuid
import json
import time
import hashlib
import os
from streamlit_cookies_manager import CookieManager

# Set OpenAI API key
openai_client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

# Set page configuration
st.set_page_config(
    page_title="Personalized Outreach Messages",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
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
    st.session_state.generated_messages = ''
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None
    st.session_state.company_data = None

cookies = CookieManager()

if not cookies.ready():
    st.stop()

# Function to generate or retrieve user ID
def get_user_id():
    if 'user_id' in cookies:
        return cookies['user_id']
    else:
        user_id = str(uuid.uuid4())
        cookies['user_id'] = user_id
        cookies.save()
        return user_id

user_id = get_user_id()

# Directory to store user data
USER_DATA_DIR = 'user_data'
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

# Function to save user data
def save_user_data(user_id):
    data = {
        'linkedin_url': st.session_state.linkedin_url,
        'goal': st.session_state.goal,
        'example_message': st.session_state.example_message
    }
    file_path = os.path.join(USER_DATA_DIR, f"{user_id}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f)

# Function to load user data
def load_user_data(user_id):
    file_path = os.path.join(USER_DATA_DIR, f"{user_id}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return {}

# Get or create a user ID
user_id = get_user_id()

# Directory to store cached API responses
CACHE_DIR = 'api_cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Function to generate a cache file path based on the profile URL
def get_cache_file_path(url):
    # Create a unique filename using a hash of the URL
    filename = hashlib.md5(url.encode('utf-8')).hexdigest() + '.json'
    return os.path.join(CACHE_DIR, filename)

# Function to parse LinkedIn profile using a third-party API with disk-based caching
def parse_linkedin_profile(profile_url, is_person):
    cache_file = get_cache_file_path(profile_url)
    cache_ttl = 86400 * 7  # Cache Time-to-Live in seconds (e.g., 86400 seconds = 1 day)

    # Check if cached file exists and is still valid
    if os.path.exists(cache_file):
        cache_age = time.time() - os.path.getmtime(cache_file)
        if cache_age < cache_ttl:
            # Load data from cache
            with open(cache_file, 'r') as f:
                return json.load(f)
        else:
            st.write("Cache expired. Fetching new data.")
    
    headers = {'Authorization': 'Bearer ' + os.getenv("PROXYCURL_TOKEN")}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin' if is_person else 'https://nubela.co/proxycurl/api/linkedin/company'
    params = {'url': profile_url}
    response = requests.get(api_endpoint, params=params, headers=headers)
    if response.status_code != 200:
        st.error("Error fetching LinkedIn profile data.")
        return
    profile = response.json()
    with open(cache_file, 'w') as f:
            json.dump(profile, f)
    return profile

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
            "linkedin_url": "https://www.linkedin.com/in/melnikoff-oleg/",
            "goal": """I'm a tech recruiter, I'm responsible for hiring the best talent for my company. I just want to start a conversation, and make the lead interested in the offered position.
Here is more information about our company and opened position:
Company: Jane Street. Position: Quantitative Researcher, Trading and Research. Location: London. Description: At Jane Street, we consider trading and programming to be two ends of a continuum. As both a trading firm and a tech firm, we have room for people who love to trade, people who love to program, and people everywhere in between. Nearly all of our traders write code, and many of our software engineers trade. The role you carve out for yourself will be largely dependent on your strengths and the types of problems you enjoy thinking about.
Researchers at Jane Street are responsible for building models, strategies, and systems that price and trade a variety of financial instruments. As a mix of the trading and software engineering roles, this work involves many things: analysing large datasets, building and testing models, creating new trading strategies, and writing the code that implements them.
Requirements
Be able to apply logical and mathematical thinking to all kinds of problems. Asking great questions is more important than knowing all the answers.
Write great code. We mostly write in OCaml, so you should want to learn functional programming if you don't already have experience with it.
Have good taste in research. The problems we work on rarely have clean, definitive answers. You should be comfortable pushing in new and unknown directions while maintaining clarity of purpose
Think and communicate precisely and openly. We believe great solutions come from the interaction between diverse groups of people across the firm
Fluency in English required.
How to write the message:
- It's a LinkedIn message, so include Subject and Body.
- Keep messages short and to the point, ideally not more than 100 words.
- Make an attention-grabbing opening, so the lead can't help but read it.
- MAKE AN ATTENTION-GRABBING OPENING, SO THE LEAD CAN'T HELP BUT READ IT.
- MAKE THE MESSAGE STAND OUT. OUR RECIPIENT GETS HUNDREDS OF MESSAGES DAILY.
- USE EXECATLY THE STYLE THAT I PROVIDED IN THE EXAMPLES.""",
            "example": """Example 1

Subject: Mark, you deserve higher salary, and better work environment

Body: hey Mark, stumbled upon your background and couldn't help but get a bit geeky-excited at the Django-to-Kubernetes spectrum you've mastered! we're ITkey, a player in OpenStack solutions, and we're on the hunt for a Python Developer. your skills in Python, FastAPI, and Kubernetes are right up our alley. 
how about swapping your current scenery with large-scale, high-load projects and a team of top-tier professionals?""",
            "key": "Recruiter Outreach"
        },
        "💼 B2B Sales Outreach": {
            "linkedin_url": "https://www.linkedin.com/in/alexhormozi/",
            "goal": """My name is Jason, I'm a CEO of Fluently, it's an AI English coach. Fluently delivers instant feedback on your daily video calls, so you can master English every day. 
Our app helps non-native English speakers improve their language skills by providing feedback on pronunciation, grammar and vocabulary after their daily video calls.
Right now we're focused on reaching out big international companies.
How to write the message:
- It's a LinkedIn message, so include Subject and Body.
- Keep messages short and to the point, ideally not more than 100 words.
- Make an attention-grabbing opening, so the lead can't help but read it.
- USE THE MOST SIMPLE ENGLISH WORDS.
- WRITE SIMPLE, SHORT SENTENCES.
- USE EXECATLY THE STYLE THAT I PROVIDED IN THE EXAMPLES.""",
            "example": """Example 1

Subject: Exploring Synergies in [Prospect's Industry]

Body: Hi [Prospect's Name],
I hope this message finds you well. I recently came across your profile while researching leaders in the [Prospect's Industry], and I was impressed by your work at [Prospect's Company].
At [Your Company], we specialize in [Your Company's Solution], which has helped companies like [Example Company] achieve [Specific Benefit/Result]. Given your focus on [Prospect's Area of Interest], I believe there might be a valuable opportunity for us to collaborate.
Would you be open to a brief call to explore how we can support your goals at [Prospect's Company]? I'm available for a call next week and would love to hear your thoughts.
Looking forward to the possibility of working together.
Best regards,
Jason, CEO, Fluently""",
            "key": "B2B Sales Outreach"
        },
        "🤝 Customer Development": {
            "linkedin_url": "https://www.linkedin.com/in/nycgareth/",
            "goal": """My name is Pepin, I'm a CEO of a company called Annora AI, we build AI automations for manufacturing companies.
I want to know whether they have any problems that AI can solve, making them more money or saving time.
How to write the message:
- It's a LinkedIn message, so include Subject and Body.
- Keep messages short and to the point, ideally not more than 100 words.
- Make an attention-grabbing opening, so the lead can't help but read it.
- USE THE MOST SIMPLE ENGLISH WORDS.
- WRITE SIMPLE, SHORT SENTENCES.
- USE EXECATLY THE STYLE THAT I PROVIDED IN THE EXAMPLES.""",
            "example": """Example 1

Subject: manufacturing companies optimize their operations with AI

Body: Hello Bobby, I appreaciate your experience in building highly efficient factories at scale.
I think AI can help you optimize some of the day-to-day processes, like customer communication or internal trainings.
Let's chat!""",
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
        # Load user data
        user_data = load_user_data(user_id)
        # Get template data
        if 'linkedin_url' not in st.session_state:
            st.session_state.linkedin_url = user_data.get('linkedin_url', '')
        if 'goal' not in st.session_state:
            st.session_state.goal = user_data.get('goal', '')
        if 'example_message' not in st.session_state:
            st.session_state.example_message = user_data.get('example_message', '')

        linkedin_url = st.text_input(
            "LinkedIn Profile URL",
            value=st.session_state.linkedin_url,
            placeholder="e.g., https://www.linkedin.com/in/johndoe/"
        )

        goal = st.text_area(
            "Your Goal and Instructions",
            value=st.session_state.goal,
            placeholder="Describe what you want to achieve with this message..."
        )

        example_message = st.text_area(
            "Examples of a Good Message (Optional)",
            value=st.session_state.example_message,
            placeholder="Paste example messages here or leave blank..."
        )

        submit_button = st.form_submit_button(label='Generate Messages')

    # Update session state with inputs
    st.session_state.linkedin_url = linkedin_url
    st.session_state.goal = goal
    st.session_state.example_message = example_message
    
    output_box = st.empty()
    if st.session_state.generated_messages:
        messages_content = st.session_state.generated_messages.replace('\n', '<br>')
        output_box.markdown(f"""
        <div style='background-color: #F5F5F5; padding: 20px; border: 1px solid #DDDDDD; border-radius: 5px; margin-bottom: 20px;'>
            <p style='font-size: 16px; color: #333333;'>{messages_content}</p>
            <div style='clear: both;'></div>
        </div>""", unsafe_allow_html=True)

    # Handle form submission
    if submit_button:
        if not linkedin_url.strip() or not goal.strip():
            st.error("Please provide both a LinkedIn Profile URL and your goal.")
        else:
            generate_messages(False, output_box)  # False indicates it's not a "Generate More Messages" action

    # Provide clear actions
    if st.session_state.generated_messages:
        st.write("")
        st.markdown("<h3 style='text-align: center;'>What would you like to do next?</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Generate More Messages"):
                generate_messages(True, output_box)  # True indicates it's a "Generate More Messages" action
        with col2:
            if st.button("📝 Start New Message"):
                st.session_state.generated_messages = ''
                # Inputs remain the same; no need to reset them
                st.rerun()

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
def generate_messages(is_generate_more, output_box):
    # Show dynamic progress updates
    try:
        save_user_data(user_id)

        if not is_generate_more:
            progress_text = st.empty()
            progress_bar = st.progress(0)

        # Check if profile data is already fetched
        if not is_generate_more or st.session_state.profile_data is None:
            # Step 1: Fetching LinkedIn profile
            progress_text.text("🔍 Fetching LinkedIn profile...")
            progress_bar.progress(0)
            person_profile = parse_linkedin_profile(st.session_state.linkedin_url, True)
            st.session_state.profile_data = person_profile
        else:
            person_profile = st.session_state.profile_data

        # Step 3: Fetching company information
        if not is_generate_more or st.session_state.company_data is None:
            progress_text.text("🏢 Fetching company information...")
            progress_bar.progress(50)
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
                    company_profile = parse_linkedin_profile(company_url, False)
            else:
                company_profile = {}
            st.session_state.company_data = company_profile
        else:
            company_profile = st.session_state.company_data


        # Build the prompt
        work_experience = ''
        for i in range(min(2, len(person_profile['experiences']))):
            q = person_profile['experiences'][i]
            for el in q:
                if q[el] is None:
                    q[el] = 'None'
            work_experience += f"Company: {q['company']}, Role: {q['title']}, Description: {q['description']}\n"
        prompt = f"""You are a professional sales manager with 10 years of experience in crafting cold outreach messages that convert. You worked with billion-dollar clients like Google, Apple, and Facebook. One hour consulatation with you costs 10 thousand dollars.
Help me write a cold outreach message that will make a recipient interested in conversation.
I will give you:
1) Information about the lead that we are reaching out to
2) My objective and requirements for this cold outreach
3) Example messages
Then you will write high-quality messages

Information about the lead that we are reaching out to:
Lead's Name: {person_profile['full_name']}
Lead's Occupation: {person_profile['occupation']}
Lead's Summary: {person_profile['summary']}
Lead's work experience: {work_experience}
Information about the lead's current company:
Company Name: {company_profile['name']}
Industry: {company_profile['industry']}
Description: {company_profile['description']}

My objective and requirements for this cold outreach:
{st.session_state.goal}

Example messages:
{st.session_state.example_message}

That's all, now it's your turn to work. Write one high quality cold outreach message for our lead.
Your work:"""

        if not is_generate_more:
            progress_bar.progress(100)
            time.sleep(0.1)
            progress_text.empty()
            progress_bar.empty()

        stream = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        if not st.session_state.generated_messages == '':
            st.session_state.generated_messages += '<br>-----------------------------------<br>'
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                st.session_state.generated_messages += chunk.choices[0].delta.content
                output_box.markdown(f"""
                    <div style='background-color: #F5F5F5; padding: 20px; border: 1px solid #DDDDDD; border-radius: 5px; margin-bottom: 20px;'>
                        <p style='font-size: 16px; color: #333333;'>{st.session_state.generated_messages}</p>
                        <div style='clear: both;'></div>
                    </div>
                """, unsafe_allow_html=True)
        st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
