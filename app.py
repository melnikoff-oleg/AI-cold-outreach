import streamlit as st
from openai import OpenAI
import requests
import os

openai_client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

# profile_url = 'https://www.linkedin.com/in/nycgareth/'

st.title("AI-Enhanced Cold Outreach Tool")

with st.form("profile_url"):
    profile_url = st.text_input("Enter LinkedIn profile URL:")
    submit_button = st.form_submit_button("Generate message")

if submit_button:
    if profile_url:
        st.write("Result:")

        headers = {'Authorization': 'Bearer ' + os.getenv("PROXYCURL_TOKEN")}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {'url': profile_url}
        person_profile = requests.get(api_endpoint, params=params, headers=headers).json()
        api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company'
        params = {'url': person_profile['experiences'][0]['company_linkedin_profile_url']}
        company_profile = requests.get(api_endpoint, params=params, headers=headers).json()
        
        prompt = ''
        prompt += f"""You are a professional B2B sales manager with 10 years of experience, you are an expert in writing cold messages that convert.
        Help me write a cold outreach message to a potential client, to make them interested in talking to me. 
        ---
        Here is a description of my intention:
        I'm a tech expert with decent experience in software development and artificial intellegence. I quit my job and started my own company to help businesses automate their processes using AI, make their employees more efficient, save time and money. Right now I'm looking for the first company to partner with, as I want to build up my portfolio and help someone at the same time.
        I would love to develop a custom AI solution for your company. And I'm happy to guide you in the world of AI if you need it. 
        Examples of solutions I can develop: 1) automate data gathering and data analysis, 2) personalize content for a specific person based on their intent, 3) analyse performance of your employees and give recommendations on how to improve it, 4) automate any sort of routine tasks, 5) build a chatbot for any purpose, 6) build an internal documentation system with an easy search, 7) many other AI solutions applicable to your business.
        In my message I wanna convey that initially I just wanna to talk, to discuss potential AI applications in their case, I don't wanna pretend being an expert, I don't wanna be sellsy, I want to have a friendly conversation first of all.
        ---\n"""
        prompt += f"""Here is the profile of the lead you are reaching out to:
        Name: {person_profile['full_name']}. Occupation: {person_profile['occupation']}. Summary: {person_profile['summary']}
        Information about their company:
        Name: {company_profile['name']}. Industry: {company_profile['industry']}. Description: {company_profile['description']}
        ---\n"""
        prompt += f"""Help me write a message for this lead that resonates with him and makes him interested in my service. Keep in mind my requirements:
        - showcase a problem that their company might have and how AI can solve it
        - introduce myself and what I want for them
        - keep it short and to the point, at max 100 words
        - make the message personalized, but don't be dishonest or insincere, don't you ever say you followed their career
        - make attention-grabbing opening
        - showcase how they can make more profit by integrating AI
        - showcase that I'm happy to navigate and just talk to them
        - add a very clear call to action: ask if they have tried and found value in using AI to improve their processes.
        - WRITE IMPERFECTLY, LIKE A HUMAN. IF THE PROSPECT WILL RECOGNISE YOU AS A BOT, THEY WILL KILL YOU
        At first brainstorm what might be specific problems and solutions the lead might face. Reason and make a chain of thought. Then write the message itself.
        ---\n"""

        completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4-turbo",
        )
        message = completion.choices[0].message.content
        st.write(message)
    else:
        st.error("Please enter a stock ticker.")
