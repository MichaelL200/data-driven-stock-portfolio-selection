"""
Code to create visualizations
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from config import PROCESSED_DATA_DIR, FIGURES_DIR


def sp500_companies_per_year_start(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['num_companies'] = df['tickers'].str.split(',').apply(len)
    df['year'] = df['date'].dt.year

    last_day_per_year = df.groupby('year').last()

    first_day_next_year = last_day_per_year.shift(1)
    first_day_next_year.index = last_day_per_year.index
    first_day_next_year = first_day_next_year.dropna(subset=['num_companies'])

    result_df = first_day_next_year[['num_companies']].reset_index().rename(
        columns={'year': 'Year', 'num_companies': 'NumCompanies'}
    )

    plt.figure(figsize=(10, 4))
    plt.plot(result_df['Year'], result_df['NumCompanies'], marker='o')
    plt.title("Number of S&P 500 Companies at the Beginning of Each Year")
    plt.xlabel("Year")
    plt.ylabel("Number of companies")
    plt.grid(True)

    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    plt.show()

    return result_df


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # -----------------------------------------
):

    pass


if __name__ == "__main__":
    main()
