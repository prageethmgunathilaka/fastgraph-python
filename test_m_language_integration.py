"""
Integration Test for M Language with FastAPI
Tests M Language functionality with the main application
"""

import sys
import os
import requests
import json
import time
from typing import Dict, Any

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_m_language_components():
    """Test individual M Language components"""
    print("Testing M Language Components...")
    
    try:
        from agents.MParser import MLexer, MParser, MCompiler, MRuntime
        
        # Test Lexer
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
        
        tokens = lexer.tokenize(m_code)
        print(f"✓ Lexer: Generated {len(tokens)} tokens")
        
        # Test Parser
        parser = MParser()
        ast = parser.parse(tokens)
        print(f"✓ Parser: Parsed swarm '{ast.name}' with {len(ast.agents)} agents")
        
        # Test Compiler
        compiler = MCompiler()
        swarm_spec = compiler.compile(ast)
        print(f"✓ Compiler: Compiled swarm specification")
        
        # Test Runtime
        runtime = MRuntime()
        validation = runtime.validate_m_code(m_code)
        print(f"✓ Runtime: Validation successful - {validation['agents_count']} agents")
        
        return True
        
    except Exception as e:
        print(f"✗ Component test failed: {str(e)}")
        return False

def test_m_language_with_api():
    """Test M Language integration with the FastAPI application"""
    print("\nTesting M Language with FastAPI API...")
    
    base_url = "http://localhost:8000"
    
    # Test if the server is running
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code != 200:
            print("✗ Server not responding properly")
            return False
        print("✓ Server is running")
    except requests.exceptions.RequestException:
        print("✗ Server not running. Please start the server with: python main.py")
        return False
    
    # Test basic ask endpoint
    try:
        ask_data = {"text": "What is 2 + 2?"}
        response = requests.post(f"{base_url}/ask", json=ask_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Ask endpoint working")
            print(f"  Response: {result.get('agent_response', 'No response')[:100]}...")
        else:
            print(f"✗ Ask endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Ask endpoint test failed: {str(e)}")
        return False
    
    # Test workflow endpoint
    try:
        workflow_data = {
            "commands": [
                "What is the capital of France?",
                "Calculate 15 + 27",
                "Translate hello to Spanish"
            ]
        }
        response = requests.post(f"{base_url}/workflowask", json=workflow_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Workflow endpoint working")
            print(f"  Finalized result: {result.get('finalizedResult', 'No result')[:100]}...")
        else:
            print(f"✗ Workflow endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Workflow endpoint test failed: {str(e)}")
        return False
    
    # Test orchestrate endpoint
    try:
        orchestrate_data = {
            "tasks": [
                ["Hello, how are you?", "What is the weather like?"],
                ["Explain quantum computing"],
                ["Write a poem", "Translate it to Spanish"]
            ]
        }
        response = requests.post(f"{base_url}/orchestrate", json=orchestrate_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Orchestrate endpoint working")
            print(f"  Finalized result: {result.get('finalizedResult', 'No result')[:100]}...")
        else:
            print(f"✗ Orchestrate endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Orchestrate endpoint test failed: {str(e)}")
        return False
    
    return True

def test_m_language_code_generation():
    """Test M Language code generation and validation"""
    print("\nTesting M Language Code Generation...")
    
    try:
        from agents.MParser import MRuntime
        
        runtime = MRuntime()
        
        # Test template generation
        template = runtime.generate_m_code_template("Research task")
        print("✓ Template generation working")
        print(f"  Template length: {len(template)} characters")
        
        # Test validation of generated template
        validation = runtime.validate_m_code(template)
        if validation["valid"]:
            print("✓ Generated template is valid")
            print(f"  Agents: {validation['agents_count']}")
            print(f"  Tokens: {validation['tokens_count']}")
        else:
            print(f"✗ Generated template is invalid: {validation['error']}")
            return False
        
        # Test custom M code
        custom_m_code = """
swarm research_swarm {
    agent research_agent {
        role: "Research and analysis specialist"
        capabilities: "llm,research,analysis"
        inputs: "user_query,context"
        outputs: "research_results,insights"
        config: {
            model: "gpt-4"
            temperature: 0.7
        }
    }
    
    workflow sequential {
        research_agent(input: "user_query", output: "research_results")
    }
}"""
        
        validation = runtime.validate_m_code(custom_m_code)
        if validation["valid"]:
            print("✓ Custom M code validation successful")
        else:
            print(f"✗ Custom M code validation failed: {validation['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ M Language code generation test failed: {str(e)}")
        return False

def test_m_language_execution():
    """Test M Language execution capabilities"""
    print("\nTesting M Language Execution...")
    
    try:
        from agents.MParser import MRuntime
        
        runtime = MRuntime()
        
        # Test execution with mock data
        m_code = """
swarm simple_swarm {
    agent simple_agent {
        role: "Simple test agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
            temperature: 0.7
        }
    }
    
    workflow sequential {
        simple_agent(input: "input", output: "output")
    }
}"""
        
        # Test parse and compile
        swarm_spec = runtime.parse_and_compile(m_code)
        print("✓ Parse and compile successful")
        print(f"  Swarm name: {swarm_spec['name']}")
        print(f"  Agents: {len(swarm_spec['agents'])}")
        
        # Test swarm summary
        summary = runtime.get_swarm_summary(swarm_spec)
        print("✓ Swarm summary generation successful")
        print(f"  Summary: {summary['description'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ M Language execution test failed: {str(e)}")
        return False

def run_all_m_language_tests():
    """Run all M Language tests"""
    print("=" * 60)
    print("M LANGUAGE INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Component Tests", test_m_language_components),
        ("API Integration", test_m_language_with_api),
        ("Code Generation", test_m_language_code_generation),
        ("Execution Tests", test_m_language_execution)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} ERROR: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All M Language tests passed!")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    run_all_m_language_tests() 