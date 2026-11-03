"""Synthetic Backtrader timing smoke test; no real ETF prices.

Expected: close-of-D1 signal => D2 open BUY; close-of-D2 signal => D3 open SELL.
This does NOT validate A-share ETF T+1, min commission, dividends or partial fills.
"""
from datetime import date

import pandas as pd
import pytest

bt = pytest.importorskip("backtrader")


def test_backtrader_next_open_order_timing():
    dates = pd.to_datetime(["2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29"])
    bars = pd.DataFrame(
        {
            "open": [1.90, 2.00, 2.20, 2.15],
            "high": [2.00, 2.10, 2.25, 2.20],
            "low": [1.80, 1.90, 2.15, 2.10],
            "close": [1.95, 2.05, 2.18, 2.16],
            "volume": [10000, 10000, 10000, 10000],
        },
        index=dates,
    )
    observed = []

    class MinimalTiming(bt.Strategy):
        def next(self):
            # Issue orders AFTER the current bar's full price is visible.
            # Do not enable cheat-on-open or cheat-on-close.
            if len(self) == 1:
                self.buy(size=100)
            elif len(self) == 2:
                self.sell(size=100)

        def notify_order(self, order):
            if order.status == order.Completed:
                observed.append(
                    (
                        "BUY" if order.isbuy() else "SELL",
                        bt.num2date(order.executed.dt).date(),
                        order.executed.size,
                        round(order.executed.price, 4),
                    )
                )

    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=bars))
    cerebro.addstrategy(MinimalTiming)
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.0)  # Isolate time ordering from fee modeling.
    cerebro.run()
    assert observed == [
        ("BUY", date(2026, 10, 27), 100, 2.0),
        ("SELL", date(2026, 10, 28), -100, 2.2),
    ]
    assert round(cerebro.broker.getvalue(), 2) == 10020.0
