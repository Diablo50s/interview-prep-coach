import streamlit as st
from database import init_db, save_session, get_past_sessions, get_session_conversation
from llm import generate_questions, get_feedback, get_next_question
from utils import extract_pdf_text, extract_score

# --- Page Config ---
st.set_page_config(
    page_title="Interview Coach",
    page_icon="🎯",
    layout="wide"
)


# --- Init ---
init_db()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "stage" not in st.session_state:
    st.session_state.stage = "start"
if "last_score" not in st.session_state:
    st.session_state.last_score = None

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🎯 Interview Coach")
    st.markdown("---")

    st.markdown("### 📄 Your Resume")
    resume_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
    if resume_file:
        st.session_state.resume_text = extract_pdf_text(resume_file)
        st.success("Resume loaded ✓")

    st.markdown("### 🎚️ Difficulty")
    difficulty = st.selectbox("", ["Fresher", "Mid-level", "Experienced"], label_visibility="collapsed")

    st.markdown("---")

    if st.button("+ New Session"):
        st.session_state.messages = []
        st.session_state.stage = "start"
        st.session_state.last_score = None
        st.rerun()

    st.markdown("### 🕐 Past Sessions")
    past_sessions = get_past_sessions()
    for session in past_sessions:
        with st.expander(f"📅 {session[1]} | {session[2]} | Score: {session[3]}/10"):
            messages = get_session_conversation(session[0])
            for msg in messages:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**AI:** {msg['content']}")

# --- Main ---
st.markdown("## 🎯 Interview Prep Coach")
st.markdown("*Upload your resume, paste a job description, and start practicing*")
st.markdown("---")

# Chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Start stage
if st.session_state.stage == "start":
    job_desc = st.text_area("Paste job description to begin:", height=100, placeholder="e.g. Looking for a Python developer with ML experience...")
    if st.button("Start Interview Practice →"):
        if job_desc.strip():
            with st.spinner("Generating questions..."):
                questions = generate_questions(job_desc, difficulty, st.session_state.resume_text)
            st.session_state.messages.append({"role": "user", "content": f"Job Description: {job_desc}"})
            st.session_state.messages.append({"role": "assistant", "content": questions})
            st.session_state.stage = "answering"
            st.rerun()

# Answering stage
elif st.session_state.stage == "answering":
    answer = st.text_area("Your answer:", height=100, placeholder="Type your answer here...", key=f"answer_{len(st.session_state.messages)}")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Get Feedback →"):
            if answer.strip():
                with st.spinner("Evaluating..."):
                    feedback = get_feedback(answer, difficulty, st.session_state.messages)
                    score = extract_score(feedback)
                    st.session_state.last_score = score
                st.session_state.messages.append({"role": "user", "content": answer})
                st.session_state.messages.append({"role": "assistant", "content": feedback})
                st.rerun()

    with col2:
        if st.button("Next Question →"):
            with st.spinner("Generating next question..."):
                next_q = get_next_question(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": next_q})
            st.rerun()

    with col3:
        if st.button("💾 Save & End"):
            save_session(difficulty, st.session_state.messages, st.session_state.last_score)
            st.session_state.messages = []
            st.session_state.stage = "start"
            st.session_state.last_score = None
            st.success("Session saved!")
            st.rerun()