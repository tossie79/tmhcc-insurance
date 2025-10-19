from fastapi import Depends
from ..infrastructure import db
from sqlalchemy.orm import Session
from ..infrastructure.policy_repository import SQLPolicyRepository
from ..application.policy_services import PolicyService

"""Dependency injection functions for FastAPI routes"""


def get_policy_repository(
    db_session: Session = Depends(db.get_db),
) -> SQLPolicyRepository:
    return SQLPolicyRepository(db_session)


def get_policy_service(
    policy_repository: SQLPolicyRepository = Depends(get_policy_repository),
) -> PolicyService:
    return PolicyService(policy_repository)
