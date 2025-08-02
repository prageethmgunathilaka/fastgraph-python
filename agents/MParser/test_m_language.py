"""
Test M Language functionality
Demonstrates the complete M language pipeline
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.MParser import MRuntime
from agents.MParser.examples import run_all_examples


def test_basic_functionality():
    """Test basic M language functionality"""
    print("Testing basic M language functionality...")
    
    runtime = MRuntime()
    
    # Simple M code
    m_code = """
swarm test_swarm {
    agent test_agent {
        role: "Test agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
            temperature: 0.7
        }
    }
    
    workflow sequential {
        test_agent(input: "input", output: "output")
    }
}"""
    
    # Test parsing and compilation
    try:
        swarm_spec = runtime.parse_and_compile(m_code)
        print("✓ Parse and compile successful")
        print(f"  Swarm name: {swarm_spec['name']}")
        print(f"  Agents: {len(swarm_spec['agents'])}")
        print(f"  Workflow type: {swarm_spec['workflow']['type']}")
    except Exception as e:
        print(f"✗ Parse and compile failed: {str(e)}")
        return False
    
    # Test validation
    validation = runtime.validate_m_code(m_code)
    if validation["valid"]:
        print("✓ Validation successful")
        print(f"  Tokens: {validation['tokens_count']}")
        print(f"  Agents: {validation['agents_count']}")
    else:
        print(f"✗ Validation failed: {validation['error']}")
        return False
    
    # Test execution (mock)
    print("✓ Basic functionality test passed")
    return True


def test_workflow_types():
    """Test different workflow types"""
    print("\nTesting workflow types...")
    
    runtime = MRuntime()
    
    # Sequential workflow
    sequential_code = """
swarm sequential_test {
    agent agent1 {
        role: "First agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output1"
        config: {
            model: "gpt-4"
        }
    }
    
    agent agent2 {
        role: "Second agent"
        capabilities: "llm"
        inputs: "output1"
        outputs: "output2"
        config: {
            model: "gpt-4"
        }
    }
    
    workflow sequential {
        agent1(input: "input", output: "output1")
        agent2(input: "output1", output: "output2")
    }
}"""
    
    try:
        swarm_spec = runtime.parse_and_compile(sequential_code)
        print("✓ Sequential workflow parsed successfully")
    except Exception as e:
        print(f"✗ Sequential workflow failed: {str(e)}")
        return False
    
    # Parallel workflow
    parallel_code = """
swarm parallel_test {
    agent agent1 {
        role: "First agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output1"
        config: {
            model: "gpt-4"
        }
    }
    
    agent agent2 {
        role: "Second agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output2"
        config: {
            model: "gpt-4"
        }
    }
    
    workflow parallel {
        agent1(input: "input", output: "output1")
        agent2(input: "input", output: "output2")
    }
}"""
    
    try:
        swarm_spec = runtime.parse_and_compile(parallel_code)
        print("✓ Parallel workflow parsed successfully")
    except Exception as e:
        print(f"✗ Parallel workflow failed: {str(e)}")
        return False
    
    print("✓ Workflow types test passed")
    return True


def test_agent_types():
    """Test different agent types"""
    print("\nTesting agent types...")
    
    runtime = MRuntime()
    
    # LLM agent
    llm_code = """
swarm llm_test {
    agent llm_agent {
        role: "LLM agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
            temperature: 0.7
        }
    }
    
    workflow sequential {
        llm_agent(input: "input", output: "output")
    }
}"""
    
    try:
        swarm_spec = runtime.parse_and_compile(llm_code)
        agent_type = swarm_spec["agents"]["llm_agent"]["type"]
        print(f"✓ LLM agent type: {agent_type}")
    except Exception as e:
        print(f"✗ LLM agent failed: {str(e)}")
        return False
    
    # MCP agent
    mcp_code = """
swarm mcp_test {
    agent mcp_agent {
        role: "MCP agent"
        capabilities: "mcp,file_operations"
        inputs: "input"
        outputs: "output"
        config: {
            timeout: 300
        }
    }
    
    workflow sequential {
        mcp_agent(input: "input", output: "output")
    }
}"""
    
    try:
        swarm_spec = runtime.parse_and_compile(mcp_code)
        agent_type = swarm_spec["agents"]["mcp_agent"]["type"]
        print(f"✓ MCP agent type: {agent_type}")
    except Exception as e:
        print(f"✗ MCP agent failed: {str(e)}")
        return False
    
    # Hybrid agent
    hybrid_code = """
