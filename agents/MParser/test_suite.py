"""
Comprehensive Test Suite for M Language System
Tests all components and complete flow
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.MParser import (
    MLexer, MParser, MCompiler, MRuntime, 
    create_workflow_orchestrator, create_swarm_executor
)


class TestMLexer(unittest.TestCase):
    """Test the M Language Lexer"""
    
    def setUp(self):
        self.lexer = MLexer()
    
    def test_basic_tokens(self):
        """Test basic token recognition"""
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
        
        tokens = self.lexer.tokenize(m_code)
        
        # Check that we have tokens
        self.assertGreater(len(tokens), 0)
        
        # Check for specific tokens
        token_types = [token.type.value for token in tokens]
        self.assertIn("SWARM", token_types)
        self.assertIn("AGENT", token_types)
        self.assertIn("WORKFLOW", token_types)
        self.assertIn("IDENTIFIER", token_types)
    
    def test_string_literals(self):
        """Test string literal parsing"""
        m_code = 'role: "Test agent"'
        tokens = self.lexer.tokenize(m_code)
        
        string_tokens = [t for t in tokens if t.type.value == "STRING"]
        self.assertGreater(len(string_tokens), 0)
        self.assertEqual(string_tokens[0].value, '"Test agent"')
    
    def test_numbers(self):
        """Test number parsing"""
        m_code = 'temperature: 0.7'
        tokens = self.lexer.tokenize(m_code)
        
        number_tokens = [t for t in tokens if t.type.value == "NUMBER"]
        self.assertGreater(len(number_tokens), 0)
        self.assertEqual(number_tokens[0].value, "0.7")


class TestMParser(unittest.TestCase):
    """Test the M Language Parser"""
    
    def setUp(self):
        self.parser = MParser()
        self.lexer = MLexer()
    
    def test_parse_simple_swarm(self):
        """Test parsing a simple swarm"""
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
        
        tokens = self.lexer.tokenize(m_code)
        ast = self.parser.parse(tokens)
        
        # Check AST structure
        self.assertEqual(ast.name, "test_swarm")
        self.assertEqual(len(ast.agents), 1)
        self.assertEqual(ast.workflow.type, "sequential")
        self.assertEqual(len(ast.workflow.steps), 1)
    
    def test_parse_agent_definition(self):
        """Test parsing agent definitions"""
        m_code = """
swarm test {
    agent research_agent {
        role: "Research specialist"
        capabilities: "llm,research"
        inputs: "query"
        outputs: "results"
        config: {
            model: "gpt-4"
            temperature: 0.5
        }
    }
    
    workflow sequential {
        research_agent(input: "query", output: "results")
    }
}"""
        
        tokens = self.lexer.tokenize(m_code)
        ast = self.parser.parse(tokens)
        
        agent = ast.agents[0]
        self.assertEqual(agent.name, "research_agent")
        self.assertEqual(agent.role, "Research specialist")
        self.assertIn("llm", agent.capabilities)
        self.assertIn("research", agent.capabilities)


class TestMCompiler(unittest.TestCase):
    """Test the M Language Compiler"""
    
    def setUp(self):
        self.compiler = MCompiler()
        self.parser = MParser()
        self.lexer = MLexer()
    
    def test_compile_simple_swarm(self):
        """Test compiling a simple swarm"""
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
        
        tokens = self.lexer.tokenize(m_code)
        ast = self.parser.parse(tokens)
        swarm_spec = self.compiler.compile(ast)
        
        # Check compiled specification
        self.assertEqual(swarm_spec["name"], "test_swarm")
        self.assertIn("test_agent", swarm_spec["agents"])
        self.assertEqual(swarm_spec["workflow"]["type"], "sequential")
        self.assertEqual(len(swarm_spec["workflow"]["steps"]), 1)
    
    def test_agent_type_detection(self):
        """Test agent type detection"""
        m_code = """
swarm test {
    agent llm_agent {
        role: "LLM agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
        }
    }
    
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
        llm_agent(input: "input", output: "output")
        mcp_agent(input: "input", output: "output")
    }
}"""
        
        tokens = self.lexer.tokenize(m_code)
        ast = self.parser.parse(tokens)
        swarm_spec = self.compiler.compile(ast)
        
        agents = swarm_spec["agents"]
        self.assertEqual(agents["llm_agent"]["type"], "llm")
        self.assertEqual(agents["mcp_agent"]["type"], "mcp")


class TestMRuntime(unittest.TestCase):
    """Test the M Language Runtime"""
    
    def setUp(self):
        self.runtime = MRuntime()
    
    def test_validate_m_code(self):
        """Test M code validation"""
        valid_code = """
swarm test {
    agent test_agent {
        role: "Test agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
        }
    }
    
    workflow sequential {
        test_agent(input: "input", output: "output")
    }
}"""
        
        validation = self.runtime.validate_m_code(valid_code)
        self.assertTrue(validation["valid"])
        self.assertGreater(validation["tokens_count"], 0)
        self.assertEqual(validation["agents_count"], 1)
    
    def test_validate_invalid_code(self):
        """Test invalid M code validation"""
        invalid_code = """
