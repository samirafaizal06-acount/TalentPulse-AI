import streamlit as st
import PyPDF2
import os

# --- 1. PAGE CONFIG & GOOGLE SEO ---
st.set_page_config(
    page_title="TalentPulse AI | Global Career, Internship, HR & Executive Intelligence Hub by Samira",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "TalentPulse AI — Universal Resume, Internship, HR Screening & CEO Leadership Intelligence Hub. Designed & Developed by Samira (BCA)."
    }
)

st.markdown(
    """
    <meta name="description" content="TalentPulse AI by Samira (BCA) — World-Wide AI Resume & Internship Analyzer, HR Candidate Screener & CEO Executive Leadership Hub covering 35+ Global Sectors." />
    <meta name="keywords" content="TalentPulse AI, Samira BCA, Resume Matcher, Internship Resume Checker, AI Cyber Cloud Data Science Resume, CA Resume, Medical Law Engineering Arts Resume, HR Screener, CEO Executive Bio" />
    """,
    unsafe_allow_html=True
)

# --- 2. DEEP SEA OCEAN GREEN THEME & ROMAN TYPOGRAPHY ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Lora', 'Times New Roman', Georgia, serif;
        background-color: #031B1E;
        color: #E6F4F1;
    }

    h1, h2, h3, .main-title {
        font-family: 'Cinzel', 'Times New Roman', serif !important;
        color: #4FD1C5 !important;
        letter-spacing: 0.8px;
    }

    .stApp {
        background: linear-gradient(160deg, #021417 0%, #062C30 55%, #041F23 100%);
    }

    .hero-banner {
        background: rgba(13, 68, 74, 0.55);
        border: 1px solid #2C7A7B;
        border-left: 6px solid #38B2AC;
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 18px;
    }

    .trust-badge {
        background: rgba(44, 122, 123, 0.25);
        border: 1px solid #38B2AC;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 0.9rem;
        color: #B2F5EA;
        margin-bottom: 14px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #0D9488 0%, #115E59 100%);
        color: #FFFFFF !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700;
        border: 1px solid #5EEAD4;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        transition: all 0.25s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #14B8A6 0%, #0F766E 100%);
        border-color: #CCFBF1;
        transform: translateY(-1px);
    }

    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #072A2E !important;
        color: #E6F4F1 !important;
        border: 1px solid #2C7A7B !important;
    }

    .footer-credit {
        text-align: center;
        padding: 18px;
        margin-top: 30px;
        border-top: 1px solid #2C7A7B;
        background: rgba(2, 20, 23, 0.7);
        border-radius: 10px;
        color: #99F6E4;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. GEMINI AI CLIENT SETUP ---
def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return os.environ.get("GEMINI_API_KEY", "")

def generate_ai_response(prompt_text, user_api_key=""):
    api_key = user_api_key.strip() if user_api_key.strip() else get_api_key()
    if not api_key:
        return "⚠️ **API Key Missing:** Please add `GEMINI_API_KEY` in Streamlit Secrets or enter it in the sidebar."

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text
        )
        return response.text
    except Exception:
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key)
            model = genai_legacy.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt_text)
            return response.text
        except Exception as e:
            return f"❌ **AI Engine Error:** {str(e)}"

# --- 4. PDF TEXT EXTRACTION ---
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    extracted = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted += page_text + "\n"
    return extracted.strip()

