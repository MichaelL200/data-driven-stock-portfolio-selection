"""
Code to download or generate data
"""

import os
import shutil
import time
import random
from datetime import datetime
from pathlib import Path
from typing import List
import pandas as pd
import pandas_market_calendars as mcal

import papermill as pm
import yfinance as yf
import eodhd

from config import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR, PROJ_ROOT, RAW_DATA_DIR


_YF_COLUMN_MAP = [
    ("Close", "Close"),
    ("Open", "Open"),
    ("High", "High"),
    ("Low", "Low"),
    ("Volume", "Volume"),
    ("Adj Close", "Adj_Close"),
]


def _normalize_index(df: pd.DataFrame) -> pd.DataFrame:
    normalized_index = pd.to_datetime(df.index, utc=True).normalize()
    result = df.copy()
    result.index = normalized_index
    return result


def _has_new_trading_days(last_date: pd.Timestamp, today: pd.Timestamp = None) -> bool:
    if today is None:
        today = pd.Timestamp.now(tz="UTC").normalize()
    calendar = mcal.get_calendar("NYSE")
    schedule = calendar.schedule(start_date=last_date.date(), end_date=today.date())
    trading_days = pd.to_datetime(schedule.index, utc=True).normalize()
    return (trading_days > last_date.normalize()).any()


def _extract_batch_columns(normalized_batch: pd.DataFrame, downloaded_parts: dict) -> None:
    for source_col, target_col in _YF_COLUMN_MAP:
        if source_col in normalized_batch.columns.get_level_values(0):
            extracted = normalized_batch.xs(source_col, level=0, axis=1)
            extracted.columns = extracted.columns.astype(str)
            extracted = _normalize_index(extracted)
            downloaded_parts[target_col].append(extracted)


class StockDataSource:
    """Base class for per-ticker stock market data sources.

    Subclasses must define a ``submodule_name`` class variable. The
    corresponding ``dst_dir`` directory is created automatically.
    """

    submodule_name: str
    dst_dir: Path

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = getattr(cls, "submodule_name", None)
        if name is not None:
            cls.dst_dir = EXTERNAL_DATA_DIR / name
            cls.dst_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_file_path(cls, ticker: str) -> Path:
        return cls.dst_dir / f"{ticker.strip()}.csv"

    @classmethod
    def load_ticker(cls, ticker: str) -> pd.DataFrame:
        clean_ticker = str(ticker).strip()
        file_path = cls._get_file_path(clean_ticker)
        if not file_path.exists():
            raise FileNotFoundError(
                f"No saved {cls.submodule_name} data file found for ticker: {clean_ticker}"
            )
        return pd.read_csv(file_path)


class SP500:

    submodule_name: str = "sp500"
    src_dir: Path = PROJ_ROOT / submodule_name
    dst_dir: Path = EXTERNAL_DATA_DIR / submodule_name
    dst_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _run_notebook(cls, nb_path: Path):
        pm.execute_notebook(str(nb_path), str(nb_path), cwd=str(nb_path.parent))

    @classmethod
    def _generate(
        cls, nb_path: Path,
        src_file: Path,
        dst_file: Path,
        cleanup_old: bool = False,
        pattern_old: str = None
    ) -> Path:

        if dst_file.exists():
            print(f"No generation needed: {dst_file.name} already exists.")
        else:
            cls._run_notebook(nb_path)
            shutil.copy(src_file, dst_file)
            print(f"Generated new file: {dst_file.name}")

        if cleanup_old and pattern_old:
            deleted: int = 0
            for f in cls.dst_dir.glob(pattern_old):
                if f != dst_file:
                    f.unlink()
                    deleted += 1
                    print(f"Deleted old file: {f.name}")
            if deleted:
                print(f"Deleted {deleted} old file(s) matching pattern: {pattern_old}")
        elif cleanup_old:
            print("cleanup_old is True but no pattern_old provided. Skipping cleanup.")

        return dst_file

    @classmethod
    def generate_current(cls, cleanup_old: bool = False) -> Path:

        ts = datetime.now().strftime("%Y-%m-%d")
        nb_current = cls.src_dir / "sp500.ipynb"
        src_file = cls.src_dir / "sp500.csv"
        dst_file = cls.dst_dir / f"sp500_{ts}.csv"

        return cls._generate(
            nb_path=nb_current,
            src_file=src_file,
            dst_file=dst_file,
            cleanup_old=cleanup_old,
            pattern_old="sp500_????-??-??.csv"
        )

    @classmethod
    def generate_historical(cls, cleanup_old: bool = False) -> Path:

        ts_dst = datetime.now().strftime("%Y-%m-%d")
        ts_src = datetime.now().strftime("%m-%d-%Y")

        nb_historical = cls.src_dir / "sp500_historical.ipynb"
        src_file = cls.src_dir / f"S&P 500 Historical Components & Changes({ts_src}).csv"
        dst_file = cls.dst_dir / f"sp500_historical_{ts_dst}.csv"

        return cls._generate(
            nb_path=nb_historical,
            src_file=src_file,
            dst_file=dst_file,
            cleanup_old=cleanup_old,
            pattern_old="sp500_historical_????-??-??.csv"
        )

    @classmethod
    def _load(cls, pattern: str) -> pd.DataFrame:

        files = list(cls.dst_dir.glob(pattern))

        if not files:
            raise FileNotFoundError(f"No files for pattern: {pattern}")

        latest_file = max(files, key=lambda f: f.name)

        return pd.read_csv(latest_file)

    @classmethod
    def load_current(cls, save_csv: bool = False) -> pd.DataFrame:
        return cls._load("sp500_????-??-??.csv")

    @classmethod
    def load_historical(cls, save_csv: bool = False) -> pd.DataFrame:
        return cls._load("sp500_historical_????-??-??.csv")


