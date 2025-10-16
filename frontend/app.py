import streamlit as st
import fitz  # PyMuPDF
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Resume Screener & Job Matcher", page_icon="🎯", layout="wide")

st.markdown("""
<style>
.gradient-header {
    background: linear-gradient(90deg, #6a82fb 0%, #fc5c7d 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem 2rem 2rem;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 4px 24px 0 rgba(80,80,80,0.08);
    text-align: center;
}
.gradient-score {
    background: linear-gradient(90deg, #c2e9fb 0%, #fbc2eb 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem 2rem 2rem;
    margin-bottom: 2rem;
    color: #222;
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    box-shadow: 0 4px 24px 0 rgba(80,80,80,0.08);
}
.analyze-btn button {
    background: linear-gradient(90deg, #6a82fb 0%, #fc5c7d 100%);
    color: white;
    font-weight: 600;
    font-size: 1.2rem;
    border-radius: 2rem;
    padding: 0.8rem 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px 0 rgba(80,80,80,0.08);
}
.analyze-btn button:hover {
    background: linear-gradient(90deg, #fc5c7d 0%, #6a82fb 100%);
}
.info-box {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 8px 0 rgba(80,80,80,0.08);
    padding: 1rem 1.5rem;
    margin-bottom: 1.2rem;
    font-size: 1.1rem;
}
.skills-tag {
    display: inline-block;
    background: #e0f7fa;
    color: #00796b;
    border-radius: 1.2rem;
    padding: 0.3rem 1.1rem;
    margin: 0.2rem 0.3rem 0.2rem 0;
    font-size: 1rem;
    font-weight: 500;
}
.skills-tag-missing {
    display: inline-block;
    background: #ffebee;
    color: #c62828;
    border-radius: 1.2rem;
    padding: 0.3rem 1.1rem;
    margin: 0.2rem 0.3rem 0.2rem 0;
    font-size: 1rem;
    font-weight: 500;
}
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    margin-top: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
/* Hide Streamlit top-right menu and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
button[data-testid="baseButton-headerMenu"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

SKILL_KEYWORDS = [
    "python", "java", "c++", "c#", "sql", "javascript", "html", "css", "react", "node", "django", "flask", "fastapi", "pandas", "numpy", "scikit-learn", "machine learning", "deep learning", "nlp", "aws", "azure", "git", "docker", "kubernetes"
]
RECOMMENDED_SKILLS = ["python", "fastapi", "flask", "django", "sql"]

def extract_text_from_pdf(pdf_file):
    try:
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.lower()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_skills(text):
    if not text:
        return []
    found = set()
    for skill in SKILL_KEYWORDS:
        if " " in skill:
            pattern = re.compile(re.escape(skill), re.IGNORECASE)
        else:
            pattern = re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)
        if pattern.search(text):
            found.add(skill)
    return sorted(found)

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def calculate_similarity(text1, text2):
    try:
        vectorizer = CountVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        return cosine_similarity(vectors)[0][1]
    except Exception as e:
        st.error(f"Error calculating similarity: {str(e)}")
        return 0

def get_match_percentage(similarity):
    return round(similarity * 100, 2)

def main():
    st.markdown(
        """
        <div class="gradient-header">
            <h1 style="font-size:2.6rem; margin-bottom:0.5rem;">🎯 AI Resume Screener & Job Matcher</h1>
            <div style="font-size:1.2rem;">Transform your hiring process with intelligent resume analysis</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">📄 Resume Upload</div>', unsafe_allow_html=True)
        resume_file = st.file_uploader("Choose a PDF file", type=["pdf"], key="resume")
        candidate_name = st.text_input("👤 Candidate Name (optional)")
    with col2:
        st.markdown('<div class="section-title">💼 Job Description</div>', unsafe_allow_html=True)
        job_description = st.text_area("Paste the job description here", height=180)

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Analyze Resume Match", key="analyze", use_container_width=True)

    if analyze_btn:
        if resume_file is not None and job_description:
            with st.spinner("Analyzing resume and job description..."):
                resume_text = extract_text_from_pdf(resume_file)
                jd_text = job_description.lower()
                resume_skills = extract_skills(resume_text)
                jd_skills = extract_skills(jd_text)
                missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
                processed_resume = preprocess_text(resume_text)
                processed_jd = preprocess_text(jd_text)
                similarity = calculate_similarity(processed_resume, processed_jd)
                match_percentage = get_match_percentage(similarity)

            st.markdown(
                f"""
                <div class=\"gradient-score\">
                    <span style=\"font-size:2.2rem;vertical-align:middle;\">📈</span>
                    <span style=\"color:#c62828;\"> {match_percentage:.1f}%</span>
                    <div style=\"font-size:1.1rem; color:#444; font-weight:400; margin-top:0.5rem;\">Match Score</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            colA, colB = st.columns(2)
            with colA:
                st.markdown('<div class="section-title">📄 Resume Skills</div>', unsafe_allow_html=True)
                if resume_skills:
                    st.markdown(
                        "".join([f'<span class=\"skills-tag\">{skill}</span>' for skill in resume_skills]),
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown('<div class="info-box">No skills detected in resume</div>', unsafe_allow_html=True)
            with colB:
                st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
                if missing_skills:
                    st.markdown(
                        "".join([f'<span class=\"skills-tag-missing\">{skill}</span>' for skill in missing_skills]),
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown('<div class="info-box">🎉 Perfect match! No missing skills</div>', unsafe_allow_html=True)

            colC, colD = st.columns(2)
            with colC:
                st.markdown('<div class="section-title">💼 Job Requirements</div>', unsafe_allow_html=True)
                if jd_skills:
                    st.markdown(
                        "".join([f'<span class=\"skills-tag\">{skill}</span>' for skill in jd_skills]),
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown('<div class="info-box">No skills detected in job description</div>', unsafe_allow_html=True)
            with colD:
                st.markdown('<div class="section-title">💡 Recommended Skills</div>', unsafe_allow_html=True)
                st.markdown(
                    "".join([f'<span class=\"skills-tag\">{skill}</span>' for skill in RECOMMENDED_SKILLS]),
                    unsafe_allow_html=True
                )
        else:
            st.error("Please upload a resume and provide a job description.")

    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class=\"gradient-header\" style=\"margin-top:2rem;\">
            <h2 style=\"font-size:2rem; margin-bottom:0.5rem;\">🚀 Powered by AI Technology</h2>
            <div style=\"font-size:1.1rem;\">Advanced NLP and Machine Learning for Intelligent Resume Matching</div>
        </div>
        <div class=\"info-box\" style=\"border-left: 6px solid #6a82fb;\">
            <b>💡 How it works:</b><br>
            <ul style=\"margin-top:0.5rem;\">
                <li>Upload a PDF resume and paste a job description</li>
                <li>AI extracts and matches skills using advanced NLP</li>
                <li>Get detailed analysis with match score and recommendations</li>
                <li>Perfect for recruiters and job seekers alike!</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()