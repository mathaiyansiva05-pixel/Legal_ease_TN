from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=1)
    parties: str = Field(..., min_length=1)
    terms: str = Field(..., min_length=1)
    effective_date: str = Field(..., min_length=1)

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
        )
        return {
            "success": True,
            "document_type": request.document_type,
            "content": content,
        }
    except Exception as exc:
        message = str(exc)
        lowered = message.lower()
        if "429" in message or "resource_exhausted" in lowered or "quota" in lowered:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota is exhausted. Check your Gemini project/model quota."
            )
        raise HTTPException(status_code=500, detail=message)