# --- 5. COMPLETE 35+ WORLD-WIDE SECTORS, INTERNSHIPS & PROFESSIONS DATABASE ---
UNIVERSAL_JOB_ROLES = {
    "✍️ Custom Job / Internship Description (Paste Any JD)": {
        "Paste Your Own Job or Internship Description": ""
    },

    # 1. STUDENT INTERNSHIPS & INDUSTRIAL TRAINING (ALL STREAMS)
    "🚀 Student Internships & Industrial Training (All Streams)": {
        "AI / Machine Learning / Python Intern": "Seeking a college student intern with Python basics, Pandas, Generative AI / API handling, mini-projects, and strong analytical problem-solving attitude.",
        "Data Analytics & Business Intelligence Intern": "Looking for a student intern skilled in MS Excel, SQL basics, Python/R, Power BI or Tableau dashboards, and data cleaning.",
        "Cybersecurity & Cloud Operations Intern": "Seeking an intern with networking fundamentals (TCP/IP), Linux command-line basics, OWASP awareness, cloud sandbox exposure, and documentation skills.",
        "Full-Stack Web / App Development Intern": "Looking for a student intern familiar with HTML5, CSS3, JavaScript, React or Python (Streamlit/Flask), and GitHub project hosting.",
        "HR, Digital Marketing & Management Intern (BBA / MBA / Arts)": "Looking for an enthusiastic student intern for social media content, recruitment coordination, market research, Canva design, and Excel tracking.",
        "Finance, Accounting & CA Articleship Intern (B.Com / CA / M.Com)": "Seeking a commerce/CA student intern with Tally Prime, MS Excel, GST documentation basics, vouching, and strong numerical accuracy.",
        "R&D / Lab / Clinical / Legal Research Intern (Science / Medical / Law)": "Looking for a dedicated student intern with strong subject fundamentals, lab/legal/clinical documentation skills, and analytical reporting."
    },

    # 2. ARTIFICIAL INTELLIGENCE, ML & DATA SCIENCE (B.Sc AI / DS)
    "🤖 Artificial Intelligence, Machine Learning & Data Science (B.Sc AI / DS)": {
        "AI / Generative AI & LLM Engineer": "Seeking an AI graduate skilled in Python, Generative AI, Prompt Engineering, LangChain/RAG pipelines, Hugging Face, NLP, and LLM API integrations.",
        "Machine Learning & Deep Learning Engineer": "Looking for an ML Engineer proficient in Scikit-Learn, TensorFlow/PyTorch, neural networks, computer vision (OpenCV), model evaluation, and deployment.",
        "Data Scientist & Predictive Modeler": "Seeking a Data Science graduate skilled in Python (Pandas, NumPy), R, statistical modeling, feature engineering, A/B testing, and SQL.",
        "Data Analyst & BI Visualization Specialist": "Looking for a Data Analyst proficient in SQL, Advanced Excel, Power BI, Tableau, data cleaning, dashboard storytelling, and KPI reporting."
    },

    # 3. CYBERSECURITY & ETHICAL HACKING (B.Sc Cyber Security)
    "🛡️ Cybersecurity, Ethical Hacking & Digital Forensics": {
        "SOC Analyst (Security Operations Center)": "Seeking a Cybersecurity graduate skilled in SIEM monitoring (Splunk/QRadar), incident response, threat intelligence, log analysis, and firewall rules.",
        "Penetration Tester / Ethical Hacker (VAPT)": "Looking for an Ethical Hacker proficient in Kali Linux, Metasploit, Burp Suite, Nmap, OWASP Top 10 web vulnerabilities, and VAPT reporting.",
        "Digital Forensics & Network Security Engineer": "Seeking a security specialist with knowledge of TCP/IP, Wireshark packet analysis, cryptography, ISO 27001, and endpoint security."
    },

    # 4. CLOUD COMPUTING & DEVOPS
    "☁️ Cloud Computing, DevOps & Site Reliability": {
        "Cloud Solutions Associate (AWS / Azure / GCP)": "Seeking a Cloud graduate skilled in AWS (EC2, S3, IAM, Lambda) or Azure fundamentals, virtual networking (VPC), cloud security, and cost optimization.",
        "DevOps & CI/CD Automation Engineer": "Looking for a DevOps engineer familiar with Linux administration, Git/GitHub Actions, Docker containers, Kubernetes basics, and Terraform.",
        "Cloud Support & Systems Administrator": "Seeking an IT/Cloud graduate skilled in Windows/Linux servers, shell scripting, backup & disaster recovery, and cloud monitoring."
    },

    # 5. BCA / COMPUTER SCIENCE / SOFTWARE ENGINEERING
    "💻 BCA / B.Sc CS / Software Engineering": {
        "Software Developer (Fresher)": "Looking for a BCA / B.Sc CS fresher with strong fundamentals in Python, Java, or C++, OOPs, Data Structures, SQL, Git, and problem-solving skills.",
        "Full-Stack Web Developer": "Seeking a Web Developer skilled in HTML5, CSS3, JavaScript, React.js, Node.js, REST APIs, and MySQL/MongoDB.",
        "Mobile App Developer (Flutter / Android)": "Looking for an app developer skilled in Flutter/Dart or Kotlin/Java, Firebase integration, REST APIs, and responsive UI design.",
        "Software Tester / QA Automation Engineer": "Seeking a QA Engineer with knowledge of Manual Testing, SDLC/STLC, test case design, Jira, and Selenium automation."
    },

    # 6. GLOBAL C-SUITE & EXECUTIVE LEADERSHIP
    "👔 C-Suite, CEO & Global Executive Leadership": {
        "Chief Executive Officer (CEO) / Managing Director": "Seeking a visionary CEO / Managing Director with proven P&L ownership, corporate strategy, global market expansion, board governance, M&A leadership, fundraising, and organizational transformation experience.",
        "Chief Technology Officer (CTO) / VP Engineering": "Looking for a strategic CTO skilled in enterprise architecture, AI/Cloud transformation, engineering team scaling, product roadmap execution, cybersecurity governance, and R&D innovation.",
        "Chief Financial Officer (CFO)": "Seeking a seasoned CFO experienced in corporate finance, capital allocation, IPO/fundraising readiness, risk management, investor relations, global compliance, and financial forecasting.",
        "Chief Operating Officer (COO) / Startup Founder": "Looking for an execution-driven COO / Founder skilled in scaling global operations, supply chain optimization, cross-functional leadership, unit economics, and strategic partnerships."
    },

    # 7. CHARTERED ACCOUNTANT (CA / CS / CMA)
    "🧾 Chartered Accountant, Audit & Corporate Governance (CA / CS / CMA)": {
        "Chartered Accountant (CA) — Statutory Audit & Assurance": "Seeking a qualified Chartered Accountant (ICAI) skilled in statutory audit, Ind AS / IFRS compliance, internal financial controls (IFC), tax audit, financial statement finalization, and risk advisory.",
        "CA Articleship Trainee (IPCC / Inter Qualified)": "Looking for a CA Intermediate (Group 1 / Both Groups) student for Articleship training in statutory audit, GST compliance, income tax filings, vouching, and Tally/SAP accounting.",
        "Direct & Indirect Taxation Specialist (GST / Corporate Tax)": "Seeking a CA / tax consultant experienced in corporate tax planning, GST returns & litigation, TDS compliance, transfer pricing, and assessment representation.",
        "Company Secretary (CS) & Corporate Compliance Officer": "Looking for a qualified Company Secretary (ICSI) skilled in Companies Act 2013 compliance, SEBI regulations, ROC filings, board meeting governance, and secretarial audit.",
        "Cost & Management Accountant (CMA)": "Seeking a CMA (ICMAI) skilled in cost accounting, budgeting, variance analysis, inventory valuation, ERP costing modules, and management reporting."
    },

    # 8. FACULTY, TEACHERS & ACADEMIC LEADERSHIP
    "👩‍🏫 Faculty, Teachers & Academic Leadership": {
        "Assistant Professor (Arts, Science & Commerce)": "Seeking an Assistant Professor with a Postgraduate degree (55%+), UGC NET/SET qualification or Ph.D., strong subject expertise, research paper publications (Scopus/UGC Care), curriculum delivery, and student mentoring skills.",
        "Professor / Head of Department (HOD)": "Looking for an experienced Professor / HOD with a Ph.D., 10+ years of teaching and research experience, academic administration, NAAC/NIRF documentation, Ph.D. scholar guidance, and funded research projects.",
        "School Teacher (PGT / TGT / Montessori)": "Seeking a passionate B.Ed. / M.Ed. qualified teacher skilled in interactive lesson planning, NEP 2020 pedagogy, classroom management, student assessment, and parent communication.",
        "Lab Instructor / Technical Demonstrator": "Seeking a Lab Instructor skilled in handling laboratory equipment, experiment setup, student lab guidance, safety compliance, and stock register maintenance.",
        "Placement Officer / Career Counselor": "Looking for a Training & Placement Officer skilled in corporate tie-ups, campus recruitment drives, aptitude & soft-skills training coordination, and student career counseling."
    },

    # 9. RESEARCH & DOCTORAL (Ph.D. / M.Phil)
    "🔬 Ph.D. / M.Phil Scholars & Researchers": {
        "Post-Doctoral Research Fellow": "Seeking a Ph.D. holder with strong research methodology, peer-reviewed publications (Scopus/SCI), grant proposal writing, data analysis, and independent lab/field research leadership.",
        "Research Associate / Project Fellow (UGC / DST / CSIR)": "Looking for an M.Phil / Ph.D. scholar skilled in literature review, qualitative/quantitative research tools (SPSS, R, Python), thesis drafting, and research documentation.",
        "Academic Journal Reviewer / Research Consultant": "Seeking a doctoral researcher with expertise in manuscript evaluation, research ethics, statistical validation, and academic publishing standards."
    },

    # 10. MEDICAL, HEALTHCARE & PHARMACY
    "🩺 Doctors, Medical, Nursing & Pharmacy (MBBS / BDS / B.Pharm)": {
        "Junior Resident Doctor / Duty Medical Officer (DMO)": "Seeking an MBBS graduate registered with the Medical Council, skilled in patient diagnosis, emergency care, OP/IP management, clinical documentation, and medical ethics.",
        "Dental Surgeon (BDS / MDS)": "Looking for a Dental Surgeon skilled in general dentistry, root canal treatment, extractions, preventive oral care, patient counseling, and clinical hygiene protocols.",
        "Clinical Pharmacist / Drug Safety Associate (B.Pharm / Pharm.D)": "Seeking a Pharmacy graduate skilled in prescription verification, pharmacovigilance, drug interaction monitoring, inventory management, and regulatory compliance.",
        "Staff Nurse / Healthcare Coordinator (B.Sc Nursing / GNM)": "Looking for a Nursing graduate skilled in patient care, ICU/ward monitoring, medication administration, infection control, and electronic health records."
    },

    # 11. LAW & LEGAL
    "⚖️ Law Students & Legal Professionals (LLB / LLM)": {
        "Junior Advocate / Litigation Associate": "Seeking an LLB graduate enrolled with the Bar Council, skilled in legal drafting (plaints, petitions, affidavits), case research (SCC Online, Manupatra), and court appearances.",
        "Corporate Legal Counsel / Contract Specialist": "Looking for a law graduate skilled in contract drafting, NDA review, corporate compliance, company law, intellectual property (IPR), and due diligence.",
        "Legal Researcher & Paralegal Intern": "Seeking a law student proficient in statutory interpretation, legal notice drafting, case brief preparation, and regulatory research."
    },

    # 12. CIVIL SERVICES, GOVERNMENT & BANKING EXAMS
    "🏛️ Civil Services, Govt & Banking Aspirants (UPSC / TNPSC / IBPS)": {
        "UPSC / TNPSC Group 1 & 2 Administrative Aspirant": "Evaluating profile for public administration, policy analysis, governance, ethics, essay articulation, leadership, and current affairs analytical depth.",
        "Bank Probationary Officer (IBPS / SBI PO)": "Seeking a graduate with strong quantitative aptitude, financial awareness, customer service orientation, credit assessment basics, and digital banking knowledge.",
        "Public Policy & Governance Fellow": "Looking for a candidate skilled in socio-economic data analysis, field research, government scheme evaluation, and stakeholder coordination."
    },

    # 13. ENGINEERING (ECE / EEE / MECH / CIVIL / AUTOMOBILE)
    "⚙️ Engineering Graduates (B.E / B.Tech — All Branches)": {
        "Embedded Systems & IoT Engineer (ECE / EEE)": "Seeking an ECE/EEE graduate skilled in C/C++, microcontrollers (ARM, ESP32, Arduino), PCB design, sensors, and IoT communication protocols.",
        "Mechanical Design & CAD Engineer (Mech)": "Looking for a Mechanical Engineer proficient in AutoCAD, SolidWorks, CATIA, GD&T, thermal/manufacturing processes, and quality control.",
        "Civil Site & Structural Engineer (Civil)": "Seeking a Civil Engineer skilled in AutoCAD, STAAD.Pro, quantity surveying, estimation, site supervision, and concrete quality testing.",
        "EV & Power Systems Engineer (EEE / Auto)": "Looking for an engineer familiar with Electric Vehicle (EV) battery management systems (BMS), motor drives, PLC/SCADA, and renewable power grids."
    },

    # 14. DIPLOMA & POLYTECHNIC
    "🛠️ Diploma & Polytechnic Students": {
        "Junior Engineer / Production Trainee": "Seeking a Diploma holder skilled in shop-floor supervision, machine operation, AutoCAD basics, quality inspection, and industrial safety.",
        "IT & Network Support Technician": "Looking for a Diploma CS/IT graduate skilled in PC hardware troubleshooting, LAN/Wi-Fi networking, OS installation, and technical support.",
        "Automobile Service & Maintenance Technician": "Seeking a Diploma Automobile graduate familiar with vehicle diagnostics, engine servicing, electrical systems, and workshop operations."
    },

    # 15. ARCHITECTURE & INTERIOR DESIGN
    "🏛️ Architecture & Interior Designing (B.Arch / B.Des)": {
        "Junior Architect (B.Arch)": "Seeking an Architecture graduate proficient in AutoCAD, Revit (BIM), SketchUp, Lumion/V-Ray rendering, building codes, and working drawings.",
        "Interior Designer & 3D Visualizer": "Looking for an Interior Designer skilled in space planning, 3ds Max, SketchUp, material selection, lighting design, and client presentations."
    },

    # 16. FASHION DESIGNING & TEXTILES
    "👗 Fashion Designing & Apparel Technology": {
        "Fashion Designer / Apparel Stylist": "Seeking a Fashion Design graduate skilled in garment construction, pattern making, draping, fabric sourcing, trend forecasting, and Adobe Illustrator / CLO 3D.",
        "Fashion Merchandiser & Retail Buyer": "Looking for a fashion graduate skilled in visual merchandising, inventory planning, vendor coordination, costing, and seasonal collection management.",
        "Costume & Bridal Wear Designer": "Seeking a creative designer experienced in embroidery detailing, bridal wear customization, client consultations, and boutique production management."
    },

    # 17. BEAUTICIAN, COSMETOLOGY & WELLNESS
    "💄 Beautician, Cosmetology & Makeup Artistry": {
        "Professional Makeup Artist (Bridal & Editorial)": "Seeking a certified Makeup Artist skilled in HD/Airbrush bridal makeup, skin tone analysis, hairstyling, hygiene standards, and client consultation.",
        "Senior Beautician & Skin Care Specialist": "Looking for a trained beautician proficient in facials, skin treatments, waxing, threading, hair spa, salon hygiene, and customer care.",
        "Cosmetologist & Salon Manager": "Seeking a cosmetology professional skilled in advanced skin/hair therapies, product recommendations, appointment scheduling, and salon operations."
    },

    # 18. AVIATION, HOSPITALITY, CULINARY & TOURISM
    "✈️ Aviation, Hotel Management & Culinary Arts": {
        "Cabin Crew / Ground Staff & Airport Operations": "Seeking a hospitality-focused candidate with exceptional grooming, safety & first-aid awareness, passenger handling, crisis communication, and multilingual fluency.",
        "Hotel Operations & Front Office Executive": "Looking for a Hotel Management graduate skilled in guest relations, reservation systems (Opera PMS), housekeeping standards, and F&B service.",
        "Commis Chef / Culinary Specialist": "Seeking a Culinary graduate skilled in continental/Indian cuisine preparation, food safety (HACCP), kitchen hygiene, menu costing, and plating."
    },

    # 19. MEDIA, CINEMA, JOURNALISM & DESIGN
    "🎬 Visual Communication, Media, Film & Graphic Design": {
        "UI/UX & Brand Graphic Designer": "Seeking a creative designer skilled in Figma, Adobe Photoshop, Illustrator, wireframing, typography, and brand identity.",
        "Video Editor & Motion Graphics Artist": "Looking for a video editor proficient in Premiere Pro, After Effects, DaVinci Resolve, color grading, sound sync, and reels/YouTube storytelling.",
        "Journalist, News Anchor & Content Creator": "Seeking a media graduate skilled in scriptwriting, investigative reporting, on-camera anchoring, interviewing, and digital media production."
    },

    # 20. AGRICULTURE, FOOD TECH & VETERINARY
    "🌱 Agriculture, Food Technology & Veterinary Sciences": {
        "Agronomist / Agribusiness Officer (B.Sc Agri)": "Seeking an Agriculture graduate skilled in crop management, soil health analysis, precision farming, agri-inputs marketing, and farmer advisory.",
        "Food Quality & Safety Officer (B.Tech Food Tech)": "Looking for a Food Technology graduate familiar with FSSAI regulations, HACCP, ISO 22000, quality testing, and food processing operations."
    },

    # 21. SPORTS, PHYSIOTHERAPY & FITNESS
    "🏅 Physiotherapy, Sports Science & Fitness (BPT / B.P.Ed)": {
        "Clinical & Sports Physiotherapist (BPT / MPT)": "Seeking a Physiotherapist skilled in musculoskeletal rehabilitation, ortho/neuro therapy, sports injury recovery, electrotherapy, and patient exercise prescription.",
        "Certified Fitness Coach & Nutrition Advisor": "Looking for a fitness professional skilled in strength & conditioning, functional training, body composition assessment, and personalized diet planning."
    },

    # 22. COMMERCE & MANAGEMENT (BBA / MBA / B.COM / M.COM)
    "💼 Management & Business (BBA / MBA)": {
        "HR Executive / Talent Acquisition": "Seeking a BBA/MBA fresher skilled in recruitment sourcing, resume screening, interview coordination, onboarding, and HRIS.",
        "Business Development & Sales Manager": "Looking for a growth-driven professional with strong B2B/B2C sales, lead generation, client pitching, negotiation, and CRM skills.",
        "Digital Marketing & Growth Strategist": "Seeking a Digital Marketer skilled in SEO, Meta/Google Ads, social media strategy, content funnels, and Google Analytics."
    },

    "📊 Commerce & Finance (B.Com / M.Com)": {
        "Senior Accountant / Tally & GST Executive": "Seeking a B.Com/M.Com graduate skilled in Tally Prime, GST/TDS filing, balance sheet finalization, bank reconciliation, and Advanced Excel.",
        "Financial & Investment Analyst": "Looking for a Finance graduate skilled in financial modeling, equity research, ratio analysis, budgeting, and valuation."
    },

    # 23. ARTS, HUMANITIES & LANGUAGES (BA / MA / TAMIL)
    "📚 Arts & Humanities (BA / MA — English / Econ / History)": {
        "Content Writer, Copywriter & Editor": "Seeking a graduate with strong English proficiency, SEO blog writing, brand copywriting, proofreading, and storytelling skills.",
        "Corporate Communications & PR Specialist": "Looking for a candidate skilled in press releases, internal communications, event management, and public speaking."
    },

    "🌺 BA / MA Tamil (தமிழ் இலக்கியம் & ஊடகம்)": {
        "Tamil Content Writer & Translator": "Seeking a Tamil graduate skilled in English-to-Tamil translation, creative writing, proofreading, and digital content creation.",
        "Tamil Media, News & Script Writer": "Looking for a candidate proficient in Tamil journalism, news reporting, video scriptwriting, anchoring, and subtitling.",
        "Tamil Teacher / Language Trainer": "Looking for a passionate Tamil graduate with strong grammar (Ilakkanam), literature knowledge, and classroom teaching skills."
    },

    # 24. PURE SCIENCES (CHEMISTRY / PHYSICS / MATHS / BIOTECH)
    "🧪 B.Sc / M.Sc Chemistry & Biotechnology": {
        "Quality Control (QC) / Analytical Chemist (HPLC / GC)": "Seeking a Chemistry/Biotech graduate skilled in wet lab analysis, HPLC, UV-Vis Spectrophotometer, GMP/SOP compliance, and lab documentation.",
        "Clinical Research & Pharma Associate": "Looking for a Life Sciences graduate familiar with clinical trials, GCP guidelines, medical terminology, and regulatory documentation."
    },

    "⚛️ B.Sc / M.Sc Physics": {
        "Instrumentation & Lab Calibration Engineer": "Seeking a Physics graduate skilled in electronic lab instruments, oscilloscopes, sensors, calibration, and data logging.",
        "Solar & Renewable Energy Analyst": "Looking for a Physics graduate with knowledge of photovoltaic (PV) systems, energy auditing, and sustainable power testing."
    },

    "📐 B.Sc / M.Sc Mathematics & Statistics": {
        "Data Scientist / Statistical Analyst": "Seeking a Mathematics/Statistics graduate strong in probability, hypothesis testing, regression modeling, SQL, Python/R, and Excel.",
        "Actuarial & Quantitative Risk Analyst": "Looking for a Mathematics graduate with strong quantitative aptitude, financial mathematics, stochastic modeling, and risk forecasting."
    },

    # 25. SOCIAL WORK (MSW)
    "🤝 MSW (Master of Social Work — HR / CSR / Medical)": {
        "HR & Employee Welfare Officer": "Seeking an MSW (HR specialization) graduate skilled in labor laws, employee engagement, grievance handling, and recruitment.",
        "CSR & NGO Project Coordinator": "Looking for an MSW graduate experienced in community development projects, NGO partnerships, impact assessment, and CSR reporting."
    }
}

