def get_risk_level(confidence: float) -> str:
    if confidence >= 0.90:
        return "High"
    elif confidence >= 0.70:
        return "Medium"
    else:
        return "Low"
