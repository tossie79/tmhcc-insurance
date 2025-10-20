from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from ..domain.value_objects import Money, PolicyNumber, Period

"""This file represents the Domain entity definitions for Policy Management"""


class PolicyStatus(str, Enum):
    """Enumeration for different statuses of a policy"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    CANCELLED = "cancelled"


class PolicyType(str, Enum):
    """Enumeration for different types of policies"""

    PROPERTY = "Property"
    CASUALTY = "Casualty"
    MARINE = "Marine"
    CONSTRUCTION = "Construction"


class Policy:
    """Policy domain entity representing an insurance policy"""

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

    def __repr__(self) -> str:
        """String representation of the Policy entity"""
        return (
            f"Policy(id={self.id}, policy_number={self.policy_number}, "
            f"insured_name={self.insured_name}, premium={self.premium}, "
            f"status={self.status.value}, policy_type={self.policy_type.value}, "
            f"period={self.period})"
        )

    def __eq__(self, other: object) -> bool:
        """Equality check based on all attributes"""
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

    def activate(self) -> None:
        """Activate the policy if it meets the criteria"""
        if self.status != PolicyStatus.PENDING:
            raise ValueError("Only pending policies can be activated")

        if not self.period.is_active:
            raise ValueError("Policy period is not active")

        if self.premium.amount <= 0:
            raise ValueError("Premium must be greater than zero to activate policy")
        self.status = PolicyStatus.ACTIVE

    def cancel(self, reason: str | None = None) -> None:
        """Cancel the policy with an optional reason"""
        if self.status in {PolicyStatus.CANCELLED, PolicyStatus.INACTIVE}:
            raise ValueError("Policy is already cancelled or inactive")
        self.status = PolicyStatus.CANCELLED
        # Optionally log the reason for cancellation
        if reason:
            print(f"Policy cancelled for reason: {reason}")
