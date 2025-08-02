"""
Integration tests for the orchestrate endpoint.
Tests various scenarios including nested workflows and complex task structures.
"""

import requests
import json
import time
import pytest
from typing import List, Any, Dict

class TestOrchestrateEndpoint:
    """Test class for orchestrate endpoint integration tests."""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()
    
    def test_simple_orchestration(self):
        """Test simple orchestration with basic agents and workflows."""
        print("\n=== Test 1: Simple Orchestration ===")
        
        request_data = {
            "tasks": [
                ["Hello, how are you?", "What is the weather like?"],  # Workflow with 2 agents
                ["Explain quantum computing"],  # Single agent
                ["Write a poem", "Translate it to Spanish"]  # Workflow with 2 agents
            ]
        }
        
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        print(f"✅ Success! Status: {response.status_code}")
        print(f"Finalized Result: {result.get('finalizedResult', 'No result')}")
        print(f"Number of responses: {len(result.get('orchestrate_responses', []))}")
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
        
        return result
    
    def test_nested_workflows(self):
        """Test nested workflow structures."""
        print("\n=== Test 2: Nested Workflows ===")
        
        request_data = {
            "tasks": [
                ["Task 1", "Task 2"],  # Simple workflow
                ["Nested task", ["Subtask 1", "Subtask 2"]],  # Nested workflow
                ["Final task"]  # Single agent
            ]
        }
        
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        print(f"✅ Success! Status: {response.status_code}")
        print(f"Finalized Result: {result.get('finalizedResult', 'No result')}")
        print(f"Number of responses: {len(result.get('orchestrate_responses', []))}")
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
        
        return result
    
    def test_complex_nested_structure(self):
        """Test complex nested structures with multiple levels."""
        print("\n=== Test 3: Complex Nested Structure ===")
        
        request_data = {
            "tasks": [
                ["Research AI", ["Find AI papers", "Summarize findings"]],  # Nested
                ["Write code", "Test code", ["Unit tests", "Integration tests"]],  # Mixed
                ["Deploy", ["Build", "Deploy to staging", "Deploy to production"]]  # Nested
            ]
        }
        
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        print(f"✅ Success! Status: {response.status_code}")
        print(f"Finalized Result: {result.get('finalizedResult', 'No result')}")
        print(f"Number of responses: {len(result.get('orchestrate_responses', []))}")
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
        
        return result
    
    def test_deep_nesting(self):
        """Test deep nesting with multiple levels."""
        print("\n=== Test 4: Deep Nesting ===")
        
        request_data = {
            "tasks": [
                ["Level 1", ["Level 2", ["Level 3", "Level 3b"]]],  # Deep nesting (3 levels)
                ["Simple task"],  # Single agent
                ["Workflow", ["Sub-workflow", "Sub-sub-workflow"]]  # Multiple levels
            ]
        }
        
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        print(f"✅ Success! Status: {response.status_code}")
        print(f"Finalized Result: {result.get('finalizedResult', 'No result')}")
        print(f"Number of responses: {len(result.get('orchestrate_responses', []))}")
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
        
        return result
    
    def test_mixed_content_types(self):
        """Test mixed content types in the same request."""
        print("\n=== Test 5: Mixed Content Types ===")
        
        request_data = {
            "tasks": [
                ["String task 1", "String task 2"],  # All strings
                ["Mixed task", ["Nested string 1", "Nested string 2"]],  # Mixed
                ["Single string task"],  # Single string
                [["Deep nested", ["Very deep", "Very deep 2"]]]  # Deep nested
            ]
        }
        
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        print(f"✅ Success! Status: {response.status_code}")
        print(f"Finalized Result: {result.get('finalizedResult', 'No result')}")
        print(f"Number of responses: {len(result.get('orchestrate_responses', []))}")
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 4  # 4 task groups
        
        return result
    
    def test_empty_and_single_tasks(self):
        """Test edge cases with empty and single tasks."""
        print("\n=== Test 6: Edge Cases ===")
        
        request_data = {
            "tasks": [
                ["Single task"],  # Single task
                [],  # Empty task group
                ["Task 1", "Task 2"]  # Multiple tasks
            ]
        }
        
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        print(f"✅ Success! Status: {response.status_code}")
        print(f"Finalized Result: {result.get('finalizedResult', 'No result')}")
        print(f"Number of responses: {len(result.get('orchestrate_responses', []))}")
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        
        return result
    
    def test_large_workflow(self):
        """Test with a larger number of tasks."""
        print("\n=== Test 7: Large Workflow ===")
        
        request_data = {
            "tasks": [
                ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"],  # Large workflow
                ["Single task"],  # Single task
                ["Task A", "Task B", ["Subtask 1", "Subtask 2", "Subtask 3"]]  # Mixed
            ]
        }
        
        print(f"Request: {json.dumps(request_data, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        print(f"✅ Success! Status: {response.status_code}")
        print(f"Finalized Result: {result.get('finalizedResult', 'No result')}")
        print(f"Number of responses: {len(result.get('orchestrate_responses', []))}")
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
        
        return result
    
    def test_error_handling(self):
        """Test error handling with invalid requests."""
        print("\n=== Test 8: Error Handling ===")
        
        # Test with empty tasks
        empty_request = {"tasks": []}
        response = self.session.post(f"{self.base_url}/orchestrate", json=empty_request)
        print(f"Empty tasks response: {response.status_code}")
        
        # Test with invalid JSON
        try:
            response = self.session.post(f"{self.base_url}/orchestrate", data="invalid json")
            print(f"Invalid JSON response: {response.status_code}")
        except Exception as e:
            print(f"Invalid JSON error: {str(e)}")
        
        # Test with missing tasks field
        invalid_request = {"wrong_field": []}
        response = self.session.post(f"{self.base_url}/orchestrate", json=invalid_request)
        print(f"Missing tasks field response: {response.status_code}")
        
        print("✅ Error handling tests completed")
    
    def run_all_tests(self):
        """Run all orchestrate endpoint tests."""
        print("🚀 Starting Orchestrate Endpoint Integration Tests")
        print("=" * 50)
        
        try:
            # Test server connectivity
            response = self.session.get(f"{self.base_url}/")
            if response.status_code != 200:
                print(f"❌ Server not accessible: {response.status_code}")
                return False
            
            print("✅ Server is accessible")
            
            # Run all tests
            self.test_simple_orchestration()
            self.test_nested_workflows()
            self.test_complex_nested_structure()
            self.test_deep_nesting()
            self.test_mixed_content_types()
            self.test_empty_and_single_tasks()
            self.test_large_workflow()
            self.test_error_handling()
            
            print("\n" + "=" * 50)
            print("🎉 All orchestrate endpoint tests completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            return False


def main():
    """Main function to run the integration tests."""
    tester = TestOrchestrateEndpoint()
    success = tester.run_all_tests()
    
    if success:
        print("✅ All tests passed!")
        exit(0)
    else:
        print("❌ Some tests failed!")
        exit(1)


if __name__ == "__main__":
    main() 