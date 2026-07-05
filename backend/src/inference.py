import os
import warnings

import torch
import torch.nn.functional as F
from transformers import BertForSequenceClassification, BertTokenizerFast

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_DIR = os.path.join(PROJECT_ROOT, "model", "phishing_bert")
MODEL_SOURCE = os.getenv("MODEL_SOURCE", DEFAULT_MODEL_DIR)


def resolve_device() -> torch.device:
    if not torch.cuda.is_available():
        return torch.device("cpu")

    return torch.device("cuda")


DEVICE = resolve_device()

tokenizer = BertTokenizerFast.from_pretrained(MODEL_SOURCE)
model = BertForSequenceClassification.from_pretrained(MODEL_SOURCE)

try:
    model.to(DEVICE)
except RuntimeError as exc:
    if DEVICE.type == "cuda":
        warnings.warn(
            "CUDA model loading failed; falling back to CPU so the backend can start."
        )
        torch.cuda.empty_cache()
        DEVICE = torch.device("cpu")
        model.to(DEVICE)
    else:
        raise

model.eval()

print(f"Model loaded on {DEVICE}")


def predict(text: str) -> dict:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128,
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)

    phishing_prob = probs[0][1].item()
    label = "phishing" if phishing_prob >= 0.5 else "legitimate"

    return {
        "prediction": label,
        "confidence": phishing_prob,
    }


def run_inference(text: str):
    result = predict(text)
    return result["prediction"], result["confidence"]
