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

    overlap = long_df.index.intersection(short_df.index)
    pre_ETF = long_df.loc[:short_df.index.min() - pd.Timedelta(days=1)]

    alpha = short_df.loc[overlap].pct_change().mean() - long_df.loc[overlap].pct_change().mean()
    pre_ETF_adjusted = pre_ETF * (1 + alpha.values[0])

    last_pre_value = pre_ETF_adjusted.iloc[-1]
    first_ETF_value = short_df.iloc[0]
    scale = last_pre_value / first_ETF_value
    adjusted_ETF = short_df * scale

    hybrid_df = pd.concat([pre_ETF_adjusted, adjusted_ETF])

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
