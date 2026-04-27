from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from preprocess import preprocess_text


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample_dataset.csv"
MODEL_DIR = BASE_DIR / "artifacts"
MODEL_DIR.mkdir(exist_ok=True)


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["text", "label"])
    df["processed_text"] = df["text"].astype(str).apply(preprocess_text)
    return df


def build_models():
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ("clf", LogisticRegression(max_iter=1000)),
            ]
        ),
        "naive_bayes": Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ("clf", MultinomialNB()),
            ]
        ),
    }


def evaluate_model(model, x_test, y_test):
    preds = model.predict(x_test)
    accuracy = accuracy_score(y_test, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, preds, average="weighted", zero_division=0)
    report = classification_report(y_test, preds, zero_division=0, output_dict=True)
    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "report": report,
    }


def train_and_save() -> None:
    df = load_dataset()
    labels = df["label"]
    n_classes = labels.nunique()
    n_rows = len(df)
    min_test_size = n_classes / n_rows if n_rows else 0.25
    test_size = max(0.25, min_test_size)
    test_size = min(test_size, 0.5)

    try:
        x_train, x_test, y_train, y_test = train_test_split(
            df["processed_text"], labels, test_size=test_size, random_state=42, stratify=labels
        )
    except ValueError:
        # Fallback for very small datasets where stratified split is not feasible.
        x_train, x_test, y_train, y_test = train_test_split(
            df["processed_text"], labels, test_size=test_size, random_state=42
        )

    models = build_models()
    metrics = {}
    best_name = None
    best_accuracy = -1.0
    best_model = None

    for name, model in models.items():
        model.fit(x_train, y_train)
        eval_metrics = evaluate_model(model, x_test, y_test)
        metrics[name] = eval_metrics
        if eval_metrics["accuracy"] > best_accuracy:
            best_accuracy = eval_metrics["accuracy"]
            best_name = name
            best_model = model

    payload = {
        "best_model_name": best_name,
        "all_metrics": metrics,
    }
    joblib.dump(best_model, MODEL_DIR / "best_model.joblib")
    joblib.dump(payload, MODEL_DIR / "metrics.joblib")
    print(f"Training complete. Best model: {best_name} ({best_accuracy:.4f})")


if __name__ == "__main__":
    train_and_save()