# --- 6. SIDEBAR SETTINGS ---
with st.sidebar:
    st.markdown("## 🌊 TalentPulse AI")
    st.markdown("**Global Career, Internship, HR & Executive Hub**")
    st.markdown("---")

    output_lang = st.selectbox(
        "🌍 Report Output Language:",
        [
            "English (Global Standard)",
            "Tamil (தமிழ்)",
            "Bilingual (English + தமிழ் Mix)"
        ]
    )

    with st.expander("🔑 Custom API Key (Optional)"):
        custom_api_key = st.text_input("Enter Gemini API Key:", type="password", help="Leave blank to use default server key.")

    st.markdown("---")
    st.markdown(
        """
        **🌐 Global Coverage (35+ Sectors):**
        * Student Internships (All Streams)
        * AI/ML, Data Science, Cyber & Cloud
        * CEOs, Founders & Corporate Boards
        * CA, CS, CMA, Banking & Finance
        * Doctors, Nurses, Dentists & Pharma
        * Lawyers, Judges & Civil Services
        * Teachers, Professors & Ph.D. Scholars
        * Engineers, Diploma, Arch & Agri
        * Fashion, Beauty, Aviation & Culinary
        * Arts, Science, Commerce, Tamil & Sports
        """
    )
    st.markdown("---")
    st.caption("🏛️ **Creator:** Samira (BCA)\nDept. of Computer Applications")

