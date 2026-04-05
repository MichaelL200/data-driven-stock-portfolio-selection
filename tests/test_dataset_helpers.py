"""Tests for the module-level helper functions in dataset.py."""

import pandas as pd

from dataset import _YF_COLUMN_MAP, _normalize_index, _has_new_trading_days, _extract_batch_columns


# ---------------------------------------------------------------------------
# _YF_COLUMN_MAP
# ---------------------------------------------------------------------------

def test_yf_column_map_contains_expected_fields():
    source_cols = [src for src, _ in _YF_COLUMN_MAP]
    assert "Close" in source_cols
    assert "Adj Close" in source_cols
    assert "Volume" in source_cols


def test_yf_column_map_adj_close_mapped_to_adj_close_underscore():
    mapping = dict(_YF_COLUMN_MAP)
    assert mapping["Adj Close"] == "Adj_Close"


# ---------------------------------------------------------------------------
# _normalize_index
# ---------------------------------------------------------------------------

def test_normalize_index_converts_to_utc_midnight():
    idx = pd.to_datetime(["2024-01-15 09:30:00", "2024-01-16 15:00:00"])
    df = pd.DataFrame({"val": [1, 2]}, index=idx)
    result = _normalize_index(df)
    assert result.index.tz is not None, "index should be timezone-aware (UTC)"
    assert all(result.index == result.index.normalize()), "index should be at midnight"


def test_normalize_index_does_not_mutate_original():
    idx = pd.to_datetime(["2024-03-01 10:00:00"])
    df = pd.DataFrame({"val": [42]}, index=idx)
    original_index = df.index.copy()
    _normalize_index(df)
    assert df.index.equals(original_index), "_normalize_index should return a copy"


def test_normalize_index_preserves_data():
    idx = pd.to_datetime(["2024-01-01", "2024-01-02"])
    df = pd.DataFrame({"a": [10, 20], "b": [30, 40]}, index=idx)
    result = _normalize_index(df)
    assert list(result["a"]) == [10, 20]
    assert list(result["b"]) == [30, 40]


# ---------------------------------------------------------------------------
# _has_new_trading_days
# ---------------------------------------------------------------------------

def test_has_new_trading_days_returns_true_when_new_days_exist():
    # last_date = a Friday at NYSE close; today = the following Monday
    last_date = pd.Timestamp("2024-01-05", tz="UTC")  # Friday
    today = pd.Timestamp("2024-01-08", tz="UTC")       # Monday
    assert _has_new_trading_days(last_date, today)


def test_has_new_trading_days_returns_false_same_day():
    last_date = pd.Timestamp("2024-01-05", tz="UTC")
    today = pd.Timestamp("2024-01-05", tz="UTC")
    assert not _has_new_trading_days(last_date, today)


def test_has_new_trading_days_returns_false_over_weekend():
    # last_date = Friday; today = Saturday (no NYSE trading)
    last_date = pd.Timestamp("2024-01-05", tz="UTC")  # Friday
    today = pd.Timestamp("2024-01-06", tz="UTC")       # Saturday
    assert not _has_new_trading_days(last_date, today)


# ---------------------------------------------------------------------------
# _extract_batch_columns
# ---------------------------------------------------------------------------

def _make_multi_index_batch(tickers, fields, n_rows=3):
    """Helper: create a mock multi-index DataFrame as yfinance would return."""
    idx = pd.date_range("2024-01-01", periods=n_rows, freq="D")
    arrays = [
        [f for f in fields for _ in tickers],
        [t for _ in fields for t in tickers],
    ]
    cols = pd.MultiIndex.from_arrays(arrays, names=["Field", "Ticker"])
    data = [[i + j for j in range(len(fields) * len(tickers))] for i in range(n_rows)]
    return pd.DataFrame(data, index=idx, columns=cols)


def test_extract_batch_columns_appends_to_parts():
    tickers = ["AAPL", "MSFT"]
    fields = ["Close", "Open", "High", "Low", "Volume", "Adj Close"]
    batch_df = _make_multi_index_batch(tickers, fields)

    downloaded_parts = {
        "Close": [], "Open": [], "High": [], "Low": [], "Volume": [], "Adj_Close": []
    }
    _extract_batch_columns(batch_df, downloaded_parts)

    for col in downloaded_parts:
        assert len(downloaded_parts[col]) == 1, f"Expected one frame appended for {col}"


def test_extract_batch_columns_result_has_correct_ticker_columns():
    tickers = ["AAPL", "TSLA"]
    fields = ["Close", "Adj Close"]
    batch_df = _make_multi_index_batch(tickers, fields)

    downloaded_parts = {"Close": [], "Adj_Close": [], "Open": [], "High": [], "Low": [], "Volume": []}
    _extract_batch_columns(batch_df, downloaded_parts)

    close_frame = downloaded_parts["Close"][0]
    assert set(close_frame.columns) == {"AAPL", "TSLA"}


def test_extract_batch_columns_index_is_utc_midnight():
    tickers = ["GOOG"]
    fields = ["Close"]
    batch_df = _make_multi_index_batch(tickers, fields)

    downloaded_parts = {"Close": [], "Open": [], "High": [], "Low": [], "Volume": [], "Adj_Close": []}
    _extract_batch_columns(batch_df, downloaded_parts)

    result_index = downloaded_parts["Close"][0].index
    assert result_index.tz is not None
    assert all(result_index == result_index.normalize())


def test_extract_batch_columns_skips_missing_fields():
    tickers = ["AAPL"]
    # Only provide "Close", not "Volume" or "Adj Close"
    fields = ["Close"]
    batch_df = _make_multi_index_batch(tickers, fields)

    downloaded_parts = {"Close": [], "Open": [], "High": [], "Low": [], "Volume": [], "Adj_Close": []}
    _extract_batch_columns(batch_df, downloaded_parts)

    assert len(downloaded_parts["Close"]) == 1
    assert len(downloaded_parts["Volume"]) == 0
    assert len(downloaded_parts["Adj_Close"]) == 0
