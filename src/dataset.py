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

_EODHD_COLUMN_MAP = [
    ("close", "Close"),
    ("open", "Open"),
    ("high", "High"),
    ("low", "Low"),
    ("volume", "Volume"),
    ("adjusted_close", "Adj_Close"),
]


def _has_new_trading_days(last_date: pd.Timestamp, today: pd.Timestamp = None) -> bool:
    if today is None:
        today = pd.Timestamp.now(tz="UTC").normalize()
    calendar = mcal.get_calendar("NYSE")
    schedule = calendar.schedule(start_date=last_date.date(), end_date=today.date())
    trading_days = pd.to_datetime(schedule.index, utc=True).normalize()
    completed_trading_days = trading_days[trading_days < today]
    return (completed_trading_days > last_date.normalize()).any()


def _normalize_columnar_index(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result.index = pd.to_datetime(result.index, utc=True).normalize()
    result.index.name = "Date"
    return result


def _load_columnar_frame(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    return _normalize_columnar_index(data)


def _combine_columnar_frames(
    existing_frames: dict[str, pd.DataFrame],
    downloaded_parts: dict[str, list[pd.DataFrame]],
    output_columns: list[str],
) -> dict[str, pd.DataFrame]:

    combined_result: dict[str, pd.DataFrame] = {}

    for col in output_columns:

        batch_combined = (
            pd.concat(downloaded_parts[col], axis=1)
            if downloaded_parts[col]
            else pd.DataFrame()
        )
        batch_combined = batch_combined.loc[:, ~batch_combined.columns.duplicated(keep="last")]
        if not batch_combined.empty:
            batch_combined.index = pd.to_datetime(batch_combined.index, utc=True).normalize()

        existing_df = existing_frames[col] if col in existing_frames else pd.DataFrame()
        if existing_df.empty and batch_combined.empty:
            combined = pd.DataFrame()
        else:
            combined = pd.concat([existing_df, batch_combined], axis=0, join="outer")
            combined = combined[~combined.index.duplicated(keep="last")].sort_index()
            combined.index = pd.to_datetime(combined.index, utc=True).normalize()
            combined.index.name = "Date"

        if not combined.empty:
            combined.index.name = "Date"

        combined_result[col] = combined

    return combined_result


def _find_incomplete_tickers(
    reference_frame: pd.DataFrame,
    tickers: list[str],
) -> list[tuple[str, float]]:

    incomplete: list[tuple[str, float]] = []

    for ticker_name in tickers:
        if ticker_name in reference_frame.columns:
            ticker_data = reference_frame[ticker_name]
            nan_ratio = ticker_data.isna().sum() / len(ticker_data)
            if nan_ratio > 0.5:
                incomplete.append((ticker_name, nan_ratio))
        else:
            incomplete.append((ticker_name, 1.0))

    return incomplete


def _print_incomplete_tickers(incomplete: list[tuple[str, float]]) -> None:

    if len(incomplete) <= 20:
        for ticker_name, nan_ratio in incomplete:
            print(f"  {ticker_name}: {nan_ratio*100:.1f}% NaN")
        return

    for ticker_name, nan_ratio in incomplete[:10]:
        print(f"  {ticker_name}: {nan_ratio*100:.1f}% NaN")
    print(f"  ... and {len(incomplete) - 10} more")


def _print_status_report(status_map: dict[str, str], header: str) -> None:

    if not status_map:
        return

    print(header)
    for ticker_name in sorted(status_map):
        print(f"  {ticker_name}: {status_map[ticker_name]}")


def _merge_missing_ticker_data(
    existing_frames: dict[str, pd.DataFrame],
    downloaded_parts: dict[str, list[pd.DataFrame]],
    missing_tickers: list[str],
    output_columns: list[str],
) -> None:

    for col in output_columns:

        parts = downloaded_parts[col]
        batch_combined = pd.concat(parts, axis=1) if parts else pd.DataFrame()
        batch_combined = batch_combined.loc[:, ~batch_combined.columns.duplicated(keep="last")]

        if batch_combined.empty:
            continue

        batch_combined.index = pd.to_datetime(batch_combined.index, utc=True).normalize()
        for ticker_name in missing_tickers:
            if ticker_name in batch_combined.columns and ticker_name in existing_frames[col].columns:
                mask = existing_frames[col][ticker_name].isna()
                existing_frames[col].loc[mask, ticker_name] = batch_combined.loc[mask, ticker_name]


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


class StockDataSource:

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


class YahooFinance(StockDataSource):

    submodule_name: str = "yfinance"

    @staticmethod
    def _normalize_index(df: pd.DataFrame) -> pd.DataFrame:
        return _normalize_columnar_index(df)

    @staticmethod
    def _extract_batch_columns(normalized_batch: pd.DataFrame, downloaded_parts: dict) -> None:
        for source_col, target_col in _YF_COLUMN_MAP:
            if source_col in normalized_batch.columns.get_level_values(0):
                extracted = normalized_batch.xs(source_col, level=0, axis=1)
                extracted.columns = extracted.columns.astype(str)
                extracted = YahooFinance._normalize_index(extracted)
                downloaded_parts[target_col].append(extracted)

    @classmethod
    def get_ticker_data_incremental(
        cls,
        ticker: str,
        save_csv: bool = False
    ) -> pd.DataFrame:

        file_path: Path = cls.dst_dir / f"{ticker}.csv"

        def load_existing_data() -> pd.DataFrame:
            print(f"Loading existing data for {ticker} from {file_path.name}")
            loaded = pd.read_csv(file_path, index_col=0, parse_dates=True)
            loaded.index = pd.to_datetime(loaded.index, utc=True)
            loaded.index.name = "Date"
            return loaded

        def update_existing_data(existing: pd.DataFrame) -> pd.DataFrame:

            last_date = existing.index.max()
            today = pd.Timestamp.now(tz="UTC")

            if not _has_new_trading_days(last_date, today):
                print(f"No new trading days for {ticker} since {last_date.date()}")
                return existing

            print(f"Fetching new data for {ticker} since {last_date.date()}")
            new_data = yf.Ticker(ticker).history(start=last_date, auto_adjust=False)

            if new_data.empty:
                print(f"No new data for {ticker}")
                return existing

            new_data.index.name = "Date"

            updated = pd.concat([existing, new_data])
            updated = updated[~updated.index.duplicated(keep="last")]
            updated = updated.sort_index()
            updated.index.name = "Date"
            print(f"Updated {ticker} with new data")
            return updated

        def fetch_full_history() -> pd.DataFrame:
            print(f"Fetching full historical data for {ticker}")
            fetched = yf.Ticker(ticker).history(period="max", auto_adjust=False)
            fetched.index.name = "Date"
            print(f"Fetched {len(fetched)} rows for {ticker}")
            return fetched

        if file_path.exists():
            data = update_existing_data(load_existing_data())
        else:
            data = fetch_full_history()

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

        output_columns = ["Close", "Open", "High", "Low", "Volume", "Adj_Close"]
        output_paths = {col: cls.dst_dir / f"{col}.csv" for col in output_columns}
        ticker_status: dict[str, str] = {}

        def _parse_sp500_tickers() -> list[str]:

            tickers_col = "tickers"
            if tickers_col not in sp500_components.columns:
                raise KeyError(f"Column '{tickers_col}' not found in sp500_components")

            exploded = sp500_components[tickers_col].dropna().astype(str).str.split(",")
            raw_tickers = (
                exploded.explode()
                .astype(str)
                .str.strip()
                .replace("", pd.NA)
                .dropna()
                .drop_duplicates()
            )
            clean = [str(ticker).strip() for ticker in sorted(raw_tickers.tolist()) if str(ticker).strip()]
            print("Number of unique tickers extracted:", len(clean))
            return clean

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

        def download_parts_for_tickers(
            tickers_to_download: list[str],
            *,
            period: str = None,
            start: pd.Timestamp = None,
        ) -> dict[str, list[pd.DataFrame]]:

            downloaded_parts_local: dict[str, list[pd.DataFrame]] = {col: [] for col in output_columns}

            for batch_index, batch_start in enumerate(range(0, len(tickers_to_download), batch_size)):
                batch = tickers_to_download[batch_start:batch_start + batch_size]
                download_kwargs = {
                    "auto_adjust": False,
                    "timeout": 30,
                    "progress": False,
                }
                if period is not None:
                    download_kwargs["period"] = period
                if start is not None:
                    download_kwargs["start"] = start

                print(f"Downloading batch {batch_index + 1} ({len(batch)} tickers)...")
                batch_df = yf.download(batch, **download_kwargs)

                if batch_df.empty:
                    print(f"Warning: empty download for batch {batch_index + 1}")
                    for ticker_name in batch:
                        ticker_status[ticker_name] = "missing_from_batch"
                else:
                    normalized_batch = normalize_download_frame(batch_df, batch)
                    cls._extract_batch_columns(normalized_batch, downloaded_parts_local)
                    available_tickers = set(normalized_batch.columns.get_level_values("Ticker"))
                    for ticker_name in batch:
                        if ticker_name in available_tickers:
                            ticker_status[ticker_name] = "downloaded"
                        else:
                            ticker_status[ticker_name] = "missing_from_batch"

                if batch_start + batch_size < len(tickers_to_download):
                    time.sleep(sleep_seconds + random.uniform(0, 3))

            return downloaded_parts_local

        def combine_final_frames(
            existing_frames: dict[str, pd.DataFrame],
            downloaded_parts_local: dict[str, list[pd.DataFrame]],
        ) -> dict[str, pd.DataFrame]:
            return _combine_columnar_frames(existing_frames, downloaded_parts_local, output_columns)

        clean_tickers = _parse_sp500_tickers()
        if not clean_tickers:
            return {col: pd.DataFrame() for col in output_columns}

        existing_data: dict[str, pd.DataFrame] = {}
        existing_paths = {col: path for col, path in output_paths.items() if path.exists()}

        yf_start = None
        if existing_paths:

            for col, path in existing_paths.items():
                existing_data[col] = _load_columnar_frame(path)

            reference_col = "Close" if "Close" in existing_data else next(iter(existing_data))
            reference_frame = existing_data[reference_col]
            last_date = reference_frame.index.max()
            today = pd.Timestamp.now(tz="UTC").normalize()

            if not _has_new_trading_days(last_date, today):

                print(f"No new trading days since {last_date.date()}.")

                if not redownload_missing_tickers:
                    print("Skipping missing ticker re-download (redownload_missing_tickers=False)")
                    _print_status_report(ticker_status, "YahooFinance per-ticker status:")
                    return existing_data

                print("Checking for missing ticker data...")
                tickers_with_incomplete_data = _find_incomplete_tickers(reference_frame, clean_tickers)

                if not tickers_with_incomplete_data:
                    print("No tickers found with significant missing data (>50% NaN)")
                    _print_status_report(ticker_status, "YahooFinance per-ticker status:")
                    return existing_data

                print(
                    f"Found {len(tickers_with_incomplete_data)} tickers with >50% missing data. "
                    f"Attempting to re-download..."
                )
                _print_incomplete_tickers(tickers_with_incomplete_data)

                all_missing_tickers = [ticker_name for ticker_name, _ in tickers_with_incomplete_data]
                downloaded_parts_missing = download_parts_for_tickers(all_missing_tickers, period="max")
                _merge_missing_ticker_data(existing_data, downloaded_parts_missing, all_missing_tickers, output_columns)
                print(f"Successfully re-downloaded and merged data for {len(all_missing_tickers)} tickers")
                _print_status_report(ticker_status, "YahooFinance per-ticker status:")
                return existing_data

            yf_start = last_date

        downloaded_parts = (
            download_parts_for_tickers(clean_tickers, start=yf_start)
            if yf_start is not None
            else download_parts_for_tickers(clean_tickers, period="max")
        )
        result = combine_final_frames(existing_data, downloaded_parts)

        if save_csv:
            for col, data in result.items():
                data.to_csv(output_paths[col])
                print(f"Saved {col}.csv ({len(data)} rows x {len(data.columns)} columns)")

        _print_status_report(ticker_status, "YahooFinance per-ticker status:")

        return result


class EODHD(StockDataSource):

    submodule_name: str = "eodhd"

    @classmethod
    def download_tickers(
        cls,
        tickers: List[str],
        api_key: str = None,
        client: eodhd.APIClient = None,
        batch_size: int = 200,
        sleep_seconds: float = 2.0,
        save_csv: bool = False,
        redownload_missing_tickers: bool = False,
    ) -> dict[str, pd.DataFrame]:

        if client is None:
            if api_key is None:
                api_key = os.getenv("EODHD_API_KEY")
            if api_key is None:
                raise ValueError(
                    "EODHD API key not found. Set the EODHD_API_KEY environment variable "
                    "or pass the key explicitly via the `api_key` parameter."
                )
            client = eodhd.APIClient(api_key)
        output_columns = [target for _, target in _EODHD_COLUMN_MAP]
        output_paths = {col: cls.dst_dir / f"{col}.csv" for col in output_columns}
        ticker_status: dict[str, str] = {}

        def _deduplicate_tickers() -> list[str]:
            clean = [str(ticker).strip() for ticker in tickers if str(ticker).strip()]
            unique = sorted(dict.fromkeys(clean))
            print("Number of unique tickers extracted:", len(unique))
            return unique

        def normalize_eodhd_frame(frame: pd.DataFrame) -> pd.DataFrame:

            if frame.empty or "date" not in frame.columns:
                return pd.DataFrame()

            normalized = frame.copy()
            normalized["date"] = pd.to_datetime(normalized["date"], errors="coerce", utc=True)
            normalized = normalized.dropna(subset=["date"]).sort_values("date")
            normalized = normalized.drop_duplicates(subset=["date"], keep="last")
            if normalized.empty:
                return pd.DataFrame()

            normalized = normalized.set_index("date").rename_axis("Date")
            normalized.index = pd.to_datetime(normalized.index, utc=True).normalize()
            normalized.index.name = "Date"
            return normalized

        def download_for_ticker(clean_ticker: str, from_date: str = None) -> pd.DataFrame:
            kwargs = {
                "symbol": clean_ticker,
                "period": "d",
                "order": "a",
            }
            if from_date is not None:
                kwargs["from_date"] = from_date
            raw_data = client.get_eod_historical_stock_market_data(**kwargs)
            return pd.DataFrame(raw_data)

        def extract_downloaded_parts(
            ticker_frame: pd.DataFrame,
            clean_ticker: str,
            downloaded_parts: dict[str, list[pd.DataFrame]],
        ) -> None:

            if ticker_frame.empty:
                return

            renamed = ticker_frame.copy()
            renamed.columns = [str(col).lower() for col in renamed.columns]

            for source_col, target_col in _EODHD_COLUMN_MAP:
                if source_col in renamed.columns:
                    extracted = renamed[[source_col]].rename(columns={source_col: clean_ticker})
                    extracted = extracted.apply(pd.to_numeric, errors="coerce")
                    downloaded_parts[target_col].append(extracted)

        def download_parts_for_tickers(
            tickers_to_download: list[str],
            *,
            from_date: str = None,
        ) -> dict[str, list[pd.DataFrame]]:

            downloaded_parts_local: dict[str, list[pd.DataFrame]] = {col: [] for col in output_columns}

            for batch_index, batch_start in enumerate(range(0, len(tickers_to_download), batch_size)):
                batch = tickers_to_download[batch_start:batch_start + batch_size]
                print(f"Downloading batch {batch_index + 1} ({len(batch)} tickers)...")

                for clean_ticker in batch:
                    try:
                        frame = download_for_ticker(clean_ticker, from_date=from_date)
                    except Exception as exc:
                        print(f"Failed to download data for {clean_ticker}: {exc}")
                        ticker_status[clean_ticker] = "failed"
                        continue

                    normalized = normalize_eodhd_frame(frame)
                    if normalized.empty:
                        print(f"No valid data returned for {clean_ticker}")
                        ticker_status[clean_ticker] = "no_valid_data"
                        continue

                    extract_downloaded_parts(normalized, clean_ticker, downloaded_parts_local)
                    ticker_status[clean_ticker] = "downloaded"

                if batch_start + batch_size < len(tickers_to_download):
                    time.sleep(sleep_seconds + random.uniform(0, 3))

            return downloaded_parts_local

        clean_tickers = _deduplicate_tickers()
        if not clean_tickers:
            return {col: pd.DataFrame() for col in output_columns}

        existing_data: dict[str, pd.DataFrame] = {}
        existing_paths = {col: path for col, path in output_paths.items() if path.exists()}

        eodhd_start = None
        if existing_paths:

            for col, path in existing_paths.items():
                existing_data[col] = _load_columnar_frame(path)

            reference_col = "Close" if "Close" in existing_data else next(iter(existing_data))
            reference_frame = existing_data[reference_col]

            if not reference_frame.empty:

                last_date = reference_frame.index.max()
                today = pd.Timestamp.now(tz="UTC").normalize()

                if not _has_new_trading_days(last_date, today):

                    print(f"No new trading days since {last_date.date()}.")
                    if not redownload_missing_tickers:
                        print("Skipping missing ticker re-download (redownload_missing_tickers=False)")
                        for clean_ticker in clean_tickers:
                            if clean_ticker in reference_frame.columns:
                                ticker_status[clean_ticker] = "skipped_already_up_to_date"
                            else:
                                ticker_status[clean_ticker] = "skipped_not_in_existing_dataset"
                        _print_status_report(ticker_status, "EODHD per-ticker status:")
                        return existing_data

                    print("Checking for missing ticker data...")
                    tickers_with_incomplete_data = _find_incomplete_tickers(reference_frame, clean_tickers)

                    if not tickers_with_incomplete_data:
                        print("No tickers found with significant missing data (>50% NaN)")
                        _print_status_report(ticker_status, "EODHD per-ticker status:")
                        return existing_data

                    print(
                        f"Found {len(tickers_with_incomplete_data)} tickers with >50% missing data. "
                        f"Attempting to re-download..."
                    )
                    _print_incomplete_tickers(tickers_with_incomplete_data)

                    all_missing_tickers = [ticker_name for ticker_name, _ in tickers_with_incomplete_data]
                    downloaded_parts_missing = download_parts_for_tickers(all_missing_tickers, from_date=None)
                    _merge_missing_ticker_data(
                        existing_data,
                        downloaded_parts_missing,
                        all_missing_tickers,
                        output_columns,
                    )

                    for ticker_name in all_missing_tickers:
                        ticker_status.setdefault(ticker_name, "redownload_missing_attempted")

                    print(
                        f"Successfully re-downloaded and merged data for {len(all_missing_tickers)} tickers"
                    )
                    _print_status_report(ticker_status, "EODHD per-ticker status:")
                    return existing_data

                eodhd_start = last_date.strftime("%Y-%m-%d")

        downloaded_parts = download_parts_for_tickers(clean_tickers, from_date=eodhd_start)
        result = _combine_columnar_frames(existing_data, downloaded_parts, output_columns)

        if save_csv:
            for col, data in result.items():
                data.to_csv(output_paths[col])
                print(f"Saved {col}.csv ({len(data)} rows x {len(data.columns)} columns)")

        _print_status_report(ticker_status, "EODHD per-ticker status:")

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
