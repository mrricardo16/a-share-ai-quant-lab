import pandas as pd
import pytest

from etf_source_probe import normalize_and_check


def test_sina_has_no_amount_column():
    frame = pd.DataFrame({
        "date": ["2026-10-29", "2026-10-30"],
        "open": [2.1, 2.2], "high": [2.2, 2.3],
        "low": [2.0, 2.1], "close": [2.15, 2.25], "volume": [1000, 2000],
    })
    normalized, result = normalize_and_check(frame, "sina")
    assert result["basic_bar_checks_passed"]
    assert not result["has_amount"]
    assert list(normalized.columns) == ["date", "open", "high", "low", "close", "volume"]


def test_em_includes_amount():
    frame = pd.DataFrame({
        "日期": ["2026-10-30"], "开盘": [2.0], "最高": [2.1],
        "最低": [1.9], "收盘": [2.05], "成交量": [1000], "成交额": [10000],
    })
    _, result = normalize_and_check(frame, "em")
    assert result["has_amount"]
    assert result["basic_bar_checks_passed"]


def test_reject_duplicate_and_bad_price():
    frame = pd.DataFrame({
        "date": ["2026-10-30", "2026-10-30"],
        "open": [2.0, 2.0], "high": [1.9, 2.1],
        "low": [1.8, 1.9], "close": [2.05, 2.05], "volume": [100, 100],
    })
    _, result = normalize_and_check(frame, "sina")
    assert result["duplicate_date_rows"] == 2
    assert result["invalid_price_rows"] == 1
    assert not result["basic_bar_checks_passed"]


def test_required_columns():
    with pytest.raises(ValueError, match="missing required"):
        normalize_and_check(pd.DataFrame({"date": ["2026-10-30"]}), "sina")
