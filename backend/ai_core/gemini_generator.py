import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to the project's .env file."
            )

        self.client = genai.Client(api_key=self.api_key)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        prompt = f"""
You are a legal-document drafting assistant for LegalEase TN.

Create a clear, professional draft of the requested legal document.

Document Type:
{document_type}

Parties:
{parties}

Effective Date:
{effective_date}

Terms:
{terms}

Requirements:
- Use the document type requested by the user.
- Preserve every user-provided term.
- Organize the document with numbered sections and clear headings.
- Include the effective date and parties.
- Include a signature section.
- Do not invent names, dates, amounts, addresses, clauses, or facts that were not supplied.
- Do not provide legal advice or claim that the document is legally valid in a particular jurisdiction.
- Return only the document text, without Markdown code fences.
"""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
