"""
Manual Test Script
Quick manual testing of M Language components
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.MParser import (
    MLexer, MParser, MCompiler, MRuntime,
    create_workflow_orchestrator, create_swarm_executor
)


def test_lexer():
    """Test the lexer"""
    print("Testing Lexer...")
    
    lexer = MLexer()
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
    
    try:
        tokens = lexer.tokenize(m_code)
        print(f"✓ Lexer: Generated {len(tokens)} tokens")
        
        # Show some tokens
        token_types = [token.type.value for token in tokens[:10]]
        print(f"  First 10 token types: {token_types}")
        
        return True
    except Exception as e:
        print(f"✗ Lexer failed: {str(e)}")
        return False


def test_parser():
    """Test the parser"""
    print("\nTesting Parser...")
    
    lexer = MLexer()
    parser = MParser()
    
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
    
    try:
        tokens = lexer.tokenize(m_code)
        ast = parser.parse(tokens)
        
        print(f"✓ Parser: Parsed swarm '{ast.name}'")
        print(f"  Agents: {len(ast.agents)}")
        print(f"  Workflow type: {ast.workflow.type}")
        print(f"  Steps: {len(ast.workflow.steps)}")
        
        return True
    except Exception as e:
        print(f"✗ Parser failed: {str(e)}")
        return False


def test_compiler():
    """Test the compiler"""
    print("\nTesting Compiler...")
    
    lexer = MLexer()
    parser = MParser()
    compiler = MCompiler()
    
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
    
    try:
        tokens = lexer.tokenize(m_code)
        ast = parser.parse(tokens)
        swarm_spec = compiler.compile(ast)
        
        print(f"✓ Compiler: Compiled swarm '{swarm_spec['name']}'")
        print(f"  Agents: {len(swarm_spec['agents'])}")
        print(f"  Workflow type: {swarm_spec['workflow']['type']}")
        print(f"  Steps: {len(swarm_spec['workflow']['steps'])}")
        
        return True
    except Exception as e:
        print(f"✗ Compiler failed: {str(e)}")
        return False


def test_runtime():
    """Test the runtime"""
    print("\nTesting Runtime...")
    
    runtime = MRuntime()
    
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
    
    try:
        # Test validation
        validation = runtime.validate_m_code(m_code)
        print(f"✓ Runtime: Validation {'passed' if validation['valid'] else 'failed'}")
        print(f"  Tokens: {validation['tokens_count']}")
        print(f"  Agents: {validation['agents_count']}")
        
        # Test template generation
        template = runtime.generate_m_code_template("Test task")
        print(f"✓ Runtime: Generated template ({len(template)} chars)")
        
        return True
    except Exception as e:
        print(f"✗ Runtime failed: {str(e)}")
        return False


def test_orchestrator():
    """Test the orchestrator"""
    print("\nTesting Orchestrator...")
    
    orchestrator = create_workflow_orchestrator()
    
    try:
        # Test prompt generation
        user_command = "Research quantum computing"
        prompt = orchestrator.generate_llm_prompt(user_command)
        print(f"✓ Orchestrator: Generated prompt ({len(prompt)} chars)")
        
        # Test with mock LLM response
        mock_response = """
swarm research_swarm {
    agent research_agent {
        role: "Research specialist"
        capabilities: "llm,research"
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
        
        # Test validation
        validation = orchestrator.validate_llm_response(mock_response)
        print(f"✓ Orchestrator: LLM response validation {'passed' if validation['valid'] else 'failed'}")
        
        # Test summary
        summary = orchestrator.get_swarm_summary(mock_response)
        print(f"✓ Orchestrator: Swarm summary generated")
        print(f"  Swarm: {summary['name']}")
        print(f"  Agents: {summary['total_agents']}")
        
        return True
    except Exception as e:
        print(f"✗ Orchestrator failed: {str(e)}")
        return False


def test_executor():
    """Test the executor"""
    print("\nTesting Executor...")
    
    executor = create_swarm_executor()
    
    # Mock swarm specification
    swarm_spec = {
        "name": "test_swarm",
        "agents": {
            "test_agent": {
                "name": "test_agent",
                "role": "Test agent",
                "capabilities": ["llm"],
                "inputs": ["input"],
                "outputs": ["output"],
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
                    "agent": "test_agent",
                    "inputs": ["input"],
                    "outputs": ["output"]
                }
            ]
        }
    }
    
    initial_data = {"input": "Test input"}
    
    try:
        # Mock the LLM agent execution
        from unittest.mock import patch
        with patch('agents.regular_agent.run_agent') as mock_run_agent:
            mock_run_agent.return_value = "Test result"
            
            result = executor.execute_swarm(swarm_spec, initial_data)
            
            print(f"✓ Executor: Swarm execution {'succeeded' if result['success'] else 'failed'}")
            print(f"  Workflow type: {result['workflow_type']}")
            print(f"  Steps completed: {len(result['results'])}")
            
            return True
    except Exception as e:
        print(f"✗ Executor failed: {str(e)}")
        return False


def run_manual_tests():
    """Run all manual tests"""
    print("=" * 60)
    print("MANUAL TESTING M LANGUAGE SYSTEM")
    print("=" * 60)
    
    tests = [
        ("Lexer", test_lexer),
        ("Parser", test_parser),
        ("Compiler", test_compiler),
        ("Runtime", test_runtime),
        ("Orchestrator", test_orchestrator),
        ("Executor", test_executor)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {str(e)}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "=" * 60)
    print("MANUAL TEST SUMMARY")
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
        print("🎉 All manual tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")
    
    return passed == total


if __name__ == "__main__":
    # Run manual tests
    success = run_manual_tests()
    
    if success:
        print("\n✅ M Language system is ready for use!")
    else:
        print("\n❌ Please fix failing tests before using the system.")
    
    print("\n" + "=" * 60) 