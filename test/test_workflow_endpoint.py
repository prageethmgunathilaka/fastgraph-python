"""
Integration test for the /workflowask endpoint.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_workflow_ask_endpoint():
    """
    Test that the /workflowask endpoint processes multiple commands correctly.
    """
    # Test request payload with multiple commands
    test_payload = {
        "commands": [
            "What is the capital of France?",
            "What is 2 + 2?",
            "Say hello in Spanish"
        ]
    }
    
    # Make POST request to /workflowask endpoint
    response = client.post("/workflowask", json=test_payload)
    
    # Assert response status is 200 OK
    assert response.status_code == 200
    
    # Get response data
    response_data = response.json()
    
    # Assert response structure
    assert "received_commands" in response_data
    assert "workflow_responses" in response_data
    assert "finalizedResult" in response_data
    
    # Assert received_commands matches input
    assert response_data["received_commands"] == test_payload["commands"]
    
    # Assert workflow_responses is a list
    assert isinstance(response_data["workflow_responses"], list)
    
    # Assert we got the same number of responses as commands
    assert len(response_data["workflow_responses"]) == len(test_payload["commands"])
    
    # Assert finalizedResult is a string and not empty
    assert isinstance(response_data["finalizedResult"], str)
    assert len(response_data["finalizedResult"]) > 0
    
    # Assert each response is not empty
    for i, response in enumerate(response_data["workflow_responses"]):
        assert response is not None
        assert len(response) > 0
        print(f"Command {i+1}: {test_payload['commands'][i]}")
        print(f"Response {i+1}: {response}")
    
    print(f"Finalized Result: {response_data['finalizedResult']}")
    print(f"Test passed! Processed {len(response_data['workflow_responses'])} commands successfully")


def test_workflow_ask_empty_commands():
    """
    Test that the /workflowask endpoint handles empty commands list gracefully.
    """
    # Test with empty commands list
    test_payload = {
        "commands": []
    }
    
    # Make POST request to /workflowask endpoint
    response = client.post("/workflowask", json=test_payload)
    
    # Assert response status is 200 OK
    assert response.status_code == 200
    
    # Get response data
    response_data = response.json()
    
    # Assert response structure
    assert "received_commands" in response_data
    assert "workflow_responses" in response_data
    assert "finalizedResult" in response_data
    
    # Assert received_commands matches input
    assert response_data["received_commands"] == test_payload["commands"]
    
    # Assert workflow_responses is empty list
    assert response_data["workflow_responses"] == []
    
    # Assert finalizedResult contains appropriate message
    assert "No commands to process" in response_data["finalizedResult"]


def test_workflow_ask_single_command():
    """
    Test that the /workflowask endpoint handles single command correctly.
    """
    # Test with single command
    test_payload = {
        "commands": ["What is the weather like today?"]
    }
    
    # Make POST request to /workflowask endpoint
    response = client.post("/workflowask", json=test_payload)
    
    # Assert response status is 200 OK
    assert response.status_code == 200
    
    # Get response data
    response_data = response.json()
    
    # Assert response structure
    assert "received_commands" in response_data
    assert "workflow_responses" in response_data
    assert "finalizedResult" in response_data
    
    # Assert we got exactly one response
    assert len(response_data["workflow_responses"]) == 1
    
    # Assert the response is not empty
    assert response_data["workflow_responses"][0] is not None
    assert len(response_data["workflow_responses"][0]) > 0
    
    # Assert finalizedResult is a string and not empty
    assert isinstance(response_data["finalizedResult"], str)
    assert len(response_data["finalizedResult"]) > 0


if __name__ == "__main__":
    # Run the main test
    test_workflow_ask_endpoint()
    print("All workflow tests passed!") 