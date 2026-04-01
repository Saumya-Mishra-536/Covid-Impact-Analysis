import pandas as pd
 
 
def summary_stats(df: pd.DataFrame) -> dict:
    numeric_cols = ["Confirmed", "Cured", "Deaths", "Active"]
    stats = df[numeric_cols].describe().round(0)
 
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
 
    date_range = {
        "start": str(df["Date"].min().date()),
        "end": str(df["Date"].max().date()),
        "total_days": (df["Date"].max() - df["Date"].min()).days,
    }
 
    return {
        "shape": df.shape,
        "stats": stats,
        "missing_values": pd.DataFrame({"count": missing, "pct": missing_pct}),
        "unique_states": df["State"].nunique(),
        "date_range": date_range,
    }
 
 
def print_eda_report(df: pd.DataFrame):
    info = summary_stats(df)
    print("=" * 60)
    print("  COVID-19 INDIA — EDA REPORT")
    print("=" * 60)
    print(f"\n📦 Dataset shape : {info['shape'][0]:,} rows × {info['shape'][1]} columns")
    print(f"🗺️  Unique states  : {info['unique_states']}")
    print(f"📅 Date range     : {info['date_range']['start']}  →  {info['date_range']['end']}")
    print(f"                   ({info['date_range']['total_days']} days)\n")
 
    print("── Descriptive Statistics ──────────────────────────────")
    print(info["stats"].to_string())
 
    print("\n── Missing Values ──────────────────────────────────────")
    mv = info["missing_values"]
    if mv["count"].sum() == 0:
        print("✅  No missing values found.")
    else:
        print(mv[mv["count"] > 0])
    print("=" * 60)
 