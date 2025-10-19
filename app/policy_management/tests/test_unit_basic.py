import pytest
from unittest.mock import Mock
from datetime import date
from decimal import Decimal


from app.policy_management.domain.entities import Policy, PolicyStatus, PolicyType
from app.policy_management.domain.value_objects import PolicyNumber, Money, Period
from app.policy_management.domain.repository import PolicyRepository

"""Basic unit tests for core functionality"""


class TestBasicUnit:
    """Test creating a policy domain entity"""

    def test_policy_creation(self):
        policy = Policy(
            policy_number=PolicyNumber("TEST00123"),
            insured_name="John Doe",
            premium=Money(1000.0),
            period=Period(date(2024, 1, 1), date(2026, 12, 31)),
            status=PolicyStatus.PENDING,
            policy_type=PolicyType.PROPERTY,
        )

        assert policy.policy_number.value == "TEST00123"
        assert policy.insured_name == "John Doe"
        assert policy.premium.amount == 1000.0
        assert policy.status == PolicyStatus.PENDING

    """Test activating a policy"""

    def test_policy_activation(self):
        # Use a valid date range (end date after start date)
        start_date = date(2024, 1, 1)
        end_date = date(2026, 12, 31)

        policy = Policy(
            policy_number=PolicyNumber("TEST00123"),
            insured_name="John Doe",
            premium=Money(1000.0),
            period=Period(start_date, end_date),
            status=PolicyStatus.PENDING,
            policy_type=PolicyType.PROPERTY,
        )

        policy.activate()
        assert policy.status == PolicyStatus.ACTIVE

    """Test PolicyService get operations with mock"""

    def test_get_policy_service(self):
        from app.policy_management.application.policy_services import PolicyService
        from app.policy_management.api.schemas import CreatePolicyDTO

        # Setup
        mock_repo = Mock(spec=PolicyRepository)
        service = PolicyService(mock_repo)

        # Test data
        policy_dto = CreatePolicyDTO(
            policy_number="TEST00123",
            insured_name="Test Customer",
            premium_amount=1000.0,
            premium_currency="GBP",
            period_start_date=date(2025, 1, 1),
            period_end_date=date(2025, 12, 31),
            status="pending",
            policy_type="Property",
        )

        test_policy = Policy(
            policy_number=PolicyNumber("TEST00123"),
            insured_name="Test Customer",
            premium=Money(1000.0),
            period=Period(date(2024, 1, 1), date(2025, 12, 31)),
            status=PolicyStatus.ACTIVE,
            policy_type=PolicyType.PROPERTY,
        )

        # Test get_policy - found
        mock_repo.get_policy_by_policy_number.return_value = test_policy
        result = service.get_policy("TEST00123")
        assert result == test_policy
        mock_repo.get_policy_by_policy_number.assert_called_with("TEST00123")

        # Test get_policy - not found
        mock_repo.get_policy_by_policy_number.return_value = None
        result = service.get_policy("NOTFOUND999")
        assert result is None

    """Test listing policies with mock"""

    def test_list_policies_service(self):
        from app.policy_management.application.policy_services import PolicyService

        mock_repo = Mock(spec=PolicyRepository)
        service = PolicyService(mock_repo)

        # Test empty list
        mock_repo.list_all_policies.return_value = []
        result = service.list_policies()
        assert result == []

        # Test with policies - use valid policy numbers (at least 5 chars)
        policies = [
            Policy(
                policy_number=PolicyNumber("POL001"),
                insured_name="Customer 1",
                premium=Money(1000.0),
                period=Period(date(2024, 1, 1), date(2025, 12, 31)),
                status=PolicyStatus.ACTIVE,
                policy_type=PolicyType.PROPERTY,
            ),
            Policy(
                policy_number=PolicyNumber("POL002"),
                insured_name="Customer 2",
                premium=Money(2000.0),
                period=Period(date(2024, 12, 1), date(2026, 12, 31)),
                status=PolicyStatus.PENDING,
                policy_type=PolicyType.CASUALTY,
            ),
        ]

        mock_repo.list_all_policies.return_value = policies
        result = service.list_policies()
        assert len(result) == 2
        assert result[0].policy_number.value == "POL001"
        assert result[1].policy_number.value == "POL002"
