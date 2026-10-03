# LegalEase TN

Full-stack AI-powered legal document generator.

## Architecture

Streamlit Frontend -> FastAPI Backend -> Gemini -> Generated Document -> Editable Preview -> DOCX/PDF

## Setup

From the project root on Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and set:

```env
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
LEGALEASE_API_URL=http://127.0.0.1:8000/generate
```

Do not commit `.env` or expose the API key.

## Run Backend

```bat
cd backend
..\.venv\Scripts\activate
uvicorn main:app --reload
```

Backend:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

## Run Frontend

Open a second terminal:

```bat
cd frontend
..\.venv\Scripts\activate
streamlit run app.py
```

## Notes

The API request uses `effective_date` consistently between frontend and backend.

PDF formatting uses FPDF2 and sanitizes the rupee symbol to `Rs.` so the built-in PDF font does not fail on Unicode currency characters.