swarm hybrid_test {
    agent hybrid_agent {
        role: "Hybrid agent"
        capabilities: "llm,mcp"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
            temperature: 0.5
            timeout: 300
        }
    }
    
    workflow sequential {
        hybrid_agent(input: "input", output: "output")
    }
}"""
    
    try:
        swarm_spec = runtime.parse_and_compile(hybrid_code)
        agent_type = swarm_spec["agents"]["hybrid_agent"]["type"]
        print(f"✓ Hybrid agent type: {agent_type}")
    except Exception as e:
        print(f"✗ Hybrid agent failed: {str(e)}")
        return False
    
    print("✓ Agent types test passed")
    return True


def test_data_flow():
    """Test data flow mechanisms"""
    print("\nTesting data flow mechanisms...")
    
    runtime = MRuntime()
    
    # Test with transformations and filters
    data_flow_code = """
swarm data_flow_test {
    agent source_agent {
        role: "Data source"
        capabilities: "llm"
        inputs: "input"
        outputs: "raw_data"
        config: {
            model: "gpt-4"
        }
    }
    
    agent processor_agent {
        role: "Data processor"
        capabilities: "llm"
        inputs: "raw_data"
        outputs: "processed_data"
        config: {
            model: "gpt-4"
        }
    }
    
    workflow sequential {
        source_agent(input: "input", output: "raw_data", transform: "to_string")
        processor_agent(input: "raw_data", output: "processed_data", filter: "non_empty", error: "retry")
    }
}"""
    
    try:
        swarm_spec = runtime.parse_and_compile(data_flow_code)
        print("✓ Data flow mechanisms parsed successfully")
        
        # Check workflow steps
        steps = swarm_spec["workflow"]["steps"]
        for i, step in enumerate(steps):
            print(f"  Step {i+1}: {step['agent']}")
            if step.get("transform"):
                print(f"    Transform: {step['transform']}")
            if step.get("filter"):
                print(f"    Filter: {step['filter']}")
            if step.get("error_handler"):
                print(f"    Error handler: {step['error_handler']}")
    except Exception as e:
        print(f"✗ Data flow test failed: {str(e)}")
        return False
    
    print("✓ Data flow test passed")
    return True


def test_template_generation():
    """Test template generation"""
    print("\nTesting template generation...")
    
    runtime = MRuntime()
    
    # Generate template
    template = runtime.generate_m_code_template("Research task")
    
    if template and "swarm" in template and "agent" in template:
        print("✓ Template generation successful")
        print(f"  Template length: {len(template)} characters")
    else:
        print("✗ Template generation failed")
        return False
    
    # Validate generated template
    validation = runtime.validate_m_code(template)
    if validation["valid"]:
        print("✓ Generated template is valid")
    else:
        print(f"✗ Generated template is invalid: {validation['error']}")
        return False
    
    print("✓ Template generation test passed")
    return True


def test_error_handling():
    """Test error handling"""
    print("\nTesting error handling...")
    
    runtime = MRuntime()
    
    # Invalid M code
    invalid_code = """
swarm invalid_swarm {
    agent invalid_agent {
        role: "Invalid agent"
        // Missing required fields
    }
}
"""
    
    # Test validation
    validation = runtime.validate_m_code(invalid_code)
    if not validation["valid"]:
        print("✓ Invalid code correctly rejected")
    else:
        print("✗ Invalid code incorrectly accepted")
        return False
    
    # Test parsing error
    try:
        runtime.parse_and_compile(invalid_code)
        print("✗ Invalid code parsing should have failed")
        return False
    except Exception as e:
        print("✓ Invalid code parsing correctly failed")
        print(f"  Error: {str(e)}")
    
    print("✓ Error handling test passed")
    return True


def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("=" * 60)
    print("M LANGUAGE COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Workflow Types", test_workflow_types),
        ("Agent Types", test_agent_types),
        ("Data Flow", test_data_flow),
        ("Template Generation", test_template_generation),
        ("Error Handling", test_error_handling)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {str(e)}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")
    
    return passed == total


if __name__ == "__main__":
    # Run comprehensive test
    success = run_comprehensive_test()
    
    if success:
        print("\n" + "=" * 60)
        print("RUNNING EXAMPLE SWARMS")
        print("=" * 60)
        
        # Run examples
        try:
            results = run_all_examples()
            print("✓ Examples completed")
        except Exception as e:
            print(f"✗ Examples failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("M LANGUAGE TEST COMPLETE")
    print("=" * 60) 