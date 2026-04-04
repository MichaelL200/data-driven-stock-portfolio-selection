"""
Code to download or generate data
"""

import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd
import pandas_market_calendars as mcal

import papermill as pm
from yaml import warnings
import yfinance as yf

from config import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR, PROJ_ROOT, RAW_DATA_DIR


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


class YahooFinance:

    submodule_name: str = "yfinance"
    dst_dir: Path = EXTERNAL_DATA_DIR / submodule_name
    dst_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_ticker_data(
        cls,
        ticker: str,
        save_csv: bool = False,
        cleanup_old: bool = False
    ) -> pd.DataFrame:

        msg = (
            "get_ticker_data is deprecated and will be removed in a future version. "
            "Use get_ticker_data_incremential instead."
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=2)

        ts = datetime.now().strftime("%Y-%m-%d")
        file_path: Path = cls.dst_dir / f"{ticker}_{ts}.csv"

        existing_files = sorted(cls.dst_dir.glob(f"{ticker}_????-??-??.csv"))
        last_file = existing_files[-1] if existing_files else None

        # Load from today's file if exists
        if file_path.exists():
            print(f"Loading existing data for {ticker} from {file_path.name}")
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)
        # Otherwise fetch from yfinance
        else:
            data = yf.Ticker(ticker).history(period="max", auto_adjust=False)
            print(f"Fetched new data for {ticker}")

            if save_csv:
                data.to_csv(file_path)
                print(f"Saved data for {ticker} to {file_path.name}")
                last_file = file_path

        # Cleanup old files, but always keep the last one
        if cleanup_old and last_file:
            deleted = 0
            for f in existing_files:
                if f != last_file:
                    f.unlink()
                    deleted += 1
                    print(f"Deleted old file: {f.name}")
            if deleted:
                print(f"Deleted {deleted} old file(s) for {ticker}")

        return data

    @classmethod
    def get_ticker_data_incremential(
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
            exchange = "NYSE"
            calendar = mcal.get_calendar(exchange)
            schedule = calendar.schedule(start_date=last_date.date(), end_date=today.date())
            trading_days = mcal.date_range(schedule, frequency='1D')
            trading_days = pd.to_datetime(trading_days, utc=True).normalize()
            has_new_trading_days = (trading_days > last_date.normalize()).any()

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


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv"
    # ----------------------------------------------
):

    pass


if __name__ == "__main__":
    main()
