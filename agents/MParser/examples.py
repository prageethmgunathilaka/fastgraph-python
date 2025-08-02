"""
M Language Examples
Simple example demonstrating M language usage
"""

from .m_runtime import MRuntime

# Initialize runtime
runtime = MRuntime()


def example_simple_research_swarm():
    """Simple research swarm with LLM agent"""
    m_code = """
swarm research_swarm {
    agent research_agent {
        role: "Research and analysis specialist"
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
    
    return runtime.execute_m_code(m_code, {"user_query": "What is quantum computing?"})


def run_example():
    """Run the simple example"""
    print("Running simple research swarm example...")
    try:
        result = example_simple_research_swarm()
        print("✓ Example completed successfully")
        return result
    except Exception as e:
        print(f"✗ Example failed: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Run the example
    result = run_example()
    
    # Print summary
    print("\n" + "="*50)
    print("EXAMPLE EXECUTION SUMMARY")
    print("="*50)
    
    success = result.get("success", False)
    status = "✓ SUCCESS" if success else "✗ FAILED"
    print(f"Simple Research Swarm: {status}")
    
    if not success and "error" in result:
        print(f"  Error: {result['error']}")
    
    print("\n" + "="*50) 