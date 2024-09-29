PAGE_CONFIG = {
    'page_title': "Personalized Outreach Messages",
    'page_icon': "💬",
    'layout': "centered",
    'initial_sidebar_state': "collapsed",
}

HIDE_STREAMLIT_STYLE = """
    <style>
    [data-testid="stStatusWidget"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """

TEMPLATES = {
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
