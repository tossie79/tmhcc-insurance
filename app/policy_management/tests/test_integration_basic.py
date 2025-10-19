import pytest
from datetime import date
from decimal import Decimal


from app.policy_management.domain.entities import PolicyStatus, PolicyType


class TestBasicIntegration:
    """Basic integration tests with real database"""

    """Fixture to provide PolicyService with real DB session"""

    @pytest.fixture
    def policy_service(self, db_session):

        from app.policy_management.application.policy_services import PolicyService
        from app.policy_management.infrastructure.policy_repository import (
            SQLPolicyRepository,
        )

        repository = SQLPolicyRepository(db_session)
        return PolicyService(repository)

    """Test creating a policy and then retrieving it"""

    def test_create_and_get_policy(self, policy_service):
        from app.policy_management.api.schemas import CreatePolicyDTO

        # Create policy
        policy_dto = CreatePolicyDTO(
            policy_number="INTEGTEST001",
            insured_name="Integration Test",
            premium_amount=Decimal("1500.0"),
            premium_currency="GBP",
            period_start_date=date(2024, 1, 1),
            period_end_date=date(2026, 12, 31),
            status="active",
            policy_type="Property",
        )

        created_policy = policy_service.create_policy(policy_dto)
        assert created_policy is not None
        assert created_policy.policy_number.value == "INTEGTEST001"

        # Retrieve policy
        retrieved_policy = policy_service.get_policy("INTEGTEST001")
        assert retrieved_policy is not None
        assert retrieved_policy.policy_number.value == "INTEGTEST001"
        assert retrieved_policy.insured_name == "Integration Test"
        assert retrieved_policy.status == PolicyStatus.ACTIVE

    """Test retrieving a policy that doesn't exist"""

    def test_get_nonexistent_policy(self, policy_service):
        result = policy_service.get_policy("DOESNOTEXIST")
        assert result is None

    """Test listing all policies"""

    def test_list_policies(self, policy_service, db_session):
        from app.policy_management.api.schemas import CreatePolicyDTO
        from app.policy_management.infrastructure.models import PolicyModel

        # Clear existing policies
        db_session.query(PolicyModel).delete()
        db_session.commit()

        # Create test policies
        test_policies = [
            CreatePolicyDTO(
                policy_number="LIST001",
                insured_name="Customer One",
                premium_amount=Decimal("1000.0"),
                premium_currency="GBP",
                period_start_date=date(2024, 1, 1),
                period_end_date=date(2025, 12, 31),
                status="active",
                policy_type="Property",
            ),
            CreatePolicyDTO(
                policy_number="LIST002",
                insured_name="Customer Two",
                premium_amount=Decimal("2000.0"),
                premium_currency="GBP",
                period_start_date=date(2024, 1, 1),
                period_end_date=date(2025, 12, 31),
                status="pending",
                policy_type="Casualty",
            ),
        ]

        for policy_dto in test_policies:
            policy_service.create_policy(policy_dto)

        # List policies
        policies = policy_service.list_policies()
        assert len(policies) == 2

        # Verify policies
        policy_dict = {p.policy_number.value: p for p in policies}
        assert "LIST001" in policy_dict
        assert "LIST002" in policy_dict
        assert policy_dict["LIST001"].insured_name == "Customer One"
        assert policy_dict["LIST002"].insured_name == "Customer Two"

    """Test listing when no policies exist"""

    def test_list_empty_policies(self, policy_service, db_session):
        from app.policy_management.infrastructure.models import PolicyModel

        # Clear all policies
        db_session.query(PolicyModel).delete()
        db_session.commit()

        policies = policy_service.list_policies()
        assert policies == []
