from backend.src.inference import run_inference
from backend.src.security_logic import get_risk_level


if __name__ == "__main__":
    test_text = """
    Your account has been suspended.
    Click the link below immediately to verify your credentials.
    """

    prediction, confidence = run_inference(test_text)
    risk_level = get_risk_level(confidence)

    print("Inference Test Result")
    print("---------------------")
    print(f"Prediction : {prediction}")
    print(f"Confidence : {confidence:.4f}")
    print(f"Risk Level : {risk_level}")
