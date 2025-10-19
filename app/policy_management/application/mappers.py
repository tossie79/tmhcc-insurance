from ..domain.entities import Policy, PolicyStatus, PolicyType
from ..domain.value_objects import PolicyNumber, Money, Period
from ..api.schemas import CreatePolicyDTO, PolicyDTO, MoneyDTO, PeriodDTO, FlatPolicyDTO
from datetime import date
from decimal import Decimal

"""This class maps between Domain entities and API DTOs"""


class PolicyDtoMapper:
    """Create Policy entity from CreatePolicyDTO"""

    @staticmethod
    def create_entity_from_dto(create_policy_dto: CreatePolicyDTO) -> Policy:
        return Policy(
            policy_number=PolicyNumber(create_policy_dto.policy_number),
            insured_name=create_policy_dto.insured_name,
            premium=Money(
                create_policy_dto.premium_amount, create_policy_dto.premium_currency
            ),
            period=Period(
                create_policy_dto.period_start_date, create_policy_dto.period_end_date
            ),
            status=PolicyStatus(create_policy_dto.status.lower()),
            policy_type=PolicyType(create_policy_dto.policy_type.capitalize()),
        )

    """Convert Policy domain entity to PolicyDTO"""

    @staticmethod
    def to_dto(policy: Policy) -> PolicyDTO:
        return PolicyDTO(
            id=policy.id,
            policy_number=policy.policy_number.value,
            insured_name=policy.insured_name,
            premium=MoneyDTO(
                amount=policy.premium.amount, currency=policy.premium.currency
            ),
            status=policy.status.value,
            policy_type=policy.policy_type.value,
            period=PeriodDTO(
                start_date=policy.period.start_date, end_date=policy.period.end_date
            ),
        )

    """Convert PolicyDTO to Policy domain entity"""

    @staticmethod
    def to_domain(policy_dto: PolicyDTO) -> Policy:
        return Policy(
            policy_number=PolicyNumber(policy_dto.policy_number),
            insured_name=policy_dto.insured_name,
            premium=Money(policy_dto.premium.amount, policy_dto.premium.currency),
            period=Period(policy_dto.period.start_date, policy_dto.period.end_date),
            status=PolicyStatus(policy_dto.status),
            policy_type=PolicyType(policy_dto.policy_type),
            id=policy_dto.id,
        )

    """Convert Policy domain entity to flat dictionary for JSON response"""

    @staticmethod
    def to_dict(policy: Policy) -> dict:
        # Currency formatting
        currency_map = {"USD": "$", "GBP": "£", "EUR": "€", "JPY": "¥"}

        symbol = currency_map.get(policy.premium.currency, policy.premium.currency)
        premium_amount = policy.premium.amount

        if isinstance(premium_amount, float) or (
            isinstance(premium_amount, Decimal)
            and premium_amount == int(premium_amount)
        ):
            formatted_amount = f"{int(premium_amount):,}"
        else:
            formatted_amount = f"{premium_amount:,.2f}"

        formatted_premium = f"{symbol}{formatted_amount}"

        # Date formatting
        def format_date(d: date) -> str:
            return d.strftime("%d/%m/%Y")

        policy_dict = {
            "id": policy.id,
            "policy_number": policy.policy_number.value,
            "insured_name": policy.insured_name,
            "premium": formatted_premium,
            "status": policy.status.value.capitalize(),
            "policy_type": policy.policy_type.value,
            "start_date": format_date(policy.period.start_date),
            "end_date": format_date(policy.period.end_date),
        }
        return policy_dict
