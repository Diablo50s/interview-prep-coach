# Interview Prep Coach 🎯

An AI-powered interview preparation tool that generates personalized interview questions based on your resume and job description, then evaluates your answers with detailed feedback.

## Features
- 📄 Upload your resume (PDF) for personalized questions
- 💼 Paste any job description
- 🎚️ Select difficulty level (Fresher / Mid-level / Experienced)
- 🤖 AI-generated interview questions using Llama 3.3 70B
- ✍️ Answer questions and get instant feedback with ratings

## Tech Stack
- Python
- Streamlit (frontend)
- Groq API + Llama 3.3 70B (LLM)
- PyPDF2 (resume parsing)

## Setup
1. Clone the repo
2. Add your Groq API key in `.env` as `GROQ_API_KEY=your_key`
3. Run `uv add groq streamlit pypdf2 python-dotenv`
4. Run `uv run streamlit run app.py`

## Built By
Vansh — CSE student at MRSPTU Bathinda, AI/ML specialization
