"""
stats_analysis.py
-----------------
Statistical analysis: growth rates, wave detection, state rankings.
"""

import pandas as pd
import numpy as np


def growth_rate_analysis(nat: pd.DataFrame) -> pd.DataFrame:
    """Week-over-week % growth rate in new confirmed cases."""
    nat2 = nat.copy()
    nat2["Week"] = nat2["Date"].dt.to_period("W")
    weekly = nat2.groupby("Week")["NewCases"].sum().reset_index()
    weekly["GrowthRate_%"] = weekly["NewCases"].pct_change() * 100
    weekly["GrowthRate_%"] = weekly["GrowthRate_%"].round(2)
    return weekly


def state_rankings(state_summary: pd.DataFrame) -> pd.DataFrame:
    df = state_summary.copy()
    df["DeathRate_%"] = (df["Deaths"] / df["Confirmed"].replace(0, pd.NA) * 100).round(2)
    df["RecoveryRate_%"] = (df["Cured"] / df["Confirmed"].replace(0, pd.NA) * 100).round(2)
    df["ActiveRate_%"] = (df["Active"] / df["Confirmed"].replace(0, pd.NA) * 100).round(2)
    df["DeathRank"] = df["DeathRate_%"].rank(ascending=False).astype(int)
    df["RecoveryRank"] = df["RecoveryRate_%"].rank(ascending=False).astype(int)
    return df.sort_values("Confirmed", ascending=False)


def detect_waves(nat: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Simple wave detection: find periods where 7-day avg new cases
    exceed `threshold` × peak value.
    """
    nat2 = nat.copy()
    nat2["Rolling7"] = nat2["NewCases"].rolling(7).mean()
    peak = nat2["Rolling7"].max()
    nat2["AboveThreshold"] = nat2["Rolling7"] >= threshold * peak

    waves = []
    in_wave = False
    for _, row in nat2.iterrows():
        if row["AboveThreshold"] and not in_wave:
            in_wave = True
            wave_start = row["Date"]
            wave_peak_val = row["Rolling7"]
        elif in_wave:
            if row["Rolling7"] > wave_peak_val:
                wave_peak_val = row["Rolling7"]
            if not row["AboveThreshold"]:
                waves.append({
                    "Wave": len(waves) + 1,
                    "Start": wave_start,
                    "End": row["Date"],
                    "PeakCases_7dayAvg": round(wave_peak_val, 0),
                    "DurationDays": (row["Date"] - wave_start).days,
                })
                in_wave = False

    return pd.DataFrame(waves)


def print_stats_report(nat: pd.DataFrame, state_summary: pd.DataFrame):
    rankings = state_rankings(state_summary)
    waves = detect_waves(nat, threshold=0.4)

    print("\n" + "=" * 60)
    print("  STATISTICAL ANALYSIS REPORT")
    print("=" * 60)

    # National totals
    last = nat.iloc[-1]
    print(f"\n📌 National Totals (as of {nat['Date'].max().date()})")
    print(f"   Confirmed  : {last['Confirmed']:>12,.0f}")
    print(f"   Recovered  : {last['Cured']:>12,.0f}")
    print(f"   Deaths     : {last['Deaths']:>12,.0f}")
    print(f"   Active     : {last['Active']:>12,.0f}")
    print(f"   CFR        : {last['CFR']:>11.2f}%")
    print(f"   Recovery % : {last['RecoveryRate']:>11.2f}%")

    # Worst hit states
    print("\n🏆 Top 5 States by Confirmed Cases")
    print(rankings[["State", "Confirmed", "DeathRate_%", "RecoveryRate_%"]].head(5).to_string(index=False))

    # Best recovery
    print("\n💚 Top 5 States by Recovery Rate")
    top_rec = rankings.nlargest(5, "RecoveryRate_%")[["State", "RecoveryRate_%", "Confirmed"]]
    print(top_rec.to_string(index=False))

    # Wave analysis
    if not waves.empty:
        print(f"\n🌊 Wave Analysis (threshold = 40% of peak)")
        print(waves.to_string(index=False))

    print("=" * 60)