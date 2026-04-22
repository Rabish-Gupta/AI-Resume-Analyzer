# app.py

import time

import streamlit as st
from utils import (
    ats_score,
    detect_sections,
    extract_text_from_pdf,
    clean_text,
    calculate_similarity,
    extract_skills_advanced,
    get_common_keywords,
    predict_role,
    advanced_suggestions,
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Analyzer", "About"])

st.set_page_config(page_title="AI Resume Analyzer")

# st.title("📄 AI Resume Analyzer")


# # Upload resume
# resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# # Job description input
# jd = st.text_area("Paste Job Description")

# if st.button("Analyze"):
if page == "Analyzer":

    st.title("🚀 AI Resume Analyzer")
    st.caption("Optimize your resume for better job matching")

    col1, col2 = st.columns(2)

    with col1:
        resume_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

    with col2:
        jd = st.text_area("📝 Job Description")

    if st.button("🔍 Analyze Resume"):
        if resume_file and jd:
            with st.spinner("Analyzing Resume..."):
                time.sleep(2)

            # Extract text
            resume_text = extract_text_from_pdf(resume_file)

            # Clean text
            resume_clean = clean_text(resume_text)
            # jd_clean = clean_text(jd)
            sections = detect_sections(resume_text)

            # Use only important sections
            important_text = sections["skills"]

            resume_clean = clean_text(important_text)
            jd_clean = clean_text(jd)

            # Similarity score
            score = calculate_similarity(resume_clean, jd_clean)

            # Skills
            resume_skills = extract_skills_advanced(resume_clean)
            jd_skills = extract_skills_advanced(jd_clean)

            missing_skills = list(set(jd_skills) - set(resume_skills))
            print("Missing Skills:", missing_skills)
            # Suggestions
            # suggestions = generate_suggestions(missing_skills, score)
            # Detect sections
            sections = detect_sections(resume_text)

            # Advanced suggestions
            suggestions = advanced_suggestions(sections, missing_skills)

            # Output

            col1, col2, col3 = st.columns(3)

            # st.subheader(f"📊 Match Score: {score}%")

            role = predict_role(resume_skills)
            # st.subheader(f"🎯 Predicted Role: {role}")

            ats = ats_score(resume_skills, jd_skills, score)
            # st.subheader(f"📈 ATS Score: {ats}/100")

            col1.metric("📊 Match Score", f"{score}%")
            col2.metric("📈 ATS Score", f"{ats}")
            col3.metric("🎯 Role", role)

            # st.subheader("✅ Skills Found")
            # st.write(resume_skills)
            common = get_common_keywords(resume_clean, jd_clean)

            # st.subheader("🔑 Matching Keywords")
            # st.write(common[:20])

            st.subheader("❌ Missing Skills")
            st.write(missing_skills)

            # st.subheader("💡 Suggestions")
            # for s in suggestions:
            #     st.write("-", s)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Skills Found")
                st.success(", ".join(resume_skills))

                st.subheader("🔑 Keywords")
                st.info(", ".join(common[:15]))

            with col2:
                st.subheader("❌ Missing Skills")
                st.error(", ".join(missing_skills))

                # st.subheader("💡 Suggestions")
                # for s in suggestions:
                #     st.write("➡️", s)

                st.subheader("💡 Suggestions")

                if suggestions:
                    for s in suggestions:
                        st.write("➡️", s)
                else:
                    st.success("Your resume looks strong! 🎉")

            sections = detect_sections(resume_text)

            # st.subheader("📂 Resume Sections")
            # st.json(sections)

            with st.expander("📂 View Resume Sections"):
                st.json(sections)

            report = f"""
            Match Score: {score}
            ATS Score: {ats}
            Role: {role}
            """

            st.download_button("📥 Download Report", report)

        else:
            st.warning("Please upload resume and enter job description.")
elif page == "About":
    st.title("📘 About This Project")

    st.write(
        """
            This AI Resume Analyzer uses NLP techniques like:
            - TF-IDF Vectorization
            - Cosine Similarity
            - Skill Extraction

            Built to help students improve their resumes.
            """
    )
