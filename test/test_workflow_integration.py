"""
Comprehensive integration tests for the /workflowask endpoint.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestWorkflowAskIntegration:
    """Integration tests for the /workflowask endpoint."""
    
    def test_workflow_multiple_commands(self):
        """Test workflow with multiple diverse commands."""
        test_payload = {
            "commands": [
                "What is the capital of France?",
                "Calculate 15 + 27",
                "Translate 'Hello world' to Spanish",
                "What is the largest planet in our solar system?"
            ]
        }
        
        response = client.post("/workflowask", json=test_payload)
        
        # Assert response status
        assert response.status_code == 200
        
        response_data = response.json()
        
        # Assert response structure
        assert "received_commands" in response_data
        assert "workflow_responses" in response_data
        assert "finalizedResult" in response_data
        
        # Assert data integrity
        assert response_data["received_commands"] == test_payload["commands"]
        assert len(response_data["workflow_responses"]) == 4
        assert isinstance(response_data["finalizedResult"], str)
        assert len(response_data["finalizedResult"]) > 0
        
        # Print results for inspection
        print("\n=== Multiple Commands Test Results ===")
        for i, (cmd, resp) in enumerate(zip(test_payload["commands"], response_data["workflow_responses"])):
            print(f"Command {i+1}: {cmd}")
            print(f"Response {i+1}: {resp}")
            print("-" * 50)
        
        print(f"Finalized Result: {response_data['finalizedResult']}")
        print("=" * 50)
    
    def test_workflow_single_command(self):
        """Test workflow with single command."""
        test_payload = {
            "commands": ["What is the weather like today?"]
        }
        
        response = client.post("/workflowask", json=test_payload)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Assert single command processing
        assert len(response_data["workflow_responses"]) == 1
        assert len(response_data["received_commands"]) == 1
        assert response_data["received_commands"][0] == "What is the weather like today?"
        assert len(response_data["workflow_responses"][0]) > 0
        assert len(response_data["finalizedResult"]) > 0
        
        print(f"\nSingle Command Test:")
        print(f"Command: {response_data['received_commands'][0]}")
        print(f"Response: {response_data['workflow_responses'][0]}")
        print(f"Summary: {response_data['finalizedResult']}")
    
    def test_workflow_empty_commands(self):
        """Test workflow with empty commands list."""
        test_payload = {
            "commands": []
        }
        
        response = client.post("/workflowask", json=test_payload)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Assert empty handling
        assert response_data["workflow_responses"] == []
        assert response_data["received_commands"] == []
        assert "No commands to process" in response_data["finalizedResult"]
        
        print(f"\nEmpty Commands Test:")
        print(f"Finalized Result: {response_data['finalizedResult']}")
    
    def test_workflow_math_commands(self):
        """Test workflow with mathematical commands."""
        test_payload = {
            "commands": [
                "What is 25 + 17?",
                "Calculate 8 * 9",
                "What is the square root of 144?",
                "What is 100 divided by 4?"
            ]
        }
        
        response = client.post("/workflowask", json=test_payload)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Assert math processing
        assert len(response_data["workflow_responses"]) == 4
        assert all(len(resp) > 0 for resp in response_data["workflow_responses"])
        assert len(response_data["finalizedResult"]) > 0
        
        print("\n=== Math Commands Test Results ===")
        for i, (cmd, resp) in enumerate(zip(test_payload["commands"], response_data["workflow_responses"])):
            print(f"Math Command {i+1}: {cmd}")
            print(f"Math Response {i+1}: {resp}")
            print("-" * 30)
        
        print(f"Math Summary: {response_data['finalizedResult']}")
    
    def test_workflow_language_commands(self):
        """Test workflow with language translation commands."""
        test_payload = {
            "commands": [
                "Translate 'Hello' to French",
                "Translate 'Good morning' to German",
                "Translate 'Thank you' to Italian",
                "Translate 'Goodbye' to Portuguese"
            ]
        }
        
        response = client.post("/workflowask", json=test_payload)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Assert language processing
        assert len(response_data["workflow_responses"]) == 4
        assert all(len(resp) > 0 for resp in response_data["workflow_responses"])
        assert len(response_data["finalizedResult"]) > 0
        
        print("\n=== Language Commands Test Results ===")
        for i, (cmd, resp) in enumerate(zip(test_payload["commands"], response_data["workflow_responses"])):
            print(f"Language Command {i+1}: {cmd}")
            print(f"Language Response {i+1}: {resp}")
            print("-" * 40)
        
        print(f"Language Summary: {response_data['finalizedResult']}")
    
    def test_workflow_mixed_commands(self):
        """Test workflow with mixed types of commands."""
        test_payload = {
            "commands": [
                "What is the population of Tokyo?",
                "Calculate 3.14 * 2",
                "Translate 'Beautiful' to Japanese",
                "What is the chemical symbol for gold?",
                "What is the speed of light?"
            ]
        }
        
        response = client.post("/workflowask", json=test_payload)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Assert mixed command processing
        assert len(response_data["workflow_responses"]) == 5
        assert all(len(resp) > 0 for resp in response_data["workflow_responses"])
        assert len(response_data["finalizedResult"]) > 0
        
        print("\n=== Mixed Commands Test Results ===")
        for i, (cmd, resp) in enumerate(zip(test_payload["commands"], response_data["workflow_responses"])):
            print(f"Mixed Command {i+1}: {cmd}")
            print(f"Mixed Response {i+1}: {resp}")
            print("-" * 35)
        
        print(f"Mixed Summary: {response_data['finalizedResult']}")
    
    def test_workflow_error_handling(self):
        """Test workflow error handling with invalid commands."""
        test_payload = {
            "commands": [
                "This is a normal command",
                "",  # Empty command
                "Another normal command"
            ]
        }
        
        response = client.post("/workflowask", json=test_payload)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Assert error handling
        assert len(response_data["workflow_responses"]) == 3
        assert len(response_data["finalizedResult"]) > 0
        
        print(f"\nError Handling Test:")
        print(f"Responses: {response_data['workflow_responses']}")
        print(f"Summary: {response_data['finalizedResult']}")


def test_workflow_performance():
    """Test workflow performance with multiple commands."""
    test_payload = {
        "commands": [
            "What is 1 + 1?",
            "What is 2 + 2?",
            "What is 3 + 3?",
            "What is 4 + 4?",
            "What is 5 + 5?"
        ]
    }
    
    import time
    start_time = time.time()
    
    response = client.post("/workflowask", json=test_payload)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    assert response.status_code == 200
    response_data = response.json()
    
    print(f"\nPerformance Test:")
    print(f"Processing time: {processing_time:.2f} seconds")
    print(f"Commands processed: {len(response_data['workflow_responses'])}")
    print(f"Average time per command: {processing_time/len(test_payload['commands']):.2f} seconds")


if __name__ == "__main__":
    # Run all tests
    test_suite = TestWorkflowAskIntegration()
    
    print("Running Workflow Integration Tests...")
    print("=" * 60)
    
    # Run each test method
    test_suite.test_workflow_multiple_commands()
    test_suite.test_workflow_single_command()
    test_suite.test_workflow_empty_commands()
    test_suite.test_workflow_math_commands()
    test_suite.test_workflow_language_commands()
    test_suite.test_workflow_mixed_commands()
    test_suite.test_workflow_error_handling()
    
    # Run performance test
    test_workflow_performance()
    
    print("\n" + "=" * 60)
    print("All workflow integration tests completed successfully!") 