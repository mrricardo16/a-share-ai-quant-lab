"""Read-only ETF data-source probe. No trades or credentials.

Examples:
    python poc/data/etf_source_probe.py --symbol 510050 --source sina
    python poc/data/etf_source_probe.py --symbol 510300 --source em --start 20240101 --end 20261030
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
from typing import Any

import pandas as pd

SOURCES = {
    "sina": {"date": "date", "open": "open", "high": "high", "low": "low", "close": "close", "volume": "volume"},
    "em": {"date": "日期", "open": "开盘", "high": "最高", "low": "最低", "close": "收盘", "volume": "成交量", "amount": "成交额"},
}


def normalize_and_check(df: pd.DataFrame, source: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    if source not in SOURCES:
        raise ValueError(f"unknown source: {source}")
    mapping = SOURCES[source]
    missing = [name for name, raw in mapping.items() if raw not in df.columns and name != "amount"]
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    result = df.rename(columns={raw: name for name, raw in mapping.items() if raw in df.columns}).copy()
    wanted = [c for c in ("date", "open", "high", "low", "close", "volume", "amount") if c in result.columns]
    result = result[wanted]
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    for col in ("open", "high", "low", "close", "volume", "amount"):
        if col in result:
            result[col] = pd.to_numeric(result[col], errors="coerce")
    duplicates = int(result["date"].duplicated(keep=False).sum())
    null_rows = int(result.isna().any(axis=1).sum())
    positive = result[["open", "high", "low", "close"]].gt(0).all(axis=1)
    coherent = (
        (result["high"] >= result[["open", "close", "low"]].max(axis=1))
        & (result["low"] <= result[["open", "close", "high"]].min(axis=1))
    )
    valid_volume = result["volume"].ge(0)
    if "amount" in result.columns:
        valid_volume &= result["amount"].ge(0)
    invalid_price_rows = int((~(positive & coherent)).sum())
    invalid_volume_rows = int((~valid_volume).sum())
    sorted_dates = result.sort_values("date").reset_index(drop=True)
    report = {
        "source": source,
        "rows": len(df),
        "first_date": None if sorted_dates.empty or pd.isna(sorted_dates["date"].iloc[0]) else sorted_dates["date"].iloc[0].strftime("%Y-%m-%d"),
        "last_date": None if sorted_dates.empty or pd.isna(sorted_dates["date"].iloc[-1]) else sorted_dates["date"].iloc[-1].strftime("%Y-%m-%d"),
        "duplicate_date_rows": duplicates,
        "null_rows": null_rows,
        "invalid_price_rows": invalid_price_rows,
        "invalid_volume_rows": invalid_volume_rows,
        "has_amount": "amount" in result.columns,
        "volume_unit": "NOT_VERIFIED",
        "adjustment": "UNADJUSTED_OR_UNVERIFIED",
        "dividend_events_checked": False,
        "basic_bar_checks_passed": bool(len(df) > 0 and duplicates == 0 and null_rows == 0 and invalid_price_rows == 0 and invalid_volume_rows == 0),
        "warning": "Only schema/price-quality checks. Corporate actions and licensing not validated.",
    }
    return sorted_dates, report


def request_data(source: str, symbol: str, start: str, end: str) -> pd.DataFrame:
    import akshare as ak
    if source == "sina":
        return ak.fund_etf_hist_sina(symbol=f"sh{symbol}")
    if source == "em":
        return ak.fund_etf_hist_em(symbol=symbol, period="daily", start_date=start, end_date=end, adjust="")
    raise ValueError(source)


def run(source: str, symbol: str, start: str, end: str) -> dict[str, Any]:
    try:
        package_version = version("akshare")
    except PackageNotFoundError:
        package_version = None
    result: dict[str, Any] = {
        "akshare_version": package_version,
        "source": source,
        "symbol": symbol,
        "requested_start": start,
        "requested_end": end,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    try:
        frame = request_data(source, symbol, start, end)
        data, metrics = normalize_and_check(frame, source)
        d1, d2 = pd.to_datetime(start), pd.to_datetime(end)
        within = data[data["date"].between(d1, d2)]
        metrics["rows_in_requested_window"] = int(len(within))
        metrics["basic_bar_checks_passed"] = metrics["basic_bar_checks_passed"] and len(within) > 0
        result.update({"status": "ok" if metrics["basic_bar_checks_passed"] else "invalid", "metrics": metrics})
    except Exception as exc:
        result.update({"status": "error", "error_type": type(exc).__name__, "message": str(exc)[:500]})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="510050", choices=["510050", "510300", "510500"])
    parser.add_argument("--source", default="sina", choices=list(SOURCES))
    parser.add_argument("--start", default="20240101")
    parser.add_argument("--end", default="20261030")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.source, args.symbol, args.start, args.end)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
