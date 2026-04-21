"""
Code to create features for modeling
"""

from pathlib import Path

import pandas as pd
import numpy as np

from config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR


PROCESSED_DATA_DIR.mkdir(exist_ok=True)


def construct_hybrid(
        long_df: pd.DataFrame,
        short_df: pd.DataFrame,
        save_csv: bool = False,
        cleanup_old: bool = False
) -> pd.DataFrame:

    ts = pd.Timestamp.now().strftime("%Y-%m-%d")
    file_path: Path = PROCESSED_DATA_DIR / f"benchmark_{ts}.csv"
    existing_files = sorted(PROCESSED_DATA_DIR.glob("benchmark_????-??-??.csv"))
    last_file = None

    if file_path.exists():
        print(f"Loading existing benchmark from {file_path}")
        hybrid_df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        last_file = file_path
    else:

        def normalize_index(df):
            idx = df.index
            if hasattr(idx, 'tz') and idx.tz is not None:
                idx = idx.tz_localize(None)
            else:
                idx = pd.to_datetime(idx, utc=True).tz_localize(None)
            return df.set_index(idx.normalize())

        # Normalize dates
        long_df = normalize_index(long_df)
        short_df = normalize_index(short_df)

        # Common columns
        common_cols = short_df.columns.intersection(long_df.columns)
        long_df = long_df[common_cols]
        short_df = short_df[common_cols]
        price_col = "Adj_Close"

        if price_col not in common_cols:
            raise KeyError(f"Column '{price_col}' not found in both dataframes")

        short_start = short_df[price_col].first_valid_index()
        if short_start is None:
            raise ValueError("short_df does not contain any valid ETF prices")

        long_start = long_df[price_col].first_valid_index()
        if long_start is None:
            raise ValueError("long_df does not contain any valid prices")

        # Compute annual tracking difference from overlap
        overlap_dates = long_df.index.intersection(short_df.index)
        overlap_dates = overlap_dates[
            long_df.loc[overlap_dates, price_col].notna()
            & short_df.loc[overlap_dates, price_col].notna()
        ]
        if overlap_dates.empty:
            raise ValueError("No overlapping valid prices found between long_df and short_df")

        long_overlap = long_df.loc[overlap_dates, price_col]
        short_overlap = short_df.loc[overlap_dates, price_col]

        long_total_return = long_overlap.iloc[-1] / long_overlap.iloc[0]
        short_total_return = short_overlap.iloc[-1] / short_overlap.iloc[0]

        TD_annual = (long_total_return / short_total_return) ** (252 / len(overlap_dates)) - 1
        daily_drag = (1 + TD_annual) ** (1 / 252)

        # Adjust pre-ETF segment backward
        pre_mask = long_df.index < short_start
        pre_df = long_df.loc[pre_mask].copy()
        if pre_df.empty:
            hybrid_df = short_df.loc[short_df[price_col].notna()].copy()
        else:
            n_days = len(pre_df)
            drag_factors = daily_drag ** np.arange(1, n_days + 1)

            pre_df[price_col] = pre_df[price_col] / drag_factors

            # Adjust other columns proportionally
            ratio = pre_df[price_col] / long_df.loc[pre_mask, price_col]
            for col in common_cols:
                if col != price_col:
                    pre_df[col] = long_df.loc[pre_mask, col] * ratio

            # Scale to ETF start for continuity using the first valid ETF point
            scale_factor = short_df.loc[short_start, price_col] / pre_df[price_col].iloc[-1]
            pre_df[common_cols] = pre_df[common_cols] * scale_factor

            # Remove any leading rows that still lack valid price data
            pre_df = pre_df.loc[pre_df[price_col].notna()]

        # Combine with ETF data
        post_df = short_df.loc[short_df.index >= short_start]
        hybrid_df = pd.concat([pre_df, post_df]).sort_index()
        hybrid_df = hybrid_df[~hybrid_df.index.duplicated(keep='last')]

        # Keep only trading days of long_df
        hybrid_df = hybrid_df.loc[hybrid_df.index.intersection(long_df.index)]

        if save_csv:
            hybrid_df.to_csv(file_path)
            print(f"Saved benchmark to {file_path}")
            last_file = file_path
    if cleanup_old and last_file:
        deleted = 0
        for f in existing_files:
            if f != last_file:
                f.unlink()
                deleted += 1
                print(f"Deleted old file: {f.name}")
        if deleted:
            print(f"Deleted {deleted} old file(s) for benchmark")
    elif cleanup_old:
        print("cleanup_old is True but no benchmark file was saved or loaded. Skipping cleanup.")

    return hybrid_df


