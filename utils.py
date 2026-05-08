# utils.py

import re
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import SKILLS

import nltk

nltk.download("punkt")
nltk.download("punkt_tab")

from nltk.tokenize import word_tokenize


# 📄 Extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# 🧹 Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text


# 📊 Calculate similarity
def calculate_similarity(resume, jd):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    return text


def extract_skills_advanced(text):
    text = normalize_text(text)
    found_skills = []

    for skill in SKILLS:
        skill_pattern = skill.lower()

        # handle variations like "machine-learning"
        if re.search(r"\b" + re.escape(skill_pattern) + r"\b", text):
            found_skills.append(skill)

    return list(set(found_skills))


# 💡 Suggest improvements
def generate_suggestions(missing_skills, score):
    suggestions = []

    if score < 60:
        suggestions.append(
            "Improve your resume with more relevant skills and projects."
        )

    for skill in missing_skills:
        suggestions.append(f"Consider adding {skill} to your skillset.")

    return suggestions


def detect_sections(text):
    sections = {"education": "", "skills": "", "projects": "", "experience": ""}

    current_section = None

    for line in text.split("\n"):
        line_lower = line.lower()

        if "education" in line_lower:
            current_section = "education"
        elif "skills" in line_lower:
            current_section = "skills"
        elif "project" in line_lower:
            current_section = "projects"
        elif "experience" in line_lower:
            current_section = "experience"

        elif current_section:
            sections[current_section] += line + " "

    return sections


def predict_role(skills):
    if "machine learning" in skills:
        return "Data Scientist"
    elif "react" in skills or "javascript" in skills:
        return "Web Developer"
    elif "sql" in skills:
        return "Data Analyst"
    else:
        return "General Software Engineer"


def get_common_keywords(resume, jd):
    resume_words = set(resume.split())
    jd_words = set(jd.split())
    return list(resume_words.intersection(jd_words))


def ats_score(resume_skills, jd_skills, similarity):
    if len(jd_skills) == 0:
        skill_score = 0
    else:
        skill_score = (len(set(resume_skills) & set(jd_skills)) / len(jd_skills)) * 60

    similarity_score = similarity * 0.4

    total = skill_score + similarity_score
    return round(total, 2)


def advanced_suggestions(sections, missing_skills):
    tips = []

    if len(sections["projects"]) < 50:
        tips.append("Add more project details.")

    if len(sections["experience"]) < 30:
        tips.append("Include internships or experience.")

    for skill in missing_skills:
        tips.append(f"Learn and add {skill}")

    return tips


print("utils loaded")
