import os

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

RAW_FILE = None
for file in os.listdir(RAW_DIR):
    if file.endswith(".csv"):
        RAW_FILE = file
        break

if RAW_FILE is None:
    raise FileNotFoundError(f"No CSV file found in {RAW_DIR}")

RAW_PATH = os.path.join(RAW_DIR, RAW_FILE)
PROCESSED_PATH = os.path.join(PROCESSED_DIR, "phishing_emails_clean.csv")
os.makedirs(PROCESSED_DIR, exist_ok=True)


def main():
    df = pd.read_csv(RAW_PATH)

    df = df.iloc[:, :2]
    df.columns = ["text", "label"]

    df = df.dropna(subset=["text"])
    df = df[df["text"].str.strip() != ""]
    df["label"] = df["label"].astype(int)
    df["text"] = df["text"].str.lower().str.strip()

    df.to_csv(PROCESSED_PATH, index=False)
    print("Preprocessing complete:", PROCESSED_PATH)


if __name__ == "__main__":
    main()
