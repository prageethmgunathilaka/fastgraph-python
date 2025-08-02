"""
Test file for the orchestrate endpoint.
"""

import requests
import json

def test_orchestrate_endpoint():
    """Test the orchestrate endpoint with various task structures."""
    
    # Test data with different structures
    test_cases = [
        {
            "name": "Simple agents and workflows",
            "tasks": [
                ["Hello, how are you?", "What is the weather like?"],  # Workflow with 2 agents
                ["Explain quantum computing"],  # Single agent
                ["Write a poem", "Translate it to Spanish"]  # Workflow with 2 agents
            ]
        },
        {
            "name": "Nested workflows",
            "tasks": [
                ["Task 1", "Task 2"],  # Simple workflow
                ["Nested task", ["Subtask 1", "Subtask 2"]],  # Nested workflow
                ["Final task"]  # Single agent
            ]
        },
        {
            "name": "Complex nested structure",
            "tasks": [
                ["Research AI", ["Find AI papers", "Summarize findings"]],  # Nested
                ["Write code", "Test code", ["Unit tests", "Integration tests"]],  # Mixed
                ["Deploy", ["Build", "Deploy to staging", "Deploy to production"]]  # Nested
            ]
        }
    ]
    
    base_url = "http://localhost:8000"
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== Test Case {i+1}: {test_case['name']} ===")
        
        # Prepare the request
        request_data = {
            "tasks": test_case["tasks"]
        }
        
        print(f"Request data: {json.dumps(request_data, indent=2)}")
        
        try:
            # Make the request
            response = requests.post(f"{base_url}/orchestrate", json=request_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Status: {response.status_code}")
                print(f"Finalized Result: {result.get('finalizedResult', 'No result')}")
                print(f"Number of responses: {len(result.get('orchestrate_responses', []))}")
            else:
                print(f"❌ Error! Status: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_orchestrate_endpoint() 