from abc import ABC, abstractmethod
from ..domain.entities import Policy

"""Abstract repository interface for Policy entity"""


class PolicyRepository(ABC):
    @abstractmethod
    def add_policy(self, policy: Policy) -> Policy:
        raise NotImplementedError

    @abstractmethod
    def update_policy(self, policy: Policy) -> Policy:
        raise NotImplementedError

    @abstractmethod
    def cancel_policy(self, policy: Policy) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_policy_by_id(self, id: int) -> Policy | None:
        raise NotImplementedError

    @abstractmethod
    def get_policy_by_policy_number(self, policy_number: str) -> Policy | None:
        raise NotImplementedError

    @abstractmethod
    def list_all_policies(self) -> list[Policy]:
        raise NotImplementedError
