"""
Code to download or generate data
"""

import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd

import papermill as pm
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
    def _generate(cls, nb_path: Path, src_file: Path, dst_file: Path) -> Path:

        if dst_file.exists():
            print(f"No generation needed: {dst_file.name} already exists.")
            return dst_file

        cls._run_notebook(nb_path)
        shutil.copy(src_file, dst_file)
        print(f"Generated new file: {dst_file.name}")

        return dst_file

    @classmethod
    def generate_current(cls) -> Path:

        ts = datetime.now().strftime("%Y-%m-%d")
        nb_current = cls.src_dir / "sp500.ipynb"
        src_file = cls.src_dir / "sp500.csv"
        dst_file = cls.dst_dir / f"sp500_{ts}.csv"

        return cls._generate(nb_current, src_file, dst_file)

    @classmethod
    def generate_historical(cls) -> Path:

        ts_dst = datetime.now().strftime("%Y-%m-%d")
        ts_src = datetime.now().strftime("%m-%d-%Y")

        nb_historical = cls.src_dir / "sp500_historical.ipynb"
        src_file = cls.src_dir / f"S&P 500 Historical Components & Changes({ts_src}).csv"
        dst_file = cls.dst_dir / f"sp500_historical_{ts_dst}.csv"

        return cls._generate(nb_historical, src_file, dst_file)

    @classmethod
    def _load_latest(cls, pattern: str) -> pd.DataFrame:

        files = list(cls.dst_dir.glob(pattern))

        if not files:
            raise FileNotFoundError(f"No files for pattern: {pattern}")

        latest_file = max(files, key=lambda f: f.name)

        return pd.read_csv(latest_file)

    @classmethod
    def load_current(cls) -> pd.DataFrame:
        return cls._load_latest("sp500_????-??-??.csv")

    @classmethod
    def load_historical(cls) -> pd.DataFrame:
        return cls._load_latest("sp500_historical_????-??-??.csv")


class YahooFinance:

    submodule_name: str = "yfinance"
    dst_dir: Path = EXTERNAL_DATA_DIR / submodule_name
    dst_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_ticker_data(cls, ticker: str, save_csv: bool = False) -> pd.DataFrame:

        ts = datetime.now().strftime("%Y-%m-%d")
        file_path: Path = cls.dst_dir / f"{ticker}_{ts}.csv"

        if file_path.exists():
            print(f"Loading existing data for {ticker} from {file_path.name}")
            return pd.read_csv(file_path, index_col=0, parse_dates=True)

        data = yf.Ticker(ticker).history(period="max", auto_adjust=False)

        if save_csv:
            data.to_csv(f"{EXTERNAL_DATA_DIR}/{{cls.submodule_name}}/{ticker}_{ts}.csv")

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
