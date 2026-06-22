"""Domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "amount", Decimal(self.amount).quantize(Decimal("0.01")))
        object.__setattr__(self, "currency", self.currency.upper())

    @classmethod
    def from_string(cls, amount: str, currency: str) -> Money:
        return cls(amount=Decimal(amount), currency=currency)

    def to_dict(self) -> dict[str, Any]:
        return {"amount": str(self.amount), "currency": self.currency}

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("Cannot add Money with different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __mul__(self, quantity: Decimal) -> Money:
        return Money(amount=self.amount * quantity, currency=self.currency)
