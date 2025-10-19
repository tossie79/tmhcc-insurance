from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from ..domain.value_objects import Money, PolicyNumber, Period

"""This file represents the Domain entity definitions for Policy Management"""

"""Enumeration for different statuses of a policy"""


class PolicyStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    CANCELLED = "cancelled"


"""Enumeration for different types of policies"""


class PolicyType(str, Enum):
    PROPERTY = "Property"
    CASUALTY = "Casualty"
    MARINE = "Marine"
    CONSTRUCTION = "Construction"


"""Policy domain entity representing an insurance policy"""


class Policy:
    def __init__(
        self,
        policy_number: PolicyNumber,
        insured_name: str,
        premium: Money,
        period: Period,
        status: PolicyStatus = PolicyStatus.PENDING,
        policy_type: PolicyType = PolicyType.PROPERTY,
        id: int | None = None,
    ):
        self.id = id
        self.policy_number = policy_number
        self.insured_name = insured_name
        self.premium = premium
        self.status = status
        self.policy_type = policy_type
        self.period = period

    """String representation of the Policy entity"""

    def __repr__(self) -> str:
        return (
            f"Policy(id={self.id}, policy_number={self.policy_number}, "
            f"insured_name={self.insured_name}, premium={self.premium}, "
            f"status={self.status.value}, policy_type={self.policy_type.value}, "
            f"period={self.period})"
        )

    """Equality check based on all attributes"""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Policy):
            return False
        return (
            self.id == other.id
            and self.policy_number == other.policy_number
            and self.insured_name == other.insured_name
            and self.premium == other.premium
            and self.period == other.period
            and self.status == other.status
            and self.policy_type == other.policy_type
        )

    """Activate the policy if it meets the criteria"""

    def activate(self) -> None:
        if self.status != PolicyStatus.PENDING:
            raise ValueError("Only pending policies can be activated")

        if not self.period.is_active:
            raise ValueError("Policy period is not active")

        if self.premium.amount <= 0:
            raise ValueError("Premium must be greater than zero to activate policy")
        self.status = PolicyStatus.ACTIVE

    """Cancel the policy with an optional reason"""

    def cancel(self, reason: str | None = None) -> None:
        if self.status in {PolicyStatus.CANCELLED, PolicyStatus.INACTIVE}:
            raise ValueError("Policy is already cancelled or inactive")
        self.status = PolicyStatus.CANCELLED
        # Optionally log the reason for cancellation
        if reason:
            print(f"Policy cancelled for reason: {reason}")
