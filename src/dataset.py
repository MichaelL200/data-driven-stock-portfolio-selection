"""
Code to download or generate data
"""

import os
import shutil
import time
import random
from datetime import datetime
from pathlib import Path
import pandas as pd

import papermill as pm
import yfinance as yf
import eodhd
from dotenv import load_dotenv

from config import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR, PROJ_ROOT, RAW_DATA_DIR


_YF_COLUMN_MAP = [
    ("Close", "Close"),
    ("Open", "Open"),
    ("High", "High"),
    ("Low", "Low"),
    ("Volume", "Volume"),
    ("Adj Close", "Adj_Close"),
    ("Dividends", "Dividends"),
    ("Stock Splits", "Stock_Splits"),
]

_YF_OUTPUT_COLUMNS = [target for _, target in _YF_COLUMN_MAP]

_EODHD_COLUMN_MAP = [
    ("close", "Close"),
    ("open", "Open"),
    ("high", "High"),
    ("low", "Low"),
    ("volume", "Volume"),
    ("adjusted_close", "Adj_Close"),
]

_EODHD_OUTPUT_COLUMNS = [target for _, target in _EODHD_COLUMN_MAP]


def _normalize_columnar_index(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result.index = pd.to_datetime(result.index, utc=True).normalize()
    result.index.name = "Date"
    return result


def _load_columnar_frame(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    return _normalize_columnar_index(data)


class SP500:

    submodule_name: str = "sp500"
    src_dir: Path = PROJ_ROOT / submodule_name
    dst_dir: Path = EXTERNAL_DATA_DIR / submodule_name
    dst_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def extract_tickers(sp500_components: pd.DataFrame) -> list[str]:
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
    def load_current(cls) -> pd.DataFrame:
        return cls._load("sp500_????-??-??.csv")

    @classmethod
    def load_historical(cls) -> pd.DataFrame:
        return cls._load("sp500_historical_????-??-??.csv")


class StockDataSource:

    submodule_name: str
    output_columns: list[str] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = getattr(cls, "submodule_name", None)
        if name is not None:
            cls.dst_dir = EXTERNAL_DATA_DIR / name
            cls.dst_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _load_existing_columnar(cls) -> dict[str, pd.DataFrame]:
        existing: dict[str, pd.DataFrame] = {}
        for col in cls.output_columns:
            path = cls.dst_dir / f"{col}.csv"
            if path.exists():
                existing[col] = _load_columnar_frame(path)
        return existing

    @classmethod
    def _save_columnar(cls, frames: dict[str, pd.DataFrame]) -> None:
        for col, data in frames.items():
            if data.empty or data.dropna(how="all").empty:
                continue
            path = cls.dst_dir / f"{col}.csv"
            data.to_csv(path)
            print(f"Saved {col}.csv ({len(data)} rows x {len(data.columns)} columns)")

    @classmethod
    def _merge_columnar(
        cls,
        existing: dict[str, pd.DataFrame],
        downloaded_parts: dict[str, list[pd.DataFrame]],
    ) -> dict[str, pd.DataFrame]:

        result: dict[str, pd.DataFrame] = {}

        for col in cls.output_columns:
            new_data = (
                pd.concat(downloaded_parts[col], axis=1)
                .loc[:, lambda df: ~df.columns.duplicated(keep="last")]
                if downloaded_parts[col]
                else pd.DataFrame()
            )
            if not new_data.empty and not new_data.dropna(how="all").empty:
                new_data = _normalize_columnar_index(new_data)
            else:
                new_data = pd.DataFrame()

            old_data = existing.get(col, pd.DataFrame())

            if old_data.empty and new_data.empty:
                result[col] = pd.DataFrame()
                continue

            if old_data.empty:
                result[col] = new_data
                continue

            if new_data.empty:
                result[col] = old_data
                continue

            # Keep old values where newly downloaded frame has NaN (e.g. other tickers),
            # but overwrite with fresh non-NaN values where present.
            merged = new_data.combine_first(old_data)
            merged = merged.sort_index().pipe(_normalize_columnar_index)
            result[col] = merged

        return result

    @classmethod
    def _load_ticker_from_columnar(cls, ticker: str) -> pd.DataFrame:

        clean_ticker = str(ticker).strip()
        frames = cls._load_existing_columnar()
        if not frames:
            raise FileNotFoundError(f"No {cls.submodule_name} data found in {cls.dst_dir}")

        series: dict[str, pd.Series] = {}
        for field, frame in frames.items():
            if clean_ticker in frame.columns:
                series[field] = frame[clean_ticker]

        if not series:
            raise KeyError(f"Ticker '{clean_ticker}' not found in {cls.submodule_name} data.")

        result = pd.DataFrame(series)
        result.index.name = "Date"
        return result


class YahooFinance(StockDataSource):

    submodule_name: str = "yfinance"
    output_columns: list[str] = _YF_OUTPUT_COLUMNS

    @staticmethod
    def _extract_batch_columns(
        normalized_batch: pd.DataFrame,
        downloaded_parts: dict[str, list[pd.DataFrame]],
    ) -> None:
        for source_col, target_col in _YF_COLUMN_MAP:
            if source_col in normalized_batch.columns.get_level_values(0):
                extracted = normalized_batch.xs(source_col, level=0, axis=1)
                extracted.columns = extracted.columns.astype(str)
                extracted = _normalize_columnar_index(extracted)
                downloaded_parts[target_col].append(extracted)

    @classmethod
    def _fetch_batches(
        cls,
        tickers: list[str],
        *,
        batch_size: int,
        sleep_seconds: float,
        period: str = "max",
    ) -> dict[str, list[pd.DataFrame]]:

        downloaded_parts: dict[str, list[pd.DataFrame]] = {col: [] for col in cls.output_columns}

        for batch_index, batch_start in enumerate(range(0, len(tickers), batch_size)):

            batch = tickers[batch_start: batch_start + batch_size]
            download_kwargs: dict = {
                "period": period,
                "auto_adjust": False,
                "actions": True,
                "timeout": 30,
                "progress": False,
            }

            print(f"Downloading batch {batch_index + 1} ({len(batch)} tickers)...")
            batch_df = yf.download(batch, **download_kwargs)

            if batch_df.empty:
                print(f"Warning: empty download for batch {batch_index + 1}")
            else:
                normalized_batch = batch_df.copy()
                if not isinstance(normalized_batch.columns, pd.MultiIndex):
                    ticker = str(batch[0])
                    normalized_batch.columns = pd.MultiIndex.from_tuples(
                        [(col, ticker) for col in normalized_batch.columns],
                        names=["Field", "Ticker"],
                    )
                else:
                    normalized_batch.columns = normalized_batch.columns.set_names(["Field", "Ticker"])

                normalized_batch = _normalize_columnar_index(normalized_batch)
                cls._extract_batch_columns(normalized_batch, downloaded_parts)

            if batch_start + batch_size < len(tickers):
                time.sleep(sleep_seconds + random.uniform(0, 3))

        return downloaded_parts

    @classmethod
    def download(
        cls,
        tickers: list[str],
        batch_size: int = 200,
        sleep_seconds: float = 2.0,
    ) -> None:

        tickers = [str(t).strip() for t in tickers if str(t).strip()]
        tickers = sorted(dict.fromkeys(tickers))
        if not tickers:
            return

        existing = cls._load_existing_columnar()
        print(f"Downloading full history for {len(tickers)} tickers.")
        downloaded_parts = cls._fetch_batches(
            tickers,
            batch_size=batch_size,
            sleep_seconds=sleep_seconds,
            period="max",
        )

        result = cls._merge_columnar(existing, downloaded_parts)
        cls._save_columnar(result)

    @classmethod
    def download_ticker(cls, ticker: str) -> None:
        cls.download([ticker])

    @classmethod
    def load(cls) -> dict[str, pd.DataFrame]:
        data = cls._load_existing_columnar()
        if not data:
            print(f"No {cls.submodule_name} CSVs found in {cls.dst_dir}")
        return data

    @classmethod
    def load_ticker(cls, ticker: str) -> pd.DataFrame:
        return cls._load_ticker_from_columnar(ticker)


class EODHD(StockDataSource):

    submodule_name: str = "eodhd"
    output_columns: list[str] = _EODHD_OUTPUT_COLUMNS

    @classmethod
    def _resolve_client(
        cls,
        api_key: str = None,
        client: eodhd.APIClient = None,
    ) -> eodhd.APIClient:

        if client is not None:
            return client

        if api_key is None:
            api_key = os.getenv("EODHD_API_KEY")
        if api_key is None:
            load_dotenv(PROJ_ROOT / ".env", override=False)
            api_key = os.getenv("EODHD_API_KEY")
        if api_key is None:
            raise ValueError(
                "EODHD API key not found. Set the EODHD_API_KEY environment variable "
                "or pass the key explicitly via the `api_key` parameter."
            )

        return eodhd.APIClient(api_key)

    @staticmethod
    def _resolve_api_symbol(ticker: str) -> str:

        map: dict[str, str] = {
            "ABI": "BUD_old",
            "ADCT": "ADCT_old",
            "ADT": "ADT_old",
            "AGC": "AGR_old",
            "ALTR": "ALTR_old",
            "AM": "AM_old",
            # "ANDW": "ANDW",
            "ARC": "ATV1",
            "ARNC": "ARNC_old",
            "ASO": "ASO_old",
            "AT": "AT_old1",
            "AV": "AV_old",
            "BBBY": "BBBY_old",
            "BEAM": "BEAM_old",
            "BF.B": "BF-A",
            # "BHGE": "BHGE",
            "BRK-B": "BRK-A",
            "BSC": "BSC_old",
            "BUD": "BUD_old",
            "CA": "CA_old",
            "CAM": "CAM_old",
            "CCE": "CCE_old",
            "CE": "CZ",
            "CEG": "CEG_old",
            "CEN": "CEN1",
            # "CF": ???,
            "CHK": "CHK_old",
            "CHIR": "CHIR1",
            "CNC": "CCNCW",
            "CNXT": "CNXT1",
            "COC.B": "COC-B",
            "CPWR": "CPWR_old",
            "CR": "CR_old",
            "DELL": "DELL_old",
            "DG": "DG1",
            "DNB": "DNB_old",
            "DO": "DO_old",
            "DOW": "DOW_old",
            "DTV": "DTV_old",
            "DYN": "DYN_old",
            "EC": "EC1",
            "EMC": "EMC_old",
            "FB": "FB_old",
            "FDC": "FDC_old",
            "FTL.A": "FTL-A",
            "FOX": "TFCF",
            # "FRO": ???,
            "FRX": "FRX_old",
            "G": "G_old",
            "GDT": "GDT_old",
            # "GLD": ???,
            "GLK": "GLK_old",
            "GNT": "DNA_old",
            # "GP": ???,
            "H": "HSY",
            "HCA": "HCA1",
            "HCP": "HCP_old",
            "HCR": "HCR_old",
            "HI": "HI1",
            "HLT": "HLT1",
            "HM": "HM_old",
            "HMA": "HMA_old",
            "HNZ": "HNZ",
            # "I": ???,
            "INFO": "INFO_old1",
            "IR": "TT",
            "KG": "KG_old",
            "KMI": "KMI1",
            "LB": "LB_old",
            "LIFE": "LIFE_old",
            "LLL": "LLL_old",
            "LU": "ALU",
            # "MDR": "MDR",
            "MEA": "MEA1",
            "MEDI": "MEDI_old",
            "MI": "MI1",
            "MIL": "MIL_old1",
            "MIR": "MIR_old",
            "MNK": "MNK_old",
            "MON": "MON_old",
            "NCC": "NCC_old",
            "NSM": "NSM_old",
            "NYX": "NYX_old",
            "ONE": "ONE1",
            "PCL": "PCL_old",
            "PCS": "PCS_old",
            "PD": "PD1",
            # "PEAK": "PEAK",
            "PGN": "PGN_old",
            "PLL": "PLL_old",
            "POM": "POM_old",
            "PSFT": "PSFT_old",
            "PX": "PX_old",
            "Q": "Q_old",
            "RAL": "RAL_old",
            "RDS.A": "RDS-B",
            "S": "S_old",
            "SAF": "SAF_old1",
            "SGP": "SGP_old",
            "SHLD": "SHLD_old",
            "SII": "SII_old",
            "SNDK": "SNDK_old",
            "SPLS": "SPLS_old",
            "STI": "STI_old",
            "SUN": "SUN1",
            "SUNEQ": "STPFQ",
            # "SYMC": "SYMC",
            "TE": "TE_old1",
            "TEK": "TEK_old",
            "TMC": "TMC-A",
            # "TMK": "TMK",
            "TOS": "TOS_old1",
            # "TRW": "TRW",
            "TSG": "TSG1",
            "TX": "TX1",
            "UCL": "UCL_old",
            "UST": "UST1",
            "WB": "WB_old1",
            "WLL": "MRCH",
            # "WLP": "WLP",
            "WYND": "TNL",
            "XL": "XL_old",
        }

        if ticker in map:
            ticker = map[ticker]

        return f"{ticker}.US" if not ticker.endswith(".US") else ticker

    @staticmethod
    def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:

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

    @classmethod
    def _fetch_tickers(
        cls,
        tickers: list[str],
        *,
        client: eodhd.APIClient,
    ) -> dict[str, list[pd.DataFrame]]:

        downloaded_parts: dict[str, list[pd.DataFrame]] = {col: [] for col in cls.output_columns}

        if not tickers:
            return downloaded_parts

        print(f"Downloading {len(tickers)} tickers...")

        for ticker in tickers:

            api_symbol: str = cls._resolve_api_symbol(ticker)
            kwargs: dict = {"symbol": api_symbol, "period": "d", "order": "a"}

            try:
                raw_data = client.get_eod_historical_stock_market_data(**kwargs)
                frame = pd.DataFrame(raw_data)
            except Exception as exc:
                print(f"Failed to download data for {api_symbol}: {exc}")
                continue

            normalized = cls._normalize_frame(frame)
            if normalized.empty:
                print(f"No valid data returned for {api_symbol}")
                continue

            renamed = normalized.copy()
            renamed.columns = [str(col).lower() for col in renamed.columns]

            for source_col, target_col in _EODHD_COLUMN_MAP:
                if source_col in renamed.columns:
                    extracted = renamed[[source_col]].rename(columns={source_col: ticker})
                    extracted = extracted.apply(pd.to_numeric, errors="coerce")
                    downloaded_parts[target_col].append(extracted)

        return downloaded_parts

    @classmethod
    def download(
        cls,
        tickers: list[str],
        api_key: str = None,
    ) -> None:

        client: eodhd.APIClient = cls._resolve_client(api_key=api_key)

        tickers = [str(t).strip().removesuffix(".US") for t in tickers if str(t).strip()]
        tickers = sorted(dict.fromkeys(tickers))
        print("Number of unique tickers extracted:", len(tickers))
        if not tickers:
            return

        existing = cls._load_existing_columnar()
        print(f"Downloading full history for {len(tickers)} tickers.")
        downloaded_parts = cls._fetch_tickers(tickers, client=client)

        result = cls._merge_columnar(existing, downloaded_parts)
        cls._save_columnar(result)

    @classmethod
    def download_ticker(cls, ticker: str, api_key: str = None) -> None:
        cls.download([ticker], api_key=api_key)

    @classmethod
    def load(cls) -> dict[str, pd.DataFrame]:
        data = cls._load_existing_columnar()
        if not data:
            print(f"No {cls.submodule_name} CSVs found in {cls.dst_dir}")
        return data

    @classmethod
    def load_ticker(cls, ticker: str) -> pd.DataFrame:
        clean_ticker = str(ticker).strip().removesuffix(".US")
        return cls._load_ticker_from_columnar(clean_ticker)

    @classmethod
    def get_delisted_tickers(cls, api_key: str = None) -> pd.DataFrame:

        client: eodhd.APIClient = cls._resolve_client(api_key=api_key)

        try:

            raw_data = client.get_list_of_tickers(code="US", delisted=1)
            frame = pd.DataFrame(raw_data)

            path = cls.dst_dir / "delisted_tickers.csv"
            frame.to_csv(path)

            return frame
        except Exception as exc:
            print(f"Failed to download delisted tickers data: {exc}")
            return pd.DataFrame()


def main(
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
):
    pass


if __name__ == "__main__":
    main()
