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

The backend uses FastAPI and loads the saved phishing BERT model from `backend/model/phishing_bert/` by default.

Install the Python dependencies you need for the backend:

```bash
pip install -r backend/requirements.txt
```

Run the backend from the project root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```bash
http://127.0.0.1:8000
```

If you deploy the model somewhere else, set:

```bash
MODEL_SOURCE
```

If you want the assistant responses to use Groq, set:

```bash
GROQ_API_KEY
GROQ_MODEL
```

If your frontend is deployed on Netlify, set:

```bash
CORS_ORIGINS
```

Use a comma-separated list of allowed origins, for example:

```bash
CORS_ORIGINS=https://your-site.netlify.app
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

For a Netlify deployment, set this to your Render backend URL at build time.

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
- The model files are expected in `backend/model/phishing_bert/` unless `MODEL_SOURCE` points somewhere else.
- The model artifact is large, so it is usually better to keep it outside the Git repo and point `MODEL_SOURCE` at a hub or storage location.
- If the model checkpoint is unavailable at deploy time, the backend will now start with a lightweight heuristic fallback instead of crashing. Set `MODEL_SOURCE` to a valid Hugging Face repo id or local path if you want the full BERT model in production.
- Groq powers the assistant-style chat responses when `GROQ_API_KEY` is set.
- If the backend cannot find the model or a dependency is missing, check the Python environment and installed packages first.

## Deployment settings

### Netlify

- Base directory: `frontend`
- Build command: `npm run build`
- Publish directory: `build`
- Environment variable: `REACT_APP_API_BASE_URL=https://your-render-backend.onrender.com`

### Render

- Root directory: repository root
- Build command: `pip install -r backend/requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Environment variable: `CORS_ORIGINS=https://your-site.netlify.app`
- Environment variable: `GROQ_API_KEY=your_groq_key`
- Optional environment variable: `GROQ_MODEL=llama-3.1-8b-instant`
- Optional environment variable: `MODEL_SOURCE=<local-path-or-hub-id>`
