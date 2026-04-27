"""
visualizations.py
-----------------
All charts for COVID-19 India Analysis.
Saves PNGs to ../outputs/plots/
"""

import os
import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

# ── Palette & theme ──────────────────────────────────────────────────────────
PALETTE = {
    "confirmed": "#4361EE",
    "cured":     "#2DC653",
    "deaths":    "#E63946",
    "active":    "#F4A261",
    "new":       "#7209B7",
}

sns.set_theme(style="darkgrid", font_scale=1.1)
plt.rcParams.update({
    "figure.facecolor": "#0F1117",
    "axes.facecolor":   "#1A1D2E",
    "axes.edgecolor":   "#2E3250",
    "grid.color":       "#2E3250",
    "text.color":       "#E0E0E0",
    "axes.labelcolor":  "#E0E0E0",
    "xtick.color":      "#A0A0B0",
    "ytick.color":      "#A0A0B0",
    "axes.titlecolor":  "#FFFFFF",
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "figure.titlesize": 16,
    "figure.titleweight": "bold",
    "font.family":      "DejaVu Sans",
})

OUT = "../outputs/plots"
os.makedirs(OUT, exist_ok=True)


def _save(fig, name: str):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✅  Saved → {path}")
    return path


def fmt_millions(x, _):
    if x >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"{x/1_000:.0f}K"
    return str(int(x))


