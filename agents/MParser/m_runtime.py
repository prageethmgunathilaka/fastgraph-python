"""
M Language Runtime
Complete interface for LLM-to-workflow agent communication
"""

import logging
from typing import Dict, List, Any, Optional, Union
from .m_lexer import MLexer
from .m_parser import MParser
from .m_compiler import MCompiler
from .m_executor import MExecutor

logger = logging.getLogger(__name__)


class MRuntime:
    """Complete M language runtime for LLM-to-workflow communication"""
    
    def __init__(self):
        self.lexer = MLexer()
        self.parser = MParser()
        self.compiler = MCompiler()
        self.executor = MExecutor()
        
        # Register default MCP tools
        self._register_default_mcp_tools()
    
    def _register_default_mcp_tools(self):
        """Register default MCP tools"""
        # File operations
        self.executor.register_mcp_tool("file_search", self._file_search)
        self.executor.register_mcp_tool("read_file", self._read_file)
        self.executor.register_mcp_tool("edit_file", self._edit_file)
        self.executor.register_mcp_tool("list_dir", self._list_dir)
        
        # Code operations
        self.executor.register_mcp_tool("codebase_search", self._codebase_search)
        self.executor.register_mcp_tool("grep_search", self._grep_search)
        
        # Terminal operations
        self.executor.register_mcp_tool("run_terminal", self._run_terminal)
        
        # Web operations
        self.executor.register_mcp_tool("web_search", self._web_search)
        self.executor.register_mcp_tool("web_navigate", self._web_navigate)
    
    def process_llm_request(self, llm_response: str, user_command: str) -> Dict[str, Any]:
        """
        Process LLM response and user command to create and execute agent swarm
        
        Args:
            llm_response: LLM's response in M language format
            user_command: Original user command
            
        Returns:
            Execution results
        """
        try:
            # Parse LLM response as M language code
            swarm_spec = self.parse_and_compile(llm_response)
            
            # Execute the swarm
            initial_data = {"user_command": user_command}
            results = self.executor.execute_swarm(swarm_spec, initial_data)
            
            return {
                "success": True,
                "swarm_spec": swarm_spec,
                "execution_results": results,
                "user_command": user_command
            }
            
        except Exception as e:
            logger.error(f"Failed to process LLM request: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "user_command": user_command
            }
    
    def parse_and_compile(self, m_code: str) -> Dict[str, Any]:
        """
        Parse and compile M language code
        
        Args:
            m_code: M language source code
            
        Returns:
            Compiled swarm specification
        """
        try:
            # Tokenize
            tokens = self.lexer.tokenize(m_code)
            
            # Parse
            ast = self.parser.parse(tokens)
            
            # Compile
            swarm_spec = self.compiler.compile(ast)
            
            return swarm_spec
            
        except Exception as e:
            logger.error(f"Parse/compile failed: {str(e)}")
            raise
    
    def execute_m_code(self, m_code: str, initial_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute M language code directly
        
        Args:
            m_code: M language source code
            initial_data: Initial data for execution
            
        Returns:
            Execution results
        """
        try:
            swarm_spec = self.parse_and_compile(m_code)
            results = self.executor.execute_swarm(swarm_spec, initial_data or {})
            
            return {
                "success": True,
                "swarm_spec": swarm_spec,
                "execution_results": results
            }
            
        except Exception as e:
            logger.error(f"Execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_m_code_template(self, task_description: str) -> str:
        """
        Generate M language code template for a task
        
        Args:
            task_description: Description of the task
            
        Returns:
            M language code template
        """
        template = f"""swarm {task_description.lower().replace(' ', '_')} {{
    agent research_agent {{
        role: "Research and analysis specialist"
        capabilities: "llm,research,analysis"
        inputs: "user_query,context"
        outputs: "research_results,insights"
        config: {{
            model: "gpt-4"
            temperature: 0.7
        }}
    }}
    
    agent action_agent {{
        role: "Action execution specialist"
        capabilities: "mcp,execution,tools"
        inputs: "research_results,action_plan"
        outputs: "execution_results,status"
        config: {{
            timeout: 300
            retry: 3
        }}
    }}
    
    workflow sequential {{
        research_agent(input: "user_query", output: "research_results")
        action_agent(input: "research_results", output: "execution_results")
    }}
}}"""
        
        return template
    
    def validate_m_code(self, m_code: str) -> Dict[str, Any]:
        """
        Validate M language code without executing
        
        Args:
            m_code: M language source code
            
        Returns:
            Validation results
        """
        try:
            # Tokenize
            tokens = self.lexer.tokenize(m_code)
            
            # Parse
            ast = self.parser.parse(tokens)
            
            # Compile (without execution)
            swarm_spec = self.compiler.compile(ast)
            
            return {
                "valid": True,
                "tokens_count": len(tokens),
                "agents_count": len(swarm_spec["agents"]),
                "workflow_type": swarm_spec["workflow"]["type"],
                "steps_count": len(swarm_spec["workflow"]["steps"])
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    def get_swarm_summary(self, swarm_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary of a swarm specification
        
        Args:
            swarm_spec: Compiled swarm specification
            
        Returns:
            Swarm summary
        """
        agents = swarm_spec.get("agents", {})
        workflow = swarm_spec.get("workflow", {})
        
        agent_types = {}
        for agent_name, agent_spec in agents.items():
            agent_type = agent_spec.get("type", "unknown")
            if agent_type not in agent_types:
                agent_types[agent_type] = 0
            agent_types[agent_type] += 1
        
        return {
            "name": swarm_spec.get("name", "unknown"),
            "total_agents": len(agents),
            "agent_types": agent_types,
            "workflow_type": workflow.get("type", "unknown"),
            "steps_count": len(workflow.get("steps", [])),
            "execution_strategy": workflow.get("execution_strategy", "unknown"),
            "description": f"Swarm '{swarm_spec.get('name', 'unknown')}' with {len(agents)} agents and {workflow.get('type', 'unknown')} workflow"
        }
    
    # Default MCP tool implementations
    def _file_search(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """File search tool"""
        query = inputs.get("query", "")
        # Implementation would use actual file search
        return {"files": [f"found_{query}.txt"]}
    
    def _read_file(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Read file tool"""
        file_path = inputs.get("file_path", "")
        # Implementation would read actual file
        return {"content": f"Content of {file_path}"}
    
    def _edit_file(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Edit file tool"""
        file_path = inputs.get("file_path", "")
        content = inputs.get("content", "")
        # Implementation would edit actual file
        return {"success": True, "file_path": file_path}
    
    def _list_dir(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """List directory tool"""
        path = inputs.get("path", ".")
        # Implementation would list actual directory
        return {"files": ["file1.txt", "file2.py"], "directories": ["dir1"]}
    
    def _codebase_search(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Codebase search tool"""
        query = inputs.get("query", "")
        # Implementation would search actual codebase
        return {"results": [f"Found: {query}"]}
    
    def _grep_search(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Grep search tool"""
        pattern = inputs.get("pattern", "")
        # Implementation would perform actual grep
        return {"matches": [f"Match: {pattern}"]}
    
    def _run_terminal(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run terminal command tool"""
        command = inputs.get("command", "")
        # Implementation would run actual command
        return {"output": f"Executed: {command}", "exit_code": 0}
    
    def _web_search(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Web search tool"""
        query = inputs.get("query", "")
        # Implementation would perform actual web search
        return {"results": [f"Web result for: {query}"]}
    
    def _web_navigate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Web navigation tool"""
        url = inputs.get("url", "")
        # Implementation would navigate to actual URL
        return {"success": True, "url": url}
    
    def get_m_language_guide(self) -> str:
        """Get M language syntax guide"""
        return """
M Language Syntax Guide
=======================

1. Swarm Definition:
   swarm swarm_name {
       agent agent_name {
           role: "Agent role description"
           capabilities: "llm,mcp,research,analysis"
           inputs: "input1,input2"
           outputs: "output1,output2"
           config: {
               model: "gpt-4"
               temperature: 0.7
               timeout: 300
           }
       }
       
       workflow sequential|parallel|conditional|loop {
           agent_name(input: "input_data", output: "output_data", transform: "to_string", filter: "non_empty", timeout: 300, retry: 3, error: "retry")
       }
   }

2. Agent Types:
   - llm: LLM-based agents
   - mcp: MCP tool-based agents  
   - hybrid: Combined LLM and MCP agents

3. Workflow Types:
   - sequential: Execute steps in order
   - parallel: Execute steps concurrently
   - conditional: Execute steps based on conditions
   - loop: Execute steps repeatedly

4. Data Flow:
   - inputs: Specify input data sources
   - outputs: Specify output data destinations
   - transform: Apply data transformations
   - filter: Apply data filters

5. Error Handling:
   - retry: Retry failed steps
   - skip: Skip failed steps
   - abort: Abort entire workflow

6. Configuration:
   - timeout: Maximum execution time
   - retry: Number of retry attempts
   - model: LLM model to use
   - temperature: LLM creativity level
""" 