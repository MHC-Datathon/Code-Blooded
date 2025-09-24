import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
VIOLATIONS_PATH = os.path.join(DATA_DIR, "violations_with_period.csv")
ALWAYS_CBD_PATH = os.path.join(DATA_DIR, "violations_always_cbd.csv")
PARTIAL_CBD_PATH = os.path.join(DATA_DIR, "violations_partial_cbd.csv")

# Threshold date for congestion pricing
THRESHOLD = datetime(2025, 1, 5)


def load_data(path: str) -> pd.DataFrame:
    """Loads a CSV file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}. Please ensure cleaning.py has been run.")
    return pd.read_csv(path)


def add_year_periods(df: pd.DataFrame) -> pd.DataFrame:
    """Assigns period labels per year before congestion pricing, else 'after'."""
    fmt = "%m/%d/%Y %I:%M:%S %p"
    df["_date"] = pd.to_datetime(df["First Occurrence"], format=fmt, errors="coerce")

    def label_period(d):
        if pd.isna(d):
            return None
        if d < THRESHOLD:
            return str(d.year)
        else:
            return "after"

    df["period"] = df["_date"].apply(label_period)
    return df


def monthly_trends(df: pd.DataFrame):
    """Plots average monthly violations with years on left and 'after' on right."""
    df["_month"] = df["_date"].dt.to_period("M")

    monthly_counts = (
        df.dropna(subset=["_month"])
        .groupby(["period", "_month"], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    avg_monthly_counts = monthly_counts.mean(axis=1)

    ordered_index = sorted([p for p in avg_monthly_counts.index if p != "after"], key=int) + ["after"]
    avg_monthly_counts = avg_monthly_counts.reindex(ordered_index)

    colors = ["blue" if p != "after" else "orange" for p in avg_monthly_counts.index]

    avg_monthly_counts.plot(kind='bar', figsize=(12, 6), color=colors)
    plt.title("Average Monthly Violations (2019–2024 vs After Congestion Pricing)")
    plt.xlabel("Period")
    plt.ylabel("Average Number of Violations (per Month)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(handles=[
        plt.Rectangle((0,0),1,1,color="blue", label="Before (2019–2024)"),
        plt.Rectangle((0,0),1,1,color="orange", label="After (2025)")
    ])
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "monthly_trends_bar_chart.png"))
    plt.close()


def daily_trends(df: pd.DataFrame):
    """Calculates daily violation trends by year + after."""
    df["_day_of_week"] = df["_date"].dt.day_name()
    df["_month"] = df["_date"].dt.to_period("M")

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["_day_of_week"] = pd.Categorical(df["_day_of_week"], categories=order, ordered=True)

    daily_counts = (
        df.dropna(subset=["_day_of_week", "_month"])
        .groupby(["period", "_day_of_week", "_month"], observed=False)
        .size()
        .groupby(level=[0, 1], observed=False).mean()
        .unstack(fill_value=0)
        .reindex(columns=order, fill_value=0)
        .T
    )

    periods = daily_counts.columns.tolist()
    color_map = {
        "2019": "royalblue",
        "2020": "forestgreen",
        "2021": "crimson",
        "2022": "purple",
        "2023": "gold",
        "2024": "darkred",
        "after": "orange"
    }
    colors = [color_map.get(p, "gray") for p in periods]

    daily_counts.plot(kind='bar', figsize=(14, 8), color=colors)
    plt.title("Average Monthly Violations by Day of Week (2019–2024 vs After)")
    plt.xlabel("Day of the Week")
    plt.ylabel("Average Violations per Month")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Period")
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "daily_trends_grouped_bar.png"))
    plt.close()


def get_monthly_counts_by_violation_type(df: pd.DataFrame) -> pd.DataFrame:
    """Helper: average monthly counts for each violation type."""
    df["_month"] = df["_date"].dt.to_period("M")

    monthly_violation_counts = (
        df.dropna(subset=["_month"])
        .groupby(["Violation Type", "period", "_month"], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    avg_monthly_counts = monthly_violation_counts.mean(axis=1).unstack(fill_value=0)
    avg_monthly_counts.columns.name = None
    return avg_monthly_counts


def violation_types_stacked(df: pd.DataFrame):
    """Plots most common violation types using monthly averages."""
    counts = get_monthly_counts_by_violation_type(df)

    periods = counts.columns.tolist()
    color_map = {
        "2019": "royalblue",
        "2020": "forestgreen",
        "2021": "crimson",
        "2022": "purple",
        "2023": "gold",
        "2024": "darkred",
        "after": "orange"
    }
    colors = [color_map.get(p, "gray") for p in periods]

    counts.plot(kind='bar', stacked=True, figsize=(14, 8), color=colors)
    plt.title("Average Monthly Violations by Type (2019–2024 vs After)")
    plt.xlabel("Violation Type")
    plt.ylabel("Average Violations per Month")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Period")
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "violation_types_stacked_bar.png"))
    plt.close()


def violation_type_changes(df: pd.DataFrame):
    """Plots grouped bar chart showing before (all years) vs after."""
    df["_month"] = df["_date"].dt.to_period("M")
    df["collapsed_period"] = df["period"].apply(lambda p: "before" if p != "after" else "after")

    monthly_violation_counts = (
        df.dropna(subset=["_month"])
        .groupby(["Violation Type", "collapsed_period", "_month"], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    avg_monthly_counts = monthly_violation_counts.mean(axis=1).unstack(fill_value=0)

    avg_monthly_counts[["before", "after"]].plot(kind='bar', figsize=(14, 8), color=["blue", "orange"])
    plt.title("Average Monthly Violation Counts (Before vs After Congestion Pricing)")
    plt.xlabel("Violation Type")
    plt.ylabel("Average Violations per Month")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "violation_change_grouped_bar.png"))
    plt.close()

    return avg_monthly_counts


def cbd_vs_partial_comparison():
    """Plots CBD and Partial CBD buses individually, collapsing years into 'before'."""
    df_always = add_year_periods(load_data(ALWAYS_CBD_PATH))
    df_partial = add_year_periods(load_data(PARTIAL_CBD_PATH))

    df_all = pd.concat([df_always, df_partial], ignore_index=True)
    df_all["_month"] = df_all["_date"].dt.to_period("M")

    # Collapse years into before vs after
    df_all["collapsed_period"] = df_all["period"].apply(lambda p: "before" if p != "after" else "after")

    monthly_counts = (
        df_all.dropna(subset=["_month"])
        .groupby(["Bus Route ID", "collapsed_period", "_month"], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    avg_monthly_counts = monthly_counts.mean(axis=1).unstack(fill_value=0)

    avg_monthly_counts[["before", "after"]].plot(kind='bar', figsize=(14, 8), color=["blue", "orange"])
    plt.title("Average Monthly Violations by Bus (Before vs After Congestion Pricing)")
    plt.xlabel("Bus Route ID")
    plt.ylabel("Average Violations per Month")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "cbd_comparison_grouped_bar.png"))
    plt.close()

    return avg_monthly_counts


def generate_summary_file(df: pd.DataFrame):
    """Generates a summary file with explanations and numbers."""
    summary_path = os.path.join(DATA_DIR, "summary.txt")

    df["_month"] = df["_date"].dt.to_period("M")

    # 1. Overall frequency
    violations_per_period = df.groupby("period", observed=False).size()
    months_per_period = df.groupby("period", observed=False)["_month"].nunique()
    avg_monthly = (violations_per_period / months_per_period).fillna(0)

    # 2. Most common violation types
    counts = get_monthly_counts_by_violation_type(df)
    most_common_before = counts.drop(columns=["after"], errors="ignore").mean(axis=1).idxmax()
    most_common_after = counts["after"].idxmax() if "after" in counts.columns else "N/A"

    count_before = counts.drop(columns=["after"], errors="ignore").mean(axis=1).max()
    count_after = counts["after"].max() if "after" in counts.columns else 0

    # 3. Most increased/decreased
    df["collapsed_period"] = df["period"].apply(lambda p: "before" if p != "after" else "after")
    monthly_violation_counts = (
        df.dropna(subset=["_month"])
        .groupby(["Violation Type", "collapsed_period", "_month"], observed=False)
        .size()
        .unstack(fill_value=0)
    )
    avg_monthly_counts = monthly_violation_counts.mean(axis=1).unstack(fill_value=0)
    avg_monthly_counts["change"] = avg_monthly_counts["after"] - avg_monthly_counts["before"]
    avg_monthly_counts["percent_change"] = (avg_monthly_counts["change"] / avg_monthly_counts["before"]) * 100

    most_increased = avg_monthly_counts["percent_change"].idxmax()
    most_decreased = avg_monthly_counts["percent_change"].idxmin()

    increased_before = avg_monthly_counts.loc[most_increased, "before"]
    increased_after = avg_monthly_counts.loc[most_increased, "after"]
    percent_change_increased = avg_monthly_counts.loc[most_increased, "percent_change"]

    decreased_before = avg_monthly_counts.loc[most_decreased, "before"]
    decreased_after = avg_monthly_counts.loc[most_decreased, "after"]
    percent_change_decreased = avg_monthly_counts.loc[most_decreased, "percent_change"]

    # 4. CBD vs Partial CBD buses individually
    df_always = add_year_periods(load_data(ALWAYS_CBD_PATH))
    df_partial = add_year_periods(load_data(PARTIAL_CBD_PATH))
    df_all = pd.concat([df_always, df_partial], ignore_index=True)
    df_all["_month"] = df_all["_date"].dt.to_period("M")
    df_all["collapsed_period"] = df_all["period"].apply(lambda p: "before" if p != "after" else "after")

    bus_monthly_counts = (
        df_all.dropna(subset=["_month"])
        .groupby(["Bus Route ID", "collapsed_period", "_month"], observed=False)
        .size()
        .unstack(fill_value=0)
    )
    avg_bus_counts = bus_monthly_counts.mean(axis=1).unstack(fill_value=0)
    avg_bus_counts["change"] = avg_bus_counts["after"] - avg_bus_counts["before"]

    # Safe percent change (ignore buses with no before data)
    avg_bus_counts["percent_change"] = np.where(
        avg_bus_counts["before"] > 0,
        (avg_bus_counts["change"] / avg_bus_counts["before"]) * 100,
        np.nan
    )

    cbd_buses = ["M34+", "M42"]
    partial_buses = ["M2", "M15+", "M4", "M101"]

    cbd_avg_change = avg_bus_counts.loc[cbd_buses, "percent_change"].dropna().mean()
    partial_avg_change = avg_bus_counts.loc[partial_buses, "percent_change"].dropna().mean()

    summary_text = f"""### Bus Violation Analysis for Congestion Pricing

