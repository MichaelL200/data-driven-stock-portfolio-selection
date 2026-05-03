import random
import pandas as pd
from datetime import datetime

from config import RANDOM_SEED


def select_random(components: pd.DataFrame, n: int, date: str | datetime = None, seed: int = RANDOM_SEED) -> list[str]:

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

    if n > len(tickers):
        print(f"Warning: Requested {n} tickers but only {len(tickers)} available. Returning all.")
        return tickers

    return random.sample(tickers, n)
