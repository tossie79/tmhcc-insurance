from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from decimal import Decimal


"""Pydantic schemas for Policy Management API"""


class MoneyDTO(BaseModel):
    amount: Decimal
    currency: str


class PeriodDTO(BaseModel):
    start_date: date
    end_date: date


class PolicyDTO(BaseModel):
    policy_number: str
    insured_name: str
    premium: MoneyDTO
    period: PeriodDTO
    status: str
    policy_type: str
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class CreatePolicyDTO(BaseModel):
    policy_number: str
    insured_name: str
    premium_amount: Decimal
    premium_currency: str = "GBP"
    period_start_date: date
    period_end_date: date
    status: Optional[str] = "pending"
    policy_type: Optional[str] = "Property"

    model_config = ConfigDict(from_attributes=True)


class FlatPolicyDTO(BaseModel):
    policy_number: str
    insured_name: str
    premium: str
    start_date: str
    end_date: str
    status: str
    policy_type: str
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
