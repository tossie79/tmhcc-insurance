from ..domain.entities import Policy
from ..domain.repository import PolicyRepository
from ..api.schemas import CreatePolicyDTO
from .mappers import PolicyDtoMapper

"""Service class for managing policies"""


class PolicyService:
    def __init__(self, repository: PolicyRepository):
        self.repository = repository

    """Create a new policy from CreatePolicyDTO"""

    def create_policy(self, policy_dto: CreatePolicyDTO) -> Policy:
        try:
            if self.repository.get_policy_by_policy_number(policy_dto.policy_number):
                raise ValueError("Policy number already exists")
            policy = PolicyDtoMapper.create_entity_from_dto(policy_dto)
            return self.repository.add_policy(policy)
        except Exception as e:
            raise e

    """Activate an existing policy by policy number"""

    def activate_policy(self, policy_number: str) -> Policy:
        try:
            policy = self.repository.get_policy_by_policy_number(policy_number)
            if not policy:
                raise ValueError("Policy not found")
            policy.activate()
            return self.repository.update_policy(policy)
        except Exception as e:
            raise e

    """Cancel an existing policy by policy number with optional reason"""

    def cancel_policy(self, policy_number: str, reason: str | None = None):
        try:
            policy = self.repository.get_policy_by_policy_number(policy_number)
            if not policy:
                raise ValueError("Policy not found")
            policy.cancel(reason)
            self.repository.update_policy(policy)
        except Exception as e:
            raise e

    """Retrieve a policy by policy number"""

    def get_policy(self, policy_number: str) -> Policy | None:
        try:
            return self.repository.get_policy_by_policy_number(policy_number)
        except Exception as e:
            raise e

    """List all policies"""

    def list_policies(self) -> list[Policy]:
        try:
            return self.repository.list_all_policies()
        except Exception as e:
            raise e
