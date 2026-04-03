"""
main.py
-------
Entry point — runs full COVID-19 India analysis pipeline.
"""

import sys
import os

# Allow running from project root OR from src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.data_loader import load_data, get_national_daily, get_state_summary
from src.eda import print_eda_report
from src.stats_analysis import print_stats_report
from src.visualizations import generate_all


def main():
    print("\n🔄  Loading data …")
    df = load_data("data/covid_19_india.csv")
    nat = get_national_daily(df)
    state_summary = get_state_summary(df)

    print_eda_report(df)
    print_stats_report(nat, state_summary)
    generate_all(nat, state_summary, df)

    print("🎉  Analysis complete! Check outputs/plots/ for all charts.\n")


if __name__ == "__main__":
    main()
