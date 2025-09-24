import os
import pandas as pd
from datetime import datetime

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LABELED_PATH = os.path.join(DATA_DIR, "violations_with_period.csv")
CONCLUSIONS_PATH = os.path.join(DATA_DIR, "conclusions.txt")

# Threshold date
THRESHOLD = datetime(2025, 1, 5)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "period" not in df.columns:
        raise KeyError("Expected column 'period' not found. Run cleaning.py first.")
    return df


def monthly_trends(df: pd.DataFrame):
    """Frequency of violations before and after congestion pricing, grouped monthly."""
    # Parse from source column; cleaned CSV does not include _parsed_date
    fmt = "%m/%d/%Y %I:%M:%S %p"
    df["_date"] = pd.to_datetime(df["First Occurrence"], format=fmt, errors="coerce")
    df["_month"] = df["_date"].dt.to_period("M")

    monthly_counts = (
        df.dropna(subset=["_month"])
          .groupby(["period", "_month"])
          .size()
          .unstack(fill_value=0)
    )

    print("\n=== Monthly Trends ===")
    # Show months as rows for readability
    print(monthly_counts.T)
    return monthly_counts


def violation_types(df: pd.DataFrame):
    """Most common violation types before and after congestion pricing."""
    counts = (
        df.groupby(["period", "Violation Type"])
          .size()
          .unstack(fill_value=0)
          .T
    )

    print("\n=== Violation Types Before vs After ===")
    print(counts)
    return counts


def violation_type_changes(df: pd.DataFrame):
    """Which violation types increased/decreased the most after congestion pricing."""
    # Pivot so rows are violation types and columns are periods
    counts = (
        df.groupby(["Violation Type", "period"]).size()
          .unstack(fill_value=0)
          .fillna(0)
    )

    # Ensure expected columns exist
    if "before" not in counts.columns:
        counts["before"] = 0
    if "after" not in counts.columns:
        counts["after"] = 0

    # Calculate change: after - before per violation type
    counts["change"] = counts["after"] - counts["before"]

    most_increased = counts["change"].idxmax() if not counts.empty else None
    most_decreased = counts["change"].idxmin() if not counts.empty else None

    print("\n=== Violation Type Changes ===")
    print(counts.sort_values("change", ascending=False))
    if most_increased is not None:
        print(f"\nMost Increased: {most_increased} (+{counts.loc[most_increased, 'change']})")
    if most_decreased is not None:
        print(f"Most Decreased: {most_decreased} ({counts.loc[most_decreased, 'change']})")

    return counts


def main():
    print(f"Loading labeled data from: {LABELED_PATH}")
    df = load_data(LABELED_PATH)

    # Q1: Monthly trends
    monthly = monthly_trends(df)

    # Q2: Common violation types before vs after
    types_counts = violation_types(df)

    # Q3: Which violation types increased/decreased the most
    change_counts = violation_type_changes(df)

    # Write all outputs to a single text file
    try:
        with open(CONCLUSIONS_PATH, "w", encoding="utf-8") as f:
            f.write("=== Conclusions Report ===\n")
            f.write(f"Source: {LABELED_PATH}\n")
            f.write(f"Threshold: {THRESHOLD.date()} (before < threshold, else after)\n")
            f.write("\n--- Monthly Trends (months as rows) ---\n")
            f.write(monthly.T.to_string())
            f.write("\n\n--- Violation Types Before vs After ---\n")
            f.write(types_counts.to_string())
            # For change summary, include sorted table and top changes
            f.write("\n\n--- Violation Type Changes (after - before) ---\n")
            sorted_changes = change_counts.sort_values("change", ascending=False)
            f.write(sorted_changes.to_string())
            if not change_counts.empty:
                most_inc = sorted_changes.index[0]
                most_dec = sorted_changes.index[-1]
                f.write("\n\nSummary:\n")
                f.write(f"Most Increased: {most_inc} (+{sorted_changes.loc[most_inc, 'change']})\n")
                f.write(f"Most Decreased: {most_dec} ({sorted_changes.loc[most_dec, 'change']})\n")
        print(f"\nWrote conclusions to: {CONCLUSIONS_PATH}")
    except Exception as e:
        print(f"Failed to write conclusions: {e}")


if __name__ == "__main__":
    main()
