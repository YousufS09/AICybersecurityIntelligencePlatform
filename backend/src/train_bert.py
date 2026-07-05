import os

import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from torch.amp import GradScaler, autocast
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from transformers import BertForSequenceClassification, BertTokenizerFast

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "phishing_emails_clean.csv",
)

MODEL_DIR = os.path.join(PROJECT_ROOT, "model", "phishing_bert")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_NAME = "bert-base-uncased"
MAX_LEN = 128
BATCH_SIZE = 8
EPOCHS = 2
LEARNING_RATE = 2e-5

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print("Using GPU:", torch.cuda.get_device_name(0))
else:
    raise RuntimeError("CUDA not available. GPU expected.")

torch.backends.cudnn.benchmark = True


class PhishingDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {
            k: torch.tensor(v[idx], dtype=torch.long)
            for k, v in self.encodings.items()
        }
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item


def compute_metrics(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
    }


def train():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    texts = df["text"].tolist()
    labels = df["label"].tolist()

    X_train, X_val, y_train, y_val = train_test_split(
        texts,
        labels,
        test_size=0.2,
        stratify=labels,
        random_state=42,
    )

    print("Tokenizing data (one-time)...")
    tokenizer = BertTokenizerFast.from_pretrained(MODEL_NAME)

    train_encodings = tokenizer(
        X_train,
        truncation=True,
        padding="max_length",
        max_length=MAX_LEN,
    )

    val_encodings = tokenizer(
        X_val,
        truncation=True,
        padding="max_length",
        max_length=MAX_LEN,
    )

    train_dataset = PhishingDataset(train_encodings, y_train)
    val_dataset = PhishingDataset(val_encodings, y_val)

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
        pin_memory=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        num_workers=0,
        pin_memory=True,
    )

    model = BertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
    ).to(DEVICE)

    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    scaler = GradScaler("cuda")

    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch + 1}/{EPOCHS}")
        model.train()
        total_loss = 0.0

        for batch in train_loader:
            optimizer.zero_grad(set_to_none=True)

            input_ids = batch["input_ids"].to(DEVICE, non_blocking=True)
            attention_mask = batch["attention_mask"].to(DEVICE, non_blocking=True)
            labels = batch["labels"].to(DEVICE, non_blocking=True)

            with autocast(device_type="cuda"):
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels,
                )
                loss = outputs.loss

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            total_loss += loss.item()

        print(f"Training loss: {total_loss / len(train_loader):.4f}")

        model.eval()
        preds, true_labels = [], []

        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch["input_ids"].to(DEVICE, non_blocking=True)
                attention_mask = batch["attention_mask"].to(DEVICE, non_blocking=True)

                with autocast(device_type="cuda"):
                    outputs = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                    )

                predictions = torch.argmax(outputs.logits, dim=1)
                preds.extend(predictions.cpu().numpy())
                true_labels.extend(batch["labels"].numpy())

        metrics = compute_metrics(true_labels, preds)

        print(
            f"Validation | "
            f"Acc: {metrics['accuracy']:.4f} | "
            f"Prec: {metrics['precision']:.4f} | "
            f"Recall: {metrics['recall']:.4f} | "
            f"F1: {metrics['f1']:.4f}"
        )

    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    print("\nTraining complete. Final model saved at:", MODEL_DIR)


if __name__ == "__main__":
    train()
