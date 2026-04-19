"""
Code to create visualizations
"""

from pathlib import Path
import json
import re
import matplotlib as mpl
from matplotlib.dates import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from IPython.display import display

from config import PROCESSED_DATA_DIR, FIGURES_DIR, REPORTS_DIR


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


def finalize_plot(fig, ax, save_figures: bool = True, filename: str | None = None):
    if getattr(ax, '_show_legend', False):
        ax.legend()
    fig.tight_layout()
    if save_figures and filename is not None:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(FIGURES_DIR / filename)
    plt.show()


class SP500:

    @classmethod
    def companies_per_year_start(
        cls,
        df: pd.DataFrame,
        save_figures: bool = True,
        filename: str | None = None,
    ) -> pd.DataFrame:

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
        finalize_plot(fig, ax, save_figures=save_figures, filename=filename)

        return result_df

    @classmethod
    def yearly_changes(
        cls,
        df: pd.DataFrame,
        save_figures: bool = True,
        filename: str | None = None,
    ) -> pd.DataFrame:

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
        finalize_plot(fig, ax, save_figures=save_figures, filename=filename)

        return result_df

    @classmethod
    def count_unique_companies(
        cls,
        df: pd.DataFrame,
        return_count: bool = False,
        save_figures: bool = True,
        filename: str | None = None,
    ) -> pd.DataFrame:

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
        finalize_plot(fig, ax, save_figures=save_figures, filename=filename)

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

        curr_df = df.copy()

        # Handle MultiIndex columns (raw yf.download output)
        if isinstance(curr_df.columns, pd.MultiIndex):
            tickers = curr_df.columns.get_level_values(1).unique()
            if len(tickers) > 0:
                ticker = tickers[0]
                # Extract first ticker's data to flatten columns
                curr_df = curr_df.xs(ticker, level=1, axis=1)

        # Check for both "Stock_Splits" (internal) and "Stock Splits" (yfinance)
        split_col = "Stock_Splits" if "Stock_Splits" in curr_df.columns else "Stock Splits"

        if split_col not in curr_df.columns:
            print(f"No stock splits column found in the data. Columns: {list(curr_df.columns)}")
            return pd.DataFrame()

        splits = curr_df[curr_df[split_col] != 0]
        if splits.empty:
            print("No stock splits found in the provided data range for this ticker.")
            return pd.DataFrame()

        last_split_date = splits.index[-1]
        last_split_pos = curr_df.index.get_loc(last_split_date)

        start = max(last_split_pos - 1, 0)
        end = min(last_split_pos + 2, len(curr_df))

        # Dynamically select available columns
        potential_cols = ["Open", "Adj_Close", "Adj Close", "Dividends", "Stock_Splits", "Stock Splits"]
        available_cols = [c for c in potential_cols if c in curr_df.columns]

        return curr_df.iloc[start:end][available_cols]

    @classmethod
    def show_chart(
        cls,
        df: pd.DataFrame,
        label: str = "Ticker",
        col: str = "Adj_Close",
        start_date: pd.Timestamp | None = None,
        end_date: pd.Timestamp | None = None,
        hide_col: bool = False,
        title: str | None = None,
        save_figures: bool = True,
        filename: str | None = None,
    ) -> pd.DataFrame:

        curr_df = df.copy()

        # Handle MultiIndex columns (raw yf.download output)
        if isinstance(curr_df.columns, pd.MultiIndex):
            tickers = curr_df.columns.get_level_values(1).unique()
            # Try to find specific ticker if label matches, otherwise take first
            target_ticker = label if label in tickers else (tickers[0] if len(tickers) > 0 else None)
            if target_ticker:
                curr_df = curr_df.xs(target_ticker, level=1, axis=1)

        if col not in curr_df.columns:
            alt_col = col.replace("_", " ")
            if alt_col in curr_df.columns:
                col = alt_col
            else:
                raise ValueError(f"Column {col} not found in {label}")

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

        # Apply date range filtering if specified
        if start_date is not None or end_date is not None:
            start = pd.Timestamp(start_date) if start_date else None
            end = pd.Timestamp(end_date) if end_date else None
            series = series.loc[start:end]

        df_plot = series.to_frame(name=label)

        if df_plot.empty:
            raise ValueError("No data available for plotting")

        chart_title = title if title is not None else (
            "Ticker Chart" if hide_col else f"Ticker Chart ({col})"
        )

        fig, ax = setup_plot(
            title=chart_title,
            xlabel="Date",
            ylabel=col,
            legend=True,
        )
        ax.plot(df_plot.index, df_plot[label], label=label)

        ax.grid(False, axis='x')
        ax.grid(True, axis='y', alpha=0.3)
        finalize_plot(fig, ax, save_figures=save_figures, filename=filename)

        return df_plot

    @classmethod
    def compare_tickers(
        cls,
        dfs: dict[str, pd.DataFrame],
        col: str = "Adj_Close",
        start_date: pd.Timestamp | None = None,
        end_date: pd.Timestamp | None = None,
        hide_col: bool = False,
        title: str | None = None,
        save_figures: bool = True,
        filename: str | None = None,
    ) -> pd.DataFrame:

        aligned_series: dict[str, pd.Series] = {}

        for label, df in dfs.items():

            curr_df = df.copy()

            # Handle MultiIndex columns (raw yf.download output)
            if isinstance(curr_df.columns, pd.MultiIndex):
                tickers = curr_df.columns.get_level_values(1).unique()
                # Try to find specific ticker if label matches, otherwise take first
                target_ticker = label if label in tickers else (tickers[0] if len(tickers) > 0 else None)
                if target_ticker:
                    curr_df = curr_df.xs(target_ticker, level=1, axis=1)

            if col not in curr_df.columns:
                alt_col = col.replace("_", " ")
                if alt_col in curr_df.columns:
                    col = alt_col
                else:
                    raise ValueError(f"Column {col} not found in {label}")

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
        start_common = df_comp.apply(lambda s: s.first_valid_index()).max()
        end_common = df_comp.apply(lambda s: s.last_valid_index()).min()
        df_comp = df_comp.loc[start_common:end_common]

        if df_comp.empty:
            raise ValueError("No data available for plotting")

        # Normalize each series from its own first valid observation so that
        # assets with shorter histories do not truncate longer series.
        for label in df_comp.columns:
            first_valid = df_comp[label].first_valid_index()
            if first_valid is None:
                continue
            df_comp[label] = df_comp[label] / df_comp.loc[first_valid, label] * 100

        # Sort by final value (highest to lowest)
        final_values = df_comp.iloc[-1].sort_values(ascending=False)
        df_comp = df_comp[final_values.index]

        chart_title = title if title is not None else (
            "Ticker Comparison" if hide_col else f"Ticker Comparison ({col})"
        )

        fig, ax = setup_plot(
            title=chart_title,
            xlabel="Date",
            ylabel="Normalized Value (Start = 100)",
            legend=True,
        )
        for label in df_comp.columns:
            ax.plot(df_comp.index, df_comp[label], label=label)

        ax.grid(False, axis='x')
        ax.grid(True, axis='y', alpha=0.3)
        finalize_plot(fig, ax, save_figures=save_figures, filename=filename)

        return df_comp


