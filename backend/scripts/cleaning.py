import os
from datetime import datetime

import pandas as pd


THRESHOLD_STR = "2025-01-05"
THRESHOLD = datetime(2025, 1, 5)
SOURCE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "violations.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Bus route groupings for CBD analysis
ALWAYS_CBD_ROUTES = {"M34+", "M42"}
PARTIAL_CBD_ROUTES = {"M2", "M15+", "M4", "M101"}


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


def label_cbd_group(df: pd.DataFrame) -> pd.DataFrame:
    """Add a column 'cbd_group' classifying bus routes by CBD coverage."""
    route_col = "Bus Route ID"
    if route_col not in df.columns:
        # If the column is missing, default to 'other'
        df["cbd_group"] = "other"
        return df

    def classify_route(val: object) -> str:
        s = str(val).strip().upper()
        if s in ALWAYS_CBD_ROUTES:
            return "always_cbd"
        if s in PARTIAL_CBD_ROUTES:
            return "partial_cbd"
        return "other"

    df["cbd_group"] = df[route_col].map(classify_route)
    return df


def save_outputs(df: pd.DataFrame, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # Columns to drop
    columns_to_drop = [
        "Stop ID", "Stop Name",
        "Bus Stop Latitude", "Bus Stop Longitude", "Bus Stop Georeference",
        "Violation ID"
    ]

    # Drop the columns (if they exist)
    df_cleaned = df.drop(columns=columns_to_drop, errors="ignore")

    labeled_path = os.path.join(output_dir, "violations_with_period.csv")
    before_path = os.path.join(output_dir, "violations_before.csv")
    after_path = os.path.join(output_dir, "violations_after.csv")
    # New: split by CBD route groups (always/partial) and period (before/after)
    # Consolidated CBD files (contain both periods)
    partial_all_path = os.path.join(output_dir, "violations_partial_cbd.csv")
    always_all_path = os.path.join(output_dir, "violations_always_cbd.csv")

    # Save labeled full dataset (keep 'cbd_group' for downstream analysis)
    base = df_cleaned.drop(columns=["_parsed_date"], errors="ignore")
    base.to_csv(labeled_path, index=False)

    # Save splits
    base[base["period"] == "before"].to_csv(before_path, index=False)
    base[base["period"] == "after"].to_csv(after_path, index=False)

    # New: Save consolidated CBD group files (both before and after in one file)
    base[base["cbd_group"] == "partial_cbd"].to_csv(partial_all_path, index=False)
    base[base["cbd_group"] == "always_cbd"].to_csv(always_all_path, index=False)

    print(f"Wrote: {labeled_path}")
    print(f"Wrote: {before_path}")
    print(f"Wrote: {after_path}")
    print(f"Wrote: {partial_all_path}")
    print(f"Wrote: {always_all_path}")



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
    df = label_cbd_group(df)
    summarize(df)
    save_outputs(df, OUTPUT_DIR)
    print(f"Threshold used: {THRESHOLD_STR} (exclusive: before < {THRESHOLD_STR}, else after)")


if __name__ == "__main__":
    main()
