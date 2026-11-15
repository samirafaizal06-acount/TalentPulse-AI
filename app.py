import os
import re
import json
import uuid
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pypdf import PdfReader

# Optional MongoDB & Gemini imports with graceful fallback
try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TalentPulse AI | Intelligent Resume Screener & Interview Coach",
    page_icon="🎯",
    layout="wide"
)
st.markdown(
    "<div style='background:#0F294A; color:#D4AF37; padding:8px 14px; border-radius:8px; "
    "border-left:4px solid #D4AF37; font-weight:600; margin-bottom:14px;'>"
    "🎓 Developed by: Samira Faizal | BCA Final Year Major Project</div>",
    unsafe_allow_html=True
)
# Custom Royal Navy & Gold Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #050e21 0%, #0b1d3f 60%, #102a5c 100%);
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #ffd966 !important;
        font-family: 'Georgia', serif;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #d4af37;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .badge-match {
        background-color: #14532d;
        color: #86efac;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        margin: 3px;
        display: inline-block;
    }
    .badge-miss {
        background-color: #7f1d1d;
        color: #fca5a5;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        margin: 3px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SAMPLE DATA ----------------
SAMPLE_JOBS = {
    "Full-Stack AI Developer (Entry Level)": {
        "department": "Engineering",
        "skills": ["Python", "Node.js", "MongoDB", "REST API", "Generative AI", "Prompt Engineering", "Git", "SQL", "JavaScript"],
        "description": "Looking for a BCA/B.Tech graduate skilled in Python, Node.js, MongoDB CRUD operations, REST APIs, and Generative AI / Vertex AI prompt design to build intelligent web applications."
    },
    "Data & Business Intelligence Analyst": {
        "department": "Analytics",
        "skills": ["Python", "Pandas", "SQL", "MongoDB", "Data Visualization", "Excel", "Statistics", "Power BI", "ETL"],
        "description": "Seeking an analyst proficient in Python, Pandas, SQL, MongoDB aggregation, data cleaning, and interactive dashboard reporting."
    },
    "Cloud & Backend Associate": {
        "department": "Cloud Infrastructure",
        "skills": ["Node.js", "MongoDB", "Google Cloud", "Docker", "Linux", "API Security", "Python", "Git"],
        "description": "Entry-level backend engineer to build scalable NoSQL databases in MongoDB, Node.js microservices, and Google Cloud AI integrations."
    }
}

SAMPLE_RESUMES = {
    "Samira I (BCA Final Year - Strong Match)": """SAMIRA I
BCA Final Year Student | Chennai, India
Skills: Python, Node.js, MongoDB, CRUD Operations, Google Cloud, Generative AI, Prompt Engineering, Vertex AI, Git, HTML, CSS, JavaScript
Certifications:
- MongoDB CRUD Operations in Node.js (SmartBridge & MongoDB)
- MongoDB Basics for Students
- Prompt Design in Vertex AI (Google Cloud Skill Badge)
- Google Cloud Generative AI Foundations Workshop
Projects:
- Built NoSQL backend APIs with MongoDB CRUD operations and Node.js.
- Designed structured LLM prompts in Google Cloud Vertex AI for automated text classification.""",
    "Arjun K (Data Focus - Moderate Match)": """ARJUN K
B.Sc Computer Science | Bengaluru
Skills: Python, Pandas, SQL, Excel, Data Visualization, Power BI, Git
Projects:
- Retail sales dashboard using Python and Power BI.
- Relational database schema design in MySQL."""
}

# ---------------- DATABASE LAYER (MONGODB + FALLBACK) ----------------
DATA_FILE = "talentpulse_records.json"

def get_db_collection(mongo_uri: str):
    if mongo_uri and PYMONGO_AVAILABLE:
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            client.admin.command("ping")
            db = client["talentpulse_ai"]
            return db["evaluations"], "MongoDB Atlas (Live Cloud)"
        except Exception:
            pass
    return None, "Local Document Store (MongoDB Schema Compatible)"

def load_records(mongo_uri: str):
    col, mode = get_db_collection(mongo_uri)
    if col is not None:
        docs = list(col.find({}, {"_id": 0}))
        return docs, mode
    if not os.path.exists(DATA_FILE):
        seed = [{
            "record_id": "TP-1001",
            "candidate_name": "Samira I",
            "target_role": "Full-Stack AI Developer (Entry Level)",
            "ats_score": 89,
            "status": "Shortlisted",
            "matched_skills": ["Python", "Node.js", "MongoDB", "Generative AI", "Prompt Engineering", "Git", "JavaScript"],
            "missing_skills": ["REST API", "SQL"],
            "timestamp": "2026-11-14 10:30"
        }]
        with open(DATA_FILE, "w") as f:
            json.dump(seed, f, indent=2)
    with open(DATA_FILE, "r") as f:
        return json.load(f), mode

def save_record(record: dict, mongo_uri: str):
    col, _ = get_db_collection(mongo_uri)
    if col is not None:
        col.insert_one(record.copy())
        return
    records, _ = load_records("")
    records.insert(0, record)
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=2)

