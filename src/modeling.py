import random
import pandas as pd
from datetime import datetime

from config import RANDOM_SEED


def select_random(
        components: pd.DataFrame,
        n: int,
        coverage: pd.DataFrame = None,
        date: str | datetime = None,
        seed: int = RANDOM_SEED
) -> dict:

    if seed is not None:
        random.seed(seed)

    components = components.copy()
    components["date"] = pd.to_datetime(components["date"])

    if date is None:
        target_date = components["date"].max()
    else:
        target_date = pd.to_datetime(date)

    # Find the latest row before or on target_date
    available_dates = components[components["date"] <= target_date]
    if available_dates.empty:
        raise ValueError(f"No S&P 500 components data available for date {target_date}")

    row = available_dates.sort_values("date").iloc[-1]
    tickers_str = row["tickers"]
    tickers = [t.strip() for t in tickers_str.split(",") if t.strip()]

    requested_n = n
    if coverage is not None:
        coverage_index = coverage.index
        if not isinstance(coverage_index, pd.DatetimeIndex):
            coverage_index = pd.to_datetime(coverage_index)
        available_coverage = coverage_index[coverage_index <= target_date]
        if available_coverage.empty:
            raise ValueError(f"No coverage data available for date {target_date}")
        nearest_coverage_date = available_coverage.max()
        coverage_pct = coverage.loc[nearest_coverage_date, "coverage_pct"]
        n = max(1, round(n * coverage_pct / 100))

    if n > len(tickers):
        print(f"Warning: Requested {n} tickers but only {len(tickers)} available. Returning all.")
        selected_tickers = tickers
    else:
        selected_tickers = random.sample(tickers, n)

    difference = requested_n - len(selected_tickers)

    return {
        'tickers': selected_tickers,
        'difference': difference
    }


def select_random_periodic(
        components: pd.DataFrame,
        n: int,
        start_date: str | datetime,
        frequency: str,
        coverage: pd.DataFrame = None,
        seed: int = RANDOM_SEED
) -> pd.DataFrame:

    if seed is not None:
        random.seed(seed)

    components = components.copy()
    components["date"] = pd.to_datetime(components["date"])
    max_date = components["date"].max()
    start_date = pd.to_datetime(start_date)

    freq_map = {
        'monthly': pd.DateOffset(months=1),
        'quarterly': pd.DateOffset(months=3),
        'yearly': pd.DateOffset(years=1)
    }
    freq = freq_map.get(frequency.lower(), frequency)

    dates = pd.date_range(start=start_date, end=max_date, freq=freq)

    results = []
    for date in dates:
        res = select_random(components, n, coverage, date, seed=seed)
        results.append({
            'date': date,
            'tickers': res['tickers'],
            'difference': res['difference']
        })

    return pd.DataFrame(results)
