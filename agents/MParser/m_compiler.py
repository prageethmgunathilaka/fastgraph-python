"""
M Language Compiler
Converts AST to executable workflow specifications
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import asdict
from .m_parser import SwarmDefinition, AgentDefinition, WorkflowDefinition, WorkflowStep


class MCompiler:
    """Compiler for M language AST to workflow specifications"""
    
    def __init__(self):
        self.compiled_swarms: Dict[str, Dict[str, Any]] = {}
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
    
    def compile(self, ast: SwarmDefinition) -> Dict[str, Any]:
        """Compile AST to workflow specification"""
        try:
            # Register all agents
            for agent in ast.agents:
                self.register_agent(agent)
            
            # Compile swarm
            swarm_spec = self.compile_swarm(ast)
            
            # Add to registry
            self.compiled_swarms[ast.name] = swarm_spec
            
            return swarm_spec
            
        except Exception as e:
            raise CompilationError(f"Compilation failed: {str(e)}")
    
    def register_agent(self, agent: AgentDefinition):
        """Register an agent definition"""
        agent_spec = {
            "name": agent.name,
            "role": agent.role,
            "capabilities": agent.capabilities,
            "inputs": agent.inputs,
            "outputs": agent.outputs,
            "config": agent.config,
            "type": "llm" if "llm" in agent.capabilities else "mcp" if "mcp" in agent.capabilities else "hybrid"
        }
        
        if agent.body:
            # Nested swarm
            agent_spec["swarm"] = self.compile_swarm(agent.body)
        
        self.agent_registry[agent.name] = agent_spec
    
    def compile_swarm(self, swarm: SwarmDefinition) -> Dict[str, Any]:
        """Compile swarm definition"""
        workflow_spec = self.compile_workflow(swarm.workflow)
        
        return {
            "type": "swarm",
            "name": swarm.name,
            "agents": {agent.name: self.agent_registry[agent.name] for agent in swarm.agents},
            "workflow": workflow_spec,
            "config": swarm.config,
            "execution_plan": self.generate_execution_plan(swarm)
        }
    
    def compile_workflow(self, workflow: WorkflowDefinition) -> Dict[str, Any]:
        """Compile workflow definition"""
        steps_spec = []
        
        for step in workflow.steps:
            step_spec = {
                "agent": step.agent_name,
                "inputs": step.inputs,
                "outputs": step.outputs,
                "transform": step.transform,
                "filter": step.filter,
                "timeout": step.timeout,
                "retry": step.retry,
                "error_handler": step.error_handler
            }
            steps_spec.append(step_spec)
        
        return {
            "type": workflow.type,
            "steps": steps_spec,
            "conditions": workflow.conditions,
            "max_iterations": workflow.max_iterations,
            "execution_strategy": self.determine_execution_strategy(workflow)
        }
    
    def determine_execution_strategy(self, workflow: WorkflowDefinition) -> str:
        """Determine execution strategy based on workflow type"""
        if workflow.type == "parallel":
            return "concurrent"
        elif workflow.type == "sequential":
            return "linear"
        elif workflow.type == "conditional":
            return "branching"
        elif workflow.type == "loop":
            return "iterative"
        else:
            return "linear"  # default
    
    def generate_execution_plan(self, swarm: SwarmDefinition) -> Dict[str, Any]:
        """Generate detailed execution plan"""
        plan = {
            "phases": [],
            "dependencies": {},
            "data_flow": {},
            "error_handling": {},
            "monitoring": {}
        }
        
        # Analyze workflow to create execution phases
        workflow = swarm.workflow
        current_phase = 0
        
        for i, step in enumerate(workflow.steps):
            phase = {
                "phase_id": current_phase,
                "step_id": i,
                "agent": step.agent_name,
                "dependencies": self.find_dependencies(step, workflow.steps[:i]),
                "inputs": step.inputs,
                "outputs": step.outputs,
                "execution_type": workflow.type
            }
            
            plan["phases"].append(phase)
            
            # Track dependencies
            plan["dependencies"][step.agent_name] = phase["dependencies"]
            
            # Track data flow
            plan["data_flow"][step.agent_name] = {
                "inputs": step.inputs,
                "outputs": step.outputs,
                "transform": step.transform,
                "filter": step.filter
            }
            
            # Error handling
            if step.error_handler:
                plan["error_handling"][step.agent_name] = step.error_handler
            
            # Move to next phase for sequential workflows
            if workflow.type == "sequential":
                current_phase += 1
        
        return plan
    
    def find_dependencies(self, step: WorkflowStep, previous_steps: List[WorkflowStep]) -> List[str]:
        """Find dependencies for a workflow step"""
        dependencies = []
        
        for prev_step in previous_steps:
            # Check if current step needs output from previous step
            for output in prev_step.outputs:
                if output in step.inputs:
                    dependencies.append(prev_step.agent_name)
                    break
        
        return dependencies
    
    def generate_agent_creation_script(self, swarm: SwarmDefinition) -> str:
        """Generate Python script for agent creation"""
        script_lines = [
            "from agents.regular_agent import run_agent",
            "from agents.workflow_agent import run_workflow_agent",
            "from agents.orchestrate_agent import run_orchestrate_agent",
            "",
            "def create_swarm():",
            f"    # Swarm: {swarm.name}",
            "    agents = {}",
            "    workflows = []",
            "",
        ]
        
        # Agent creation
        for agent in swarm.agents:
            script_lines.extend([
                f"    # Agent: {agent.name}",
                f"    agents['{agent.name}'] = {{",
                f"        'role': '{agent.role}',",
                f"        'capabilities': {agent.capabilities},",
                f"        'inputs': {agent.inputs},",
                f"        'outputs': {agent.outputs},",
                f"        'config': {agent.config}",
                "    }",
                ""
            ])
        
        # Workflow execution
        script_lines.extend([
            "    # Execute workflow",
            f"    workflow_type = '{swarm.workflow.type}'",
            "    steps = []",
            ""
        ])
        
        for step in swarm.workflow.steps:
            script_lines.extend([
                f"    steps.append({{",
                f"        'agent': '{step.agent_name}',",
                f"        'inputs': {step.inputs},",
                f"        'outputs': {step.outputs},",
                f"        'transform': {repr(step.transform)},",
                f"        'filter': {repr(step.filter)},",
                f"        'timeout': {step.timeout},",
                f"        'retry': {step.retry},",
                f"        'error_handler': {repr(step.error_handler)}",
                "    })",
                ""
            ])
        
        script_lines.extend([
            "    return agents, workflow_type, steps",
            "",
            "if __name__ == '__main__':",
            "    agents, workflow_type, steps = create_swarm()",
            "    print(f'Created swarm with {len(agents)} agents')",
            "    print(f'Workflow type: {workflow_type}')",
            "    print(f'Steps: {len(steps)}')"
        ])
        
        return "\n".join(script_lines)
    
    def to_json(self, swarm: SwarmDefinition) -> str:
        """Convert compiled swarm to JSON"""
        compiled = self.compile(swarm)
        return json.dumps(compiled, indent=2, default=str)
    
    def to_python(self, swarm: SwarmDefinition) -> str:
        """Convert compiled swarm to Python code"""
        return self.generate_agent_creation_script(swarm)


class CompilationError(Exception):
    """Compilation error"""
    pass 