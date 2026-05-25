import random
import numpy as np
import pandas as pd
from datetime import datetime

from config import RANDOM_SEED


def select_random(
        components: pd.DataFrame,
        n: int,
        coverage: pd.DataFrame = None,
        date: str | datetime = None,
        seed: int = RANDOM_SEED,
        rng: random.Random | None = None
) -> dict:

    if rng is None:
        rng = random.Random(seed) if seed is not None else random

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
    coverage_pct = None
    if coverage is not None:
        coverage_index = coverage.index
        if not isinstance(coverage_index, pd.DatetimeIndex):
            coverage_index = pd.to_datetime(coverage_index)
        available_coverage = coverage_index[coverage_index <= target_date]
        if available_coverage.empty:
            raise ValueError(f"No coverage data available for date {target_date}")
        nearest_coverage_date = available_coverage.max()
        coverage_pct = coverage.loc[nearest_coverage_date, "coverage_pct"]

    if n > len(tickers):
        print(f"Warning: Requested {n} tickers but only {len(tickers)} available. Returning all.")
        selected_tickers = tickers
    else:
        selected_tickers = rng.sample(tickers, n)

    if coverage_pct is not None:
        difference = max(0, round(requested_n * (1 - coverage_pct / 100)))
    else:
        difference = max(0, requested_n - len(selected_tickers))

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

    rng = random.Random(seed) if seed is not None else random

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
        res = select_random(components, n, coverage, date, rng=rng)
        results.append({
            'date': date,
            'tickers': res['tickers'],
            'difference': res['difference']
        })

    return pd.DataFrame(results)


def backtest_portfolio(
    selected_companies: pd.DataFrame,
    price_data: dict[str, pd.DataFrame],
    start_date: str | datetime = None,
    initial_value: float = 100.0,
    price_col: str = "Adj_Close",
    coverage: pd.DataFrame | None = None,
    missing_ticker: pd.DataFrame | None = None,
    max_abs_return: float | None = 2.0
) -> pd.DataFrame:

    if price_col not in price_data:
        raise KeyError(f"Price column '{price_col}' not found in price_data")

    prices = price_data[price_col].copy()

    missing_prices = None
    if missing_ticker is not None:
        missing_prices = missing_ticker.copy()
        if not isinstance(missing_prices.index, pd.DatetimeIndex):
            inferred_index = pd.to_datetime(missing_prices.index, errors="coerce")
            if inferred_index.notna().any():
                missing_prices.index = inferred_index
            else:
                for col in missing_prices.columns:
                    maybe_date = pd.to_datetime(missing_prices[col], errors="coerce")
                    if maybe_date.notna().any():
                        missing_prices = missing_prices.drop(columns=[col])
                        missing_prices.index = maybe_date
                        break
        if missing_prices.index.tz is not None:
            missing_prices.index = missing_prices.index.tz_localize(None)
        missing_prices.index = missing_prices.index.normalize()

    # Ensure index is datetime and normalized
    if not isinstance(prices.index, pd.DatetimeIndex):
        prices.index = pd.to_datetime(prices.index)

    # Fix timezone mismatch: if prices index is tz-aware, remove tz to match naive rebalance dates
    if prices.index.tz is not None:
        prices.index = prices.index.tz_localize(None)

    prices.index = prices.index.normalize()

    selected_companies = selected_companies.sort_values("date").copy()
    selected_companies["date"] = pd.to_datetime(selected_companies["date"]).dt.normalize()
    if selected_companies["date"].dt.tz is not None:
        selected_companies["date"] = selected_companies["date"].dt.tz_localize(None)

    if start_date is not None:
        start_date = pd.to_datetime(start_date).normalize()
        if start_date.tzinfo is not None:
            start_date = start_date.tz_localize(None)

        # Filter rebalances
        past_rebalances = selected_companies[selected_companies["date"] <= start_date]
        future_rebalances = selected_companies[selected_companies["date"] > start_date]

        if not past_rebalances.empty:
            last_rebalance = past_rebalances.iloc[-1:].copy()
            last_rebalance["date"] = start_date
            selected_companies = pd.concat([last_rebalance, future_rebalances])

    portfolio_series = []
    current_value = float(initial_value)

    for i in range(len(selected_companies)):
        period_start = selected_companies.iloc[i]["date"]
        tickers = selected_companies.iloc[i]["tickers"]
        if isinstance(tickers, str):
            tickers = [t.strip() for t in tickers.split(",") if t.strip()]
        valid_tickers = [t for t in tickers if t in prices.columns]

        # Determine end_date for this period
        if i < len(selected_companies) - 1:
            period_end = selected_companies.iloc[i+1]["date"]
        else:
            period_end = prices.index.max()

        # Get prices for selected tickers in this period
        period_mask = (prices.index >= period_start) & (prices.index <= period_end)
        period_index = prices.index[period_mask]

        if period_index.empty:
            continue

        if valid_tickers:
            period_prices = prices.loc[period_index, valid_tickers].where(lambda df: df > 0)
            period_returns = period_prices.pct_change().replace([np.inf, -np.inf], np.nan)
            if max_abs_return is not None:
                period_returns = period_returns.mask(period_returns.abs() > max_abs_return)
            observed_returns = period_returns.mean(axis=1, skipna=True)
        else:
            observed_returns = pd.Series(0.0, index=period_index)

        if missing_prices is not None:
            missing_col = price_col if price_col in missing_prices.columns else missing_prices.columns[0]
            missing_series = missing_prices[missing_col].reindex(period_index).ffill().bfill()
            missing_returns = missing_series.pct_change().replace([np.inf, -np.inf], np.nan)
            if max_abs_return is not None:
                missing_returns = missing_returns.mask(missing_returns.abs() > max_abs_return)
        else:
            missing_returns = pd.Series(0.0, index=period_index)

        if coverage is not None and "coverage_pct" in coverage.columns:
            coverage_index = coverage.index
            if not isinstance(coverage_index, pd.DatetimeIndex):
                coverage_index = pd.to_datetime(coverage_index)
            coverage_series = coverage["coverage_pct"]
            coverage_series.index = coverage_index
            coverage_frac = coverage_series.reindex(period_index).ffill().bfill() / 100.0
        else:
            coverage_frac = pd.Series(1.0, index=period_index)

        if not valid_tickers and missing_prices is not None:
            coverage_frac = pd.Series(0.0, index=period_index)

        if missing_prices is not None:
            observed_nan = observed_returns.isna()
            if observed_nan.any():
                coverage_frac = coverage_frac.copy()
                coverage_frac[observed_nan] = 0.0
                observed_returns = observed_returns.fillna(0)

        daily_port_returns = (coverage_frac * observed_returns) + ((1 - coverage_frac) * missing_returns)
        daily_port_returns = daily_port_returns.fillna(0)
        daily_port_returns.iloc[0] = 0

        # Cumulative growth in this period
        period_value = current_value * (1 + daily_port_returns).cumprod()

        # Store results
        if i < len(selected_companies) - 1:
            portfolio_series.append(period_value.iloc[:-1])
        else:
            portfolio_series.append(period_value)

        # Update current_value for next rebalance
        current_value = float(period_value.iloc[-1])

    if not portfolio_series:
        return pd.DataFrame(columns=[price_col])

    portfolio_df = pd.concat(portfolio_series).to_frame(price_col)

    # Handle start_date trimming
    if start_date is not None:
        portfolio_df = portfolio_df[portfolio_df.index >= start_date]

    if not portfolio_df.empty:
        portfolio_df[price_col] = (portfolio_df[price_col] / portfolio_df[price_col].iloc[0]) * initial_value

    return portfolio_df
