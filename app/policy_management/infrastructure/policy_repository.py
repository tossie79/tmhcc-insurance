from sqlalchemy.orm import Session, joinedload
from ..domain.entities import Policy, PolicyStatus, PolicyType
from ..domain.value_objects import PolicyNumber, Money, Period
from .models import PolicyModel, PolicyStatusModel, PolicyTypeModel
from .mappers import PolicyDbMapper

"""SQL-based implementation of the Policy Repository"""


class SQLPolicyRepository:
    def __init__(self, db: Session):
        self.db = db

    ""

    def add_policy(self, policy: Policy) -> Policy:
        """Add a new policy to the database"""
        # Convert domain entity to ORM model using mapper
        try:
            db_policy = PolicyDbMapper.to_orm(policy)

            # Set the foreign key relationships
            db_policy.status_id = self._get_status_id(policy.status.value)
            db_policy.type_id = self._get_type_id(policy.policy_type.value)

            self.db.add(db_policy)
            self.db.commit()
            self.db.refresh(db_policy)

            # Return the full policy with relationships loaded
            full_db_policy = self._get_policy_with_relationships(db_policy.id)
            return PolicyDbMapper.to_domain(full_db_policy)
        except Exception as e:
            self.db.rollback()
            raise e

    def update_policy(self, policy: Policy) -> Policy:
        """Update an existing policy"""
        try:
            db_policy = (
                self.db.query(PolicyModel).filter(PolicyModel.id == policy.id).first()
            )
            if not db_policy:
                raise ValueError("Policy not found")

            # Update basic fields
            db_policy.insured_name = policy.insured_name
            db_policy.premium_amount = policy.premium.amount
            db_policy.premium_currency = policy.premium.currency
            db_policy.period_start_date = policy.period.start_date
            db_policy.period_end_date = policy.period.end_date

            # Update status and type using their IDs
            db_policy.status_id = self._get_status_id(policy.status.value)
            db_policy.type_id = self._get_type_id(policy.policy_type.value)

            self.db.commit()
            self.db.refresh(db_policy)

            # Return the full policy with relationships
            full_db_policy = self._get_policy_with_relationships(db_policy.id)
            return PolicyDbMapper.to_domain(full_db_policy)
        except Exception as e:
            self.db.rollback()
            raise e

    def cancel_policy(self, policy: Policy) -> None:
        """Cancel (delete) a policy by updating its status to cancelled"""
        try:
            db_policy = (
                self.db.query(PolicyModel).filter(PolicyModel.id == policy.id).first()
            )
            if db_policy:
                # Instead of deleting, update status to cancelled
                db_policy.status_id = self._get_status_id(PolicyStatus.CANCELLED.value)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_policy_by_id(self, policy_id: int) -> Policy | None:
        """Retrieve a policy by its ID"""
        try:
            db_policy = self._get_policy_with_relationships(policy_id)
            return PolicyDbMapper.to_domain(db_policy)
        except Exception as e:
            raise e

    def get_policy_by_policy_number(self, policy_number: str) -> Policy | None:
        """Retrieve a policy by its policy number"""
        try:
            db_policy = self._get_policy_with_relationships_by_number(policy_number)
            return PolicyDbMapper.to_domain(db_policy)
        except Exception as e:
            raise e

    def list_all_policies(self) -> list[Policy]:
        """List all policies in the database"""
        try:
            db_policies = self._get_all_policies_with_relationships()
            return [PolicyDbMapper.to_domain(db_policy) for db_policy in db_policies]
        except Exception as e:
            raise e

    # Helper methods for database operations
    def _get_policy_with_relationships(self, policy_id: int) -> PolicyModel | None:
        """Get policy with status and type relationships loaded"""
        try:
            return (
                self.db.query(PolicyModel)
                .options(
                    joinedload(PolicyModel.status_rel), joinedload(PolicyModel.type_rel)
                )
                .filter(PolicyModel.id == policy_id)
                .first()
            )
        except Exception as e:
            raise e

    def _get_policy_with_relationships_by_number(
        self, policy_number: str
    ) -> PolicyModel | None:
        """Get policy by number with relationships loaded"""
        try:
            return (
                self.db.query(PolicyModel)
                .options(
                    joinedload(PolicyModel.status_rel), joinedload(PolicyModel.type_rel)
                )
                .filter(PolicyModel.policy_number == policy_number)
                .first()
            )
        except Exception as e:
            raise e

    def _get_all_policies_with_relationships(self) -> list[PolicyModel]:
        """Get all policies with relationships loaded"""
        try:
            return (
                self.db.query(PolicyModel)
                .options(
                    joinedload(PolicyModel.status_rel), joinedload(PolicyModel.type_rel)
                )
                .all()
            )
        except Exception as e:
            raise e

    def _get_status_id(self, status_name: str) -> int:
        """Get status ID by name"""
        try:
            status = (
                self.db.query(PolicyStatusModel)
                .filter(PolicyStatusModel.name == status_name)
                .first()
            )
            if not status:
                raise ValueError(f"Status '{status_name}' not found")
            return status.id
        except Exception as e:
            raise e

    def _get_type_id(self, type_name: str) -> int:
        """Get type ID by name"""
        try:
            policy_type = (
                self.db.query(PolicyTypeModel)
                .filter(PolicyTypeModel.name == type_name)
                .first()
            )
            if not policy_type:
                raise ValueError(f"Policy type '{type_name}' not found")
            return policy_type.id
        except Exception as e:
            raise e
