"""
Code to create features for modeling
"""

from pathlib import Path

import pandas as pd

from config import PROCESSED_DATA_DIR


def construct_hybrid(
        long_df: pd.DataFrame,
        short_df: pd.DataFrame,
        save_csv: bool = False
) -> pd.DataFrame:

    long_df = long_df.copy()
    short_df = short_df.copy()
    long_df.index = pd.to_datetime(long_df.index, utc=True).normalize()
    short_df.index = pd.to_datetime(short_df.index, utc=True).normalize()

    price_cols = [c for c in long_df.columns if "volume" not in c.lower()]

    overlap = long_df.index.intersection(short_df.index)
    pre_ETF = long_df.loc[:short_df.index.min() - pd.Timedelta(days=1)]

    alpha = (short_df[price_cols].loc[overlap].pct_change().mean() -
             long_df[price_cols].loc[overlap].pct_change().mean())

    pre_returns = pre_ETF[price_cols].pct_change().fillna(0)
    pre_adjusted_prices = (1 + (pre_returns + alpha)).cumprod() * pre_ETF[price_cols].iloc[0]

    vol_cols = [c for c in long_df.columns if "volume" in c.lower()]
    pre_adjusted_vol = pre_ETF[vol_cols]

    pre_ETF_full = pd.concat([pre_adjusted_prices, pre_adjusted_vol], axis=1)

    scale = pre_adjusted_prices.iloc[-1] / short_df[price_cols].iloc[0]

    adjusted_short_prices = short_df[price_cols] * scale
    adjusted_short_full = pd.concat([adjusted_short_prices, short_df[vol_cols]], axis=1)

    hybrid_df = pd.concat([pre_ETF_full, adjusted_short_full]).sort_index()

    if save_csv:
        hybrid_df.to_csv("hybrid.csv")

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
