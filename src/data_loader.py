"""
data_loader.py
--------------
Loads and cleans the COVID-19 India dataset.
"""

import pandas as pd


def load_data(path: str = "../data/covid_19_india.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # Parse dates
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    # Clean column names
    df.rename(columns={"State/UnionTerritory": "State"}, inplace=True)

    # Drop helper column
    df.drop(columns=["Sno", "Time"], inplace=True, errors="ignore")

    # Fix known state name inconsistencies
    state_map = {
        "Telengana": "Telangana",
        "Dadra and Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
        "Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu",
    }
    df["State"] = df["State"].replace(state_map)

    # Derived columns
    df["Active"] = df["Confirmed"] - df["Cured"] - df["Deaths"]
    df["Active"] = df["Active"].clip(lower=0)
    df["Month"] = df["Date"].dt.to_period("M")
    df["Week"] = df["Date"].dt.isocalendar().week

    df.sort_values(["State", "Date"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def get_national_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate all states to get national daily totals."""
    nat = (
        df.groupby("Date")[["Confirmed", "Cured", "Deaths", "Active"]]
        .sum()
        .reset_index()
    )
    nat["NewCases"] = nat["Confirmed"].diff().fillna(0).clip(lower=0)
    nat["NewDeaths"] = nat["Deaths"].diff().fillna(0).clip(lower=0)
    nat["NewRecoveries"] = nat["Cured"].diff().fillna(0).clip(lower=0)
    nat["CFR"] = (nat["Deaths"] / nat["Confirmed"].replace(0, pd.NA) * 100).round(2)
    nat["RecoveryRate"] = (nat["Cured"] / nat["Confirmed"].replace(0, pd.NA) * 100).round(2)
    return nat


def get_state_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Latest snapshot per state."""
    return (
        df.sort_values("Date")
        .groupby("State")
        .last()
        .reset_index()[["State", "Confirmed", "Cured", "Deaths", "Active"]]
        .sort_values("Confirmed", ascending=False)
    )
