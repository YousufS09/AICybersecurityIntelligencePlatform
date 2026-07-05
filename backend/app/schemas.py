from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    prediction: str
    confidence: float
    risk_level: str

class ChatRequest(BaseModel):
    message: str
    prediction: str
    confidence: float
    risk_level: str

class ChatResponse(BaseModel):
    reply: str