⚠️ Important Note: The 'before' period is split into years (2019–2024), while the 'after' period includes <1 year (since Jan 5, 2025).
To account for this imbalance, all comparisons are reported as *average monthly violations*.

---

### 1. Overall Frequency
Violations steadily declined from 2019 through 2024. After congestion pricing began in 2025, average monthly violations increased relative to recent years.

Average monthly counts (per period):
{avg_monthly.to_string()}

---

### 2. Most Common Violation Types
Before congestion pricing: "{most_common_before}" with ~{count_before:.1f} avg monthly violations  
After congestion pricing: "{most_common_after}" with ~{count_after:.1f} avg monthly violations

---

### 3. Violations with the Most Change
The violation type that saw the most significant increase after congestion pricing was "{most_increased}".  
It increased from {increased_before:.1f} → {increased_after:.1f}, a change of {percent_change_increased:+.1f}%.

"{most_decreased}" experienced the largest decrease.  
It dropped from {decreased_before:.1f} → {decreased_after:.1f}, a change of {percent_change_decreased:+.1f}%.  
This suggests the new policy may have had a positive impact on this specific behavior.

---

### 4. CBD vs Partial CBD Buses
Individual bus percent changes (before → after, NaN = no before data):
{avg_bus_counts[["before", "after", "percent_change"]].to_string()}

On average, CBD-only buses (M34+, M42) changed by {cbd_avg_change:+.1f}%.  
Partial-CBD buses (M2, M15+, M4, M101) changed by {partial_avg_change:+.1f}%.

Conclusion: {"CBD-only buses increased more." if cbd_avg_change > partial_avg_change else "Partial-CBD buses increased more."}
"""

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"\nSummary saved to {summary_path}")


def main():
    if not os.path.exists("visuals"):
        os.makedirs("visuals")

    print("Loading data...")
    df_full = add_year_periods(load_data(VIOLATIONS_PATH))

    print("Generating monthly trend bar chart...")
    monthly_trends(df_full)

    print("Generating daily trend grouped bar chart...")
    daily_trends(df_full)

    print("Generating stacked bar chart for violation types...")
    violation_types_stacked(df_full)

    print("Generating grouped bar chart for violation changes...")
    violation_type_changes(df_full)

    print("Generating CBD vs. Partial CBD comparison chart...")
    cbd_vs_partial_comparison()

    print("Generating analysis summary file...")
    generate_summary_file(df_full)


if __name__ == "__main__":
    main()
