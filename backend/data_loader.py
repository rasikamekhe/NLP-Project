from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def export_from_url() -> None:
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_csv(url, sep="\t", names=["label", "text"])
    mapping = {"ham": "normal", "spam": "spam"}
    df["label"] = df["label"].map(mapping).fillna("normal")
    out_path = DATA_DIR / "sms_spam_from_source.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved dataset to {out_path}")


if __name__ == "__main__":
    export_from_url()
