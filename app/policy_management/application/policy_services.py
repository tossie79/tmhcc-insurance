from ..domain.entities import Policy
from ..domain.repository import PolicyRepository
from ..api.schemas import CreatePolicyDTO
from .mappers import PolicyDtoMapper


class PolicyService:
    """Service class for managing policies"""

    def __init__(self, repository: PolicyRepository):
        self.repository = repository

    def create_policy(self, policy_dto: CreatePolicyDTO) -> Policy:
        """Create a new policy from CreatePolicyDTO"""
        try:
            if self.repository.get_policy_by_policy_number(policy_dto.policy_number):
                raise ValueError("Policy number already exists")
            policy = PolicyDtoMapper.create_entity_from_dto(policy_dto)
            return self.repository.add_policy(policy)
        except Exception as e:
            raise e

    def activate_policy(self, policy_number: str) -> Policy:
        """Activate an existing policy by policy number"""
        try:
            policy = self.repository.get_policy_by_policy_number(policy_number)
            if not policy:
                raise ValueError("Policy not found")
            policy.activate()
            return self.repository.update_policy(policy)
        except Exception as e:
            raise e

    def cancel_policy(self, policy_number: str, reason: str | None = None):
        """Cancel an existing policy by policy number with optional reason"""
        try:
            policy = self.repository.get_policy_by_policy_number(policy_number)
            if not policy:
                raise ValueError("Policy not found")
            policy.cancel(reason)
            self.repository.update_policy(policy)
        except Exception as e:
            raise e

    def get_policy(self, policy_number: str) -> Policy | None:
        """Retrieve a policy by policy number"""
        try:
            return self.repository.get_policy_by_policy_number(policy_number)
        except Exception as e:
            raise e

    def list_policies(self) -> list[Policy]:
        """List all policies"""
        try:
            return self.repository.list_all_policies()
        except Exception as e:
            raise e
