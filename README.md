# KaziAI Starter MVP

A mobile-friendly Streamlit app for creating CVs and job application letters.

## Run on Streamlit Community Cloud
1. Create a GitHub repository and upload `app.py` and `requirements.txt`.
2. On Streamlit Community Cloud, create an app pointing to `app.py`.
3. To enable real Gemini AI, create a Gemini API key in Google AI Studio.
4. In Streamlit app settings, open **Secrets** and add:
   `GEMINI_API_KEY = "paste-your-key-here"`
5. Save and reboot the app.

Without a key, the app still runs in demo mode with starter templates.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Keep API keys in Streamlit Secrets or environment variables. Never paste them into public source code or share them in screenshots.
