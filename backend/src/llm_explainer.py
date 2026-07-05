import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

USE_LIVE_LLM = True  # 🔥 ENABLE LLM


def build_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None
    return OpenAI(api_key=api_key)


# ------------------------------
# FALLBACK: Intent-Based Logic
# ------------------------------
def fallback_chatbot(user_message, prediction, confidence, risk_level):
    msg = user_message.lower()

    if any(k in msg for k in ["why", "reason", "how"]):
        return (
            f"This message was classified as {prediction.upper()} because it "
            "contains social-engineering indicators such as urgency, "
            "account threats, or deceptive calls to action."
        )

    if any(k in msg for k in ["what should", "next", "action"]):
        if risk_level == "High":
            return (
                "Immediate mitigation is required. Do not click any links or respond. "
                "Report the message and reset credentials if interaction occurred."
            )
        return "Avoid interaction and forward the message for review."

    if any(k in msg for k in ["risk", "danger", "impact"]):
        return (
            f"The threat is categorized as {risk_level} risk and may lead to "
            "credential theft, financial loss, or system compromise."
        )

    return (
        f"Threat classified as {prediction.upper()} "
        f"({confidence:.2%} confidence, {risk_level} risk)."
    )


# ------------------------------
# LLM-POWERED CHATBOT
# ------------------------------
def llm_chatbot(user_message, prediction, confidence, risk_level):
    client = build_client()
    if client is None:
        return fallback_chatbot(user_message, prediction, confidence, risk_level)

    prompt = f"""
You are a cybersecurity analyst assisting a SOC operator.

Threat Details:
- Classification: {prediction}
- Confidence: {confidence:.2%}
- Risk Level: {risk_level}

User Question:
"{user_message}"

Guidelines:
- Stay factual and security-focused
- Avoid speculation or hallucination
- Provide mitigation guidance when appropriate
- Be concise and professional
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


# ------------------------------
# MAIN ENTRYPOINT
# ------------------------------
def chatbot_reply(user_message, prediction, confidence, risk_level):
    msg = user_message.lower()

    conversational = any(
        k in msg for k in [
            "why", "how", "what happens", "impact", "consequence"
        ]
    )

    if USE_LIVE_LLM and conversational:
        try:
            return llm_chatbot(
                user_message, prediction, confidence, risk_level
            )
        except Exception:
            pass  # fall through safely

    return fallback_chatbot(
        user_message, prediction, confidence, risk_level
    )