class YahooFinance(StockDataSource):

    submodule_name: str = "yfinance"

    @classmethod
    def get_ticker_data_incremental(
        cls,
        ticker: str,
        save_csv: bool = False
    ) -> pd.DataFrame:

        file_path: Path = cls.dst_dir / f"{ticker}.csv"

        if file_path.exists():

            print(f"Loading existing data for {ticker} from {file_path.name}")
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)
            data.index = pd.to_datetime(data.index, utc=True)
            last_date = data.index.max()
            today = pd.Timestamp.now(tz='UTC')

            # Check if there have been trading days since last date
            has_new_trading_days = _has_new_trading_days(last_date, today)

            if has_new_trading_days:
                # Fetch new data starting from last date (will include overlaps)
                print(f"Fetching new data for {ticker} since {last_date.date()}")
                new_data = yf.Ticker(ticker).history(start=last_date, auto_adjust=False)

                if not new_data.empty:
                    # Concatenate and remove duplicates, keeping last (most recent)
                    data = pd.concat([data, new_data])
                    data = data[~data.index.duplicated(keep='last')]
                    data = data.sort_index()
                    print(f"Updated {ticker} with new data")
                else:
                    print(f"No new data for {ticker}")
            else:
                print(f"No new trading days for {ticker} since {last_date.date()}")
        else:
            print(f"Fetching full historical data for {ticker}")
            data = yf.Ticker(ticker).history(period="max", auto_adjust=False)
            print(f"Fetched {len(data)} rows for {ticker}")

        if save_csv:
            data.to_csv(file_path)
            print(f"Saved data for {ticker} to {file_path.name}")

        return data

    @classmethod
    def download_batch(
        cls,
        sp500_components: pd.DataFrame,
        batch_size: int = 200,
        sleep_seconds: float = 2.0,
        save_csv: bool = False,
        redownload_missing_tickers: bool = False,
    ) -> dict[str, pd.DataFrame]:

        # Extract unique tickers from sp500_components
        tickers_col = "tickers"
        if tickers_col not in sp500_components.columns:
            raise KeyError(f"Column '{tickers_col}' not found in sp500_components")

        exploded = sp500_components[tickers_col].dropna().astype(str).str.split(",")
        tickers = (
            exploded.explode()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .drop_duplicates()
        )
        tickers = sorted(tickers.tolist())
        print("Number of unique tickers extracted:", len(tickers))

        output_columns = ["Close", "Open", "High", "Low", "Volume", "Adj_Close"]
        output_paths = {col: cls.dst_dir / f"{col}.csv" for col in output_columns}

        def load_existing(path: Path) -> pd.DataFrame:
            data = pd.read_csv(path, index_col=0, parse_dates=True)
            return _normalize_index(data)

        def normalize_download_frame(batch_df: pd.DataFrame, batch_tickers: list[str]) -> pd.DataFrame:
            if not isinstance(batch_df.columns, pd.MultiIndex):
                ticker = str(batch_tickers[0])
                batch_df = batch_df.copy()
                batch_df.columns = pd.MultiIndex.from_tuples(
                    [(col, ticker) for col in batch_df.columns],
                    names=["Field", "Ticker"],
                )
                return batch_df

            result = batch_df.copy()
            result.columns = result.columns.set_names(["Field", "Ticker"])
            return result

        existing_data: dict[str, pd.DataFrame] = {}
        existing_paths = {col: path for col, path in output_paths.items() if path.exists()}

        clean_tickers = [str(ticker).strip() for ticker in tickers if str(ticker).strip()]
        if not clean_tickers:
            return {col: pd.DataFrame() for col in output_columns}

        yf_start = None
        if existing_paths:

            for col, path in existing_paths.items():
                existing_data[col] = load_existing(path)

            reference_col = "Close" if "Close" in existing_data else next(iter(existing_data))
            last_date = existing_data[reference_col].index.max()
            today = pd.Timestamp.now(tz="UTC").normalize()

            if not _has_new_trading_days(last_date, today):
                print(f"No new trading days since {last_date.date()}.")

                if not redownload_missing_tickers:
                    print("Skipping missing ticker re-download (redownload_missing_tickers=False)")
                    return existing_data

                print("Checking for missing ticker data...")

                # Identify tickers with incomplete data
                # A ticker has incomplete data if it has significant NaN values
                tickers_with_incomplete_data = []

                for ticker in clean_tickers:
                    if ticker in existing_data[reference_col].columns:

                        ticker_data = existing_data[reference_col][ticker]
                        # Calculate percentage of NaN values
                        nan_ratio = ticker_data.isna().sum() / len(ticker_data)

                        # If more than 50% NaN, mark as incomplete
                        if nan_ratio > 0.5:
                            tickers_with_incomplete_data.append((ticker, nan_ratio))
                    else:
                        # Ticker not in columns at all (shouldn't happen if data was merged)
                        tickers_with_incomplete_data.append((ticker, 1.0))

                if tickers_with_incomplete_data:

                    print(
                        f"Found {len(tickers_with_incomplete_data)} tickers with >50% missing data. "
                        f"Attempting to re-download..."
                    )

                    if len(tickers_with_incomplete_data) <= 20:
                        for ticker, nan_ratio in tickers_with_incomplete_data:
                            print(f"  {ticker}: {nan_ratio*100:.1f}% NaN")
                    else:
                        for ticker, nan_ratio in tickers_with_incomplete_data[:10]:
                            print(f"  {ticker}: {nan_ratio*100:.1f}% NaN")
                        print(f"  ... and {len(tickers_with_incomplete_data) - 10} more")

                    all_missing_tickers = [t[0] for t in tickers_with_incomplete_data]

                    # Try to download data for incomplete tickers
                    downloaded_parts_missing: dict[str, list[pd.DataFrame]] = {
                        col: [] for col in output_columns
                    }

                    for batch_index, batch_start in enumerate(range(0, len(all_missing_tickers), batch_size)):

                        batch = all_missing_tickers[batch_start:batch_start + batch_size]
                        download_kwargs = {
                            "auto_adjust": False,
                            "timeout": 30,
                            "progress": False,
                            "period": "max",
                        }

                        print(f"Downloading batch {batch_index + 1} ({len(batch)} tickers)...")
                        batch_df = yf.download(batch, **download_kwargs)

                        if batch_df.empty:
                            print(f"Warning: empty download for batch {batch_index + 1}")
                        else:
                            normalized_batch = normalize_download_frame(batch_df, batch)
                            _extract_batch_columns(normalized_batch, downloaded_parts_missing)

                        if batch_start + batch_size < len(all_missing_tickers):
                            time.sleep(sleep_seconds + random.uniform(0, 3))

                    # Merge newly downloaded data with existing data
                    # Use outer join to preserve all dates, then take last (prefer new data)
                    for col in output_columns:

                        parts = downloaded_parts_missing[col]
                        batch_combined = pd.concat(parts, axis=1) if parts else pd.DataFrame()
                        batch_combined = batch_combined.loc[:, ~batch_combined.columns.duplicated(keep="last")]

                        if not batch_combined.empty:
                            batch_combined.index = pd.to_datetime(batch_combined.index, utc=True).normalize()
                            # Merge by combining: existing data + new data, prefer non-null values
                            for ticker in all_missing_tickers:
                                if ticker in batch_combined.columns and ticker in existing_data[col].columns:
                                    # Update null values in existing data with new data
                                    mask = existing_data[col][ticker].isna()
                                    existing_data[col].loc[mask, ticker] = batch_combined.loc[mask, ticker]

                    print(f"Successfully re-downloaded and merged data for {len(all_missing_tickers)} tickers")
                else:
                    print("No tickers found with significant missing data (>50% NaN)")

                return existing_data

            yf_start = last_date

        downloaded_parts: dict[str, list[pd.DataFrame]] = {col: [] for col in output_columns}

        for batch_index, batch_start in enumerate(range(0, len(clean_tickers), batch_size)):

            batch = clean_tickers[batch_start:batch_start + batch_size]
            download_kwargs = {
                "auto_adjust": False,
                "timeout": 30,
                "progress": False,
            }
            if yf_start is None:
                download_kwargs["period"] = "max"
            else:
                download_kwargs["start"] = yf_start

            batch_df = yf.download(batch, **download_kwargs)

            if batch_df.empty:
                print(f"Warning: empty download for batch {batch_index + 1} ({len(batch)} tickers)")
            else:
                normalized_batch = normalize_download_frame(batch_df, batch)
                _extract_batch_columns(normalized_batch, downloaded_parts)

            if batch_start + batch_size < len(clean_tickers):
                time.sleep(sleep_seconds + random.uniform(0, 3))

        result: dict[str, pd.DataFrame] = {}
        for col in output_columns:

            batch_combined = pd.concat(downloaded_parts[col], axis=1) if downloaded_parts[col] else pd.DataFrame()
            batch_combined = batch_combined.loc[:, ~batch_combined.columns.duplicated(keep="last")]

            if not batch_combined.empty:
                batch_combined.index = pd.to_datetime(batch_combined.index, utc=True).normalize()

            existing_df = existing_data[col] if col in existing_data else pd.DataFrame()

            if existing_df.empty and batch_combined.empty:
                combined = pd.DataFrame()
            else:
                combined = pd.concat([existing_df, batch_combined], axis=0, join="outer")
                combined = combined[~combined.index.duplicated(keep="last")].sort_index()
                combined.index = pd.to_datetime(combined.index, utc=True).normalize()

            result[col] = combined

        if save_csv:
            for col, data in result.items():
                data.to_csv(output_paths[col])
                print(f"Saved {col}.csv ({len(data)} rows x {len(data.columns)} columns)")

        return result


