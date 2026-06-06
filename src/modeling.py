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


def select_monte_carlo_periodic(
        components: pd.DataFrame,
        price_data: dict[str, pd.DataFrame],
        n: int,
        start_date: str | datetime,
        frequency: str,
        lookback_days: int = 252,
        n_trials: int = 500,
        min_obs: int = 60,
        price_col: str = "Adj_Close",
        max_abs_return: float | None = 2.0,
        coverage: pd.DataFrame = None,
        seed: int = RANDOM_SEED
) -> pd.DataFrame:

    if price_col not in price_data:
        raise KeyError(f"Price column '{price_col}' not found in price_data")

    rng = random.Random(seed) if seed is not None else random

    components = components.copy()
    components["date"] = pd.to_datetime(components["date"])
    max_date = components["date"].max()
    start_date = pd.to_datetime(start_date)

    prices = price_data[price_col].copy()
    if not isinstance(prices.index, pd.DatetimeIndex):
        prices.index = pd.to_datetime(prices.index)
    if prices.index.tz is not None:
        prices.index = prices.index.tz_localize(None)
    prices.index = prices.index.normalize()

    returns = prices.where(lambda df: df > 0).pct_change().replace([np.inf, -np.inf], np.nan)
    if max_abs_return is not None:
        returns = returns.mask(returns.abs() > max_abs_return)

    freq_map = {
        'monthly': pd.DateOffset(months=1),
        'quarterly': pd.DateOffset(months=3),
        'yearly': pd.DateOffset(years=1)
    }
    freq = freq_map.get(frequency.lower(), frequency)
    dates = pd.date_range(start=start_date, end=max_date, freq=freq)

    results = []
    for date in dates:
        target_date = pd.to_datetime(date).normalize()
        available_dates = components[components["date"] <= target_date]
        if available_dates.empty:
            continue

        row = available_dates.sort_values("date").iloc[-1]
        tickers_str = row["tickers"]
        tickers = [t.strip() for t in tickers_str.split(",") if t.strip()]
        valid_tickers = [t for t in tickers if t in returns.columns]

        if not valid_tickers:
            continue

        available_price_dates = prices.index[prices.index <= target_date]
        if len(available_price_dates) == 0:
            continue

        window_end = available_price_dates.max()
        window = returns.loc[:window_end, valid_tickers].tail(lookback_days)
        counts = window.count()
        valid_tickers = [t for t in valid_tickers if counts.get(t, 0) >= min_obs]

        if not valid_tickers:
            continue

        means = window[valid_tickers].mean(skipna=True)
        stds = window[valid_tickers].std(skipna=True)

        requested_n = n
        selected_tickers = None
        best_sharpe_ratio = -np.inf

        if len(valid_tickers) <= n or n_trials <= 1:
            selected_tickers = valid_tickers
            mean_ret = means.mean()
            vol = stds.mean()
            sharpe_ratio = mean_ret / vol if pd.notna(vol) and vol != 0 else np.nan
        else:
            for _ in range(n_trials):
                sample = rng.sample(valid_tickers, n)
                mean_ret = means[sample].mean()
                vol = stds[sample].mean()
                if pd.isna(vol) or vol == 0:
                    sharpe_ratio = -np.inf
                else:
                    sharpe_ratio = mean_ret / vol
                if sharpe_ratio > best_sharpe_ratio:
                    best_sharpe_ratio = sharpe_ratio
                    selected_tickers = sample
            sharpe_ratio = best_sharpe_ratio if best_sharpe_ratio != -np.inf else np.nan

        if selected_tickers is None:
            selected_tickers = rng.sample(valid_tickers, min(n, len(valid_tickers)))
            sharpe_ratio = np.nan

        coverage_pct = None
        if coverage is not None:
            coverage_index = coverage.index
            if not isinstance(coverage_index, pd.DatetimeIndex):
                coverage_index = pd.to_datetime(coverage_index)
            available_coverage = coverage_index[coverage_index <= target_date]
            if not available_coverage.empty:
                nearest_coverage_date = available_coverage.max()
                coverage_pct = coverage.loc[nearest_coverage_date, "coverage_pct"]

        if coverage_pct is not None:
            difference = max(0, round(requested_n * (1 - coverage_pct / 100)))
        else:
            difference = max(0, requested_n - len(selected_tickers))

        results.append({
            'date': target_date,
            'tickers': selected_tickers,
            'difference': difference,
            'sharpe_ratio': sharpe_ratio
        })

    return pd.DataFrame(results)


