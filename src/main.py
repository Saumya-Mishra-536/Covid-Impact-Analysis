from data_loader import load_data, get_national_daily, get_state_summary
from eda import print_eda_report
from stats_analysis import print_stats_report
from visualizations import generate_all

def main():
    print("\n🔄  Loading data …")
    df = load_data("../data/covid_19_india.csv")   # 👈 FIXED PATH
    nat = get_national_daily(df)
    state_summary = get_state_summary(df)

    print_eda_report(df)
    print_stats_report(nat, state_summary)
    generate_all(nat, state_summary, df)

    print("🎉  Analysis complete! Check outputs/plots/ for all charts.\n")

if __name__ == "__main__":
    main()