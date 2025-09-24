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
    """Loads a CSV file and validates the 'period' column."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}. Please ensure cleaning.py has been run.")
    df = pd.read_csv(path)
    if "period" not in df.columns:
        raise KeyError("Expected column 'period' not found. Run cleaning.py first.")
    return df

def plot_bar_chart(data: pd.DataFrame, x_col: str, title: str, xlabel: str, ylabel: str, filename: str):
    """
    Generates a simple bar chart.
    data: DataFrame with 'before' and 'after' columns.
    x_col: The column to use for x-axis labels.
    """
    data.plot(kind='bar', figsize=(10, 6))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", filename))
    plt.close()

def plot_stacked_bar_chart(data: pd.DataFrame, title: str, xlabel: str, ylabel: str, filename: str):
    """
    Generates a stacked bar chart.
    data: DataFrame with 'before' and 'after' columns.
    """
    data.T.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title='Violation Type')
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", filename))
    plt.close()

def plot_diverging_bar_chart(data: pd.DataFrame, title: str, xlabel: str, ylabel: str, filename: str):
    """
    Generates a diverging bar chart to show increases/decreases.
    data: DataFrame with a 'change' column.
    """
    data = data.sort_values(by="change", ascending=True)
    df_plot = data.reset_index()
    df_plot['colors'] = ['red' if x < 0 else 'green' for x in df_plot['change']]
    plt.figure(figsize=(12, 8))
    plt.hlines(y=df_plot.index, xmin=0, xmax=df_plot['change'], color=df_plot['colors'], alpha=0.7)
    plt.scatter(x=df_plot['change'], y=df_plot.index, s=120, color=df_plot['colors'], alpha=0.9)
    plt.yticks(df_plot.index, labels=df_plot['Violation Type'])
    plt.title(title, fontdict={'size': 20})
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", filename))
    plt.close()

def monthly_trends(df: pd.DataFrame):
    """Calculates monthly violation trends and plots the average monthly violations."""
    fmt = "%m/%d/%Y %I:%M:%S %p"
    df["_date"] = pd.to_datetime(df["First Occurrence"], format=fmt, errors="coerce")
    df["_month"] = df["_date"].dt.to_period("M")
    
    monthly_counts = (
        df.dropna(subset=["_month"])
        .groupby(["period", "_month"], observed=False)
        .size()
        .unstack(fill_value=0)
    )
    
    # Calculate average monthly violations per period and reorder them
    avg_monthly_counts = monthly_counts.mean(axis=1).reindex(['before', 'after'])
    
    # Plotting with the specified colors
    ax = avg_monthly_counts.plot(kind='bar', figsize=(10, 6), color=['blue', 'orange'])
    
    plt.title("Average Monthly Violations Before and After Congestion Pricing")
    plt.xlabel("Period")
    plt.ylabel("Average Number of Violations")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "monthly_trends_bar_chart.png"))
    plt.close()

def daily_trends(df: pd.DataFrame):
    """Calculates daily violation trends and plots them."""
    fmt = "%m/%d/%Y %I:%M:%S %p"
    df["_date"] = pd.to_datetime(df["First Occurrence"], format=fmt, errors="coerce")
    df["_day_of_week"] = df["_date"].dt.day_name()
    
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["_day_of_week"] = pd.Categorical(df["_day_of_week"], categories=order, ordered=True)
    
    daily_counts = (
        df.dropna(subset=["_day_of_week"])
        .groupby(["period", "_day_of_week"], observed=False)
        .size()
        .unstack(fill_value=0)
    ).reindex(columns=order, fill_value=0).T
    
    # Plotting with the specified colors
    daily_counts.plot(kind='bar', figsize=(12, 8), color={'before': 'blue', 'after': 'orange'})
    plt.title("Daily Violations Before and After Congestion Pricing")
    plt.xlabel("Day of the Week")
    plt.ylabel("Number of Violations")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "daily_trends_grouped_bar.png"))
    plt.close()
    
def get_monthly_counts_by_violation_type(df: pd.DataFrame) -> pd.DataFrame:
    """Helper function to get monthly average counts for each violation type."""
    df["_date"] = pd.to_datetime(df["First Occurrence"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
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
    """Calculates and plots the most common violation types using monthly averages."""
    counts = get_monthly_counts_by_violation_type(df)
    
    # Reorder columns to ensure 'before' is on the left
    counts = counts.reindex(['before', 'after'], axis=1)

    plot_stacked_bar_chart(
        counts, 
        "Average Monthly Violations by Type Before and After Congestion Pricing",
        "Violation Type", "Average Number of Violations", 
        "violation_types_stacked_bar.png"
    )

def violation_type_changes(df: pd.DataFrame):
    """Calculates which violation types increased/decreased the most and plots."""
    counts = get_monthly_counts_by_violation_type(df)
    
    if "before" not in counts.columns:
        counts["before"] = 0
    if "after" not in counts.columns:
        counts["after"] = 0

    # Calculate percent change, handling division by zero
    counts['percent_change'] = (counts['after'] - counts['before']) / counts['before'] * 100
    counts['percent_change'] = counts['percent_change'].replace([np.inf, -np.inf], np.nan).fillna(0)

    ax = counts[['before', 'after']].plot(kind='bar', figsize=(12, 8))
    
    # Add percentage labels inside the bars
    for i, p in enumerate(ax.patches):
        bar_height = p.get_height()
        bar_width = p.get_width()
        x_pos = p.get_x() + bar_width / 2.
        y_pos = bar_height / 2.
        
        # Determine which period the bar belongs to and get the corresponding percent change
        if i >= len(counts):
            perc_change = counts['percent_change'].iloc[i - len(counts)]
            label = f"{perc_change:+.1f}%"
            ax.annotate(label, (x_pos, y_pos), ha='center', va='center', rotation=90, color='white')
    
    plt.title("Average Monthly Violation Counts Before and After Congestion Pricing")
    plt.xlabel("Violation Type")
    plt.ylabel("Average Number of Violations")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "violation_change_grouped_bar.png"))
    plt.close()

def cbd_vs_partial_comparison():
    """Compares violations for buses fully within vs. partially within the CBD zone,
    using monthly averages."""
    
    df_always = load_data(ALWAYS_CBD_PATH)
    df_partial = load_data(PARTIAL_CBD_PATH)

    def get_avg_monthly_by_period(df):
        df["_date"] = pd.to_datetime(df["First Occurrence"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
        df["_month"] = df["_date"].dt.to_period("M")
        
        total_counts = df.groupby("period").size()
        months_count = df.groupby("period")["_month"].nunique()
        
        avg_monthly = (total_counts / months_count).fillna(0)
        return avg_monthly

    avg_monthly_always = get_avg_monthly_by_period(df_always)
    avg_monthly_partial = get_avg_monthly_by_period(df_partial)
    
    combined_df = pd.DataFrame({
        "CBD Only": [avg_monthly_always.get('before', 0), avg_monthly_always.get('after', 0)],
        "Partial CBD": [avg_monthly_partial.get('before', 0), avg_monthly_partial.get('after', 0)]
    }, index=["before", "after"])
    
    # Plotting as a grouped bar chart
    combined_df.plot(kind='bar', figsize=(10, 6))
    plt.title("Average Monthly Violations: CBD vs. Partial CBD")
    plt.xlabel("Period")
    plt.ylabel("Average Number of Violations")
    plt.xticks(rotation=0)
    plt.legend(title='Bus Group')
    plt.tight_layout()
    plt.savefig(os.path.join("visuals", "cbd_comparison_grouped_bar.png"))
    plt.close()

def generate_summary_file(df: pd.DataFrame):
    """
    Generates a summary file based on the analysis results.
    """
    summary_path = os.path.join(DATA_DIR, "summary.txt")

    # 1. Frequency of Violations (now per month)
    df["_date"] = pd.to_datetime(df["First Occurrence"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    df["_month"] = df["_date"].dt.to_period("M")
    
    violations_before = len(df[df['period'] == 'before'])
    violations_after = len(df[df['period'] == 'after'])
    
    months_before = df[df['period'] == 'before']['_month'].nunique()
    months_after = df[df['period'] == 'after']['_month'].nunique()

    avg_monthly_before = violations_before / months_before if months_before > 0 else 0
    avg_monthly_after = violations_after / months_after if months_after > 0 else 0

    change_text_overall = "decreased" if avg_monthly_after < avg_monthly_before else "increased"
    
    # 2. Most Common Violation Types
    counts = get_monthly_counts_by_violation_type(df)
    most_common_before = counts['before'].idxmax() if 'before' in counts.columns and not counts.empty else "N/A"
    most_common_after = counts['after'].idxmax() if 'after' in counts.columns and not counts.empty else "N/A"
    
    count_before = counts.loc[most_common_before, 'before'] if most_common_before != "N/A" else 0
    count_after = counts.loc[most_common_after, 'after'] if most_common_after != "N/A" else 0
    
    # 3. Violations with the Most Change
    counts['change'] = counts['after'] - counts['before']
    most_increased = counts['change'].idxmax() if not counts.empty else "N/A"
    most_decreased = counts['change'].idxmin() if not counts.empty else "N/A"
    
    change_df = (counts['after'] - counts['before'])
    
    increased_before_count = counts.loc[most_increased, 'before'] if most_increased != "N/A" else 0
    increased_after_count = counts.loc[most_increased, 'after'] if most_increased != "N/A" else 0
    decreased_before_count = counts.loc[most_decreased, 'before'] if most_decreased != "N/A" else 0
    decreased_after_count = counts.loc[most_decreased, 'after'] if most_decreased != "N/A" else 0
    
    # Handle division by zero for percent change
    percent_change_increased = (change_df.loc[most_increased] / counts.loc[most_increased, 'before'] * 100) if counts.loc[most_increased, 'before'] > 0 else float('inf')
    percent_change_decreased = (change_df.loc[most_decreased] / counts.loc[most_decreased, 'before'] * 100) if counts.loc[most_decreased, 'before'] > 0 else float('-inf')
    
    # 4. CBD vs Partial CBD comparison
    df_always = load_data(ALWAYS_CBD_PATH)
    df_partial = load_data(PARTIAL_CBD_PATH)
    
    def get_avg_monthly_by_period(df):
        df["_date"] = pd.to_datetime(df["First Occurrence"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
        df["_month"] = df["_date"].dt.to_period("M")
        
        total_counts = df.groupby("period").size()
        months_count = df.groupby("period")["_month"].nunique()
        
        avg_monthly = (total_counts / months_count).fillna(0)
        return avg_monthly

    avg_monthly_always = get_avg_monthly_by_period(df_always)
    avg_monthly_partial = get_avg_monthly_by_period(df_partial)

    # Determine increase or decrease for each group
    cbd_change_text = "decreased" if avg_monthly_always.get('after', 0) < avg_monthly_always.get('before', 0) else "increased"
    partial_change_text = "decreased" if avg_monthly_partial.get('after', 0) < avg_monthly_partial.get('before', 0) else "increased"

    # Format the summary text
    summary_text = f"""### Bus Violation Analysis for Congestion Pricing

