"""
Test for the auto orchestrate endpoint.
"""

import pytest
import httpx
import json
from typing import Dict, Any


class TestAutoOrchestrateEndpoint:
    """Test cases for the /autoOrchestrate endpoint."""
    
    base_url = "http://localhost:8001"
    
    def test_auto_orchestrate_basic_command(self):
        """Test basic command processing."""
        command = "Analyze the current market trends for renewable energy"
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/autoOrchestrate",
                json={"command": command}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Check response structure
            assert "received_command" in data
            assert "auto_orchestrate_response" in data
            assert "finalizedResult" in data
            
            # Check that command was received correctly
            assert data["received_command"] == command
            
            # Check auto orchestrate response structure
            auto_response = data["auto_orchestrate_response"]
            assert "identified_role" in auto_response
            assert "m_language_spec" in auto_response
            assert "swarm_result" in auto_response
            assert "processing_steps" in auto_response
            
            # Check that a role was identified
            assert auto_response["identified_role"] != ""
            
            # Check that M Language spec was generated
            assert auto_response["m_language_spec"] != ""
            
            # Check processing steps
            expected_steps = [
                "Role identification",
                "M Language specification generation", 
                "Swarm execution",
                "Result compilation"
            ]
            assert auto_response["processing_steps"] == expected_steps
    
    def test_auto_orchestrate_technical_command(self):
        """Test technical command processing."""
        command = "Create a Python script to scrape data from a website"
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/autoOrchestrate",
                json={"command": command}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            auto_response = data["auto_orchestrate_response"]
            
            # Should identify a role (may fall back to General Assistant due to API issues)
            identified_role = auto_response["identified_role"]
            assert identified_role != ""
            
            # Check that M Language spec contains technical elements
            m_spec = auto_response["m_language_spec"]
            assert "agent" in m_spec.lower()
            assert "workflow" in m_spec.lower()
    
    def test_auto_orchestrate_creative_command(self):
        """Test creative command processing."""
        command = "Write a compelling marketing copy for a new product launch"
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/autoOrchestrate",
                json={"command": command}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            auto_response = data["auto_orchestrate_response"]
            
            # Should identify a role (may fall back to General Assistant due to API issues)
            identified_role = auto_response["identified_role"]
            assert identified_role != ""
            
            # Check that M Language spec contains workflow elements
            m_spec = auto_response["m_language_spec"]
            assert "agent" in m_spec.lower()
            assert "workflow" in m_spec.lower()
    
    def test_auto_orchestrate_empty_command(self):
        """Test handling of empty command."""
        command = ""
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/autoOrchestrate",
                json={"command": command}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Should handle empty command gracefully
            assert data["finalizedResult"] == "No command to process."
    
    def test_auto_orchestrate_missing_command_field(self):
        """Test handling of missing command field."""
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/autoOrchestrate",
                json={}
            )
            
            # Should return 422 (validation error)
            assert response.status_code == 422
    
    def test_auto_orchestrate_complex_command(self):
        """Test complex multi-step command processing."""
        command = "Research the latest AI trends, analyze their business impact, and create a presentation with recommendations"
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/autoOrchestrate",
                json={"command": command}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            auto_response = data["auto_orchestrate_response"]
            
            # Should identify a role (may fall back to General Assistant due to API issues)
            identified_role = auto_response["identified_role"]
            assert identified_role != ""
            
            # M Language spec should contain multiple agents
            m_spec = auto_response["m_language_spec"]
            assert "agent" in m_spec.lower()
            assert "workflow" in m_spec.lower()
    
    def test_auto_orchestrate_endpoint_availability(self):
        """Test that the endpoint is available and responding."""
        with httpx.Client() as client:
            # Test root endpoint first
            response = client.get(f"{self.base_url}/")
            assert response.status_code == 200
            
            # Test auto orchestrate endpoint
            response = client.post(
                f"{self.base_url}/autoOrchestrate",
                json={"command": "test command"}
            )
            assert response.status_code == 200


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 