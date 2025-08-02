"""
M Language Executor
Executes compiled swarm specifications
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from .m_compiler import MCompiler
from .m_parser import SwarmDefinition

logger = logging.getLogger(__name__)


@dataclass
class ExecutionContext:
    """Execution context for swarm"""
    swarm_name: str
    agents: Dict[str, Any]
    workflow: Dict[str, Any]
    data: Dict[str, Any]
    results: Dict[str, Any]
    errors: List[str]


class MExecutor:
    """Executor for M language compiled specifications"""
    
    def __init__(self):
        self.compiler = MCompiler()
        self.execution_contexts: Dict[str, ExecutionContext] = {}
        self.agent_factories: Dict[str, Callable] = {}
        self.mcp_tools: Dict[str, Callable] = {}
    
    def register_agent_factory(self, agent_type: str, factory: Callable):
        """Register an agent factory function"""
        self.agent_factories[agent_type] = factory
    
    def register_mcp_tool(self, tool_name: str, tool_func: Callable):
        """Register an MCP tool"""
        self.mcp_tools[tool_name] = tool_func
    
    def execute_swarm(self, swarm_spec: Dict[str, Any], initial_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a compiled swarm specification"""
        try:
            # Create execution context
            context = ExecutionContext(
                swarm_name=swarm_spec["name"],
                agents=swarm_spec["agents"],
                workflow=swarm_spec["workflow"],
                data=initial_data or {},
                results={},
                errors=[]
            )
            
            self.execution_contexts[swarm_spec["name"]] = context
            
            # Execute based on workflow type
            workflow_type = swarm_spec["workflow"]["type"]
            
            if workflow_type == "sequential":
                return self.execute_sequential_workflow(context)
            elif workflow_type == "parallel":
                return self.execute_parallel_workflow(context)
            elif workflow_type == "conditional":
                return self.execute_conditional_workflow(context)
            elif workflow_type == "loop":
                return self.execute_loop_workflow(context)
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
                
        except Exception as e:
            logger.error(f"Swarm execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "results": {},
                "context": context if 'context' in locals() else None
            }
    
    def execute_sequential_workflow(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute sequential workflow"""
        logger.info(f"Executing sequential workflow for swarm: {context.swarm_name}")
        
        results = {}
        current_data = context.data.copy()
        
        for step in context.workflow["steps"]:
            try:
                agent_name = step["agent"]
                agent_spec = context.agents[agent_name]
                
                logger.info(f"Executing agent: {agent_name}")
                
                # Prepare inputs
                inputs = self.prepare_agent_inputs(step, current_data)
                
                # Execute agent
                result = self.execute_agent(agent_name, agent_spec, inputs)
                
                # Process outputs
                outputs = self.process_agent_outputs(step, result, current_data)
                current_data.update(outputs)
                
                results[agent_name] = {
                    "success": True,
                    "result": result,
                    "outputs": outputs
                }
                
                logger.info(f"Agent {agent_name} completed successfully")
                
            except Exception as e:
                error_msg = f"Agent {agent_name} failed: {str(e)}"
                logger.error(error_msg)
                context.errors.append(error_msg)
                
                results[agent_name] = {
                    "success": False,
                    "error": str(e)
                }
                
                # Handle error based on step configuration
                if step.get("error_handler"):
                    self.handle_agent_error(step, e, context)
        
        return {
            "success": len(context.errors) == 0,
            "results": results,
            "final_data": current_data,
            "errors": context.errors
        }
    
    def execute_parallel_workflow(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute parallel workflow"""
        logger.info(f"Executing parallel workflow for swarm: {context.swarm_name}")
        
        # Group steps by dependencies
        independent_steps = []
        dependent_steps = []
        
        for step in context.workflow["steps"]:
            if not step.get("dependencies"):
                independent_steps.append(step)
            else:
                dependent_steps.append(step)
        
        results = {}
        current_data = context.data.copy()
        
        # Execute independent steps in parallel
        with ThreadPoolExecutor(max_workers=len(independent_steps)) as executor:
            future_to_step = {}
            
            for step in independent_steps:
                future = executor.submit(
                    self.execute_workflow_step,
                    step, context, current_data
                )
                future_to_step[future] = step
            
            # Collect results
            for future in as_completed(future_to_step):
                step = future_to_step[future]
                try:
                    result = future.result()
                    results[step["agent"]] = result
                    current_data.update(result.get("outputs", {}))
                except Exception as e:
                    results[step["agent"]] = {
                        "success": False,
                        "error": str(e)
                    }
        
        # Execute dependent steps sequentially
        for step in dependent_steps:
            try:
                result = self.execute_workflow_step(step, context, current_data)
                results[step["agent"]] = result
                current_data.update(result.get("outputs", {}))
            except Exception as e:
                results[step["agent"]] = {
                    "success": False,
                    "error": str(e)
                }
        
        return {
            "success": len(context.errors) == 0,
            "results": results,
            "final_data": current_data,
            "errors": context.errors
        }
    
    def execute_conditional_workflow(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute conditional workflow"""
        logger.info(f"Executing conditional workflow for swarm: {context.swarm_name}")
        
        results = {}
        current_data = context.data.copy()
        
        conditions = context.workflow.get("conditions", [])
        
        for i, step in enumerate(context.workflow["steps"]):
            # Check condition if available
            if i < len(conditions):
                condition = conditions[i]
                if not self.evaluate_condition(condition, current_data):
                    logger.info(f"Skipping step {step['agent']} due to condition: {condition}")
                    continue
            
            try:
                result = self.execute_workflow_step(step, context, current_data)
                results[step["agent"]] = result
                current_data.update(result.get("outputs", {}))
            except Exception as e:
                results[step["agent"]] = {
                    "success": False,
                    "error": str(e)
                }
        
        return {
            "success": len(context.errors) == 0,
            "results": results,
            "final_data": current_data,
            "errors": context.errors
        }
    
    def execute_loop_workflow(self, context: ExecutionContext) -> Dict[str, Any]:
        """Execute loop workflow"""
        logger.info(f"Executing loop workflow for swarm: {context.swarm_name}")
        
        max_iterations = context.workflow.get("max_iterations", 10)
        results = {}
        current_data = context.data.copy()
        
        for iteration in range(max_iterations):
            logger.info(f"Loop iteration {iteration + 1}/{max_iterations}")
            
            iteration_results = {}
            
            for step in context.workflow["steps"]:
                try:
                    result = self.execute_workflow_step(step, context, current_data)
                    iteration_results[step["agent"]] = result
                    current_data.update(result.get("outputs", {}))
                except Exception as e:
                    iteration_results[step["agent"]] = {
                        "success": False,
                        "error": str(e)
                    }
            
            results[f"iteration_{iteration}"] = iteration_results
            
            # Check for loop termination condition
            if self.should_terminate_loop(iteration_results, current_data):
                break
        
        return {
            "success": len(context.errors) == 0,
            "results": results,
            "final_data": current_data,
            "errors": context.errors,
            "iterations": len(results)
        }
    
    def execute_workflow_step(self, step: Dict[str, Any], context: ExecutionContext, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        agent_name = step["agent"]
        agent_spec = context.agents[agent_name]
        
        # Prepare inputs
        inputs = self.prepare_agent_inputs(step, current_data)
        
        # Execute agent
        result = self.execute_agent(agent_name, agent_spec, inputs)
        
        # Process outputs
        outputs = self.process_agent_outputs(step, result, current_data)
        
        return {
            "success": True,
            "result": result,
            "outputs": outputs
        }
    
    def execute_agent(self, agent_name: str, agent_spec: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Execute a single agent"""
        agent_type = agent_spec.get("type", "llm")
        
        if agent_type == "llm":
            return self.execute_llm_agent(agent_name, agent_spec, inputs)
        elif agent_type == "mcp":
            return self.execute_mcp_agent(agent_name, agent_spec, inputs)
        elif agent_type == "hybrid":
            return self.execute_hybrid_agent(agent_name, agent_spec, inputs)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    
    def execute_llm_agent(self, agent_name: str, agent_spec: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Execute LLM-based agent"""
        # Import here to avoid circular imports
        from ..regular_agent import run_agent
        
        # Convert inputs to string for LLM agent
        input_text = self.format_inputs_for_llm(inputs)
        
        # Execute using existing regular agent
        result = run_agent(input_text)
        
        return result
    
    def execute_mcp_agent(self, agent_name: str, agent_spec: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Execute MCP-based agent"""
        capabilities = agent_spec.get("capabilities", [])
        results = {}
        
        for capability in capabilities:
            if capability in self.mcp_tools:
                try:
                    tool_result = self.mcp_tools[capability](inputs)
                    results[capability] = tool_result
                except Exception as e:
                    logger.error(f"MCP tool {capability} failed: {str(e)}")
                    results[capability] = {"error": str(e)}
            else:
                logger.warning(f"MCP tool {capability} not registered")
                results[capability] = {"error": "Tool not available"}
        
        return results
    
    def execute_hybrid_agent(self, agent_name: str, agent_spec: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Execute hybrid agent (LLM + MCP)"""
        llm_result = self.execute_llm_agent(agent_name, agent_spec, inputs)
        mcp_result = self.execute_mcp_agent(agent_name, agent_spec, inputs)
        
        return {
            "llm": llm_result,
            "mcp": mcp_result
        }
    
    def prepare_agent_inputs(self, step: Dict[str, Any], current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare inputs for agent execution"""
        inputs = {}
        
        for input_name in step.get("inputs", []):
            if input_name in current_data:
                inputs[input_name] = current_data[input_name]
            else:
                logger.warning(f"Input {input_name} not found in current data")
        
        return inputs
    
    def process_agent_outputs(self, step: Dict[str, Any], result: Any, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process agent outputs"""
        outputs = {}
        
        # Apply transform if specified
        if step.get("transform"):
            result = self.apply_transform(step["transform"], result)
        
        # Apply filter if specified
        if step.get("filter"):
            result = self.apply_filter(step["filter"], result)
        
        # Map outputs
        for output_name in step.get("outputs", []):
            outputs[output_name] = result
        
        return outputs
    
    def apply_transform(self, transform: str, data: Any) -> Any:
        """Apply transformation to data"""
        # Simple transformation - can be extended
        if transform == "to_string":
            return str(data)
        elif transform == "to_json":
            import json
            return json.dumps(data)
        elif transform == "extract_text":
            # Extract text from various formats
            if isinstance(data, dict):
                return data.get("text", str(data))
            return str(data)
        else:
            return data
    
    def apply_filter(self, filter_expr: str, data: Any) -> Any:
        """Apply filter to data"""
        # Simple filtering - can be extended
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
    
    def format_inputs_for_llm(self, inputs: Dict[str, Any]) -> str:
        """Format inputs for LLM agent"""
        if not inputs:
            return ""
        
        formatted = []
        for key, value in inputs.items():
            formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)
    
    def evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """Evaluate a condition"""
        # Simple condition evaluation - can be extended
        try:
            # For now, just check if the condition key exists and is truthy
            return bool(data.get(condition, False))
        except:
            return False
    
    def should_terminate_loop(self, iteration_results: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Check if loop should terminate"""
        # Simple termination logic - can be extended
        all_success = all(result.get("success", False) for result in iteration_results.values())
        return all_success
    
    def handle_agent_error(self, step: Dict[str, Any], error: Exception, context: ExecutionContext):
        """Handle agent execution error"""
        error_handler = step.get("error_handler")
        if error_handler == "retry":
            # Implement retry logic
            pass
        elif error_handler == "skip":
            # Skip this step
            pass
        elif error_handler == "abort":
            # Abort entire workflow
            raise error 