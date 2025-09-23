import os
from datetime import datetime

import pandas as pd


THRESHOLD_STR = "2025-01-05"
THRESHOLD = datetime(2025, 1, 5)
SOURCE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "violations.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def parse_dates(df: pd.DataFrame, date_col: str = "First Occurrence") -> pd.DataFrame:
    if date_col not in df.columns:
        raise KeyError(f"Expected date column '{date_col}' not found in CSV. Available: {list(df.columns)}")

    # Input format example: 08/13/2025 08:52:12 AM
    fmt = "%m/%d/%Y %I:%M:%S %p"
    df["_parsed_date"] = pd.to_datetime(df[date_col], format=fmt, errors="coerce")

    # Report rows that failed to parse (if any)
    invalid = df["_parsed_date"].isna().sum()
    if invalid:
        print(f"Warning: {invalid} row(s) had unparseable '{date_col}' values and will be labeled as 'unknown'.")

    return df


def label_period(df: pd.DataFrame) -> pd.DataFrame:
    def classify(ts: pd.Timestamp) -> str:
        if pd.isna(ts):
            return "unknown"
        return "before" if ts.to_pydatetime() < THRESHOLD else "after"

    df["period"] = df["_parsed_date"].map(classify)
    return df


def save_outputs(df: pd.DataFrame, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    labeled_path = os.path.join(output_dir, "violations_with_period.csv")
    before_path = os.path.join(output_dir, "violations_before.csv")
    after_path = os.path.join(output_dir, "violations_after.csv")

    # Save labeled full dataset
    df.drop(columns=["_parsed_date"], errors="ignore").to_csv(labeled_path, index=False)

    # Save splits
    df[df["period"] == "before"].drop(columns=["_parsed_date"], errors="ignore").to_csv(before_path, index=False)
    df[df["period"] == "after"].drop(columns=["_parsed_date"], errors="ignore").to_csv(after_path, index=False)

    print(f"Wrote: {labeled_path}")
    print(f"Wrote: {before_path}")
    print(f"Wrote: {after_path}")


def summarize(df: pd.DataFrame):
    counts = df["period"].value_counts(dropna=False).to_dict()
    print("Summary by period:")
    for k in ("before", "after", "unknown"):
        if k in counts:
            print(f"  {k}: {counts[k]}")


def main():
    print(f"Loading data from: {SOURCE_PATH}")
    df = load_data(SOURCE_PATH)
    df = parse_dates(df, date_col="First Occurrence")
    df = label_period(df)
    summarize(df)
    save_outputs(df, OUTPUT_DIR)
    print(f"Threshold used: {THRESHOLD_STR} (exclusive: before < {THRESHOLD_STR}, else after)")


if __name__ == "__main__":
    main()