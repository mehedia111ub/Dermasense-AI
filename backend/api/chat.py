from fastapi import APIRouter
from pydantic import BaseModel
from services.mistral_chat import generate_mistral_response
from services.safety_guardrails import apply_safety_filter

router = APIRouter()

chat_memory = []

class ChatRequest(BaseModel):
    question: str
    analysis_report: dict

@router.post("/chat")
def chat_with_ai(request: ChatRequest):

    user_question = request.question
    report = request.analysis_report

    response = generate_mistral_response(user_question, report)

    response = apply_safety_filter(user_question, response)

    chat_memory.append({
        "question": user_question,
        "response": response
    })

    return {
        "answer": response,
        "chat_turns": len(chat_memory),
        "disclaimer": "This system provides educational information only and does not provide medical diagnosis."
    }