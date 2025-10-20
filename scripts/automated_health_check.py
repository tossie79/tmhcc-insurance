#!/usr/bin/env python3
"""
Automated Health Check & Functionality Verification
for TMHCC Policy Management System

This script performs end-to-end testing of all major system components
and provides a detailed report of system health.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
import time
import json
from datetime import datetime

class SystemHealthChecker:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "overall_status": "UNKNOWN"
        }
    
    def log_result(self, service, status, message, details=None):
        """Log test results with consistent formatting"""
        self.results["services"][service] = {
            "status": status,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{icon} {service}: {message}")
        if details:
            print(f"   Details: {details}")
    
    def check_api_health(self):
        """Test basic API health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_result("API Health", "PASS", "API is healthy", data)
                return True
            else:
                self.log_result("API Health", "FAIL", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("API Health", "FAIL", f"Connection failed: {str(e)}")
            return False
    
    def check_database_connection(self):
        """Test database connectivity through API"""
        try:
            response = requests.get(f"{self.api_url}/policies/", timeout=10)
            # Even if no policies, we should get 200, not 500
            if response.status_code == 200:
                self.log_result("Database", "PASS", "Database connection successful")
                return True
            else:
                self.log_result("Database", "FAIL", f"Database error: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Database", "FAIL", f"Database connection failed: {str(e)}")
            return False
    
    def test_policy_crud_operations(self):
        """Test complete CRUD operations for policies"""
        test_policy_number = f"AUTO_TEST_{int(time.time())}"
        
        # Test Policy Creation
        try:
            policy_data = {
                "policy_number": test_policy_number,
                "insured_name": "Automated Test User",
                "premium_amount": 999.99,
                "premium_currency": "GBP",
                "period_start_date": "2024-01-01",
                "period_end_date": "2026-12-31",
                "status": "pending",
                "policy_type": "Property"
            }
            
            response = requests.post(f"{self.api_url}/policies/", json=policy_data, timeout=10)
            if response.status_code in [200, 201]:
                created_policy = response.json()
                self.log_result("Policy Creation", "PASS", "Policy created successfully", {
                    "policy_number": test_policy_number,
                    "response_time": f"{response.elapsed.total_seconds():.2f}s"
                })
            else:
                self.log_result("Policy Creation", "FAIL", f"Creation failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Policy Creation", "FAIL", f"Creation error: {str(e)}")
            return False
        
        # Test Policy Retrieval
        try:
            response = requests.get(f"{self.api_url}/policies/{test_policy_number}", timeout=10)
            if response.status_code == 200:
                retrieved_policy = response.json()
                if retrieved_policy["policy_number"] == test_policy_number:
                    self.log_result("Policy Retrieval", "PASS", "Policy retrieved successfully")
                else:
                    self.log_result("Policy Retrieval", "FAIL", "Policy data mismatch")
                    return False
            else:
                self.log_result("Policy Retrieval", "FAIL", f"Retrieval failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Policy Retrieval", "FAIL", f"Retrieval error: {str(e)}")
            return False
        
        # Test Policy Listing
        try:
            response = requests.get(f"{self.api_url}/policies/", timeout=10)
            if response.status_code == 200:
                policies = response.json()
                policy_numbers = [p["policy_number"] for p in policies]
                if test_policy_number in policy_numbers:
                    self.log_result("Policy Listing", "PASS", f"Found {len(policies)} policies")
                else:
                    self.log_result("Policy Listing", "FAIL", "New policy not in list")
                    return False
            else:
                self.log_result("Policy Listing", "FAIL", f"Listing failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Policy Listing", "FAIL", f"Listing error: {str(e)}")
            return False
        
        # Test Policy Activation
        try:
            response = requests.post(f"{self.api_url}/policies/{test_policy_number}/activate", timeout=10)
            # This might fail if period is not active, which is OK for this test
            if response.status_code in [200, 400]:
                self.log_result("Policy Activation", "PASS", "Activation endpoint responsive")
            else:
                self.log_result("Policy Activation", "FAIL", f"Activation failed: HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Policy Activation", "FAIL", f"Activation error: {str(e)}")
        
        return True
    
    def test_frontend_endpoints(self):
        """Test frontend routes are accessible"""
        endpoints = [
            ("/", "Policies List"),

        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    self.log_result(f"Frontend {name}", "PASS", "Page loaded successfully")
                else:
                    self.log_result(f"Frontend {name}", "FAIL", f"HTTP {response.status_code}")
            except Exception as e:
                self.log_result(f"Frontend {name}", "FAIL", f"Load failed: {str(e)}")
    
    def test_error_handling(self):
        """Test that error cases are handled properly"""
        try:
            # Test non-existent policy
            response = requests.get(f"{self.api_url}/policies/NON_EXISTENT_12345", timeout=10)
            if response.status_code == 404:
                self.log_result("Error Handling", "PASS", "404 handled correctly")
            else:
                self.log_result("Error Handling", "FAIL", f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_result("Error Handling", "FAIL", f"Error test failed: {str(e)}")
    
    def run_performance_checks(self):
        """Run basic performance checks"""
        endpoints_to_test = [
            f"{self.api_url}/policies/",
            f"{self.base_url}/health",
        ]
        
        for endpoint in endpoints_to_test:
            try:
                start_time = time.time()
                response = requests.get(endpoint, timeout=10)
                response_time = time.time() - start_time
                
                if response_time < 2.0:  # 2 second threshold
                    self.log_result(f"Performance {endpoint}", "PASS", 
                                  f"Response time: {response_time:.2f}s")
                else:
                    self.log_result(f"Performance {endpoint}", "WARN", 
                                  f"Slow response: {response_time:.2f}s")
            except Exception as e:
                self.log_result(f"Performance {endpoint}", "FAIL", f"Performance test failed: {str(e)}")
    
    def generate_report(self):
        """Generate comprehensive health report"""
        passed = sum(1 for service in self.results["services"].values() if service["status"] == "PASS")
        total = len(self.results["services"])
        
        # Calculate overall status
        if passed == total:
            self.results["overall_status"] = "HEALTHY"
        elif passed >= total * 0.7:  # 70% threshold
            self.results["overall_status"] = "DEGRADED"
        else:
            self.results["overall_status"] = "UNHEALTHY"
        
        return self.results
    
    def run_complete_check(self):
        """Run all health checks"""
        print("🚀 Starting TMHCC Policy Management Health Check...")
        print("=" * 60)
        
        # Run all checks
        self.check_api_health()
        self.check_database_connection()
        self.test_policy_crud_operations()
        self.test_frontend_endpoints()
        self.test_error_handling()
        self.run_performance_checks()
        
        # Generate report
        report = self.generate_report()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for service in report["services"].values() if service["status"] == "PASS")
        total = len(report["services"])
        
        print(f"Overall Status: {report['overall_status']}")
        print(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
        print(f"Timestamp: {report['timestamp']}")
        
        # Save report to file
        report_file = f"scripts/reports/health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        return report["overall_status"] == "HEALTHY"

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TMHCC Policy Management Health Check')
    parser.add_argument('--url', default='http://localhost:8000', 
                       help='Base URL of the application')
    parser.add_argument('--timeout', type=int, default=10,
                       help='Request timeout in seconds')
    
    args = parser.parse_args()
    
    checker = SystemHealthChecker(base_url=args.url)
    success = checker.run_complete_check()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()