# AI Cybersecurity Intelligence Platform

AI Cybersecurity Intelligence Platform is a full-stack security assistant that analyzes text for phishing risk, returns a prediction with confidence scoring, and provides risk-aware explanations through an interactive dashboard.

## What it does

- Classifies text as `phishing` or `legitimate`
- Returns a confidence score and risk level
- Exposes an AI-assisted chat response for threat interpretation
- Provides a React dashboard for analysis and results

## Project structure

- `backend/` - FastAPI service, inference pipeline, and risk logic
- `frontend/` - React application with the security analysis dashboard
- `backend/model/phishing_bert/` - Saved BERT model and tokenizer files
- `backend/data/` - Raw and processed data used for training and evaluation

## Tech stack

- Python
- FastAPI
- PyTorch
- Hugging Face Transformers
- React
- Tailwind CSS

## Backend setup

The backend uses FastAPI and loads the saved phishing BERT model from `backend/model/phishing_bert/`.

Install the Python dependencies you need for the backend:

```bash
pip install fastapi uvicorn torch transformers pydantic
```

Run the backend from the project root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```bash
http://127.0.0.1:8000
```

## Frontend setup

Install frontend dependencies:

```bash
cd frontend
npm install
```

Start the React app:

```bash
npm start
```

By default, the frontend expects the backend at:

```bash
http://127.0.0.1:8000
```

If your backend runs somewhere else, set:

```bash
REACT_APP_API_BASE_URL
```

## API endpoints

### `POST /analyze`

Analyzes submitted text and returns:

- `prediction`
- `confidence`
- `risk_level`

Example request:

```json
{
  "text": "Your account has been suspended. Click here to verify immediately."
}
```

### `POST /chat`

Generates an AI-assisted explanation based on the current prediction context.

Example request:

```json
{
  "message": "Why is this suspicious?",
  "prediction": "phishing",
  "confidence": 0.97,
  "risk_level": "High"
}
```

## Notes

- The backend is configured for local development with CORS allowed from `http://localhost:3000` and `http://127.0.0.1:3000`.
- The model files are already stored in the repository under `backend/model/phishing_bert/`.
- If the backend cannot find the model or a dependency is missing, check the Python environment and installed packages first.

