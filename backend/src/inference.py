import logging
import os
from pathlib import Path
import warnings

import torch
import torch.nn.functional as F
from transformers import BertForSequenceClassification, BertTokenizerFast

LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_DIR = PROJECT_ROOT / "model" / "phishing_bert"
MODEL_SOURCE = os.getenv("MODEL_SOURCE", "").strip()

tokenizer = None
model = None


def resolve_device() -> torch.device:
    if not torch.cuda.is_available():
        return torch.device("cpu")

    return torch.device("cuda")


DEVICE = resolve_device()


def resolve_model_source() -> str | None:
    """Resolve the best available model source.

    Prefer an explicitly configured local directory, then the bundled local
    checkpoint, then a valid Hugging Face repo id. If nothing usable exists,
    return None so the service can fall back to heuristics.
    """

    if MODEL_SOURCE:
        source_path = Path(MODEL_SOURCE).expanduser()
        if source_path.exists():
            return str(source_path)

        is_repo_id = (
            "/" in MODEL_SOURCE
            and MODEL_SOURCE.count("/") == 1
            and not MODEL_SOURCE.startswith((".", "/", "~"))
            and "\\" not in MODEL_SOURCE
        )
        if is_repo_id:
            # Treat single-slash identifiers as Hugging Face repo ids.
            return MODEL_SOURCE

    if DEFAULT_MODEL_DIR.exists():
        return str(DEFAULT_MODEL_DIR)

    return None


def load_model_artifacts():
    global tokenizer, model, DEVICE

    source = resolve_model_source()
    if source is None:
        LOGGER.warning(
            "No phishing model checkpoint found. Using heuristic inference fallback."
        )
        return False

    try:
        tokenizer = BertTokenizerFast.from_pretrained(source)
        model = BertForSequenceClassification.from_pretrained(source)
        try:
            model.to(DEVICE)
        except RuntimeError:
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
        LOGGER.info("Phishing model loaded from %s on %s", source, DEVICE)
        return True
    except Exception as exc:
        tokenizer = None
        model = None
        LOGGER.exception(
            "Failed to load phishing model from %s; using heuristic fallback.", source
        )
        warnings.warn(f"Phishing model unavailable: {exc}")
        return False


def heuristic_predict(text: str) -> dict:
    """Fallback classifier for when the BERT checkpoint is unavailable."""

    message = text.lower()
    signals = {
        "urgency": ["urgent", "immediately", "asap", "verify now", "act now"],
        "credential": ["password", "login", "credential", "account", "suspended"],
        "payment": ["invoice", "payment", "wire", "bank", "refund"],
        "link": ["click", "link", "open attachment", "attachment", "download"],
        "threat": ["locked", "terminated", "warning", "security alert", "confirm"],
    }

    score = 0
    for keywords in signals.values():
        if any(keyword in message for keyword in keywords):
            score += 1

    phishing_prob = min(0.95, max(0.05, 0.12 + (score * 0.18)))
    label = "phishing" if phishing_prob >= 0.5 else "legitimate"

    return {
        "prediction": label,
        "confidence": phishing_prob,
    }


load_model_artifacts()


def predict(text: str) -> dict:
    if tokenizer is None or model is None:
        return heuristic_predict(text)

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