def select_best_sharpe_periodic(
        components: pd.DataFrame,
        price_data: dict[str, pd.DataFrame],
        n: int,
        start_date: str | datetime,
        frequency: str,
        lookback_days: int = 252,
        n_trials: int = 500,  # Unused, kept for interface compatibility
        min_obs: int = 60,
        price_col: str = "Adj_Close",
        max_abs_return: float | None = 2.0,
        coverage: pd.DataFrame = None,
        seed: int = RANDOM_SEED  # Unused, kept for interface compatibility
) -> pd.DataFrame:

    if price_col not in price_data:
        raise KeyError(f"Price column '{price_col}' not found in price_data")

    components = components.copy()
    components["date"] = pd.to_datetime(components["date"])
    max_date = components["date"].max()
    start_date = pd.to_datetime(start_date)

    prices = price_data[price_col].copy()
    if not isinstance(prices.index, pd.DatetimeIndex):
        prices.index = pd.to_datetime(prices.index)
    if prices.index.tz is not None:
        prices.index = prices.index.tz_localize(None)
    prices.index = prices.index.normalize()

    returns = prices.where(lambda df: df > 0).pct_change().replace([np.inf, -np.inf], np.nan)
    if max_abs_return is not None:
        returns = returns.mask(returns.abs() > max_abs_return)

    freq_map = {
        'monthly': pd.DateOffset(months=1),
        'quarterly': pd.DateOffset(months=3),
        'yearly': pd.DateOffset(years=1)
    }
    freq = freq_map.get(frequency.lower(), frequency)
    dates = pd.date_range(start=start_date, end=max_date, freq=freq)

    results = []
    for date in dates:
        target_date = pd.to_datetime(date).normalize()
        available_dates = components[components["date"] <= target_date]
        if available_dates.empty:
            continue

        row = available_dates.sort_values("date").iloc[-1]
        tickers_str = row["tickers"]
        tickers = [t.strip() for t in tickers_str.split(",") if t.strip()]
        valid_tickers = [t for t in tickers if t in returns.columns]

        if not valid_tickers:
            continue

        available_price_dates = prices.index[prices.index <= target_date]
        if len(available_price_dates) == 0:
            continue

        window_end = available_price_dates.max()
        window = returns.loc[:window_end, valid_tickers].tail(lookback_days)
        counts = window.count()
        valid_tickers = [t for t in valid_tickers if counts.get(t, 0) >= min_obs]

        if not valid_tickers:
            continue

        means = window[valid_tickers].mean(skipna=True)
        stds = window[valid_tickers].std(skipna=True)

        # Calculate individual Sharpe ratios
        individual_sharpe = means / stds
        individual_sharpe = individual_sharpe.replace([np.inf, -np.inf], np.nan).dropna()

        # Select top N tickers by Sharpe ratio
        top_n_sharpe = individual_sharpe.nlargest(n)
        selected_tickers = top_n_sharpe.index.tolist()

        sharpe_ratio = np.nan
        if not top_n_sharpe.empty:
            sharpe_ratio = top_n_sharpe.mean()

        requested_n = n
        coverage_pct = None
        if coverage is not None:
            coverage_index = coverage.index
            if not isinstance(coverage_index, pd.DatetimeIndex):
                coverage_index = pd.to_datetime(coverage_index)
            available_coverage = coverage_index[coverage_index <= target_date]
            if not available_coverage.empty:
                nearest_coverage_date = available_coverage.max()
                coverage_pct = coverage.loc[nearest_coverage_date, "coverage_pct"]

        if coverage_pct is not None:
            difference = max(0, round(requested_n * (1 - coverage_pct / 100)))
        else:
            difference = max(0, requested_n - len(selected_tickers))

        results.append({
            'date': target_date,
            'tickers': selected_tickers,
            'difference': difference,
            'sharpe_ratio': sharpe_ratio
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


def calculate_sharpe_ratios(
    strategies: dict[str, pd.DataFrame | pd.Series] | None = None,
    *,
    value_col: str = "Adj_Close",
    risk_free_rate: float = 0.0,
    annualization_factor: float = 252.0,
    **named_strategies: pd.DataFrame | pd.Series
) -> pd.DataFrame:

    combined_strategies: dict[str, pd.DataFrame | pd.Series] = {}
    if strategies is not None:
        combined_strategies.update(strategies)
    combined_strategies.update(named_strategies)

    if not combined_strategies:
        raise ValueError("At least one strategy must be provided")

    if annualization_factor <= 0:
        raise ValueError("annualization_factor must be greater than 0")

    period_risk_free_rate = (1 + risk_free_rate) ** (1 / annualization_factor) - 1 if risk_free_rate else 0.0

    aligned_strategies: dict[str, pd.Series] = {}
    common_index: pd.DatetimeIndex | None = None

    for strategy_name, strategy_data in combined_strategies.items():
        if isinstance(strategy_data, pd.DataFrame):
            if value_col not in strategy_data.columns:
                raise KeyError(f"Column '{value_col}' not found in strategy '{strategy_name}'")
            values = strategy_data[value_col]
        elif isinstance(strategy_data, pd.Series):
            values = strategy_data
        else:
            raise TypeError(
                f"Strategy '{strategy_name}' must be a pandas DataFrame or Series, got {type(strategy_data).__name__}"
            )

        values = pd.Series(values).dropna()
        if not isinstance(values.index, pd.DatetimeIndex):
            values.index = pd.to_datetime(values.index)
        if values.index.tz is not None:
            values.index = values.index.tz_localize(None)
        values.index = values.index.normalize()

        aligned_strategies[strategy_name] = values.sort_index()
        common_index = values.index if common_index is None else common_index.intersection(values.index)

    if common_index is None or common_index.empty:
        raise ValueError("No common date range found across the provided strategies")

    results = []
    for strategy_name, values in aligned_strategies.items():
        common_values = values.reindex(common_index).dropna()
        returns = common_values.pct_change().replace([np.inf, -np.inf], np.nan).dropna()

        if returns.empty:
            sharpe_ratio = np.nan
        else:
            excess_returns = returns - period_risk_free_rate
            volatility = excess_returns.std()
            if pd.isna(volatility) or volatility == 0:
                sharpe_ratio = np.nan
            else:
                sharpe_ratio = np.sqrt(annualization_factor) * excess_returns.mean() / volatility

        results.append({
            "strategy": strategy_name,
            "sharpe_ratio": sharpe_ratio
        })

    return pd.DataFrame(results).sort_values("sharpe_ratio", ascending=False, na_position="last").reset_index(drop=True)