The average number of violations per month was approximately {avg_monthly_before:.0f} before congestion pricing, which {change_text_overall} to approximately {avg_monthly_after:.0f} after the policy went into effect. This represents a significant overall {change_text_overall} in the monthly frequency of violations.

---

### Most Common Violation Types

The most common violation type before congestion pricing was "{most_common_before}", with an average of {count_before:.2f} violations per month. After the policy, the most common violation type was "{most_common_after}", with an average of {count_after:.2f} violations per month.

---

### Violations with the Most Change

The analysis of percentage change revealed significant shifts in specific violation types on a monthly basis:

* The violation type that saw the most significant increase after congestion pricing was "{most_increased}". The average number of monthly violations for this type increased from {increased_before_count:.2f} to {increased_after_count:.2f}, a change of approximately {percent_change_increased:+.1f}%.

* "{most_decreased}" experienced the largest decrease. The average number of monthly violations for this type dropped from {decreased_before_count:.2f} to {decreased_after_count:.2f}, a change of approximately {percent_change_decreased:+.1f}%. This suggests the new policy may have had a positive impact on this specific behavior.

---

### CBD vs. Partial CBD Bus Violations

The analysis of monthly violation frequency revealed that buses that were always in the CBD {cbd_change_text}. They experienced an average monthly violation count of {avg_monthly_always.get('before', 0):.0f} before congestion pricing, which changed to {avg_monthly_always.get('after', 0):.0f} after the policy. Buses that were only partially in the CBD also {partial_change_text}. They saw a change from {avg_monthly_partial.get('before', 0):.0f} to {avg_monthly_partial.get('after', 0):.0f} in their average monthly violations.
"""

    with open(summary_path, "w") as f:
        f.write(summary_text)

    print(f"\nSummary saved to {summary_path}")


def main():
    """Main function to perform analysis and generate plots."""
    if not os.path.exists("visuals"):
        os.makedirs("visuals")
    
    print("Loading data...")
    df_full = load_data(VIOLATIONS_PATH)
    
    print("Generating monthly trend bar chart...")
    monthly_trends(df_full)
    
    print("Generating daily trend grouped bar chart...")
    daily_trends(df_full)
    
    print("Generating stacked bar chart for violation types...")
    violation_types_stacked(df_full)
    
    print("Generating diverging bar chart for violation changes...")
    violation_type_changes(df_full)
    
    print("Generating CBD vs. Partial CBD comparison chart...")
    cbd_vs_partial_comparison()
    
    print("Generating analysis summary file...")
    generate_summary_file(df_full)


if __name__ == "__main__":
    main()
