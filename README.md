# 🚀 AI System for Cold Outreach

🌐 **Live Website**: https://evolva.ai/cold-outreach/

Welcome to the **AI cold outreach assistant**! This tool helps you craft personalized cold messages for LinkedIn leads using AI. Simply input a LinkedIn URL, your outreach goal, and any specific instructions or example messages, and the tool will generate tailored cold outreach options. Perfect for recruiters, B2B sales teams, startup founders, and any other cold outreacher! 🎯

## 💡 How it Works
1. Provide a LinkedIn URL for the lead.
2. Input your outreach goal and instructions.
3. Add example messages for reference.
4. AI processes it all and gives you message options!

### 🔧 Tech Stack
- **Streamlit** for the web interface
- **OpenAI API** for message generation
- **Proxycurl** for LinkedIn data parsing
- **Docker** for containerization
- **AWS** for deployment

## 🚀 Quickstart Guide

### 1. Clone the repository:
```console
git clone https://github.com/melnikoff-oleg/AI-cold-outreach.git 
cd AI-cold-outreach
```

### 2. Add environment variables:
You'll need tokens for OpenAI and Proxycurl (paid, from [Proxycurl](https://nubela.co/proxycurl/)).
```console
export OPENAI_TOKEN=your_openai_token
export PROXYCURL_TOKEN=your_proxycurl_token
```

### 3. Install dependencies:
Create a virtual environment and install required packages:
```console
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Deploy the App:
Without Docker:
```console
streamlit run app.py --server.port=8501 --client.showErrorDetails=false
```
With Docker:
```console
docker build -t my-python-app .
docker run \
  --env-file .env \
  -p 8501:8501 \
  -v $(pwd)/api_cache:/app/api_cache \
  -v $(pwd)/user_data:/app/user_data \
  my-python-app
```

## 🗂️ File Structure
- Dockerfile: Docker setup
- app.py: Main application script
- api_cache/ & user_data/: Caching and data storage for efficiency
- cold_outreach_lection.txt: Instructions for cold outreach
- prompts.txt: AI prompts used by the app
- playbook.ipynb: Jupyter Notebook playbook
- requirements.txt: Python dependencies

## 🧑‍🏫 Templates for Outreach
We’ve included templates for:
- Recruiters: To reach out to potential job candidates.
- B2B Sales: To contact potential clients.
- Startup Founders: For customer development outreach.