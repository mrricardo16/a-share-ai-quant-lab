from datetime import date
from decimal import Decimal

import pytest

from reference_ledger import Ledger, Order, Rules, next_session_trade

D1 = date(2026, 10, 26)
D2 = date(2026, 10, 27)
D3 = date(2026, 10, 28)


def test_next_session_not_same_session():
    with pytest.raises(ValueError, match="same-session"):
        next_session_trade(Ledger(), D1, D1, "BUY", 100, Decimal("2"))


def test_buy_sell_and_cash_reconciles_with_slippage_and_min_commission():
    ledger = Ledger()
    buy = next_session_trade(ledger, D1, D2, "BUY", 100, Decimal("2"))
    assert buy.price == Decimal("2.002000")
    assert buy.gross == Decimal("200.20")
    assert buy.commission == Decimal("5.00")
    assert ledger.cash == Decimal("9794.80")
    assert ledger.quantity == 100
    assert ledger.mark_to_market(Decimal("2.10")) == Decimal("10004.80")
    sell = next_session_trade(ledger, D2, D3, "SELL", 100, Decimal("2.20"))
    assert sell.price == Decimal("2.197800")
    assert sell.gross == Decimal("219.78")
    assert ledger.cash == Decimal("10009.58")
    assert ledger.quantity == 0


def test_t1_selling_same_day_is_rejected_without_cash_change():
    ledger = Ledger()
    ledger.execute(Order(D2, "BUY", 100), Decimal("2"))
    before = ledger.cash
    with pytest.raises(ValueError, match=r"T\+1"):
        ledger.execute(Order(D2, "SELL", 100), Decimal("2.1"))
    assert ledger.cash == before
    assert ledger.quantity == 100


def test_lot_size_insufficient_cash_and_bad_price():
    ledger = Ledger()
    for quantity, price, error in [(50, "2", "trading lot"), (100, "200", "insufficient cash"), (100, "0", "opening price")]:
        with pytest.raises(ValueError, match=error):
            ledger.execute(Order(D2, "BUY", quantity), Decimal(price))
    assert ledger.cash == Decimal("10000") and ledger.quantity == 0


def test_untradable_is_not_filled():
    ledger = Ledger()
    with pytest.raises(ValueError, match="not tradable"):
        next_session_trade(ledger, D1, D2, "BUY", 100, Decimal("2"), tradable=False)
    assert len(ledger.fills) == 0


def test_fifo_after_two_purchases_respects_t1():
    ledger = Ledger()
    ledger.execute(Order(D1, "BUY", 100), Decimal("2"))
    ledger.execute(Order(D2, "BUY", 100), Decimal("2"))
    ledger.execute(Order(D2, "SELL", 100), Decimal("2.1"))
    assert ledger.quantity == 100
    assert ledger.sellable(D2) == 0
    assert ledger.sellable(D3) == 100


def test_higher_commission_rate_is_used():
    ledger = Ledger(rules=Rules(commission_rate=Decimal("0.01")))
    fill = ledger.execute(Order(D1, "BUY", 100), Decimal("20"))
    assert fill.commission == Decimal("20.02")
    assert ledger.cash == Decimal("7977.98")


def test_same_inputs_same_deterministic_ledger():
    def scenario():
        l = Ledger()
        next_session_trade(l, D1, D2, "BUY", 100, Decimal("2"))
        next_session_trade(l, D2, D3, "SELL", 100, Decimal("2.2"))
        return l.cash, l.quantity, l.fills
    assert scenario() == scenario()
