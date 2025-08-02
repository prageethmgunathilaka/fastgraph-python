"""
Tests for the /ask endpoint.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_ask_endpoint_llm_response():
    """
    Test that the /ask endpoint returns a valid LLM response.
    """
    # Test request payload
    test_payload = {
        "text": "if you are an LLM just say... I'm LLM here. How can I assist you today?"
    }
    
    # Make POST request to /ask endpoint
    response = client.post("/ask", json=test_payload)
    
    # Assert response status is 200 OK
    assert response.status_code == 200
    
    # Get response data
    response_data = response.json()
    
    # Assert response structure
    assert "received_text" in response_data
    assert "agent_response" in response_data
    
    # Assert received_text matches input
    assert response_data["received_text"] == test_payload["text"]
    
    # Assert agent_response is not empty
    assert response_data["agent_response"] is not None
    assert len(response_data["agent_response"]) > 0
    
    # Assert agent_response contains expected LLM acknowledgment
    agent_response = response_data["agent_response"].lower()
    assert "llm" in agent_response or "assist" in agent_response or "help" in agent_response
    
    print(f"Test passed! Agent response: {response_data['agent_response']}")


def test_ask_endpoint_empty_input():
    """
    Test that the /ask endpoint handles empty input gracefully.
    """
    # Test with empty text
    test_payload = {
        "text": ""
    }
    
    # Make POST request to /ask endpoint
    response = client.post("/ask", json=test_payload)
    
    # Assert response status is 200 OK
    assert response.status_code == 200
    
    # Get response data
    response_data = response.json()
    
    # Assert response structure
    assert "received_text" in response_data
    assert "agent_response" in response_data
    
    # Assert received_text matches input
    assert response_data["received_text"] == test_payload["text"]
    
    # Assert agent_response is not empty (should have some response even for empty input)
    assert response_data["agent_response"] is not None


def test_ask_endpoint_invalid_payload():
    """
    Test that the /ask endpoint handles invalid payloads correctly.
    """
    # Test with missing text field
    test_payload = {}
    
    # Make POST request to /ask endpoint
    response = client.post("/ask", json=test_payload)
    
    # Assert response status is 422 (validation error)
    assert response.status_code == 422


if __name__ == "__main__":
    # Run the main test
    test_ask_endpoint_llm_response()
    print("All tests passed!") 