"""
Swarm Executor
Shows exactly how to execute parsed M language swarms
"""

import logging
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from .m_runtime import MRuntime

logger = logging.getLogger(__name__)


class SwarmExecutor:
    """Executes parsed M language swarms"""
    
    def __init__(self):
        self.m_runtime = MRuntime()
        self.execution_history = []
    
    def execute_swarm(self, swarm_spec: Dict[str, Any], initial_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a parsed swarm specification
        
        Args:
            swarm_spec: Parsed swarm specification from M language
            initial_data: Initial data for execution
            
        Returns:
            Execution results
        """
        try:
            logger.info(f"Executing swarm: {swarm_spec.get('name', 'unknown')}")
            
            # Step 1: Extract swarm components
            agents = swarm_spec.get("agents", {})
            workflow = swarm_spec.get("workflow", {})
            workflow_type = workflow.get("type", "sequential")
            steps = workflow.get("steps", [])
            
            logger.info(f"Swarm has {len(agents)} agents, {len(steps)} steps, workflow type: {workflow_type}")
            
            # Step 2: Execute based on workflow type
            if workflow_type == "sequential":
                return self._execute_sequential_workflow(agents, steps, initial_data)
            elif workflow_type == "parallel":
                return self._execute_parallel_workflow(agents, steps, initial_data)
            elif workflow_type == "conditional":
                return self._execute_conditional_workflow(agents, steps, initial_data)
            elif workflow_type == "loop":
                return self._execute_loop_workflow(agents, steps, initial_data)
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
                
        except Exception as e:
            logger.error(f"Swarm execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "swarm_name": swarm_spec.get("name", "unknown")
            }
    
    def _execute_sequential_workflow(self, agents: Dict[str, Any], steps: List[Dict[str, Any]], initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sequential workflow"""
        logger.info("Executing sequential workflow")
        
        results = {}
        current_data = initial_data or {}
        
        for i, step in enumerate(steps):
            try:
                agent_name = step["agent"]
                agent_spec = agents[agent_name]
                
                logger.info(f"Executing step {i+1}/{len(steps)}: {agent_name}")
                
                # Prepare inputs for this step
                inputs = self._prepare_step_inputs(step, current_data)
                logger.debug(f"Step inputs: {inputs}")
                
                # Execute the agent
                agent_result = self._execute_agent(agent_name, agent_spec, inputs)
                
                # Process outputs
                outputs = self._process_step_outputs(step, agent_result, current_data)
                current_data.update(outputs)
                
                results[agent_name] = {
                    "success": True,
                    "result": agent_result,
                    "outputs": outputs,
                    "step_number": i + 1
                }
                
                logger.info(f"✓ Step {agent_name} completed successfully")
                
            except Exception as e:
                error_msg = f"Step {agent_name} failed: {str(e)}"
                logger.error(error_msg)
                
                results[agent_name] = {
                    "success": False,
                    "error": str(e),
                    "step_number": i + 1
                }
                
                # Handle error based on step configuration
                if step.get("error_handler"):
                    self._handle_step_error(step, e)
        
        return {
            "success": all(result.get("success", False) for result in results.values()),
            "results": results,
            "final_data": current_data,
            "workflow_type": "sequential"
        }
    
    def _execute_parallel_workflow(self, agents: Dict[str, Any], steps: List[Dict[str, Any]], initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parallel workflow"""
        logger.info("Executing parallel workflow")
        
        # Group steps by dependencies
        independent_steps = []
        dependent_steps = []
        
        for step in steps:
            if not step.get("dependencies"):
                independent_steps.append(step)
            else:
                dependent_steps.append(step)
        
        results = {}
        current_data = initial_data or {}
        
        # Execute independent steps in parallel
        if independent_steps:
            logger.info(f"Executing {len(independent_steps)} independent steps in parallel")
            
            with ThreadPoolExecutor(max_workers=len(independent_steps)) as executor:
                future_to_step = {}
                
                for step in independent_steps:
                    future = executor.submit(
                        self._execute_workflow_step,
                        step, agents, current_data
                    )
                    future_to_step[future] = step
                
                # Collect results
                for future in as_completed(future_to_step):
                    step = future_to_step[future]
                    try:
                        result = future.result()
                        results[step["agent"]] = result
                        current_data.update(result.get("outputs", {}))
                        logger.info(f"✓ Parallel step {step['agent']} completed")
                    except Exception as e:
                        results[step["agent"]] = {
                            "success": False,
                            "error": str(e)
                        }
                        logger.error(f"✗ Parallel step {step['agent']} failed: {str(e)}")
        
        # Execute dependent steps sequentially
        for step in dependent_steps:
            try:
                result = self._execute_workflow_step(step, agents, current_data)
                results[step["agent"]] = result
                current_data.update(result.get("outputs", {}))
                logger.info(f"✓ Dependent step {step['agent']} completed")
            except Exception as e:
                results[step["agent"]] = {
                    "success": False,
                    "error": str(e)
                }
                logger.error(f"✗ Dependent step {step['agent']} failed: {str(e)}")
        
        return {
            "success": all(result.get("success", False) for result in results.values()),
            "results": results,
            "final_data": current_data,
            "workflow_type": "parallel"
        }
    
    def _execute_conditional_workflow(self, agents: Dict[str, Any], steps: List[Dict[str, Any]], initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute conditional workflow"""
        logger.info("Executing conditional workflow")
        
        results = {}
        current_data = initial_data or {}
        
        conditions = []  # Would be extracted from workflow spec
        condition_index = 0
        
        for i, step in enumerate(steps):
            # Check condition if available
            if condition_index < len(conditions):
                condition = conditions[condition_index]
                if not self._evaluate_condition(condition, current_data):
                    logger.info(f"Skipping step {step['agent']} due to condition: {condition}")
                    continue
                condition_index += 1
            
            try:
                result = self._execute_workflow_step(step, agents, current_data)
                results[step["agent"]] = result
                current_data.update(result.get("outputs", {}))
                logger.info(f"✓ Conditional step {step['agent']} completed")
            except Exception as e:
                results[step["agent"]] = {
                    "success": False,
                    "error": str(e)
                }
                logger.error(f"✗ Conditional step {step['agent']} failed: {str(e)}")
        
        return {
            "success": all(result.get("success", False) for result in results.values()),
            "results": results,
            "final_data": current_data,
            "workflow_type": "conditional"
        }
    
    def _execute_loop_workflow(self, agents: Dict[str, Any], steps: List[Dict[str, Any]], initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute loop workflow"""
        logger.info("Executing loop workflow")
        
        max_iterations = 10  # Would be extracted from workflow spec
        results = {}
        current_data = initial_data or {}
        
        for iteration in range(max_iterations):
            logger.info(f"Loop iteration {iteration + 1}/{max_iterations}")
            
            iteration_results = {}
            
            for step in steps:
                try:
                    result = self._execute_workflow_step(step, agents, current_data)
                    iteration_results[step["agent"]] = result
                    current_data.update(result.get("outputs", {}))
                except Exception as e:
                    iteration_results[step["agent"]] = {
                        "success": False,
                        "error": str(e)
                    }
            
            results[f"iteration_{iteration}"] = iteration_results
            
            # Check for loop termination condition
            if self._should_terminate_loop(iteration_results, current_data):
                logger.info(f"Loop terminating at iteration {iteration + 1}")
                break
        
        return {
            "success": all(result.get("success", False) for result in results.values()),
            "results": results,
            "final_data": current_data,
            "workflow_type": "loop",
            "iterations": len(results)
        }
    
    def _execute_workflow_step(self, step: Dict[str, Any], agents: Dict[str, Any], current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        agent_name = step["agent"]
        agent_spec = agents[agent_name]
        
        # Prepare inputs
        inputs = self._prepare_step_inputs(step, current_data)
        
        # Execute agent
        result = self._execute_agent(agent_name, agent_spec, inputs)
        
        # Process outputs
        outputs = self._process_step_outputs(step, result, current_data)
        
        return {
            "success": True,
            "result": result,
            "outputs": outputs
        }
    
    def _execute_agent(self, agent_name: str, agent_spec: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Execute a single agent"""
        agent_type = agent_spec.get("type", "llm")
        
        logger.info(f"Executing {agent_type} agent: {agent_name}")
        
        if agent_type == "llm":
            return self._execute_llm_agent(agent_name, agent_spec, inputs)
        elif agent_type == "mcp":
            return self._execute_mcp_agent(agent_name, agent_spec, inputs)
        elif agent_type == "hybrid":
            return self._execute_hybrid_agent(agent_name, agent_spec, inputs)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    
    def _execute_llm_agent(self, agent_name: str, agent_spec: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Execute LLM-based agent"""
        # Import here to avoid circular imports
        from ..regular_agent import run_agent
        
        # Convert inputs to string for LLM agent
        input_text = self._format_inputs_for_llm(inputs)
        
        # Execute using existing regular agent
        result = run_agent(input_text)
        
        logger.info(f"LLM agent {agent_name} completed")
        return result
    
    def _execute_mcp_agent(self, agent_name: str, agent_spec: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Execute MCP-based agent"""
        capabilities = agent_spec.get("capabilities", [])
        results = {}
        
        for capability in capabilities:
            if capability in self.m_runtime.executor.mcp_tools:
                try:
                    tool_result = self.m_runtime.executor.mcp_tools[capability](inputs)
                    results[capability] = tool_result
                except Exception as e:
                    logger.error(f"MCP tool {capability} failed: {str(e)}")
                    results[capability] = {"error": str(e)}
            else:
                logger.warning(f"MCP tool {capability} not registered")
                results[capability] = {"error": "Tool not available"}
        
        logger.info(f"MCP agent {agent_name} completed")
        return results
    
    def _execute_hybrid_agent(self, agent_name: str, agent_spec: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Execute hybrid agent (LLM + MCP)"""
        llm_result = self._execute_llm_agent(agent_name, agent_spec, inputs)
        mcp_result = self._execute_mcp_agent(agent_name, agent_spec, inputs)
        
        logger.info(f"Hybrid agent {agent_name} completed")
        return {
            "llm": llm_result,
            "mcp": mcp_result
        }
    
    def _prepare_step_inputs(self, step: Dict[str, Any], current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare inputs for a workflow step"""
        inputs = {}
        
        for input_name in step.get("inputs", []):
            if input_name in current_data:
                inputs[input_name] = current_data[input_name]
            else:
                logger.warning(f"Input {input_name} not found in current data")
        
        return inputs
    
    def _process_step_outputs(self, step: Dict[str, Any], result: Any, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process outputs from a workflow step"""
        outputs = {}
        
        # Apply transform if specified
        if step.get("transform"):
            result = self._apply_transform(step["transform"], result)
        
        # Apply filter if specified
        if step.get("filter"):
            result = self._apply_filter(step["filter"], result)
        
        # Map outputs
        for output_name in step.get("outputs", []):
            outputs[output_name] = result
        
        return outputs
    
    def _apply_transform(self, transform: str, data: Any) -> Any:
        """Apply transformation to data"""
        if transform == "to_string":
            return str(data)
        elif transform == "to_json":
            import json
            return json.dumps(data)
        elif transform == "extract_text":
            if isinstance(data, dict):
                return data.get("text", str(data))
            return str(data)
        else:
            return data
    
    def _apply_filter(self, filter_expr: str, data: Any) -> Any:
        """Apply filter to data"""
        if filter_expr == "non_empty":
            if isinstance(data, list):
                return [item for item in data if item]
            return data if data else None
        elif filter_expr == "unique":
            if isinstance(data, list):
                return list(set(data))
            return data
        else:
            return data
    
    def _format_inputs_for_llm(self, inputs: Dict[str, Any]) -> str:
        """Format inputs for LLM agent"""
        if not inputs:
            return ""
        
        formatted = []
        for key, value in inputs.items():
            formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)
    
    def _evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """Evaluate a condition"""
        try:
            return bool(data.get(condition, False))
        except:
            return False
    
    def _should_terminate_loop(self, iteration_results: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Check if loop should terminate"""
        all_success = all(result.get("success", False) for result in iteration_results.values())
        return all_success
    
    def _handle_step_error(self, step: Dict[str, Any], error: Exception):
        """Handle step execution error"""
        error_handler = step.get("error_handler")
        if error_handler == "retry":
            logger.info(f"Retrying step {step['agent']}")
            # Implement retry logic
        elif error_handler == "skip":
            logger.info(f"Skipping step {step['agent']}")
        elif error_handler == "abort":
            logger.error(f"Aborting workflow due to step {step['agent']} failure")
            raise error


def create_swarm_executor() -> SwarmExecutor:
    """Create a swarm executor instance"""
    return SwarmExecutor()


# Example usage
if __name__ == "__main__":
    executor = create_swarm_executor()
    
    # Example swarm specification
    swarm_spec = {
        "name": "test_swarm",
        "agents": {
            "research_agent": {
                "name": "research_agent",
                "role": "Research specialist",
                "capabilities": ["llm", "research"],
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
    
    # Execute the swarm
    initial_data = {"user_query": "What is quantum computing?"}
    result = executor.execute_swarm(swarm_spec, initial_data)
    
    print("=" * 60)
    print("SWARM EXECUTION RESULT")
    print("=" * 60)
    print(f"Success: {result['success']}")
    print(f"Workflow type: {result['workflow_type']}")
    print(f"Results: {len(result['results'])} steps completed")
    print("=" * 60) 