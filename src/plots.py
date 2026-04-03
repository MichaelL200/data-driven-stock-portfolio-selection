"""
Code to create visualizations
"""

from pathlib import Path
import matplotlib as mpl
from matplotlib.dates import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from IPython.display import display

from config import PROCESSED_DATA_DIR, FIGURES_DIR


# Paul Tol's colorblind-safe palette
TOL_COLORS = [
    '#0077BB',  # blue
    '#EE7733',  # orange
    '#009988',  # teal
    '#CC3311',  # red
    '#EE3377',  # magenta
    '#33BBEE',  # cyan
    '#BBBBBB',  # grey
]

COLORS = {
    'entered':    '#0077BB',
    'exited':     '#EE7733',
    'cumulative': '#009988',
    'num_companies': '#0077BB',
}

mpl.rcParams.update({
    # Figure
    'figure.figsize':       (7, 4),
    'figure.facecolor':     'white',
    'figure.dpi':           150,

    # Axes
    'axes.facecolor':       'white',
    'axes.edgecolor':       '#333333',
    'axes.linewidth':       0.8,
    'axes.spines.top':      False,
    'axes.spines.right':    False,
    'axes.prop_cycle':      mpl.cycler(color=TOL_COLORS),

    # Grid — off by default, enable per-plot if needed
    'axes.grid':            False,
    'grid.color':           '#CCCCCC',
    'grid.linewidth':       0.5,
    'grid.linestyle':       '--',

    # Lines & markers
    'lines.linewidth':      1.5,
    'lines.markersize':     4,

    # Font — serif to match LaTeX's Computer Modern
    'font.family':          'serif',
    'font.serif':           ['Computer Modern Roman', 'Latin Modern Roman',
                             'Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset':     'cm',

    # Sizes
    'axes.titlesize':       11,
    'axes.labelsize':       10,
    'xtick.labelsize':      9,
    'ytick.labelsize':      9,
    'legend.fontsize':      9,
    'axes.titlepad':        8,

    # Ticks
    'xtick.direction':      'out',
    'ytick.direction':      'out',
    'xtick.major.size':     4,
    'ytick.major.size':     4,
    'xtick.major.width':    0.8,
    'ytick.major.width':    0.8,

    # Legend
    'legend.frameon':       False,
    'legend.borderpad':     0,

    # Export
    'savefig.dpi':          300,
    'savefig.bbox':         'tight',
    'savefig.facecolor':    'white',
})


def summarize_df(df: pd.DataFrame, n_head: int = 2, n_tail: int = 2) -> pd.DataFrame:
    print("DataFrame summary:")
    print(df.info())
    display(df.describe())
    return pd.concat([df.head(n_head), df.tail(n_tail)])


def setup_plot(title: str, xlabel: str, ylabel: str, legend: bool = True):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax._show_legend = legend
    return fig, ax


def finalize_plot(fig, ax):
    if getattr(ax, '_show_legend', False):
        ax.legend()
    fig.tight_layout()
    plt.show()


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

        fig, ax = setup_plot(
            title="Number of S&P 500 Companies at the Beginning of Each Year",
            xlabel="Year",
            ylabel="Number of companies",
            legend=False,
        )
        ax.plot(
            result_df['Year'],
            result_df['NumCompanies'],
            marker='o',
            color=COLORS['num_companies'],
        )
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        finalize_plot(fig, ax)

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

        fig, ax = setup_plot(
            title="Number of Companies Entering and Exiting S&P 500 Each Year",
            xlabel="Year",
            ylabel="Number of companies",
            legend=True,
        )
        ax.bar(
            x - width / 2,
            result_df['Entered'],
            width=width,
            color=COLORS['entered'],
            label='Entered',
        )
        ax.bar(
            x + width / 2,
            result_df['Exited'],
            width=width,
            color=COLORS['exited'],
            label='Exited',
        )
        ax.grid(False, axis='x')
        ax.grid(True, axis='y', alpha=0.3)
        finalize_plot(fig, ax)

        return result_df

    @classmethod
    def count_unique_companies(cls, df: pd.DataFrame, return_count: bool = False) -> pd.DataFrame:

        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])

        unique_tickers = set()
        cumulative_counts = []

        for tickers_str in df["tickers"]:
            tickers = tickers_str.split(",")
            unique_tickers.update(tickers)
            cumulative_counts.append(len(unique_tickers))

        df["unique_cum"] = cumulative_counts

        fig, ax = setup_plot(
            title=f"Unique S&P 500 Companies Over Time (counted since {df['date'].min().year})",
            xlabel="Date",
            ylabel="Cumulative unique tickers",
            legend=False,
        )
        ax.plot(
            df["date"],
            df["unique_cum"],
            color=COLORS['cumulative'],
        )
        finalize_plot(fig, ax)

        start_date = df["date"].min()
        end_date = df["date"].max()
        diff = relativedelta(end_date, start_date)
        years, months = diff.years, diff.months

        print(
            f"{len(unique_tickers)} unique companies were listed in the S&P 500 "
            f"over the period {start_date.date()} → {end_date.date()} "
            f"({years} years, {months} months)"
        )

        return df


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

    @classmethod
    def compare_tickers(
        cls,
        dfs: dict[str, pd.DataFrame],
        col: str = "Adj Close",
        start_date: pd.Timestamp | None = None,
        end_date: pd.Timestamp | None = None
    ) -> pd.DataFrame:

        aligned_series: dict[str, pd.Series] = {}

        for label, df in dfs.items():

            if col not in df.columns:
                raise ValueError(f"Column {col} not found in {label}")

            curr_df = df.copy()

            # Ensure datetime index
            if "date" in curr_df.columns:
                idx = pd.to_datetime(curr_df["date"], utc=True)
            elif isinstance(curr_df.index, pd.DatetimeIndex):
                idx = curr_df.index
                idx = idx.tz_convert("UTC") if idx.tz else idx.tz_localize("UTC")
            else:
                idx = pd.to_datetime(curr_df.index, utc=True)

            # Align by trading day (date only) instead of exact timestamp
            curr_df.index = idx.tz_convert(None).normalize()
            series = curr_df[col].groupby(curr_df.index).last().sort_index()

            aligned_series[label] = series

        # Apply date range filtering if specified
        if start_date is not None or end_date is not None:
            start = pd.Timestamp(start_date) if start_date else None
            end = pd.Timestamp(end_date) if end_date else None
            aligned_series = {
                label: series.loc[start:end]
                for label, series in aligned_series.items()
            }

        df_comp = pd.concat(aligned_series, axis=1).sort_index()
        df_comp = df_comp.ffill()
        df_comp = df_comp.dropna()

        if df_comp.empty:
            raise ValueError("Still no overlapping data after ffill")

        # Normalize
        df_comp = df_comp / df_comp.iloc[0] * 100

        # Sort by final value (highest to lowest)
        final_values = df_comp.iloc[-1].sort_values(ascending=False)
        df_comp = df_comp[final_values.index]

        fig, ax = setup_plot(
            title=f"Ticker Comparison ({col})",
            xlabel="Date",
            ylabel="Normalized Value (Start = 100)",
            legend=True,
        )
        for label in df_comp.columns:
            ax.plot(df_comp.index, df_comp[label], label=label)

        ax.grid(False, axis='x')
        ax.grid(True, axis='y', alpha=0.3)
        finalize_plot(fig, ax)

        return df_comp


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # -----------------------------------------
):

    pass


if __name__ == "__main__":
    main()
