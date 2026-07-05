import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from backend.app.schemas import AnalyzeRequest, AnalyzeResponse, ChatRequest, ChatResponse
from backend.src.inference import run_inference
from backend.src.llm_explainer import chatbot_reply
from backend.src.security_logic import get_risk_level

app = FastAPI(
    title="AI-Powered Cybersecurity Intelligence Platform",
    version="1.0",
)

raw_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
)
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(request: AnalyzeRequest):
    prediction, confidence = run_inference(request.text)
    risk_level = get_risk_level(confidence)

    return {
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "risk_level": risk_level,
    }


@app.post("/chat", response_model=ChatResponse)
def chat_with_assistant(request: ChatRequest):
    reply = chatbot_reply(
        request.message,
        request.prediction,
        request.confidence,
        request.risk_level,
    )
    return {"reply": reply}