# --- 7. HERO BANNER ---
st.markdown(
    """
    <div class="hero-banner">
        <h1 class="main-title" style="margin-bottom:4px;">🌊 TALENTPULSE AI — GLOBAL EDITION</h1>
        <p style="font-size:1.1rem; color:#B2F5EA; margin-bottom:6px;">
            <b>Universal Resume &amp; Internship Intelligence, HR Screening &amp; Executive Leadership Platform</b>
        </p>
        <p style="font-size:0.92rem; color:#81E6D9; margin-bottom:0;">
            Built for Every Career Stage &amp; Profession: Interns • Freshers • AI/Cyber/Cloud Specialists • CAs • Doctors • Lawyers • Teachers • Ph.D. Scholars • HR Recruiters • Global CEOs
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="trust-badge">🛡️ <b>100% Confidential &amp; Zero-Storage Privacy:</b> Your resumes and executive documents are analyzed in real time and never stored on any server.</div>',
    unsafe_allow_html=True
)

# --- 8. 3-WAY GLOBAL MODE SELECTOR ---
user_mode = st.radio(
    "🌐 Choose Your Portal Mode:",
    [
        "🎓 Candidate / Intern / Professional / Faculty (Analyze My Resume)",
        "🏢 HR / Recruiter (Screen Candidate Resume)",
        "👔 CEO / Executive & Board Leadership"
    ],
    horizontal=True
)

st.markdown("---")

# ==============================================================================
# MODE 1: CANDIDATE / INTERN / STUDENT / SCHOLAR / FACULTY / ANY GLOBAL PROFESSION
# ==============================================================================
if user_mode == "🎓 Candidate / Intern / Professional / Faculty (Analyze My Resume)":
    st.subheader("📄 Universal Career, Internship & Academic Resume Analyzer")

    career_stage = st.radio(
        "🎯 Your Career Stage:",
        ["🌱 Student Internship / Fresher (0–1 Yrs)", "💼 Experienced / Full-Time / Academic / Senior Role"],
        horizontal=True
    )

    col1, col2 = st.columns(2)
    with col1:
        selected_dept = st.selectbox("🏛️ Select Industry / Department / Profession:", list(UNIVERSAL_JOB_ROLES.keys()))
    with col2:
        dept_roles = UNIVERSAL_JOB_ROLES[selected_dept]
        selected_role = st.selectbox("🎯 Select Target Role / Internship:", list(dept_roles.keys()))

    jd_text = st.text_area(
        "📋 Target Job / Internship Description (Auto-filled — You can edit or paste any custom JD):",
        value=dept_roles[selected_role],
        height=140,
        placeholder="Select a category above or paste any Job/Internship Description here...",
        key=f"jd_{selected_role}"
    )

    uploaded_resume = st.file_uploader("📎 Upload Your Resume / CV / Portfolio (PDF):", type=["pdf"], key="cand_pdf")

    if st.button("⚡ Analyze My Resume & Generate ATS Upgrades"):
        if uploaded_resume and jd_text.strip():
            with st.spinner("🌊 Analyzing resume alignment, domain keywords & ATS impact..."):
                resume_text = extract_text_from_pdf(uploaded_resume)
                if not resume_text:
                    st.error("❌ Could not read text from this PDF. Please upload a text-based PDF (not a scanned image).")
                else:
                    cand_prompt = f"""
                    You are an elite Global Career Strategist and ATS (Applicant Tracking System) Specialist.
                    Output Language Requirement: {output_lang}
                    Candidate Career Stage: {career_stage}

                    Target Industry/Department: {selected_dept}
                    Target Role / Internship: {selected_role}

                    Job / Internship Description:
                    {jd_text}

                    Candidate Resume / CV:
                    {resume_text}

                    Tailor your evaluation strictly to their career stage ({career_stage} — e.g., for Internships/Freshers prioritize projects, coursework, hackathons, and learning agility; for Experienced/Academic roles prioritize measurable impact, publications, or leadership).

                    Provide a comprehensive, high-impact evaluation including:
                    1. **Overall ATS Match Score (0 - 100%)** with a clear verdict.
                    2. **Matched Core Skills, Projects & Strengths** found in the resume.
                    3. **Missing Keywords & Skill Gaps** compared to the Job/Internship Description.
                    4. **✨ ATS Resume Bullet-Point Rewriter:** Write 3 quantified, high-impact resume bullet points the candidate can directly copy-paste into their resume to boost their score above 90%.
                    5. **Actionable Next Steps** (certifications, mini-projects, labs, portfolio items, or formatting improvements tailored specifically to {selected_dept}).
                    """
                    result = generate_ai_response(cand_prompt, custom_api_key)
                    st.markdown("### 📊 Resume & Internship Intelligence Report")
                    st.markdown(result)

                    st.download_button(
                        label="📥 Download Resume Report (.md)",
                        data=result,
                        file_name=f"TalentPulse_Report_{selected_role.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
        else:
            st.warning("⚠️ Please upload your PDF resume and ensure a Job/Internship Description is selected or pasted.")

# ==============================================================================
# MODE 2: HR / RECRUITER SCREENING PORTAL
# ==============================================================================
elif user_mode == "🏢 HR / Recruiter (Screen Candidate Resume)":
    st.subheader("🏢 HR & Recruiter — Smart Candidate & Intern Screening Portal")
    st.caption("Evaluate applicant resumes across any global industry, detect red flags & auto-generate tailored interview questions.")

    col_hr1, col_hr2 = st.columns(2)
    with col_hr1:
        hr_dept_preset = st.selectbox("🏛️ Quick Industry Template (Optional):", list(UNIVERSAL_JOB_ROLES.keys()), key="hr_dept")
    with col_hr2:
        hr_roles_dict = UNIVERSAL_JOB_ROLES[hr_dept_preset]
        hr_role_preset = st.selectbox("🎯 Select Role Template:", list(hr_roles_dict.keys()), key="hr_role")

    hr_jd = st.text_area(
        "📋 Company Job / Internship Description & Must-Have Requirements:",
        value=hr_roles_dict[hr_role_preset],
        height=140,
        placeholder="Paste your company's job or internship description, required skills, and experience criteria..."
    )

    hr_resume = st.file_uploader("📎 Upload Candidate Resume (PDF):", type=["pdf"], key="hr_pdf")

    if st.button("🔍 Screen Candidate & Generate Interview Questions"):
        if hr_resume and hr_jd.strip():
            with st.spinner("🏢 Evaluating candidate fit, red flags & preparing interview guide..."):
                resume_text = extract_text_from_pdf(hr_resume)
                if not resume_text:
                    st.error("❌ Could not read text from this PDF. Please upload a valid text-based PDF.")
                else:
                    hr_prompt = f"""
                    You are a Senior Global HR Director & Talent Acquisition Lead.
                    Output Language Requirement: {output_lang}

                    Job / Internship Description:
                    {hr_jd}

                    Candidate Resume:
                    {resume_text}

                    Generate a structured HR Hiring Evaluation Report:
                    1. **Candidate Fit Score (0 - 100%)**
                    2. **Hiring Verdict:** [STRONGLY RECOMMEND / SHORTLIST FOR INTERVIEW / HOLD / REJECT] with a 2-sentence justification.
                    3. **Verified Strengths, Projects & Relevant Experience**
                    4. **Skill Gaps & Potential Red Flags**
                    5. **5 Tailored Technical & Behavioral Interview Questions** specifically designed to test this candidate's resume claims and missing areas.
                    """
                    hr_result = generate_ai_response(hr_prompt, custom_api_key)
                    st.markdown("### 📋 HR Candidate Screening Report")
                    st.markdown(hr_result)

                    st.download_button(
                        label="📥 Download HR Screening Report (.md)",
                        data=hr_result,
                        file_name="TalentPulse_HR_Screening_Report.md",
                        mime="text/markdown"
                    )
        else:
            st.warning("⚠️ Please upload a candidate PDF resume and provide the Job Description.")

# ==============================================================================
# MODE 3: CEO / EXECUTIVE & BOARD LEADERSHIP PORTAL
# ==============================================================================
else:
    st.subheader("👔 CEO, C-Suite & Global Board Leadership Portal")
    st.caption("Designed for CEOs, Founders, CXOs & Corporate Boards — Strategic Vision, P&L Ownership & Board-Readiness Intelligence.")

    exec_objective = st.selectbox(
        "🎯 Select Executive Objective:",
        [
            "Evaluate My CEO / C-Suite Profile for Global & Board Roles",
            "Screen an Executive Candidate (CEO / CTO / CFO / COO) for Our Board"
        ]
    )

    exec_jd = st.text_area(
        "📋 Board Mandate / Company Vision & Strategic KPIs:",
        value=UNIVERSAL_JOB_ROLES["👔 C-Suite, CEO & Global Executive Leadership"]["Chief Executive Officer (CEO) / Managing Director"],
        height=140,
        placeholder="Enter board mandate, company stage (Startup / Enterprise), revenue scale, global expansion goals, or executive KPIs..."
    )

    exec_resume = st.file_uploader("📎 Upload Executive CV / Board Bio (PDF):", type=["pdf"], key="exec_pdf")

    if st.button("🚀 Run Global Executive Intelligence Analysis"):
        if exec_resume and exec_jd.strip():
            with st.spinner("👔 Analyzing executive leadership impact, P&L alignment & board readiness..."):
                resume_text = extract_text_from_pdf(exec_resume)
                if not resume_text:
                    st.error("❌ Could not read text from this PDF. Please upload a valid text-based PDF.")
                else:
                    exec_prompt = f"""
                    You are an elite Global Executive Search Partner (Korn Ferry / Spencer Stuart caliber) and Corporate Board Advisor.
                    Output Language Requirement: {output_lang}
                    Objective: {exec_objective}

                    Board Mandate / Executive Vision:
                    {exec_jd}

                    Executive CV / Bio:
                    {resume_text}

                    Deliver an Executive-Grade Assessment covering:
                    1. **Executive & Board Readiness Score (0 - 100%)**
                    2. **Strategic Vision, P&L Ownership & Global Scaling Impact**
                    3. **Core Governance & C-Suite Leadership Strengths**
                    4. **Strategic Blind Spots / Board-Level Risks**
                    5. **3 High-Stakes Boardroom / Investor Due-Diligence Questions**
                    6. **✨ Polished 3-Line Executive Bio** ready for Board Presentations, Investor Decks, or Global Keynotes.
                    """
                    exec_result = generate_ai_response(exec_prompt, custom_api_key)
                    st.markdown("### 🏛️ Executive Leadership & Board Report")
                    st.markdown(exec_result)

                    st.download_button(
                        label="📥 Download Executive Report (.md)",
                        data=exec_result,
                        file_name="TalentPulse_Executive_Leadership_Report.md",
                        mime="text/markdown"
                    )
        else:
            st.warning("⚠️ Please upload the Executive CV / Bio PDF and enter the Board Mandate.")

# --- 9. PERMANENT DEVELOPER CREDIT FOOTER ---
st.markdown(
    """
    <div class="footer-credit">
        🌊 <b>TALENTPULSE AI — Global Career, Internship, HR &amp; Executive Intelligence Hub</b><br/>
        Architected, Designed &amp; Developed by <b>Samira</b> — <i>Department of Computer Applications (BCA)</i> 🎓<br/>
        <span style="font-size:0.83rem; color:#5EEAD4;">Covering 35+ Global Sectors • Empowering Interns, Students, Scholars, Educators, Recruiters &amp; World Leaders</span>
    </div>
    """,
    unsafe_allow_html=True
)