swarm test {
    agent test_agent {
        role: "Test agent"
        // Missing required fields
    }
}"""
        
        validation = self.runtime.validate_m_code(invalid_code)
        self.assertFalse(validation["valid"])
        self.assertIn("error", validation)
    
    def test_generate_template(self):
        """Test template generation"""
        template = self.runtime.generate_m_code_template("Research task")
        
        self.assertIn("swarm", template)
        self.assertIn("agent", template)
        self.assertIn("workflow", template)
        self.assertIn("Research task", template.lower())


class TestWorkflowOrchestrator(unittest.TestCase):
    """Test the Workflow Orchestrator"""
    
    def setUp(self):
        self.orchestrator = create_workflow_orchestrator()
    
    def test_generate_llm_prompt(self):
        """Test LLM prompt generation"""
        user_command = "Research quantum computing"
        prompt = self.orchestrator.generate_llm_prompt(user_command)
        
        self.assertIn("USER REQUEST", prompt)
        self.assertIn("Research quantum computing", prompt)
        self.assertIn("M LANGUAGE SYNTAX", prompt)
        self.assertIn("swarm", prompt)
        self.assertIn("agent", prompt)
    
    def test_validate_llm_response(self):
        """Test LLM response validation"""
        valid_response = """
swarm test {
    agent test_agent {
        role: "Test agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
        }
    }
    
    workflow sequential {
        test_agent(input: "input", output: "output")
    }
}"""
        
        validation = self.orchestrator.validate_llm_response(valid_response)
        self.assertTrue(validation["valid"])
    
    def test_get_swarm_summary(self):
        """Test swarm summary generation"""
        llm_response = """
swarm research_swarm {
    agent research_agent {
        role: "Research specialist"
        capabilities: "llm,research"
        inputs: "query"
        outputs: "results"
        config: {
            model: "gpt-4"
        }
    }
    
    workflow sequential {
        research_agent(input: "query", output: "results")
    }
}"""
        
        summary = self.orchestrator.get_swarm_summary(llm_response)
        
        self.assertEqual(summary["name"], "research_swarm")
        self.assertEqual(summary["total_agents"], 1)
        self.assertEqual(summary["workflow_type"], "sequential")
        self.assertEqual(summary["steps_count"], 1)


class TestSwarmExecutor(unittest.TestCase):
    """Test the Swarm Executor"""
    
    def setUp(self):
        self.executor = create_swarm_executor()
    
    def test_execute_simple_swarm(self):
        """Test executing a simple swarm"""
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
        
        # Mock the LLM agent execution
        with patch('agents.regular_agent.run_agent') as mock_run_agent:
            mock_run_agent.return_value = "Test result"
            
            result = self.executor.execute_swarm(swarm_spec, initial_data)
            
            self.assertTrue(result["success"])
            self.assertEqual(result["workflow_type"], "sequential")
            self.assertIn("test_agent", result["results"])
            self.assertTrue(result["results"]["test_agent"]["success"])
    
    def test_execute_parallel_workflow(self):
        """Test executing parallel workflow"""
        swarm_spec = {
            "name": "parallel_swarm",
            "agents": {
                "agent1": {
                    "name": "agent1",
                    "role": "Agent 1",
                    "capabilities": ["llm"],
                    "inputs": ["input"],
                    "outputs": ["output1"],
                    "config": {"model": "gpt-4"},
                    "type": "llm"
                },
                "agent2": {
                    "name": "agent2",
                    "role": "Agent 2",
                    "capabilities": ["llm"],
                    "inputs": ["input"],
                    "outputs": ["output2"],
                    "config": {"model": "gpt-4"},
                    "type": "llm"
                }
            },
            "workflow": {
                "type": "parallel",
                "steps": [
                    {
                        "agent": "agent1",
                        "inputs": ["input"],
                        "outputs": ["output1"]
                    },
                    {
                        "agent": "agent2",
                        "inputs": ["input"],
                        "outputs": ["output2"]
                    }
                ]
            }
        }
        
        initial_data = {"input": "Test input"}
        
        # Mock the LLM agent execution
        with patch('agents.regular_agent.run_agent') as mock_run_agent:
            mock_run_agent.return_value = "Test result"
            
            result = self.executor.execute_swarm(swarm_spec, initial_data)
            
            self.assertTrue(result["success"])
            self.assertEqual(result["workflow_type"], "parallel")
            self.assertEqual(len(result["results"]), 2)


class TestIntegration(unittest.TestCase):
    """Test complete integration flow"""
    
    def setUp(self):
        self.orchestrator = create_workflow_orchestrator()
        self.executor = create_swarm_executor()
    
    def test_complete_flow(self):
        """Test the complete flow from user command to execution"""
        user_command = "Research quantum computing"
        
        # Step 1: Generate LLM prompt
        prompt = self.orchestrator.generate_llm_prompt(user_command)
        self.assertIn("USER REQUEST", prompt)
        
        # Step 2: Mock LLM response
        mock_llm_response = """
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
        
        # Step 3: Validate LLM response
        validation = self.orchestrator.validate_llm_response(mock_llm_response)
        self.assertTrue(validation["valid"])
        
        # Step 4: Get swarm summary
        summary = self.orchestrator.get_swarm_summary(mock_llm_response)
        self.assertEqual(summary["name"], "research_swarm")
        
        # Step 5: Execute swarm (with mocked LLM agent)
        with patch('agents.regular_agent.run_agent') as mock_run_agent:
            mock_run_agent.return_value = "Quantum computing research results"
            
            result = self.orchestrator.m_runtime.process_llm_request(mock_llm_response, user_command)
            
            self.assertTrue(result["success"])
            self.assertIn("execution_results", result)


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("RUNNING M LANGUAGE TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestMLexer,
        TestMParser,
        TestMCompiler,
        TestMRuntime,
        TestWorkflowOrchestrator,
        TestSwarmExecutor,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    status = "✓ ALL TESTS PASSED" if success else "✗ SOME TESTS FAILED"
    print(f"\nOverall: {status}")
    
    return success


if __name__ == "__main__":
    # Run all tests
    success = run_all_tests()
    
    if success:
        print("\n🎉 M Language system is ready for use!")
    else:
        print("\n⚠️  Please fix failing tests before using the system.")
    
    print("\n" + "=" * 60) 