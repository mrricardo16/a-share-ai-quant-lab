"""Deterministic reference ledger for synthetic stock-ETF order tests.

NOT a production broker, backtester, or claim of ETF rule completeness.
No corporate action, trading halt queue, or partial-fill modeling.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

Action = Literal["BUY", "SELL"]


@dataclass(frozen=True)
class Rules:
    lot_size: int = 100
    commission_rate: Decimal = Decimal("0.0003")
    minimum_commission: Decimal = Decimal("5")
    slippage_rate: Decimal = Decimal("0.001")
    t_plus_one: bool = True


@dataclass(frozen=True)
class Order:
    session: date
    action: Action
    quantity: int


@dataclass(frozen=True)
class Fill:
    session: date
    action: Action
    quantity: int
    price: Decimal
    gross: Decimal
    commission: Decimal


@dataclass
class Ledger:
    cash: Decimal = Decimal("10000")
    rules: Rules = field(default_factory=Rules)
    lots: list[tuple[date, int]] = field(default_factory=list)
    fills: list[Fill] = field(default_factory=list)

    @property
    def quantity(self) -> int:
        return sum(quantity for _, quantity in self.lots)

    def sellable(self, session: date) -> int:
        return sum(q for purchase_day, q in self.lots
                   if not self.rules.t_plus_one or purchase_day < session)

    def mark_to_market(self, close: Decimal) -> Decimal:
        return self.cash + Decimal(self.quantity) * close

    def execute(self, order: Order, open_price: Decimal, *, tradable: bool = True) -> Fill:
        """Execute at next session open; rejects rather than fabricates a fill."""
        r = self.rules
        if not tradable:
            raise ValueError("not tradable")
        if open_price <= 0:
            raise ValueError("invalid opening price")
        if order.action not in ("BUY", "SELL"):
            raise ValueError("unsupported action")
        if order.quantity <= 0 or order.quantity % r.lot_size:
            raise ValueError("not an integer trading lot")
        if order.action == "BUY":
            execution_price = open_price * (Decimal(1) + r.slippage_rate)
        else:
            execution_price = open_price * (Decimal(1) - r.slippage_rate)
        # Currency precision is part of this synthetic reference model, not the exchange matching rule.
        execution_price = execution_price.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
        gross = (execution_price * order.quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        commission = max(r.minimum_commission, gross * r.commission_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if order.action == "BUY":
            if gross + commission > self.cash:
                raise ValueError("insufficient cash")
            self.cash -= gross + commission
            self.lots.append((order.session, order.quantity))
        else:
            if order.quantity > self.sellable(order.session):
                raise ValueError("insufficient T+1 sellable quantity")
            self.cash += gross - commission
            to_remove = order.quantity
            remaining = []
            for purchase_day, quantity in self.lots:
                available = quantity if (not r.t_plus_one or purchase_day < order.session) else 0
                removed = min(to_remove, available)
                quantity -= removed
                to_remove -= removed
                if quantity:
                    remaining.append((purchase_day, quantity))
            if to_remove:
                raise AssertionError("sellable inventory out of sync")
            self.lots = remaining
        fill = Fill(order.session, order.action, order.quantity, execution_price, gross, commission)
        self.fills.append(fill)
        return fill


def next_session_trade(
    ledger: Ledger,
    signal_session: date,
    next_session: date,
    action: Action,
    quantity: int,
    next_open_price: Decimal,
    *,
    tradable: bool = True,
) -> Fill:
    """Never permit a completed-session signal to fill in the same session."""
    if next_session <= signal_session:
        raise ValueError("look-ahead or same-session fill forbidden")
    return ledger.execute(Order(next_session, action, quantity), next_open_price, tradable=tradable)
