#  COVID-19 India Data Analysis

A modular Python project for exploratory data analysis, statistical analysis, and visualization of COVID-19 data across Indian states (January 2020 – August 2021).

---

## 📁 Folder Structure

```
covid_analysis/
├── data/
│   └── covid_19_india.csv        # Raw dataset
├── src/
│   ├── data_loader.py            # Data ingestion, cleaning & feature engineering
│   ├── eda.py                    # Exploratory Data Analysis & summary report
│   ├── stats_analysis.py         # Growth rates, wave detection, state rankings
│   └── visualizations.py         # All 10 charts (matplotlib + seaborn)
    |__ main.py                   # Entry point — runs the full pipeline
├── outputs/
│   └── plots/                    # Auto-generated PNG charts                    
└── requirements.txt              # Python dependencies
```

---

## ⚙️ Setup & Installation

**1. Clone / download the project**
```bash
git clone https://github.com/your-username/covid-analysis.git
cd covid-analysis
```

**2. (Optional) Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add the dataset**

Place `covid_19_india.csv` inside the `data/` folder.

---

## ▶️ Run

```bash
python main.py
```

This will:
- Load and clean the dataset
- Print the EDA report to the console
- Print the statistical analysis report to the console
- Generate all 10 charts and save them to `outputs/plots/`

---

## 📊 Dataset Overview

| Field | Description |
|---|---|
| `Date` | Date of record |
| `State/UnionTerritory` | Indian state or UT |
| `Confirmed` | Cumulative confirmed cases |
| `Cured` | Cumulative recovered cases |
| `Deaths` | Cumulative deaths |
| `ConfirmedIndianNational` | Confirmed cases among Indian nationals |
| `ConfirmedForeignNational` | Confirmed cases among foreign nationals |

**Coverage:** 43 states/UTs · 559 days · 18,110 rows · No missing values

---

## 📈 Visualizations Generated

| # | File | Description |
|---|------|-------------|
| 1 | `01_national_cumulative_trend.png` | Cumulative Confirmed / Recovered / Deaths / Active over time |
| 2 | `02_daily_new_cases.png` | Daily new cases, deaths & recoveries with 7-day rolling average |
| 3 | `03_top10_states_bar.png` | Top 10 states across all 4 metrics (grouped bar chart) |
| 4 | `04_state_monthly_heatmap.png` | Month-by-month confirmed cases for top 15 states |
| 5 | `05_cfr_recovery_rate.png` | Case Fatality Rate & Recovery Rate over time |
| 6 | `06_active_cases.png` | Active cases area chart with peak annotated |
| 7 | `07_state_pie.png` | State-wise share of total confirmed cases |
| 8 | `08_monthly_wave.png` | Monthly new cases vs deaths — wave analysis |
| 9 | `09_death_rate_scatter.png` | Death rate vs confirmed cases by state (bubble chart) |
| 10 | `10_correlation_heatmap.png` | Correlation between COVID metrics at state level |

---

## 🔬 Analysis Modules

### `data_loader.py`
- Parses and standardizes dates
- Fixes inconsistent state names
- Engineers derived columns: `Active`, `Month`
- Provides `get_national_daily()` and `get_state_summary()` helpers

### `eda.py`
- Descriptive statistics for all numeric columns
- Missing value report
- Dataset shape, unique states, date range summary

### `stats_analysis.py`
- Week-over-week growth rate calculation
- State rankings by death rate, recovery rate, active rate
- Automatic wave detection based on 7-day rolling average threshold

### `visualizations.py`
- Dark-themed charts using `matplotlib` + `seaborn`
- All charts saved as high-resolution PNGs (150 DPI)
- Fully self-contained — call `generate_all()` to produce every chart

---

## 📦 Dependencies

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

---

## 📌 Key Findings

- **Maharashtra** had the highest confirmed cases (~6.3M) and death toll
- **Kerala** was the most affected southern state with ~3.6M cases
- **India's second wave** peaked in May 2021 with ~391K daily cases (7-day avg)
- National **recovery rate** reached **97.45%** by August 2021
- National **case fatality rate** stood at **1.34%**
- States like **Rajasthan** and **Gujarat** achieved recovery rates above 99%

---

## 🙌 Acknowledgements

Dataset sourced from publicly available COVID-19 India tracking data.
