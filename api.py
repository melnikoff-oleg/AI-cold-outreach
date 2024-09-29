import streamlit as st
import time
import threading
import requests
import os
from openai import OpenAI
from utils import extract_messages, update_progress
from config import PAGE_CONFIG

# Set OpenAI API key
openai_client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

def fetch_profile_data(fetch_profile=True, fetch_company=True):
    if fetch_profile:
        # Fetch LinkedIn profile data
        headers = {'Authorization': 'Bearer ' + os.getenv("PROXYCURL_TOKEN")}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {'url': st.session_state.linkedin_url}
        response = requests.get(api_endpoint, params=params, headers=headers)
        if response.status_code != 200:
            st.error("Error fetching LinkedIn profile data.")
            return
        st.session_state.profile_data = response.json()
        time.sleep(1)  # Simulate processing time

    if fetch_company:
        # Fetch company data
        person_profile = st.session_state.profile_data
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
        time.sleep(1)  # Simulate processing time

def generate_messages():
    progress_text = st.empty()
    progress_bar = st.progress(0)
    progress = 0

    # Display initial progress
    update_progress(progress_text, progress_bar, progress, "🚀 Starting message generation...")

    # Adjust progress based on whether profile data was fetched
    if st.session_state.is_generate_more:
        progress = 65
    else:
        progress = 50

    # Build the prompt
    person_profile = st.session_state.profile_data
    company_profile = st.session_state.company_data
    prompt = build_prompt(person_profile, company_profile)

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
    messages_during_wait = [
        "🔄 Refining language and tone...",
        "🔄 Tailoring content to the recipient...",
        "🔄 Finalizing message drafts..."
    ]
    message_index = 0
    while api_thread.is_alive():
        progress += 1
        if progress >= 95:
            progress = 95
        update_progress(progress_text, progress_bar, progress, messages_during_wait[message_index % len(messages_during_wait)])
        time.sleep(3)
        message_index += 1
    api_thread.join()

    update_progress(progress_text, progress_bar, 100, "✅ Completed!")
    time.sleep(0.5)
    progress_text.empty()
    progress_bar.empty()

    # Extract messages from AI response
    messages = extract_messages(ai_response)

    # Append new messages to session state
    st.session_state.generated_messages.extend(messages)
    st.session_state.submit_button = False  # Reset submit button state

def build_prompt(person_profile, company_profile):
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
    return prompt
