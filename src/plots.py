"""
Code to create visualizations
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from IPython.display import display

from config import PROCESSED_DATA_DIR, FIGURES_DIR


def summarize_df(df: pd.DataFrame, n_head: int = 2, n_tail: int = 2) -> pd.DataFrame:
    print("DataFrame summary:")
    print(df.info())
    display(df.describe())
    return pd.concat([df.head(n_head), df.tail(n_tail)])


class SP500:

    @classmethod
    def companies_per_year_start(cls, df: pd.DataFrame) -> pd.DataFrame:

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

    @classmethod
    def yearly_changes(cls, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year

        last_day_per_year = df.groupby('year').last()

        last_day_per_year['tickers_set'] = last_day_per_year['tickers'].str.split(',').apply(set)

        years = last_day_per_year.index.tolist()

        entered_list = []
        exited_list = []

        for i in range(1, len(years)):
            prev = last_day_per_year.iloc[i - 1]['tickers_set']
            curr = last_day_per_year.iloc[i]['tickers_set']

            entered = len(curr - prev)
            exited = len(prev - curr)

            entered_list.append(entered)
            exited_list.append(exited)

        result_df = pd.DataFrame({
            'Year': years[1:],
            'Entered': entered_list,
            'Exited': exited_list
        })

        x = result_df['Year']
        width = 0.4

        plt.figure(figsize=(10, 4))
        plt.bar(x - width/2, result_df['Entered'], width=width, label='Entered')
        plt.bar(x + width/2, result_df['Exited'], width=width, label='Exited')

        plt.title("Number of Companies Entering and Exiting S&P 500 Each Year")
        plt.xlabel("Year")
        plt.ylabel("Number of companies")
        plt.legend()
        plt.grid(axis='y')

        plt.tight_layout()
        plt.show()

        return result_df


class YahooFinance:

    @classmethod
    def show_last_split(cls, df: pd.DataFrame) -> pd.DataFrame:

        splits = df[df["Stock Splits"] != 0]
        if splits.empty:
            print("No stock splits found in the data for this ticker.")
            return pd.DataFrame()

        last_split_date = splits.index[-1]
        last_split_pos = df.index.get_loc(last_split_date)

        start = max(last_split_pos - 1, 0)
        end = min(last_split_pos + 2, len(df))

        return df.iloc[start:end][["Open", "Adj Close", "Dividends", "Stock Splits"]]


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # -----------------------------------------
):

    pass


if __name__ == "__main__":
    main()