def update_record_status(record_id: str, new_status: str, mongo_uri: str):
    col, _ = get_db_collection(mongo_uri)
    if col is not None:
        col.update_one({"record_id": record_id}, {"$set": {"status": new_status}})
        return
    records, _ = load_records("")
    for r in records:
        if r["record_id"] == record_id:
            r["status"] = new_status
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=2)

def delete_record(record_id: str, mongo_uri: str):
    col, _ = get_db_collection(mongo_uri)
    if col is not None:
        col.delete_one({"record_id": record_id})
        return
    records, _ = load_records("")
    records = [r for r in records if r["record_id"] != record_id]
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=2)

# ---------------- AI / VERTEX PROMPT ENGINE ----------------
def analyze_resume(resume_text: str, role_title: str, job_info: dict, gemini_key: str):
    req_skills = job_info["skills"]
    resume_lower = resume_text.lower()
    matched = [s for s in req_skills if s.lower() in resume_lower]
    missing = [s for s in req_skills if s.lower() not in resume_lower]
    base_score = int((len(matched) / max(len(req_skills), 1)) * 100)

    # Default structured response (works offline/without API key)
    result = {
        "ats_score": min(98, max(25, base_score + (8 if "project" in resume_lower else 0))),
        "matched_skills": matched,
        "missing_skills": missing,
        "summary": f"Candidate matches {len(matched)} of {len(req_skills)} core skills required for {role_title}. Strong alignment in {', '.join(matched[:3]) if matched else 'foundational skills'}.",
        "improvements": [
            f"Add hands-on project bullet points demonstrating {', '.join(missing[:2])}." if missing else "Quantify project impact with latency or accuracy metrics.",
            "Include GitHub repository links and live deployment URLs for each technical project.",
            "Highlight MongoDB schema design and prompt engineering workflows clearly."
        ],
        "interview_questions": [
            f"Explain how you implemented CRUD operations and indexing in MongoDB for {role_title}.",
            "How do you design system prompts and few-shot examples in Vertex AI to reduce LLM hallucinations?",
            f"Walk through a real bug you solved while working with {matched[0] if matched else 'Python'}."
        ],
        "engine": "Built-in Structured ATS Engine"
    }

    # Live Gemini / Vertex AI Prompt Design Mode if API key is provided
    if gemini_key and GENAI_AVAILABLE:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            You are an expert Technical Recruiter & Vertex AI Prompt Engineer.
            Analyze the following Resume against the Target Job Role and return ONLY valid JSON with keys:
            "ats_score" (int 0-100), "summary" (string), "improvements" (list of 3 strings), "interview_questions" (list of 3 technical questions).

            Target Role: {role_title}
            Job Description: {job_info['description']}
            Required Skills: {', '.join(req_skills)}

            Resume Text:
            {resume_text}
            """
            response = model.generate_content(prompt)
            clean_json = re.sub(r"```json|```", "", response.text).strip()
            ai_data = json.loads(clean_json)
            result["ats_score"] = int(ai_data.get("ats_score", result["ats_score"]))
            result["summary"] = ai_data.get("summary", result["summary"])
            result["improvements"] = ai_data.get("improvements", result["improvements"])
            result["interview_questions"] = ai_data.get("interview_questions", result["interview_questions"])
            result["engine"] = "Google Generative AI / Vertex Prompt Engine"
        except Exception:
            pass

    return result

# ---------------- SIDEBAR CONFIG ----------------
with st.sidebar:
    st.markdown("## 🎯 TalentPulse AI")
    st.caption("Developed by **Samira I** | BCA Final Year Major Project")
    st.divider()
    st.markdown("### ⚙️ Cloud & AI Connectors")
    mongo_uri = st.text_input("MongoDB Atlas URI (Optional)", type="password", placeholder="mongodb+srv://...")
    gemini_key = st.text_input("Google AI / Gemini API Key (Optional)", type="password", placeholder="AIza...")
    records, active_db_mode = load_records(mongo_uri)
    st.success(f"**DB Active:** {active_db_mode}")
    st.info("**Tech Stack:** MongoDB CRUD • Python • Streamlit • Vertex AI Prompt Design")

# ---------------- MAIN HEADER ----------------
st.title("🎯 TalentPulse AI — Smart Resume Screener & Interview Coach")
st.markdown("**AI-Powered ATS Screening, Skill-Gap Diagnostics & MongoDB Candidate Management System**")

tab1, tab2, tab3 = st.tabs(["🚀 AI Resume Analyzer", "🗄️ MongoDB Candidate CRUD", "📊 Recruitment Analytics"])

# ---------------- TAB 1: ANALYZER ----------------
with tab1:
    col1, col2 = st.columns([1.1, 1])
    with col1:
        st.subheader("1. Candidate & Job Input")
        cand_name = st.text_input("Candidate Name", value="Samira I")
        selected_role = st.selectbox("Select Target Job Role", list(SAMPLE_JOBS.keys()))
        job_info = SAMPLE_JOBS[selected_role]
        st.caption(f"**Role Requirements:** {', '.join(job_info['skills'])}")

        input_mode = st.radio("Resume Input Mode", ["Select Sample Resume", "Paste Resume Text", "Upload PDF Resume"], horizontal=True)
        resume_text = ""
        if input_mode == "Select Sample Resume":
            sample_choice = st.selectbox("Choose Sample Profile", list(SAMPLE_RESUMES.keys()))
            resume_text = st.text_area("Resume Content", value=SAMPLE_RESUMES[sample_choice], height=210)
        elif input_mode == "Paste Resume Text":
            resume_text = st.text_area("Paste Full Resume Here", height=210, placeholder="Paste skills, education, projects...")
        else:
            uploaded_pdf = st.file_uploader("Upload Candidate PDF", type=["pdf"])
            if uploaded_pdf:
                reader = PdfReader(uploaded_pdf)
                resume_text = "\n".join([page.extract_text() or "" for page in reader.pages])
                st.text_area("Extracted PDF Text", value=resume_text, height=160)

        analyze_btn = st.button("✨ Run AI Screening & Save to MongoDB", type="primary", use_container_width=True)

    with col2:
        st.subheader("2. AI Evaluation & Interview Prep")
        if analyze_btn and resume_text.strip():
            analysis = analyze_resume(resume_text, selected_role, job_info, gemini_key)
            rec_id = f"TP-{str(uuid.uuid4())[:4].upper()}"
            status = "Shortlisted" if analysis["ats_score"] >= 70 else "Needs Upskilling"

            new_doc = {
                "record_id": rec_id,
                "candidate_name": cand_name or "Candidate",
                "target_role": selected_role,
                "ats_score": analysis["ats_score"],
                "status": status,
                "matched_skills": analysis["matched_skills"],
                "missing_skills": analysis["missing_skills"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            save_record(new_doc, mongo_uri)

            # Gauge Chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=analysis["ats_score"],
                title={"text": f"ATS Match Score ({status})", "font": {"color": "#ffd966", "size": 18}},
                number={"suffix": "%", "font": {"color": "#ffffff"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#ffd966"},
                    "bar": {"color": "#d4af37"},
                    "bgcolor": "#0b1d3f",
                    "steps": [
                        {"range": [0, 50], "color": "#450a0a"},
                        {"range": [50, 75], "color": "#713f12"},
                        {"range": [75, 100], "color": "#14532d"}
                    ]
                }
            ))
            fig_gauge.update_layout(height=230, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown(f"**AI Executive Summary:** {analysis['summary']}")
            st.markdown("**Matched Skills:** " + "".join([f"<span class='badge-match'>{s}</span>" for s in analysis["matched_skills"]]), unsafe_allow_html=True)
            st.markdown("**Skill Gaps:** " + ("".join([f"<span class='badge-miss'>{s}</span>" for s in analysis["missing_skills"]]) if analysis["missing_skills"] else "None!"), unsafe_allow_html=True)

            with st.expander("💡 Resume Optimization Tips & Mock Interview Questions", expanded=True):
                st.markdown("**Resume Improvements:**")
                for tip in analysis["improvements"]:
                    st.markdown(f"- {tip}")
                st.markdown("**Generated Technical Interview Questions:**")
                for idx, q in enumerate(analysis["interview_questions"], 1):
                    st.markdown(f"{idx}. {q}")
            st.toast(f"Saved {cand_name} ({rec_id}) to Database!", icon="✅")
        else:
            st.info("Click **Run AI Screening & Save to MongoDB** to evaluate a candidate and store the record.")

# ---------------- TAB 2: MONGODB CRUD ----------------
with tab2:
    st.subheader("🗄️ MongoDB Candidate Records (Create • Read • Update • Delete)")
    records, _ = load_records(mongo_uri)
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df[["record_id", "candidate_name", "target_role", "ats_score", "status", "timestamp"]], use_container_width=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            selected_id = st.selectbox("Select Record ID", df["record_id"].tolist())
        with c2:
            new_stat = st.selectbox("Update Hiring Status", ["Shortlisted", "Interview Scheduled", "Selected", "Needs Upskilling", "Rejected"])
            if st.button("🔄 Update Status (UPDATE)", use_container_width=True):
                update_record_status(selected_id, new_stat, mongo_uri)
                st.success(f"Updated {selected_id} to {new_stat}")
                st.rerun()
        with c3:
            st.write("")
            st.write("")
            if st.button("🗑️ Delete Record (DELETE)", use_container_width=True):
                delete_record(selected_id, mongo_uri)
                st.warning(f"Deleted record {selected_id}")
                st.rerun()
    else:
        st.info("No candidate records found yet.")

# ---------------- TAB 3: ANALYTICS ----------------
with tab3:
    st.subheader("📊 Talent Pipeline & Skill-Gap Analytics")
    records, _ = load_records(mongo_uri)
    if records:
        df = pd.DataFrame(records)
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Screened Candidates", len(df))
        m2.metric("Average ATS Score", f"{df['ats_score'].mean():.1f}%")
        m3.metric("Shortlisted Rate", f"{(df['status'].isin(['Shortlisted', 'Interview Scheduled', 'Selected']).mean()*100):.0f}%")

        ch1, ch2 = st.columns(2)
        with ch1:
            fig_bar = px.bar(df, x="candidate_name", y="ats_score", color="status",
                             title="ATS Match Score by Candidate",
                             color_discrete_sequence=["#d4af37", "#38bdf8", "#4ade80", "#f87171"])
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#ffffff")
            st.plotly_chart(fig_bar, use_container_width=True)
        with ch2:
            fig_pie = px.pie(df, names="status", title="Candidate Pipeline Distribution",
                             color_discrete_sequence=["#d4af37", "#2563eb", "#16a34a", "#dc2626"])
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#ffffff")
            st.plotly_chart(fig_pie, use_container_width=True)
