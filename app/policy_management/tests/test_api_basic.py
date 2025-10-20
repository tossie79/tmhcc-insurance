import pytest


class TestAPIGetEndpoints:
    """Basic API tests for GET endpoints in the Policy Management API"""

    def test_get_policy_success(self, client):
        """Test getting a policy by policy number successfully"""
        # First create a policy to retrieve
        policy_data = {
            "policy_number": "APIGET001",
            "insured_name": "API Get Test",
            "premium_amount": 2500.0,
            "premium_currency": "GBP",
            "period_start_date": "2024-01-01",
            "period_end_date": "2024-12-31",
            "status": "active",
            "policy_type": "Property",
        }

        create_response = client.post("/api/v1/policies/", json=policy_data)
        assert create_response.status_code in [
            200,
            201,
        ], f"Create failed: {create_response.text}"

        # Then get it
        response = client.get("/api/v1/policies/APIGET001")
        assert response.status_code == 200

        data = response.json()
        assert data["policy_number"] == "APIGET001"
        assert data["insured_name"] == "API Get Test"

    def test_get_policy_not_found(self, client):
        """Test getting a policy that doesn't exist"""
        response = client.get("/api/v1/policies/NONEXIST999")
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data
        assert "Policy not found" in error_data["detail"]

    def test_list_policies(self, client):
        """Test listing all policies"""
        response = client.get("/api/v1/policies/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_policies_response_structure(self, client):
        """Test that list response has correct structure"""
        response = client.get("/api/v1/policies/")
        assert response.status_code == 200
        policies = response.json()

        required_fields = ["policy_number", "insured_name", "status", "policy_type"]
        for policy in policies:
            for field in required_fields:
                assert field in policy, f"Missing field {field} in policy {policy}"

    def test_health_check(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "TMHCC Policy Management" in data["service"]

    def test_get_policy_with_special_characters(self, client):
        """Test getting policy with special characters in policy number"""
        response = client.get("/api/v1/policies/SPECIAL123")
        assert response.status_code == 404


class TestAPIWorkflows:
    """Test complete API workflows for GET operations"""

    def test_create_and_retrieve_workflow(self, client):
        """Test complete workflow: create policy then retrieve it"""
        create_data = {
            "policy_number": "WORKFLOW001",
            "insured_name": "Workflow Test",
            "premium_amount": 3000.0,
            "premium_currency": "GBP",
            "period_start_date": "2024-01-01",
            "period_end_date": "2024-12-31",
            "status": "pending",
            "policy_type": "Marine",
        }

        create_response = client.post("/api/v1/policies/", json=create_data)
        assert create_response.status_code in [
            200,
            201,
        ], f"Create failed: {create_response.text}"

        # Retrieve by policy number
        get_response = client.get("/api/v1/policies/WORKFLOW001")
        assert get_response.status_code == 200

        retrieved_data = get_response.json()
        assert retrieved_data["policy_number"] == "WORKFLOW001"
        assert retrieved_data["insured_name"] == "Workflow Test"

    def test_multiple_retrieval_workflow(self, client):
        """Test retrieving multiple policies"""
        policies_to_create = [
            {
                "policy_number": "MULTI001",
                "insured_name": "Multi Test 1",
                "premium_amount": 1000.0,
                "premium_currency": "GBP",
                "period_start_date": "2024-01-01",
                "period_end_date": "2024-12-31",
                "status": "active",
                "policy_type": "Property",
            },
            {
                "policy_number": "MULTI002",
                "insured_name": "Multi Test 2",
                "premium_amount": 2000.0,
                "premium_currency": "GBP",
                "period_start_date": "2024-01-01",
                "period_end_date": "2024-12-31",
                "status": "pending",
                "policy_type": "Casualty",
            },
        ]

        # Create all policies
        for policy_data in policies_to_create:
            response = client.post("/api/v1/policies/", json=policy_data)
            assert response.status_code in [200, 201], f"Create failed: {response.text}"

        # Retrieve each one individually
        for policy_data in policies_to_create:
            policy_number = policy_data["policy_number"]
            response = client.get(f"/api/v1/policies/{policy_number}")
            assert response.status_code == 200
            retrieved = response.json()
            assert retrieved["policy_number"] == policy_data["policy_number"]
            assert retrieved["insured_name"] == policy_data["insured_name"]
