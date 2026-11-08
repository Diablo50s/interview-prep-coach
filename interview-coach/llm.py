from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# llama-3.3-70b-versatile was retired by Groq on 16 Aug 2026.
# Override with GROQ_MODEL in .env if Groq retires this one too.
MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

MAX_RESUME_CHARS = 6000


def _chat(messages):
    """Single place for every Groq call, with friendly error handling."""
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Could not reach the AI service ({type(e).__name__}). Check your GROQ_API_KEY and model name, then try again."


def generate_questions(job_description, difficulty, resume_text=""):
    prompt = f"Generate 5 {difficulty} level interview questions for this job:\n\n{job_description}"
    if resume_text:
        prompt += f"\n\nCandidate resume:\n{resume_text[:MAX_RESUME_CHARS]}\n\nMake questions relevant to both."
    return _chat([
        {"role": "system", "content": "You are an expert technical interviewer."},
        {"role": "user", "content": prompt},
    ])


def get_feedback(answer, difficulty, messages):
    return _chat([
        {"role": "system", "content": f"You are an expert interviewer evaluating a {difficulty} candidate. Be specific and constructive. End with a score on its own line in exactly this format: 'Score: X/10'."},
        *messages,
        {"role": "user", "content": f"Candidate answered:\n\n{answer}"},
    ])


def get_next_question(messages):
    return _chat([
        {"role": "system", "content": "You are an expert technical interviewer. Ask one follow-up interview question based on the conversation so far."},
        *messages,
    ])
