"""
Code to create features for modeling
"""

from pathlib import Path

import pandas as pd
import numpy as np

from config import PROCESSED_DATA_DIR


PROCESSED_DATA_DIR.mkdir(exist_ok=True)


def construct_hybrid(
        long_df: pd.DataFrame,
        short_df: pd.DataFrame,
        save_csv: bool = False,
        # cleanup_old: bool = False
) -> pd.DataFrame:

    ts = pd.Timestamp.now().strftime("%Y-%m-%d")
    file_path: Path = PROCESSED_DATA_DIR / f"benchmark_{ts}.csv"
    if file_path.exists():
        print(f"Loading existing benchmark from {file_path}")
        return pd.read_csv(file_path, index_col=0, parse_dates=True)

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
    price_col = "Adj Close"

    # Compute annual tracking difference from overlap
    overlap_dates = long_df.index.intersection(short_df.index)
    long_overlap = long_df.loc[overlap_dates, price_col]
    short_overlap = short_df.loc[overlap_dates, price_col]

    long_total_return = long_overlap.iloc[-1] / long_overlap.iloc[0]
    short_total_return = short_overlap.iloc[-1] / short_overlap.iloc[0]

    TD_annual = (long_total_return / short_total_return) ** (252 / len(overlap_dates)) - 1
    daily_drag = (1 + TD_annual) ** (1 / 252)

    # Adjust pre-ETF segment backward
    pre_mask = long_df.index < short_df.index[0]
    pre_df = long_df.loc[pre_mask].copy()
    n_days = len(pre_df)
    drag_factors = daily_drag ** np.arange(1, n_days + 1)

    pre_df[price_col] = pre_df[price_col] / drag_factors

    # Adjust other columns proportionally
    ratio = pre_df[price_col] / long_df.loc[pre_mask, price_col]
    for col in common_cols:
        if col != price_col:
            pre_df[col] = long_df.loc[pre_mask, col] * ratio

    # Scale to ETF start for continuity
    scale_factor = short_df[price_col].iloc[0] / pre_df[price_col].iloc[-1]
    pre_df[common_cols] = pre_df[common_cols] * scale_factor

    # Combine with ETF data
    post_df = short_df.loc[short_df.index >= short_df.index[0]]
    hybrid_df = pd.concat([pre_df, post_df]).sort_index()
    hybrid_df = hybrid_df[~hybrid_df.index.duplicated(keep='last')]

    # Keep only trading days of long_df
    hybrid_df = hybrid_df.loc[hybrid_df.index.intersection(long_df.index)]

    if save_csv:
        ts = pd.Timestamp.now().strftime("%Y-%m-%d")
        hybrid_df.to_csv(file_path)

    return hybrid_df


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
    # -----------------------------------------
):
    pass


if __name__ == "__main__":
    main()
