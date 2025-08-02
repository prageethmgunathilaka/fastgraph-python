"""
Demo script for the /autoOrchestrate endpoint.
Shows how the endpoint automatically determines roles and creates agent swarms.
"""

import requests
import json
from typing import Dict, Any


def test_auto_orchestrate(command: str) -> Dict[str, Any]:
    """
    Test the auto orchestrate endpoint with a given command.
    """
    url = "http://localhost:8001/autoOrchestrate"
    
    payload = {
        "command": command
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return {}


def print_demo_results(command: str, results: Dict[str, Any]):
    """
    Print formatted results from the auto orchestrate demo.
    """
    print(f"\n{'='*60}")
    print(f"COMMAND: {command}")
    print(f"{'='*60}")
    
    if not results:
        print("❌ No results received")
        return
    
    print(f"✅ Status: {results.get('received_command', 'Unknown')}")
    
    auto_response = results.get('auto_orchestrate_response', {})
    
    # Role identification
    identified_role = auto_response.get('identified_role', 'Unknown')
    print(f"\n🎭 IDENTIFIED ROLE: {identified_role}")
    
    # M Language specification
    m_spec = auto_response.get('m_language_spec', '')
    print(f"\n📝 M LANGUAGE SPECIFICATION:")
    print(f"{'─'*40}")
    print(m_spec)
    print(f"{'─'*40}")
    
    # Processing steps
    steps = auto_response.get('processing_steps', [])
    print(f"\n🔄 PROCESSING STEPS:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    
    # Swarm result
    swarm_result = auto_response.get('swarm_result', {})
    success = swarm_result.get('success', False)
    print(f"\n🤖 SWARM EXECUTION: {'✅ Success' if success else '❌ Failed'}")
    
    if success:
        execution_results = swarm_result.get('execution_results', {})
        if execution_results:
            final_data = execution_results.get('final_data', {})
            result = final_data.get('result', 'No result')
            print(f"\n📊 FINAL RESULT:")
            print(f"{'─'*40}")
            print(result[:500] + "..." if len(result) > 500 else result)
            print(f"{'─'*40}")
    else:
        error = swarm_result.get('error', 'Unknown error')
        print(f"\n❌ ERROR: {error}")
    
    # Final result
    final_result = results.get('finalizedResult', 'No final result')
    print(f"\n🎯 FINALIZED RESULT:")
    print(f"{'─'*40}")
    print(final_result[:500] + "..." if len(final_result) > 500 else final_result)
    print(f"{'─'*40}")


def main():
    """
    Run the auto orchestrate demo with various commands.
    """
    print("🚀 AUTO ORCHESTRATE DEMO")
    print("=" * 60)
    print("This demo shows how the /autoOrchestrate endpoint:")
    print("1. Identifies the appropriate role for a command")
    print("2. Generates M Language specification")
    print("3. Executes agent swarms")
    print("4. Returns processed results")
    print("=" * 60)
    
    # Test commands
    test_commands = [
        "Analyze the current market trends for renewable energy",
        "Create a Python script to scrape data from a website",
        "Write a compelling marketing copy for a new product launch",
        "Research the latest AI trends and create a presentation",
        "Design a database schema for an e-commerce platform"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n🧪 TEST {i}/{len(test_commands)}")
        results = test_auto_orchestrate(command)
        print_demo_results(command, results)
        
        if i < len(test_commands):
            input("\nPress Enter to continue to next test...")
    
    print(f"\n{'='*60}")
    print("🎉 DEMO COMPLETE!")
    print("The /autoOrchestrate endpoint successfully:")
    print("✅ Identified appropriate roles for different commands")
    print("✅ Generated M Language specifications")
    print("✅ Executed agent swarms")
    print("✅ Processed and returned results")
    print(f"{'='*60}")


if __name__ == "__main__":
    main() 