def merge_price_data(
    primary_data: dict[str, pd.DataFrame],
    supplemental_data: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:

    all_keys = set(primary_data) | set(supplemental_data)
    result: dict[str, pd.DataFrame] = {}

    for key in sorted(all_keys):
        primary_frame = primary_data.get(key, pd.DataFrame())
        supplemental_frame = supplemental_data.get(key, pd.DataFrame())

        if primary_frame.empty and supplemental_frame.empty:
            result[key] = pd.DataFrame()
            continue

        if primary_frame.empty:
            result[key] = supplemental_frame.copy()
            continue

        if supplemental_frame.empty:
            result[key] = primary_frame.copy()
            continue

        overlapping = primary_frame.columns.intersection(supplemental_frame.columns)
        supplemental_only = supplemental_frame.columns.difference(primary_frame.columns)

        primary_preferred = primary_frame.copy()
        if len(overlapping):
            primary_preferred[overlapping] = primary_frame[overlapping].combine_first(
                supplemental_frame[overlapping]
            )

        if len(supplemental_only):
            merged = pd.concat(
                [primary_preferred, supplemental_frame[supplemental_only]], axis=1
            ).sort_index()
        else:
            merged = primary_preferred.sort_index()

        result[key] = merged

    return result


def merge_index_data(
    primary_df: pd.DataFrame,
    supplemental_df: pd.DataFrame,
) -> pd.DataFrame:

    if primary_df.empty:
        return supplemental_df.copy()
    if supplemental_df.empty:
        return primary_df.copy()

    def normalize(df):
        df = df.copy()
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df.index = df.index.normalize()
        return df

    p = normalize(primary_df)
    s = normalize(supplemental_df)

    # combine_first prefers values from 'p' and fills from 's' for
    # both missing indices (dates) and NaN values.
    return p.combine_first(s).sort_index()


def save_merged_data(
    df: dict[str, pd.DataFrame],
) -> None:
    output_path = Path(INTERIM_DATA_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    for col, frame in df.items():
        if frame.empty or frame.dropna(how="all").empty:
            continue
        path = output_path / f"{col}.csv"
        frame.to_csv(path)
        print(f"Saved {col}.csv ({len(frame)} rows x {len(frame.columns)} columns)")


def average_companies(
    companies: dict[str, pd.DataFrame], components: pd.DataFrame
) -> dict[str, pd.DataFrame]:

    if not companies:
        print("No company data provided for averaging.")
        return {}

    if components.empty:
        print("No S&P 500 components data provided for filtering.")
        return {}

    # Pre-process components into a time-indexed map for efficient lookup
    comp_df = components.copy()
    comp_df["date"] = pd.to_datetime(comp_df["date"]).dt.normalize()
    comp_df = comp_df.sort_values("date")

    ticker_map = {}
    for _, row in comp_df.iterrows():
        dt = row["date"]
        tickers = {t.strip() for t in str(row["tickers"]).split(",") if t.strip()}
        ticker_map[dt] = tickers

    comp_dates = sorted(ticker_map.keys())

    result = {}
    from bisect import bisect_right

    for feature, df in companies.items():
        if df.empty:
            result[feature] = pd.DataFrame()
            continue

        # Normalize df index to match components normalization
        df_clean = df.copy()
        if not isinstance(df_clean.index, pd.DatetimeIndex):
            df_clean.index = pd.to_datetime(df_clean.index)

        # Ensure UTC-naive for normalization and comparison
        if df_clean.index.tz is not None:
            df_clean.index = df_clean.index.tz_localize(None)
        df_clean.index = df_clean.index.normalize()

        # Compute the mean for each row individually because the set of
        # active tickers changes over time.
        means = []
        for date, row in df_clean.iterrows():

            # Find the set of S&P 500 tickers active on or before this date
            idx = bisect_right(comp_dates, date) - 1
            if idx >= 0:
                active_sp500 = ticker_map[comp_dates[idx]]
            else:
                active_sp500 = set()

            # Intersection of available data columns and active S&P 500 tickers
            valid_tickers = [t for t in df_clean.columns if t in active_sp500]

            if valid_tickers:
                # Calculate mean for the valid tickers on this date, ignoring NaNs
                row_mean = row[valid_tickers].mean()
                means.append(row_mean)
            else:
                means.append(np.nan)

        result[feature] = pd.DataFrame(means, index=df_clean.index, columns=[feature])

    return result


def construct_missing_ticker(
    companies_average: dict[str, pd.DataFrame],
    index_data: pd.DataFrame,
    coverage: pd.DataFrame,
) -> pd.DataFrame:

    if "Adj_Close" not in companies_average:
        raise KeyError("companies_average must contain 'Adj_Close'")

    # 1. Get the observed average returns (delta_r_observed)
    observed_prices: pd.DataFrame = companies_average["Adj_Close"]
    observed_returns: pd.DataFrame = observed_prices.pct_change()

    # 2. Get index returns (delta_r_index)
    price_col = "Adj_Close" if "Adj_Close" in index_data.columns else "Close"
    if price_col not in index_data.columns:
        price_col = index_data.columns[0]
    index_returns: pd.DataFrame = index_data[price_col].pct_change()

    # 3. Get coverage fraction
    if "coverage_pct" not in coverage.columns:
        raise KeyError("coverage DataFrame must contain 'coverage_pct' column")
    coverage_fraction: pd.DataFrame = coverage["coverage_pct"] / 100.0

    # 4. Align all data by creating a combined DataFrame
    combined = pd.DataFrame({
            "index_ret": index_returns,
            "observed_ret": observed_returns.iloc[:, 0],
            "coverage": coverage_fraction,
        }
    ).dropna(subset=["index_ret", "observed_ret", "coverage"])

    # 5. Apply the formula
    # Handle the 100% coverage case to avoid division by zero
    mask = combined["coverage"] < 1.0
    combined["missing_ret"] = np.nan
    combined.loc[mask, "missing_ret"] = (
        combined.loc[mask, "index_ret"]
        - combined.loc[mask, "coverage"] * combined.loc[mask, "observed_ret"]
    ) / (1 - combined.loc[mask, "coverage"])

    # If coverage is 100%, there is no missing return to compute (set to index_ret or 0)
    combined.loc[~mask, "missing_ret"] = combined.loc[~mask, "index_ret"]

    # 6. Reconstruct price series from returns
    # We start with an arbitrary base price of 100.0
    missing_prices = (1 + combined["missing_ret"].fillna(0)).cumprod() * 100.0

    result = pd.DataFrame(index=combined.index)
    result["Adj_Close"] = missing_prices
    for col in ["Open", "High", "Low", "Close"]:
        result[col] = result["Adj_Close"]
    result["Volume"] = 0

    return result


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
    # -----------------------------------------
):
    pass


if __name__ == "__main__":
    main()
