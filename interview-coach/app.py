import os
import sqlite3
import datetime
import PyPDF2
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Database setup
def init_db():
    conn = sqlite3.connect("sessions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            job_description TEXT,
            difficulty TEXT,
            questions TEXT,
            answer TEXT,
            feedback TEXT,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

st.title("Interview Prep Coach")

# Resume upload
st.subheader("Step 1: Upload Your Resume")
resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

resume_text = ""
if resume_file:
    pdf_reader = PyPDF2.PdfReader(resume_file)
    for page in pdf_reader.pages:
        resume_text += page.extract_text()
    st.success("Resume loaded!")

# Job description
st.subheader("Step 2: Paste Job Description")
job_description = st.text_area("Paste Job Description here:", height=150)

# Difficulty
st.subheader("Step 3: Select Difficulty")
difficulty = st.selectbox("Level:", ["Fresher", "Mid-level", "Experienced"])

if st.button("Generate Interview Questions"):
    if job_description.strip() == "":
        st.warning("Please paste a job description first.")
    else:
        prompt = f"""Generate 5 interview questions for a {difficulty} candidate.
Job Description: {job_description}"""
        
        if resume_text:
            prompt += f"\n\nCandidate Resume:\n{resume_text}\n\nMake questions relevant to both the job and the candidate's background."

        with st.spinner("Generating questions..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert technical interviewer."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.session_state["questions"] = response.choices[0].message.content

if "questions" in st.session_state:
    st.subheader("Your Interview Questions:")
    st.write(st.session_state["questions"])

    st.subheader("Practice Answering:")
    user_answer = st.text_area("Type your answer here:", height=150)

    if st.button("Get Feedback"):
        if user_answer.strip() == "":
            st.warning("Type your answer first.")
        else:
            with st.spinner("Evaluating..."):
                feedback_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"You are an expert interviewer giving feedback to a {difficulty} candidate. Be specific and constructive."},
                        {"role": "user", "content": f"Candidate answered:\n\n{user_answer}\n\nGive feedback on clarity, technical accuracy, and improvement areas. Also rate the answer from 1 to 10."}
                    ]
                )
                st.session_state["feedback"] = feedback_response.choices[0].message.content

if "feedback" in st.session_state:
    st.subheader("Feedback:")
    st.write(st.session_state["feedback"])
    
    # Extract score from feedback
    feedback_text = st.session_state["feedback"]
    score = None
    for word in feedback_text.split():
        word = word.strip("./,")
        if word.isdigit() and 1 <= int(word) <= 10:
            score = int(word)
            break
    
    if score:
        st.metric("Your Score", f"{score}/10")
    
    # Save to database
    if st.button("Save Session"):
        conn = sqlite3.connect("sessions.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO sessions (date, job_description, difficulty, questions, answer, feedback, score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            job_description,
            difficulty,
            st.session_state.get("questions", ""),
            st.session_state.get("user_answer", ""),
            feedback_text,
            score
        ))
        conn.commit()
        conn.close()
        st.success("Session saved!")


# Session History
st.divider()
st.subheader("📋 Session History")

if st.button("Show Past Sessions"):
    conn = sqlite3.connect("sessions.db")
    c = conn.cursor()
    c.execute("SELECT date, difficulty, score FROM sessions ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    
    if rows:
        for row in rows:
            st.write(f"🗓 {row[0]} | Level: {row[1]} | Score: {row[2]}/10")
    else:
        st.info("No sessions saved yet.")