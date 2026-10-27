import os
import requests
import streamlit as st

st.set_page_config(page_title="KaziAI | CV & Job Letter Builder", page_icon="💼", layout="centered")

st.markdown("""
<style>
  .stApp { background: #f6f8fc; }
  .hero { padding: 1.2rem; border-radius: 18px; background: linear-gradient(135deg,#102a56,#2563eb); color: white; }
  .hero h1 { color: white; margin-bottom: .25rem; }
  .small { opacity: .9; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>💼 KaziAI</h1>
  <div>Make your next application stronger.</div>
  <p class="small">Create a professional CV or job application letter in minutes.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
mode = st.radio("What would you like to create?", ["CV / Resume", "Job application letter"], horizontal=False)

with st.form("application_form"):
    name = st.text_input("Your full name", placeholder="e.g. Amina Wanjiku")
    contact = st.text_input("Phone or email (optional)", placeholder="e.g. 07xx xxx xxx")
    location = st.text_input("Town / County (optional)", placeholder="e.g. Nairobi")
    role = st.text_input("Job you want", placeholder="e.g. Shop assistant")
    education = st.text_area("Education", placeholder="School, qualification, and year")
    skills = st.text_area("Skills", placeholder="e.g. customer service, teamwork, computer skills")
    experience = st.text_area("Work experience (if any)", placeholder="Include jobs, attachments, volunteering, or practical experience. If none, write 'No formal experience yet'.")
    job_ad = st.text_area("Job advert or extra details (optional)", placeholder="Paste the job advert here to tailor the application.")
    language = st.selectbox("Output language", ["English", "Kiswahili"])
    submitted = st.form_submit_button("✨ Create my document", use_container_width=True)

def demo_document():
    safe_name = name.strip() or "[Your Full Name]"
    safe_role = role.strip() or "[Job Title]"
    safe_education = education.strip() or "Add your education details here."
    safe_skills = skills.strip() or "Communication, teamwork, reliability, willingness to learn"
    safe_experience = experience.strip() or "Add relevant work, volunteering, attachment, or practical experience here."
    if language == "Kiswahili":
        if mode == "CV / Resume":
            return f"""{safe_name}
{contact}
{location}

WASIFU WA KITAALAMU
Mtu mwenye bidii, mwaminifu na aliye tayari kujifunza na kuchangia katika nafasi ya {safe_role}. Ninalenga kutumia ujuzi wangu, kushirikiana na wengine na kutoa huduma bora.

ELIMU
{safe_education}

UJUZI
{safe_skills}

UZOEFU
{safe_experience}

MAREJELEO
Yatatolewa yakihitajika."""
        return f"""Kwa: Meneja wa Ajira

YAH: MAOMBI YA KAZI YA {safe_role.upper()}

Ninaandika kuomba nafasi ya {safe_role}. Nina bidii, ninawajibika na niko tayari kujifunza na kutekeleza majukumu nitakayokabidhiwa.

Elimu yangu: {safe_education}
Ujuzi wangu: {safe_skills}
Uzoefu wangu: {safe_experience}

Ningefurahi kupata nafasi ya kueleza zaidi jinsi ninavyoweza kuchangia katika timu yenu. Asanteni kwa kuzingatia ombi langu.

Wako mwaminifu,
{safe_name}
{contact}"""
    if mode == "CV / Resume":
        return f"""{safe_name}
{contact}
{location}

PROFESSIONAL PROFILE
Motivated and dependable candidate seeking a {safe_role} position. Ready to learn, work collaboratively, and contribute positively to the organisation.

EDUCATION
{safe_education}

KEY SKILLS
{safe_skills}

WORK EXPERIENCE
{safe_experience}

REFERENCES
Available upon request."""
    return f"""Dear Hiring Manager,

RE: APPLICATION FOR THE POSITION OF {safe_role.upper()}

I am writing to apply for the {safe_role} position. I am a motivated, responsible, and willing-to-learn candidate who is ready to contribute to your team.

My education: {safe_education}

Relevant skills: {safe_skills}

Experience: {safe_experience}

I would welcome the opportunity to discuss how my skills and commitment can contribute to your organisation. Thank you for considering my application.

Yours faithfully,
{safe_name}
{contact}"""

def gemini_document(prompt):
    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        pass
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, "Demo mode"
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    try:
        response = requests.post(
            url,
            params={"key": api_key},
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"temperature": 0.6, "maxOutputTokens": 1800}},
            timeout=45
        )
        response.raise_for_status()
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return text, "Gemini AI"
    except Exception as exc:
        return None, f"AI request failed: {exc}"

if submitted:
    if not name.strip() or not role.strip():
        st.error("Please enter at least your name and the job you want.")
    else:
        prompt = f"""
You are KaziAI, a careful career-document assistant helping job seekers.
Write a polished, realistic {mode} in {language} for a job seeker in Kenya.
Use only facts provided below. Never invent qualifications, employers, dates, achievements, certificates, or references.
If details are missing, use a clear placeholder or omit that section. Keep the tone professional and the result easy to copy.
Name: {name}
Contact: {contact}
Location: {location}
Target role: {role}
Education: {education}
Skills: {skills}
Experience: {experience}
Job advert / extra details: {job_ad}
"""
        with st.spinner("Preparing your document..."):
            generated, source = gemini_document(prompt)
        if generated:
            result = generated
            st.success(f"Created with {source}. Please review all details before sending.")
        else:
            result = demo_document()
            st.info("Created in starter demo mode. Add a Gemini API key to enable real AI rewriting.")
        st.subheader("Your document")
        st.text_area("Review and edit your document", value=result, height=420, key="result")
        st.download_button("⬇️ Download as text file", data=result, file_name="kaziai_document.txt", mime="text/plain", use_container_width=True)
        st.caption("Privacy tip: avoid entering national ID numbers or other sensitive information. Always verify that the document is accurate.")

st.divider()
st.caption("KaziAI Starter MVP • Free prototype • Not affiliated with any employer or government agency")
