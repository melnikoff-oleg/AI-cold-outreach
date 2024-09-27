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
        Help me write a cold outreach message to a potential partner, that will make them interested in conversation.
        ---
        Here is a description of my intention:
        I'm a tech expert with decent experience in software development and artificial intellegence. I wanna know if they tried to use AI in their processes and if yes, how it worked out, are they satisfied.
        I'm interested in what might be the problems in their industry that AI can solve and make the company more profitable. 
        I don't wanna offer any services yet, but I wanna show them that I have one strong idea of how AI can help them.
        The goal of my initial message is to start a conversation and make them respond.
        ---\n"""
        prompt += f"""Here is the profile of the lead you are reaching out to:
        Name: {person_profile['full_name']}. Occupation: {person_profile['occupation']}. Summary: {person_profile['summary']}
        Information about their company:
        Name: {company_profile['name']}. Industry: {company_profile['industry']}. Description: {company_profile['description']}
        ---\n"""
        prompt += f"""Help me write a message for this lead that resonates with him and makes him want to reply. Keep in mind my requirements:
        - provide 1 very specific problem that their company might have and how AI can solve it - as my hypothesis and that I don't know if it's true
        - keep it short and to the point, at max 100 words
        - make attention-grabbing opening
        - WRITE IMPERFECTLY, LIKE A HUMAN. IF THE PROSPECT WILL RECOGNISE YOU AS A BOT, THEY WILL KILL YOU
        - USE SIMPLE, THE MOST POPULAR ENGLISH WORDS
        - GO STRAIGHT TO THE POINT, AVOID ANY COMPLIMENTS TO THEIR COMPANY OR SAYING THAT I FOLLOWED THEM FOR A LONG TIME
        - don't use capitalisation as in examples, use small letters everywhere

        Here are 3 examples of how the final message should look like, imitate the style as close as possible:

        Subject: AI is absolutely useless in <their industry>
        Body: hey Jacob, I was looking for someone in <their industry> and found you. 
        do you know by any chance, are there any valuable AI applications in your business?
        maybe you tried something yourself. I though about <custom idea>, but I have no idea if it's really valuable.
        would be grateful for any advice.

        Subject: "AI might kick me out of business" (with quotes)
        Body: hi Jennifer, I'm looking to talk to someone in <their industry> about the application of AI. 
        seems like you might be a right person.
        I'm no expert in <their industry> as you are, but I'm experienced with software engineering and AI and would love to have a chat.
        are you down to it? or maybe you know someone who would be interested?

        Subject: "AI is a scam" (with quotes)
        Body: hi Alex, I'm a software engineer with a decent experience in AI.
        I'm curious, have you tried to use AI in your business?
        I have a hypothesis that it can solve <specific problem>, but I'm not sure if it's true.
        would love to hear your thoughts on this.

        Now brainstorm about how to write a catchy subject and opening line, prove that you're a genius here! Then brainstorm about the specific problem that AI can solve for them.
        Write your ideas.
        Then write 5 highly diverse options for the message. Gauge each of them in terms of how likely they will get a response, and how human they sound. Then choose the best one of them.
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
