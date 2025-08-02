"""
Workflow Orchestrator
Handles LLM prompting and M language execution
"""

import logging
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from config import Config
from .m_runtime import MRuntime

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Orchestrates the workflow from user command to swarm execution"""
    
    def __init__(self):
        self.m_runtime = MRuntime()
        self.llm = self._create_llm()
    
    def _create_llm(self):
        """Create LLM instance"""
        Config.validate()
        return ChatOpenAI(
            model=Config.DEFAULT_LLM_MODEL,
            temperature=Config.LLM_TEMPERATURE,
            api_key=Config.OPENAI_API_KEY
        )
    
    def generate_llm_prompt(self, user_command: str) -> str:
        """Generate the prompt to send to LLM"""
        return f"""You are an expert agent swarm architect. Your task is to analyze a user request and create a detailed agent swarm specification using the M language.

USER REQUEST: "{user_command}"

Please create an M language specification that defines:
1. The agents needed to complete this task
2. Their roles and capabilities (LLM, MCP, or hybrid)
3. The workflow execution pattern (sequential, parallel, conditional, or loop)
4. Data flow between agents
5. Configuration for each agent

M LANGUAGE SYNTAX:
```m
swarm swarm_name {{
    agent agent_name {{
        role: "Agent role description"
        capabilities: "llm,mcp,research,analysis"
        inputs: "input1,input2"
        outputs: "output1,output2"
        config: {{
            model: "gpt-4"
            temperature: 0.7
            timeout: 300
        }}
    }}
    
    workflow sequential|parallel|conditional|loop {{
        agent_name(input: "input_data", output: "output_data")
    }}
}}
```

AVAILABLE CAPABILITIES:
- LLM: gpt-4, gpt-3.5-turbo, claude-3, etc.
- MCP: file_operations, web_search, code_analysis, terminal_commands
- Hybrid: Combine LLM reasoning with MCP tools

WORKFLOW TYPES:
- sequential: Execute steps in order
- parallel: Execute steps concurrently
- conditional: Execute based on conditions
- loop: Execute repeatedly

Please respond ONLY with valid M language code that the workflow agent can parse and execute. Do not include any explanations or markdown formatting."""
    
    def process_user_command(self, user_command: str) -> Dict[str, Any]:
        """
        Process user command through the complete workflow
        
        Args:
            user_command: User's original command
            
        Returns:
            Complete execution results
        """
        try:
            logger.info(f"Processing user command: {user_command}")
            
            # Step 1: Generate LLM prompt
            prompt = self.generate_llm_prompt(user_command)
            logger.debug("Generated LLM prompt")
            
            # Step 2: Get LLM response
            llm_response = self._get_llm_response(prompt)
            logger.info("Received LLM response")
            
            # Step 3: Parse and execute M language
            result = self.m_runtime.process_llm_request(llm_response, user_command)
            logger.info("Executed M language swarm")
            
            return {
                "success": True,
                "user_command": user_command,
                "llm_response": llm_response,
                "execution_result": result
            }
            
        except Exception as e:
            logger.error(f"Workflow orchestration failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "user_command": user_command
            }
    
    def _get_llm_response(self, prompt: str) -> str:
        """Get response from LLM"""
        try:
            response = self.llm.invoke(prompt)
            
            # Extract content from response
            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, str):
                return response
            else:
                return str(response)
                
        except Exception as e:
            logger.error(f"LLM request failed: {str(e)}")
            raise
    
    def validate_llm_response(self, llm_response: str) -> Dict[str, Any]:
        """Validate LLM response as M language code"""
        return self.m_runtime.validate_m_code(llm_response)
    
    def get_swarm_summary(self, llm_response: str) -> Dict[str, Any]:
        """Get summary of the swarm specified by LLM"""
        try:
            swarm_spec = self.m_runtime.parse_and_compile(llm_response)
            return self.m_runtime.get_swarm_summary(swarm_spec)
        except Exception as e:
            return {"error": str(e)}


def create_workflow_orchestrator() -> WorkflowOrchestrator:
    """Create a workflow orchestrator instance"""
    return WorkflowOrchestrator()


# Example usage
if __name__ == "__main__":
    orchestrator = create_workflow_orchestrator()
    
    # Test with a simple command
    user_command = "Research quantum computing applications in healthcare"
    
    print("=" * 60)
    print("WORKFLOW ORCHESTRATOR TEST")
    print("=" * 60)
    
    print(f"User Command: {user_command}")
    print("\nGenerating LLM prompt...")
    
    prompt = orchestrator.generate_llm_prompt(user_command)
    print(f"Prompt length: {len(prompt)} characters")
    
    print("\nSimulating LLM response...")
    # For testing, we'll use a mock response
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
    
    print("Validating LLM response...")
    validation = orchestrator.validate_llm_response(mock_llm_response)
    if validation["valid"]:
        print("✓ LLM response is valid M language")
        
        print("\nGetting swarm summary...")
        summary = orchestrator.get_swarm_summary(mock_llm_response)
        print(f"Swarm: {summary['name']}")
        print(f"Agents: {summary['total_agents']}")
        print(f"Workflow: {summary['workflow_type']}")
        
    else:
        print(f"✗ LLM response is invalid: {validation['error']}")
    
    print("\n" + "=" * 60) 