class EODHD(StockDataSource):

    submodule_name: str = "eodhd"

    @classmethod
    def download_tickers(
        cls,
        tickers: List[str],
        api_key: str = None,
        save_csv: bool = False
    ) -> dict[str, pd.DataFrame]:

        if api_key is None:
            api_key = os.getenv("EODHD_API_KEY")
        if api_key is None:
            raise ValueError(
                "EODHD API key not found. Set the EODHD_API_KEY environment variable "
                "or pass the key explicitly via the `api_key` parameter."
            )

        client = eodhd.APIClient(api_key)
        result: dict[str, pd.DataFrame] = {}

        for ticker in tickers:

            clean_ticker = str(ticker).strip()
            if not clean_ticker:
                continue

            file_path = cls.dst_dir / f"{clean_ticker}.csv"

            if file_path.exists():
                print(f"Loading existing data for {clean_ticker} from {file_path.name}")
                frame = pd.read_csv(file_path)

                if frame.empty or "date" not in frame.columns:
                    print(
                        f"Skipping incremental update for {clean_ticker}: "
                        "missing or empty 'date' column"
                    )
                    result[clean_ticker] = frame
                    continue

                parsed_dates = pd.to_datetime(frame["date"], errors="coerce", utc=True)
                valid_dates = parsed_dates.dropna()

                if valid_dates.empty:
                    print(
                        f"Skipping incremental update for {clean_ticker}: "
                        "no valid dates in existing file"
                    )
                    result[clean_ticker] = frame
                    continue

                last_date = valid_dates.max().normalize()
                today = pd.Timestamp.now(tz="UTC").normalize()

                has_new_trading_days = _has_new_trading_days(last_date, today)

                if not has_new_trading_days:
                    print(f"No new trading days for {clean_ticker} since {last_date.date()}")
                    result[clean_ticker] = frame
                    continue

                from_date = last_date.strftime("%Y-%m-%d")

                try:
                    raw_data = client.get_eod_historical_stock_market_data(
                        symbol=clean_ticker,
                        period="d",
                        order="a",
                        from_date=from_date,
                    )
                except Exception as exc:
                    print(f"Failed to download incremental data for {clean_ticker}: {exc}")
                    result[clean_ticker] = frame
                    continue

                new_frame = pd.DataFrame(raw_data)

                if new_frame.empty:
                    print(f"No new API data returned for {clean_ticker}")
                    result[clean_ticker] = frame
                    continue

                combined = pd.concat([frame, new_frame], ignore_index=True)
                combined["date"] = pd.to_datetime(combined["date"], errors="coerce", utc=True)
                combined = combined.dropna(subset=["date"])
                combined = combined.sort_values("date")
                combined = combined.drop_duplicates(subset=["date"], keep="last")
                combined["date"] = combined["date"].dt.strftime("%Y-%m-%d")
                combined = combined.reset_index(drop=True)

                result[clean_ticker] = combined

                if save_csv:
                    combined.to_csv(file_path, index=False)
                    print(f"Updated data for {clean_ticker} in {file_path.name}")

                continue

            try:
                raw_data = client.get_eod_historical_stock_market_data(
                    symbol=clean_ticker,
                    period="d",
                    order="a"
                )
            except Exception as exc:
                print(f"Failed to download data for {clean_ticker}: {exc}")
                continue

            frame = pd.DataFrame(raw_data)
            result[clean_ticker] = frame

            if save_csv:
                frame.to_csv(file_path, index=False)
                print(f"Saved data for {clean_ticker} to {file_path.name}")

        return result


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv"
    # ----------------------------------------------
):

    pass


if __name__ == "__main__":
    main()
