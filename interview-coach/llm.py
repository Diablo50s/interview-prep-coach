from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

def generate_questions(job_description, difficulty, resume_text=""):
    prompt = f"Generate 5 {difficulty} level interview questions for this job:\n\n{job_description}"
    if resume_text:
        prompt += f"\n\nCandidate resume:\n{resume_text}\n\nMake questions relevant to both."

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def get_feedback(answer, difficulty, messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"You are an expert interviewer evaluating a {difficulty} candidate. Be specific and constructive. End with a score like 'Score: X/10'."},
            *messages,
            {"role": "user", "content": f"Candidate answered:\n\n{answer}"}
        ]
    )
    return response.choices[0].message.content

def get_next_question(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer. Ask one follow-up interview question based on the conversation so far."},
            *messages
        ]
    )
    return response.choices[0].message.content