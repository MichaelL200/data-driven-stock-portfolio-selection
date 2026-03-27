"""
Code to download or generate data
"""

import shutil
from datetime import datetime
from pathlib import Path

import papermill as pm

from config import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR, PROJ_ROOT, RAW_DATA_DIR


class SP500:
    """
    Class to handle S&P 500 historical components
    """

    submodule_name: str = "sp500"
    src_dir: Path = PROJ_ROOT / submodule_name
    dst_dir: Path = EXTERNAL_DATA_DIR / submodule_name
    dst_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _run_notebook(cls, nb_path: Path):
        pm.execute_notebook(str(nb_path), str(nb_path), cwd=str(nb_path.parent))

    @classmethod
    def generate_current(cls):
        nb_current: Path = cls.src_dir / "sp500.ipynb"
        cls._run_notebook(nb_current)
        ts = datetime.now().strftime("%Y-%m-%d")
        dst_file: Path = cls.dst_dir / f"sp500_{ts}.csv"
        shutil.copy(cls.src_dir / "sp500.csv", dst_file)
        return dst_file

    @classmethod
    def generate_historical(cls):
        nb_historical: Path = cls.src_dir / "sp500_historical.ipynb"
        cls._run_notebook(nb_historical)
        ts_src = datetime.now().strftime("%m-%d-%Y")
        ts_dst = datetime.now().strftime("%Y-%m-%d")
        src_file: Path = cls.src_dir / f"S&P 500 Historical Components & Changes({ts_src}).csv"
        dst_file: Path = cls.dst_dir / f"sp500_historical_{ts_dst}.csv"
        shutil.copy(src_file, dst_file)
        return dst_file


def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv"
    # ----------------------------------------------
):

    pass


if __name__ == "__main__":
    main()
