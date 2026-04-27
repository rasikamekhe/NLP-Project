<<<<<<< HEAD
# AI-Based Cybersecurity Threat Intelligence System using NLP

End-to-end project to detect and classify cyber threats from text inputs (emails, logs, reports) using NLP + machine learning, with a FastAPI backend and React dashboard.

## Features

- Threat detection categories: `phishing`, `spam`, `malware`, `brute_force`, `insider_threat`, `normal`
- NLP preprocessing: tokenization, stopword removal, lemmatization
- ML models: Logistic Regression and Naive Bayes with TF-IDF
- Model comparison with metrics: Accuracy, Precision, Recall, F1-score
- REST API: `POST /predict`, `POST /login`, `GET /metrics`, `GET /history`
- SQLite persistence for users and prediction history
- Dashboard charts: threat distribution (pie) + model accuracy comparison (bar)
- Safe vs malicious color indicators
- Basic authentication screen

## Project Structure

```text
backend/
├── app.py
├── model.py
├── preprocess.py
├── train.py
├── data_loader.py
├── database.py
├── requirements.txt
├── data/
│   └── sample_dataset.csv
└── tests/
    └── sample_inputs.json

frontend/
├── package.json
├── public/
│   └── index.html
└── src/
    ├── App.js
    ├── api.js
    ├── index.js
    ├── styles.css
    └── components/
        ├── Dashboard.js
        └── Login.js
```

## Dataset

- Included local dataset: `backend/data/sample_dataset.csv`
- Optional open-source dataset script: `backend/data_loader.py`
  - Source used: [SMS Spam Collection (UCI derivative)](https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv)
- Kaggle option (recommended for larger training): [Phishing Email Dataset](https://www.kaggle.com/datasets/subhajournal/phishingemails)

## Backend Setup (FastAPI)

1. Open terminal in project root.
2. Create and activate virtual environment:

   - Windows PowerShell:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. Install dependencies:

   ```powershell
   pip install -r backend/requirements.txt
   ```

4. Train model:

   ```powershell
   cd backend
   python train.py
   cd ..
   ```

5. Start API server:

   ```powershell
   uvicorn backend.app:app --reload
   ```

API will run on `http://127.0.0.1:8000`.

## Frontend Setup (React)

1. Open another terminal in project root.
2. Install frontend dependencies:

   ```powershell
   cd frontend
   npm install
   ```

3. Start frontend:

   ```powershell
   npm start
   ```

Frontend runs on `http://localhost:3000`.

## API Usage

### Login

`POST /login`

```json
{
  "username": "admin",
  "password": "admin123"
}
```

### Predict

`POST /predict`

```json
{
  "username": "admin",
  "text": "Repeated failed login attempts from external IP."
}
```

Response:

```json
{
  "prediction": "brute_force",
  "confidence": 0.88,
  "probabilities": {
    "brute_force": 0.88,
    "normal": 0.07
  },
  "is_malicious": true
}
```

## Testing Inputs

Sample test file: `backend/tests/sample_inputs.json`

Expected examples:

- `Reset your account immediately by clicking this unknown link.` -> `phishing`
- `Repeated login failure for root user from a single host.` -> `brute_force`
- `Team sync meeting is postponed to tomorrow.` -> `normal`

## Notes on Code Quality

- Separation of concerns:
  - `preprocess.py` for NLP pipeline
  - `train.py` for training/evaluation
  - `model.py` for model loading/inference
  - `app.py` for API endpoints
  - `database.py` for persistence
- Frontend is component-based and API-driven.

## Suggested Upgrades

1. BERT/Transformers integration:
   - Use `sentence-transformers` embeddings or fine-tuned `bert-base-uncased`.
   - Replace TF-IDF features with dense embeddings for better semantic understanding.
2. Real-time streaming:
   - Add Kafka + Spark/Flink consumer for live SIEM logs.
   - Trigger predictions asynchronously and push updates via WebSocket.
3. Security improvements:
   - Hash passwords with `bcrypt`.
   - Add JWT-based auth and role-based access.
4. MLOps:
   - Add model versioning (MLflow), drift monitoring, and scheduled retraining.

=======
# NLP-Project
DeepShield: AI-Powered Cyber Threat Detection using NLP
>>>>>>> 1d2bcea1a85ba823952267ff3fb719ba86b2fddd
