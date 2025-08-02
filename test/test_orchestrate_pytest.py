"""
Pytest integration tests for the orchestrate endpoint.
Tests various scenarios including nested workflows and complex task structures.
"""

import pytest
import requests
import json
import time
from typing import List, Any, Dict


class TestOrchestrateEndpointPytest:
    """Pytest test class for orchestrate endpoint integration tests."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()
        
        # Test server connectivity
        response = self.session.get(f"{self.base_url}/")
        if response.status_code != 200:
            pytest.skip("Server not accessible")
    
    def test_simple_orchestration(self):
        """Test simple orchestration with basic agents and workflows."""
        request_data = {
            "tasks": [
                ["Hello, how are you?", "What is the weather like?"],  # Workflow with 2 agents
                ["Explain quantum computing"],  # Single agent
                ["Write a poem", "Translate it to Spanish"]  # Workflow with 2 agents
            ]
        }
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
        
        # Validate that finalizedResult is not empty
        assert result["finalizedResult"] is not None
        assert len(result["finalizedResult"]) > 0
    
    def test_nested_workflows(self):
        """Test nested workflow structures."""
        request_data = {
            "tasks": [
                ["Task 1", "Task 2"],  # Simple workflow
                ["Nested task", ["Subtask 1", "Subtask 2"]],  # Nested workflow
                ["Final task"]  # Single agent
            ]
        }
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
    
    def test_complex_nested_structure(self):
        """Test complex nested structures with multiple levels."""
        request_data = {
            "tasks": [
                ["Research AI", ["Find AI papers", "Summarize findings"]],  # Nested
                ["Write code", "Test code", ["Unit tests", "Integration tests"]],  # Mixed
                ["Deploy", ["Build", "Deploy to staging", "Deploy to production"]]  # Nested
            ]
        }
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
    
    def test_deep_nesting(self):
        """Test deep nesting with multiple levels."""
        request_data = {
            "tasks": [
                ["Level 1", ["Level 2", ["Level 3", ["Level 4", "Level 4b"]]]],  # Deep nesting
                ["Simple task"],  # Single agent
                ["Workflow", ["Sub-workflow", ["Sub-sub-workflow"]]]  # Multiple levels
            ]
        }
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
    
    def test_mixed_content_types(self):
        """Test mixed content types in the same request."""
        request_data = {
            "tasks": [
                ["String task 1", "String task 2"],  # All strings
                ["Mixed task", ["Nested string 1", "Nested string 2"]],  # Mixed
                ["Single string task"],  # Single string
                [["Deep nested", ["Very deep", "Very deep 2"]]]  # Deep nested
            ]
        }
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 4  # 4 task groups
    
    def test_empty_and_single_tasks(self):
        """Test edge cases with empty and single tasks."""
        request_data = {
            "tasks": [
                ["Single task"],  # Single task
                [],  # Empty task group
                ["Task 1", "Task 2"]  # Multiple tasks
            ]
        }
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
    
    def test_large_workflow(self):
        """Test with a larger number of tasks."""
        request_data = {
            "tasks": [
                ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"],  # Large workflow
                ["Single task"],  # Single task
                ["Task A", "Task B", ["Subtask 1", "Subtask 2", "Subtask 3"]]  # Mixed
            ]
        }
        
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        result = response.json()
        
        # Validate response structure
        assert "received_tasks" in result
        assert "orchestrate_responses" in result
        assert "finalizedResult" in result
        assert len(result["orchestrate_responses"]) == 3  # 3 task groups
    
    def test_error_handling_empty_tasks(self):
        """Test error handling with empty tasks."""
        empty_request = {"tasks": []}
        response = self.session.post(f"{self.base_url}/orchestrate", json=empty_request)
        
        # Should handle empty tasks gracefully
        assert response.status_code in [200, 422], f"Unexpected status code: {response.status_code}"
    
    def test_error_handling_invalid_json(self):
        """Test error handling with invalid JSON."""
        try:
            response = self.session.post(f"{self.base_url}/orchestrate", data="invalid json")
            # Should return 422 for invalid JSON
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        except Exception:
            # Connection error is also acceptable
            pass
    
    def test_error_handling_missing_tasks_field(self):
        """Test error handling with missing tasks field."""
        invalid_request = {"wrong_field": []}
        response = self.session.post(f"{self.base_url}/orchestrate", json=invalid_request)
        
        # Should return 422 for missing required field
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    
    def test_response_time(self):
        """Test that responses are returned within reasonable time."""
        request_data = {
            "tasks": [
                ["Simple task 1", "Simple task 2"],
                ["Another task"]
            ]
        }
        
        start_time = time.time()
        response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
        end_time = time.time()
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        # Should complete within 30 seconds (adjust as needed)
        response_time = end_time - start_time
        assert response_time < 30, f"Response took too long: {response_time:.2f} seconds"
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import threading
        import queue
        
        request_data = {
            "tasks": [
                ["Test task 1"],
                ["Test task 2"]
            ]
        }
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = self.session.post(f"{self.base_url}/orchestrate", json=request_data)
                results.put(response.status_code)
            except Exception as e:
                results.put(f"Error: {str(e)}")
        
        # Start multiple concurrent requests
        threads = []
        for i in range(3):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        status_codes = []
        while not results.empty():
            status_codes.append(results.get())
        
        # All requests should succeed
        for status in status_codes:
            if isinstance(status, str):
                pytest.fail(f"Request failed: {status}")
            else:
                assert status == 200, f"Expected 200, got {status}"


# Pytest markers for different test categories
import pytest

# Mark tests that require the server to be running
pytest.mark.integration = pytest.mark.skipif(
    True,  # Always skip integration tests by default
    reason="integration tests require server to be running"
) 