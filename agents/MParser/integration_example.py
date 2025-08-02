"""
Integration Example
Shows the complete flow from user command to swarm execution
"""

from agents.MParser import create_workflow_orchestrator


def run_complete_flow():
    """Run the complete workflow from user command to execution"""
    
    print("=" * 60)
    print("COMPLETE WORKFLOW INTEGRATION EXAMPLE")
    print("=" * 60)
    
    # Create orchestrator
    orchestrator = create_workflow_orchestrator()
    
    # Example user command
    user_command = "Research quantum computing applications in healthcare"
    
    print(f"User Command: {user_command}")
    print("\n" + "-" * 40)
    
    # Step 1: Generate LLM prompt
    print("Step 1: Generating LLM prompt...")
    prompt = orchestrator.generate_llm_prompt(user_command)
    print(f"✓ Generated prompt ({len(prompt)} characters)")
    
    # Step 2: Simulate LLM response (in real usage, this would be from actual LLM)
    print("\nStep 2: LLM generates M language code...")
    mock_llm_response = """
swarm healthcare_research_swarm {
    agent research_agent {
        role: "Healthcare research specialist"
        capabilities: "llm,research,analysis"
        inputs: "user_query"
        outputs: "research_results"
        config: {
            model: "gpt-4"
            temperature: 0.7
        }
    }
    
    workflow sequential {
        research_agent(input: "user_query", output: "research_results")
    }
}"""
    print("✓ LLM generated M language code")
    
    # Step 3: Validate LLM response
    print("\nStep 3: Validating M language code...")
    validation = orchestrator.validate_llm_response(mock_llm_response)
    if validation["valid"]:
        print("✓ M language code is valid")
        print(f"  - Tokens: {validation['tokens_count']}")
        print(f"  - Agents: {validation['agents_count']}")
        print(f"  - Workflow: {validation['workflow_type']}")
    else:
        print(f"✗ M language code is invalid: {validation['error']}")
        return
    
    # Step 4: Get swarm summary
    print("\nStep 4: Analyzing swarm specification...")
    summary = orchestrator.get_swarm_summary(mock_llm_response)
    print(f"✓ Swarm: {summary['name']}")
    print(f"  - Total agents: {summary['total_agents']}")
    print(f"  - Agent types: {summary['agent_types']}")
    print(f"  - Workflow type: {summary['workflow_type']}")
    print(f"  - Steps: {summary['steps_count']}")
    
    # Step 5: Execute the swarm (simulated)
    print("\nStep 5: Executing swarm...")
    try:
        result = orchestrator.m_runtime.process_llm_request(mock_llm_response, user_command)
        print("✓ Swarm execution completed")
        print(f"  - Success: {result.get('success', False)}")
        if 'execution_results' in result:
            print(f"  - Results available: {len(result['execution_results'])}")
    except Exception as e:
        print(f"✗ Swarm execution failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("INTEGRATION EXAMPLE COMPLETE")
    print("=" * 60)


def show_prompt_example():
    """Show what the LLM prompt looks like"""
    print("\n" + "=" * 60)
    print("LLM PROMPT EXAMPLE")
    print("=" * 60)
    
    orchestrator = create_workflow_orchestrator()
    user_command = "Research quantum computing applications in healthcare"
    
    prompt = orchestrator.generate_llm_prompt(user_command)
    print(prompt)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Run the complete flow
    run_complete_flow()
    
    # Show prompt example
    show_prompt_example() 