def coverage_over_time(
    price_data: dict[str, pd.DataFrame],
    components: pd.DataFrame,
    col: str = "Adj_Close",
    save_figures: bool = True,
    filename: str | None = None,
) -> pd.DataFrame:

    if col not in price_data:
        raise ValueError(f"Column {col} not found in price_data")

    if components.empty:
        raise ValueError("components is empty")

    df = price_data[col].copy()

    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    df = df.sort_index()

    components_df = components.copy()
    components_df["date"] = pd.to_datetime(components_df["date"]).dt.normalize()

    available_values = []
    missing_values = []
    not_downloaded_values = []
    total_values = []
    coverage_values = []
    result_index = []

    component_dates = components_df["date"].tolist()
    date_to_pos = {date: pos for pos, date in enumerate(component_dates)}
    missing_tracker: dict[str, dict[str, list[pd.Timestamp]]] = {}

    for _, row in components_df.iterrows():

        date = row["date"]
        active_tickers = {ticker.strip() for ticker in str(row["tickers"]).split(",") if ticker.strip()}
        if not active_tickers:
            available_values.append(0)
            missing_values.append(0)
            not_downloaded_values.append(0)
            total_values.append(0)
            coverage_values.append(0.0)
            result_index.append(date)
            continue

        nearest_pos = df.index.get_indexer([date], method="nearest")[0]
        nearest_date = df.index[nearest_pos]
        row_data = df.loc[nearest_date]

        available = 0
        missing = 0
        not_downloaded = 0

        for ticker in active_tickers:
            if ticker not in df.columns:
                not_downloaded += 1
                ticker_tracker = missing_tracker.setdefault(
                    ticker, {"missing": [], "not_downloaded": []}
                )
                ticker_tracker["not_downloaded"].append(date)
            elif pd.notna(row_data.get(ticker)):
                available += 1
            else:
                missing += 1
                ticker_tracker = missing_tracker.setdefault(
                    ticker, {"missing": [], "not_downloaded": []}
                )
                ticker_tracker["missing"].append(date)

        total = len(active_tickers)
        coverage_pct = available / total * 100 if total else 0.0

        available_values.append(available)
        missing_values.append(missing)
        not_downloaded_values.append(not_downloaded)
        total_values.append(total)
        coverage_values.append(coverage_pct)
        result_index.append(date)

    result_df = pd.DataFrame(
        {
            "available": available_values,
            "missing": missing_values,
            "not_downloaded": not_downloaded_values,
            "total": total_values,
            "coverage_pct": coverage_values,
        },
        index=pd.DatetimeIndex(result_index),
    )

    result_df = result_df.sort_index()

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(result_df.index, result_df["coverage_pct"], color=TOL_COLORS[2], label="Coverage %")
    ax.set_ylabel("Coverage (%)")
    ax.set_xlabel("Date")
    ax.set_ylim(0, 100)
    ax.set_title(f"Index Coverage Over Time — {col}")
    ax.axhline(y=50, color="#CCCCCC", linewidth=0.8, linestyle="--", zorder=0)
    ax.axhline(y=90, color="#CCCCCC", linewidth=0.8, linestyle="--", zorder=0)
    ax.legend(loc="lower right")
    ax.grid(True, axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()

    if save_figures and filename is not None:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(FIGURES_DIR / filename)

    plt.show()

    def _to_periods(dates: list[pd.Timestamp]) -> list[tuple[pd.Timestamp, pd.Timestamp]]:

        if not dates:
            return []
        unique_dates = sorted(set(dates), key=lambda d: date_to_pos[d])
        periods: list[tuple[pd.Timestamp, pd.Timestamp]] = []
        start = unique_dates[0]
        prev = unique_dates[0]

        for curr in unique_dates[1:]:
            if date_to_pos[curr] == date_to_pos[prev] + 1:
                prev = curr
                continue
            periods.append((start, prev))
            start = curr
            prev = curr

        periods.append((start, prev))
        return periods

    if missing_tracker:
        print("Missing ticker coverage periods:")
        for ticker in sorted(missing_tracker):
            ticker_data = missing_tracker[ticker]
            missing_periods = _to_periods(ticker_data["missing"])
            not_downloaded_periods = _to_periods(ticker_data["not_downloaded"])

            if not missing_periods and not not_downloaded_periods:
                continue

            print(f"- {ticker}:")
            for start, end in missing_periods:
                if start == end:
                    print(f"  missing on {start.date()}")
                else:
                    print(f"  missing from {start.date()} to {end.date()}")

            for start, end in not_downloaded_periods:
                if start == end:
                    print(f"  not downloaded on {start.date()}")
                else:
                    print(f"  not downloaded from {start.date()} to {end.date()}")
    else:
        print("No missing ticker periods found.")

    return result_df


def plot_missing_data_reasons(
    source: str,
    save_figures: bool = True,
    filename: str | None = None,
):

    report_path = REPORTS_DIR / "missing_ticker_coverage.md"
    if not report_path.exists():
        print(f"Warning: {report_path} not found.")
        return

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the JSON comment at the end of the file
    match = re.search(r"<!--\s*({.*?})\s*-->", content, re.DOTALL)
    if not match:
        print("Warning: No JSON data found in reports/missing_ticker_coverage.md.")
        return

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from report: {e}")
        return

    if source not in data:
        print(f"Warning: Source '{source}' not found in data. Available: {list(data.keys())}")
        return

    source_data = data[source]
    labels = list(source_data.keys())
    values = list(source_data.values())

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))

    # Pie chart
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=TOL_COLORS,
        pctdistance=0.80,
        explode=[0.03] * len(labels),
        textprops={'fontsize': 10}
    )

    # Style percentages
    plt.setp(autotexts, size=9, weight="bold", color="white")

    ax.set_title(f"Reasons for missing data - {source}", fontsize=12, pad=20)
    ax.axis('equal')

    plt.tight_layout()
    if save_figures and filename is not None:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(FIGURES_DIR / filename)
    plt.show()


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # -----------------------------------------
):

    pass


if __name__ == "__main__":
    main()
