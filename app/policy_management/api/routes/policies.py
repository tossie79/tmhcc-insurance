from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List

from ...application.policy_services import PolicyService
from .. import schemas
from ...application.mappers import PolicyDtoMapper
from ..dependencies import get_policy_service

router = APIRouter(prefix="/api/v1/policies", tags=["policies"])


@router.post("/", response_model=Dict[str, Any])
def create_policy(
    policy_dto: schemas.CreatePolicyDTO,
    policy_service: PolicyService = Depends(get_policy_service),
):
    """This endpoint Create a new policy and returns the newly created policy"""
    try:
        new_policy = policy_service.create_policy(policy_dto)
        return PolicyDtoMapper.to_dict(new_policy)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{policy_number}/activate", response_model=Dict[str, Any])
def activate_policy(
    policy_number: str, policy_service: PolicyService = Depends(get_policy_service)
):
    """This endpoint activates an existing policy using the policy number and returns the updated policy"""
    try:
        policy = policy_service.activate_policy(policy_number)
        return PolicyDtoMapper.to_dict(policy)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{policy_number}", response_model=Dict[str, Any])
def get_policy(
    policy_number: str, policy_service: PolicyService = Depends(get_policy_service)
):
    """This endpoint returns a  single policy by policy number"""
    try:
        policy = policy_service.get_policy(policy_number)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return PolicyDtoMapper.to_dict(policy)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Dict[str, Any]])
def list_policies(policy_service: PolicyService = Depends(get_policy_service)):
    """This endpoint returns all policies as a list"""
    try:
        policies = policy_service.list_policies()
        return [PolicyDtoMapper.to_dict(policy) for policy in policies]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
