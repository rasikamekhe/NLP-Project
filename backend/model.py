from pathlib import Path
from typing import Any, Dict

import joblib
import traceback

try:
    from .preprocess import preprocess_text
except ImportError:
    from preprocess import preprocess_text


BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
PIPELINE_PATH = ARTIFACTS_DIR / "best_model.joblib"
MODEL_PATH = ARTIFACTS_DIR / "model.pkl"
VECTORIZER_PATH = ARTIFACTS_DIR / "vectorizer.pkl"
METRICS_PATH = ARTIFACTS_DIR / "metrics.joblib"


class ThreatModelService:
    def __init__(self) -> None:
        self.model = None
        self.vectorizer = None
        self.metrics: Dict[str, Any] = {}

    def load(self) -> None:
        print(f"[model] Loading artifacts from: {ARTIFACTS_DIR}")

        # Prefer a single pipeline artifact if available.
        if PIPELINE_PATH.exists():
            self.model = joblib.load(PIPELINE_PATH)
            self.vectorizer = None
            print(f"[model] Loaded pipeline: {PIPELINE_PATH}")
        else:
            missing = [p for p in (MODEL_PATH, VECTORIZER_PATH) if not p.exists()]
            if missing:
                missing_list = ", ".join(str(p) for p in missing)
                raise FileNotFoundError(
                    "Model artifacts missing. Expected either "
                    f"'{PIPELINE_PATH.name}' OR both '{MODEL_PATH.name}' and '{VECTORIZER_PATH.name}'. "
                    f"Missing: {missing_list}. Run python train.py first."
                )
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            print(f"[model] Loaded model: {MODEL_PATH}")
            print(f"[model] Loaded vectorizer: {VECTORIZER_PATH}")

        if METRICS_PATH.exists():
            self.metrics = joblib.load(METRICS_PATH)
            print(f"[model] Loaded metrics: {METRICS_PATH}")
        else:
            self.metrics = {}
            print(f"[model] Metrics not found (continuing): {METRICS_PATH}")

    def predict(self, text: str) -> Dict[str, Any]:
        try:
            if self.model is None:
                self.load()
            print(f"[model] Predict input (raw): {text!r}")
            processed = preprocess_text(text)
            print(f"[model] Predict input (processed): {processed!r}")

            if self.vectorizer is not None:
                X = self.vectorizer.transform([processed])
                pred_label = self.model.predict(X)[0]
                probabilities = self.model.predict_proba(X)[0]
            else:
                pred_label = self.model.predict([processed])[0]
                probabilities = self.model.predict_proba([processed])[0]

            classes = list(self.model.classes_)
            confidence = float(max(probabilities))
            proba_by_class = {label: float(probabilities[i]) for i, label in enumerate(classes)}
            result = {
                "prediction": str(pred_label),
                "confidence": confidence,
                "probabilities": proba_by_class,
                "is_malicious": pred_label != "normal",
            }
            print(f"[model] Predict output: {result}")
            return result
        except Exception as exc:
            print(f"[model] Predict error: {exc!r}")
            traceback.print_exc()
            raise RuntimeError(str(exc)) from exc

    def get_metrics(self) -> Dict[str, Any]:
        if self.metrics:
            return self.metrics

        # If metrics don't exist, return a safe default instead of crashing.
        if not METRICS_PATH.exists():
            return {}

        if self.model is None:
            self.load()
        return self.metrics