# ── 1. National cumulative trend ─────────────────────────────────────────────
def plot_national_trend(nat: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("#0F1117")

    for col, label, color in [
        ("Confirmed", "Confirmed",  PALETTE["confirmed"]),
        ("Cured",     "Recovered",  PALETTE["cured"]),
        ("Deaths",    "Deaths",     PALETTE["deaths"]),
        ("Active",    "Active",     PALETTE["active"]),
    ]:
        ax.plot(nat["Date"], nat[col], label=label, color=color, linewidth=2)
        ax.fill_between(nat["Date"], nat[col], alpha=0.08, color=color)

    ax.set_title("📈  India COVID-19 — Cumulative Cases Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax.legend(facecolor="#1A1D2E", edgecolor="#2E3250", labelcolor="#E0E0E0")
    fig.tight_layout()
    return _save(fig, "01_national_cumulative_trend.png")


# ── 2. Daily new cases (7-day rolling avg) ───────────────────────────────────
def plot_daily_new_cases(nat: pd.DataFrame):
    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
    fig.patch.set_facecolor("#0F1117")

    specs = [
        ("NewCases",      "Daily New Cases",      PALETTE["confirmed"]),
        ("NewDeaths",     "Daily New Deaths",      PALETTE["deaths"]),
        ("NewRecoveries", "Daily New Recoveries",  PALETTE["cured"]),
    ]

    for ax, (col, title, color) in zip(axes, specs):
        rolling = nat[col].rolling(7).mean()
        ax.bar(nat["Date"], nat[col], color=color, alpha=0.3, width=1, label="Daily")
        ax.plot(nat["Date"], rolling, color=color, linewidth=2.5, label="7-day avg")
        ax.set_title(title)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
        ax.legend(facecolor="#1A1D2E", edgecolor="#2E3250", labelcolor="#E0E0E0")

    axes[-1].set_xlabel("Date")
    fig.suptitle("📊  Daily Cases, Deaths & Recoveries (7-day rolling average)", y=1.01)
    fig.tight_layout()
    return _save(fig, "02_daily_new_cases.png")


# ── 3. Top-10 states — bar chart ─────────────────────────────────────────────
def plot_top_states(state_summary: pd.DataFrame):
    top10 = state_summary.head(10)

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("#0F1117")

    x = np.arange(len(top10))
    w = 0.22
    bars = [
        (top10["Confirmed"], "Confirmed", PALETTE["confirmed"]),
        (top10["Cured"],     "Recovered", PALETTE["cured"]),
        (top10["Deaths"],    "Deaths",    PALETTE["deaths"]),
        (top10["Active"],    "Active",    PALETTE["active"]),
    ]

    for i, (vals, label, color) in enumerate(bars):
        ax.bar(x + i * w, vals, width=w, label=label, color=color, alpha=0.9)

    ax.set_xticks(x + w * 1.5)
    ax.set_xticklabels(top10["State"], rotation=30, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax.set_title("🏆  Top 10 States by Confirmed Cases")
    ax.set_xlabel("State")
    ax.set_ylabel("Cases")
    ax.legend(facecolor="#1A1D2E", edgecolor="#2E3250", labelcolor="#E0E0E0")
    fig.tight_layout()
    return _save(fig, "03_top10_states_bar.png")


# ── 4. State-wise heatmap (monthly confirmed) ────────────────────────────────
def plot_state_monthly_heatmap(df: pd.DataFrame):
    top_states = (
        df.groupby("State")["Confirmed"].max()
        .nlargest(15).index.tolist()
    )
    sub = df[df["State"].isin(top_states)].copy()
    sub["MonthStr"] = sub["Date"].dt.to_period("M").astype(str)

    pivot = (
        sub.groupby(["State", "MonthStr"])["Confirmed"]
        .max()
        .unstack(fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor("#0F1117")

    sns.heatmap(
        pivot,
        ax=ax,
        cmap="YlOrRd",
        linewidths=0.3,
        linecolor="#0F1117",
        fmt=".0f",
        cbar_kws={"label": "Confirmed Cases"},
        xticklabels=True,
        yticklabels=True,
    )
    ax.set_title("🗓️  Monthly Confirmed Cases Heatmap — Top 15 States")
    ax.set_xlabel("Month")
    ax.set_ylabel("")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    return _save(fig, "04_state_monthly_heatmap.png")


# ── 5. CFR & Recovery rate over time ─────────────────────────────────────────
def plot_rates(nat: pd.DataFrame):
    nat2 = nat[nat["Confirmed"] > 1000].copy()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    fig.patch.set_facecolor("#0F1117")

    ax1.plot(nat2["Date"], nat2["CFR"].rolling(7).mean(),
             color=PALETTE["deaths"], linewidth=2)
    ax1.fill_between(nat2["Date"], nat2["CFR"].rolling(7).mean(),
                     alpha=0.15, color=PALETTE["deaths"])
    ax1.set_title("⚠️  Case Fatality Rate (7-day avg) %")
    ax1.set_ylabel("CFR %")

    ax2.plot(nat2["Date"], nat2["RecoveryRate"].rolling(7).mean(),
             color=PALETTE["cured"], linewidth=2)
    ax2.fill_between(nat2["Date"], nat2["RecoveryRate"].rolling(7).mean(),
                     alpha=0.15, color=PALETTE["cured"])
    ax2.set_title("💚  Recovery Rate (7-day avg) %")
    ax2.set_ylabel("Recovery %")
    ax2.set_xlabel("Date")

    fig.suptitle("📉  CFR & Recovery Rate Over Time", y=1.01)
    fig.tight_layout()
    return _save(fig, "05_cfr_recovery_rate.png")


# ── 6. Active cases — area chart ─────────────────────────────────────────────
def plot_active_cases(nat: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(14, 5))
    fig.patch.set_facecolor("#0F1117")

    ax.fill_between(nat["Date"], nat["Active"], color=PALETTE["active"], alpha=0.6, label="Active")
    ax.plot(nat["Date"], nat["Active"], color=PALETTE["active"], linewidth=1.5)

    peak_idx = nat["Active"].idxmax()
    ax.annotate(
        f"  Peak: {nat.loc[peak_idx, 'Active']:,.0f}\n  {nat.loc[peak_idx, 'Date'].date()}",
        xy=(nat.loc[peak_idx, "Date"], nat.loc[peak_idx, "Active"]),
        xytext=(nat.loc[peak_idx, "Date"], nat.loc[peak_idx, "Active"] * 0.75),
        arrowprops=dict(arrowstyle="->", color="white"),
        color="white", fontsize=10,
    )

    ax.set_title("🟠  Active Cases Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Active Cases")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    fig.tight_layout()
    return _save(fig, "06_active_cases.png")


# ── 7. State pie chart — share of total confirmed ────────────────────────────
def plot_state_pie(state_summary: pd.DataFrame):
    top8 = state_summary.head(8).copy()
    others = pd.DataFrame([{
        "State": "Others",
        "Confirmed": state_summary.iloc[8:]["Confirmed"].sum()
    }])
    data = pd.concat([top8[["State", "Confirmed"]], others], ignore_index=True)

    colors = sns.color_palette("tab10", len(data))
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#0F1117")

    wedges, texts, autotexts = ax.pie(
        data["Confirmed"],
        labels=data["State"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        wedgeprops=dict(linewidth=0.5, edgecolor="#0F1117"),
    )
    for t in texts:
        t.set_color("#E0E0E0")
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")

    ax.set_title("🗺️  State-wise Share of Total Confirmed Cases")
    fig.tight_layout()
    return _save(fig, "07_state_pie.png")


# ── 8. Monthly wave analysis ──────────────────────────────────────────────────
def plot_monthly_wave(nat: pd.DataFrame):
    nat2 = nat.copy()
    nat2["MonthStr"] = nat2["Date"].dt.to_period("M").astype(str)
    monthly = (
        nat2.groupby("MonthStr")[["NewCases", "NewDeaths"]]
        .sum()
        .reset_index()
    )

    fig, ax1 = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("#0F1117")

    x = np.arange(len(monthly))
    ax2 = ax1.twinx()

    ax1.bar(x, monthly["NewCases"], color=PALETTE["confirmed"], alpha=0.7, label="New Cases")
    ax2.plot(x, monthly["NewDeaths"], color=PALETTE["deaths"], linewidth=2.5,
             marker="o", markersize=5, label="New Deaths")

    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly["MonthStr"], rotation=45, ha="right")
    ax1.set_ylabel("New Cases", color=PALETTE["confirmed"])
    ax2.set_ylabel("New Deaths", color=PALETTE["deaths"])
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax1.set_title("🌊  Monthly New Cases & Deaths — Wave Analysis")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
               facecolor="#1A1D2E", edgecolor="#2E3250", labelcolor="#E0E0E0")

    fig.tight_layout()
    return _save(fig, "08_monthly_wave.png")


# ── 9. Death rate vs confirmed — scatter ─────────────────────────────────────
def plot_death_scatter(state_summary: pd.DataFrame):
    df2 = state_summary.copy()
    df2["DeathRate"] = (df2["Deaths"] / df2["Confirmed"].replace(0, pd.NA) * 100).round(2)
    df2.dropna(subset=["DeathRate"], inplace=True)

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("#0F1117")

    scatter = ax.scatter(
        df2["Confirmed"], df2["DeathRate"],
        c=df2["Confirmed"], cmap="plasma",
        s=df2["Confirmed"] / df2["Confirmed"].max() * 600 + 50,
        alpha=0.8, edgecolors="white", linewidths=0.4,
    )

    for _, row in df2.nlargest(10, "Confirmed").iterrows():
        ax.annotate(row["State"],
                    (row["Confirmed"], row["DeathRate"]),
                    fontsize=8, color="#E0E0E0",
                    xytext=(6, 3), textcoords="offset points")

    plt.colorbar(scatter, ax=ax, label="Confirmed Cases")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax.set_title("💀  Death Rate vs Confirmed Cases by State")
    ax.set_xlabel("Confirmed Cases")
    ax.set_ylabel("Death Rate %")
    fig.tight_layout()
    return _save(fig, "09_death_rate_scatter.png")


# ── 10. Correlation heatmap ───────────────────────────────────────────────────
def plot_correlation(state_summary: pd.DataFrame):
    cols = ["Confirmed", "Cured", "Deaths", "Active"]
    corr = state_summary[cols].corr()

    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor("#0F1117")

    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr, mask=mask, ax=ax,
        cmap="coolwarm", annot=True, fmt=".2f",
        linewidths=0.5, linecolor="#0F1117",
        vmin=-1, vmax=1,
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("🔗  Correlation Between COVID Metrics (State Level)")
    fig.tight_layout()
    return _save(fig, "10_correlation_heatmap.png")


# ── Run all ───────────────────────────────────────────────────────────────────
def generate_all(nat, state_summary, df):
    print("\n🎨  Generating visualizations …\n")
    plot_national_trend(nat)
    plot_daily_new_cases(nat)
    plot_top_states(state_summary)
    plot_state_monthly_heatmap(df)
    plot_rates(nat)
    plot_active_cases(nat)
    plot_state_pie(state_summary)
    plot_monthly_wave(nat)
    plot_death_scatter(state_summary)
    plot_correlation(state_summary)
    print("\n✅  All plots saved to outputs/plots/\n")
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE_DIR, "outputs", "plots")

os.makedirs(OUT, exist_ok=True)   # ✅ creates folder automatically