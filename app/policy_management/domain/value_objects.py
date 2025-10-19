from __future__ import annotations
from dataclasses import dataclass
from datetime import date

"""This file contains value object definitions for Policy Management Domain"""


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "GBP"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if not self.currency.isalpha() or len(self.currency) != 3:
            raise ValueError("Currency must be a 3-letter ISO code")


@dataclass(frozen=True)
class PolicyNumber:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) < 5:
            raise ValueError("Policy number must be at least 5 characters long")
        if not self.value.isalnum():
            raise ValueError("Policy number must be alphanumeric")


@dataclass(frozen=True)
class Period:
    start_date: date
    end_date: date

    def __post_init__(self):
        if not isinstance(self.start_date, date) or not isinstance(self.end_date, date):
            raise TypeError("start_date and end_date must be datetime instances")

        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")

    @property
    def is_active(self) -> bool:
        today = date.today()
        result = self.start_date <= today <= self.end_date
        return result
