"""
Execution Example
Shows exactly how the workflow agent executes the parsed swarm
"""

from agents.MParser import create_swarm_executor


def demonstrate_swarm_execution():
    """Demonstrate how to execute a parsed swarm"""
    
    print("=" * 60)
    print("SWARM EXECUTION DEMONSTRATION")
    print("=" * 60)
    
    # Create swarm executor
    executor = create_swarm_executor()
    
    # Example: Parsed swarm specification (this would come from LLM response)
    parsed_swarm = {
        "name": "healthcare_research_swarm",
        "agents": {
            "research_agent": {
                "name": "research_agent",
                "role": "Healthcare research specialist",
                "capabilities": ["llm", "research", "analysis"],
                "inputs": ["user_query"],
                "outputs": ["research_results"],
                "config": {
                    "model": "gpt-4",
                    "temperature": 0.7
                },
                "type": "llm"
            }
        },
        "workflow": {
            "type": "sequential",
            "steps": [
                {
                    "agent": "research_agent",
                    "inputs": ["user_query"],
                    "outputs": ["research_results"]
                }
            ]
        }
    }
    
    print("Parsed Swarm Specification:")
    print(f"  Name: {parsed_swarm['name']}")
    print(f"  Agents: {len(parsed_swarm['agents'])}")
    print(f"  Workflow Type: {parsed_swarm['workflow']['type']}")
    print(f"  Steps: {len(parsed_swarm['workflow']['steps'])}")
    
    # Initial data (user's original command)
    initial_data = {
        "user_query": "Research quantum computing applications in healthcare"
    }
    
    print(f"\nInitial Data: {initial_data}")
    print("\n" + "-" * 40)
    
    # Execute the swarm
    print("Executing swarm...")
    result = executor.execute_swarm(parsed_swarm, initial_data)
    
    # Display results
    print("\nExecution Results:")
    print("=" * 40)
    print(f"Success: {result['success']}")
    print(f"Workflow Type: {result['workflow_type']}")
    print(f"Steps Completed: {len(result['results'])}")
    
    if result['success']:
        print("\nStep Results:")
        for agent_name, step_result in result['results'].items():
            status = "✓ SUCCESS" if step_result['success'] else "✗ FAILED"
            print(f"  {agent_name}: {status}")
            
            if step_result['success']:
                print(f"    Outputs: {list(step_result['outputs'].keys())}")
            else:
                print(f"    Error: {step_result['error']}")
        
        print(f"\nFinal Data: {list(result['final_data'].keys())}")
    else:
        print(f"Execution failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)


def show_execution_steps():
    """Show the detailed execution steps"""
    
    print("\n" + "=" * 60)
    print("DETAILED EXECUTION STEPS")
    print("=" * 60)
    
    print("""
1. WORKFLOW AGENT RECEIVES USER COMMAND
   User: "Research quantum computing applications in healthcare"
   
2. WORKFLOW AGENT SENDS PROMPT TO LLM
   - Generates specific prompt asking for M language code
   - Sends to LLM with syntax examples and capabilities
   
3. LLM RESPONDS WITH M LANGUAGE CODE
   ```m
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
   }
   ```
   
4. WORKFLOW AGENT PARSES M LANGUAGE
   - Tokenizes the code
   - Builds Abstract Syntax Tree (AST)
   - Compiles to executable specification
   
5. WORKFLOW AGENT EXECUTES SWARM
   - Extracts agents and workflow information
   - Prepares initial data
   - Executes based on workflow type (sequential/parallel/etc.)
   
6. AGENT EXECUTION
   - For each step in workflow:
     a. Prepare inputs from current data
     b. Execute agent (LLM/MCP/Hybrid)
     c. Process outputs and transformations
     d. Update data for next step
   
7. RETURN RESULTS TO USER
   - Compile final results
   - Return success/failure status
   - Provide execution details
""")
    
    print("=" * 60)


if __name__ == "__main__":
    # Demonstrate execution
    demonstrate_swarm_execution()
    
    # Show detailed steps
    show_execution_steps() 