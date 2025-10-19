from ..domain.entities import Policy, PolicyStatus, PolicyType
from ..infrastructure.models import PolicyModel, PolicyStatusModel, PolicyTypeModel
from ..domain.value_objects import PolicyNumber, Money, Period

"""Maps between Domain entities and Database models"""


class PolicyDbMapper:
    """Convert ORM model to domain entity"""

    @staticmethod
    def to_domain(db_policy: PolicyModel) -> Policy:
        if not db_policy:
            return None

        # Get status and type names from relationships
        status_name = (
            db_policy.status_rel.name if db_policy.status_rel else db_policy.status
        )
        type_name = (
            db_policy.type_rel.name if db_policy.type_rel else db_policy.policy_type
        )

        policy = Policy(
            policy_number=PolicyNumber(db_policy.policy_number),
            insured_name=db_policy.insured_name,
            premium=Money(db_policy.premium_amount, db_policy.premium_currency),
            period=Period(db_policy.period_start_date, db_policy.period_end_date),
            status=PolicyStatus(status_name),
            policy_type=PolicyType(type_name),
            id=db_policy.id,
        )
        return policy

    """Convert domain entity to ORM model

        Args:
            policy: Domain policy entity
            db_status: Pre-fetched PolicyStatusModel (optional)
            db_type: Pre-fetched PolicyTypeModel (optional)
        """

    @staticmethod
    def to_orm(
        policy: Policy,
        db_status: PolicyStatusModel = None,
        db_type: PolicyTypeModel = None,
    ) -> PolicyModel:

        policy_model = PolicyModel(
            policy_number=policy.policy_number.value,
            insured_name=policy.insured_name,
            premium_amount=policy.premium.amount,
            premium_currency=policy.premium.currency,
            period_start_date=policy.period.start_date,
            period_end_date=policy.period.end_date,
        )

        # Set the ID if it exists
        if policy.id is not None:
            policy_model.id = policy.id

        # Set relationships - these will be handled by the repository
        # The repository will set status_id and type_id based on the status/type names

        return policy_model

    """Get status name from PolicyModel"""

    @staticmethod
    def get_status_name(db_policy: PolicyModel) -> str:

        if hasattr(db_policy, "status_rel") and db_policy.status_rel:
            return db_policy.status_rel.name
        else:
            return db_policy.status

    """Get type name from PolicyModel"""

    @staticmethod
    def get_type_name(db_policy: PolicyModel) -> str:

        if hasattr(db_policy, "type_rel") and db_policy.type_rel:
            return db_policy.type_rel.name
        else:
            return db_policy.policy_type
