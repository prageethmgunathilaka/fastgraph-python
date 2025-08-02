"""
Auto Orchestrate Agent
Automatically determines roles and creates agent swarms for user commands.
"""

import logging
from typing import TypedDict, List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from config import Config
from .MParser import MRuntime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AutoOrchestrateState(TypedDict):
    """State schema for the auto orchestrate agent."""
    messages: list[BaseMessage]
    command: str
    identified_role: str
    m_language_spec: str
    swarm_result: Dict[str, Any]
    final_result: str


def create_llm():
    """
    Create an LLM instance using configuration.
    """
    # Validate configuration
    Config.validate()
    
    logger.debug(f"Creating LLM with model: {Config.DEFAULT_LLM_MODEL}, temperature: {Config.LLM_TEMPERATURE}")
    
    # Create LLM instance using config
    llm = ChatOpenAI(
        model=Config.DEFAULT_LLM_MODEL, 
        temperature=Config.LLM_TEMPERATURE,
        api_key=Config.OPENAI_API_KEY
    )
    
    return llm


def identify_role_node(state: AutoOrchestrateState) -> AutoOrchestrateState:
    """
    Identify the appropriate role for the given command.
    """
    command = state["command"]
    
    # Create prompt to identify role
    role_prompt = f"""Given the following command, identify the most appropriate professional role that would be best suited to handle this task.

Command: {command}

Return ONLY the role name (e.g., "Data Scientist", "Software Engineer", "Research Analyst", "Content Writer", "Financial Analyst", "Marketing Specialist", "Legal Advisor", "Medical Consultant", "Educational Instructor", "Technical Support Specialist", "Project Manager", "Business Analyst", "Creative Designer", "Security Expert", "Environmental Scientist", "Healthcare Provider", "Sales Representative", "Human Resources Specialist", "Logistics Coordinator", "Quality Assurance Specialist").

Do not include any explanations, just the role name:"""
    
    try:
        logger.debug("Identifying role for command...")
        llm = create_llm()
        
        logger.debug("Invoking LLM for role identification...")
        llm_response = llm.invoke(role_prompt)
        
        # Extract role name
        if hasattr(llm_response, 'content'):
            identified_role = llm_response.content.strip()
        else:
            identified_role = str(llm_response).strip()
        
        logger.debug(f"Identified role: {identified_role}")
        
        # Add to state
        state["identified_role"] = identified_role
        state["messages"].append(HumanMessage(content=f"Role identification for: {command}"))
        state["messages"].append(AIMessage(content=f"Identified role: {identified_role}"))
        
    except Exception as e:
        error_msg = f"Error identifying role: {str(e)}"
        logger.error(f"Role identification failed: {str(e)}")
        state["identified_role"] = "General Assistant"
        state["messages"].append(AIMessage(content=error_msg))
    
    return state


def generate_m_language_spec_node(state: AutoOrchestrateState) -> AutoOrchestrateState:
    """
    Generate M Language specification for the identified role and command.
    """
    command = state["command"]
    identified_role = state["identified_role"]
    
    # Create prompt to generate M Language specification
    m_language_prompt = f"""Act as {identified_role}. 

Given the command: "{command}"

Generate an M Language specification that defines a swarm of agents to handle this task. The specification should include:

1. A main agent with the identified role
2. Any supporting agents needed (e.g., research agent, analysis agent, output agent)
3. A workflow that processes the command through these agents
4. Appropriate configurations for each agent

Return ONLY the M Language code, no explanations. Use this format:

```
swarm task_swarm {{
    agent main_agent {{
        role: "{identified_role}"
        capabilities: "llm,analysis"
        inputs: "user_command"
        outputs: "analysis_result"
        config: {{
            model: "gpt-4"
            temperature: 0.7
        }}
    }}
    
    agent research_agent {{
        role: "Research Specialist"
        capabilities: "llm,research"
        inputs: "research_query"
        outputs: "research_data"
        config: {{
            model: "gpt-4"
            temperature: 0.3
        }}
    }}
    
    workflow sequential {{
        main_agent(input: "user_command", output: "analysis_result")
    }}
}}
```"""
    
    try:
        logger.debug("Generating M Language specification...")
        llm = create_llm()
        
        logger.debug("Invoking LLM for M Language generation...")
        llm_response = llm.invoke(m_language_prompt)
        
        # Extract M Language specification
        if hasattr(llm_response, 'content'):
            m_language_spec = llm_response.content.strip()
        else:
            m_language_spec = str(llm_response).strip()
        
        # Strip markdown code block syntax if present
        if m_language_spec.startswith('```'):
            # Remove opening ```m or ``` and closing ```
            lines = m_language_spec.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]  # Remove first line
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]  # Remove last line
            m_language_spec = '\n'.join(lines).strip()
        
        logger.debug(f"Generated M Language spec: {m_language_spec}")
        
        # Add to state
        state["m_language_spec"] = m_language_spec
        state["messages"].append(HumanMessage(content=f"Generate M Language spec for role: {identified_role}"))
        state["messages"].append(AIMessage(content=f"Generated specification"))
        
    except Exception as e:
        error_msg = f"Error generating M Language specification: {str(e)}"
        logger.error(f"M Language generation failed: {str(e)}")
        
        # Fallback specification
        fallback_spec = f"""
swarm fallback_swarm {{
    agent main_agent {{
        role: "{identified_role}"
        capabilities: "llm,analysis"
        inputs: "user_command"
        outputs: "analysis_result"
        config: {{
            model: "gpt-4"
            temperature: 0.7
        }}
    }}
    
    workflow sequential {{
        main_agent(input: "user_command", output: "analysis_result")
    }}
}}
"""
        state["m_language_spec"] = fallback_spec.strip()
        state["messages"].append(AIMessage(content=error_msg))
    
    return state


def execute_swarm_node(state: AutoOrchestrateState) -> AutoOrchestrateState:
    """
    Execute the M Language specification using the MParser runtime.
    """
    m_language_spec = state["m_language_spec"]
    command = state["command"]
    
    try:
        logger.debug("Executing M Language specification...")
        m_runtime = MRuntime()
        
        # Execute the M Language specification
        initial_data = {"user_command": command}
        swarm_result = m_runtime.execute_m_code(m_language_spec, initial_data)
        
        logger.debug(f"Swarm execution result: {swarm_result}")
        
        # Add to state
        state["swarm_result"] = swarm_result
        state["messages"].append(HumanMessage(content="Execute M Language swarm"))
        state["messages"].append(AIMessage(content="Swarm executed successfully"))
        
    except Exception as e:
        error_msg = f"Error executing swarm: {str(e)}"
        logger.error(f"Swarm execution failed: {str(e)}")
        
        # Fallback result
        state["swarm_result"] = {
            "success": False,
            "error": error_msg,
            "fallback_response": f"Acting as {state['identified_role']}, I processed your command: {command}. However, there was an error in the swarm execution."
        }
        state["messages"].append(AIMessage(content=error_msg))
    
    return state


def create_final_result_node(state: AutoOrchestrateState) -> AutoOrchestrateState:
    """
    Create the final result from the swarm execution.
    """
    swarm_result = state["swarm_result"]
    identified_role = state["identified_role"]
    command = state["command"]
    
    try:
        if swarm_result.get("success", False):
            # Extract the result from swarm execution
            if "execution_results" in swarm_result:
                final_result = str(swarm_result["execution_results"])
            elif "result" in swarm_result:
                final_result = str(swarm_result["result"])
            else:
                final_result = f"Acting as {identified_role}, I have processed your command: {command}. The task has been completed successfully."
        else:
            # Use fallback response
            final_result = swarm_result.get("fallback_response", f"Acting as {identified_role}, I processed your command: {command}.")
        
        logger.debug(f"Final result: {final_result}")
        
        # Add to state
        state["final_result"] = final_result
        state["messages"].append(AIMessage(content=final_result))
        
    except Exception as e:
        error_msg = f"Error creating final result: {str(e)}"
        logger.error(f"Final result creation failed: {str(e)}")
        state["final_result"] = f"Acting as {identified_role}, I processed your command: {command}. There was an error in processing."
        state["messages"].append(AIMessage(content=error_msg))
    
    return state


def create_auto_orchestrate_agent():
    """
    Create a LangGraph auto orchestrate agent.
    """
    logger.debug("Creating LangGraph auto orchestrate agent...")
    
    # Create the graph with state schema
    workflow = StateGraph(AutoOrchestrateState)
    
    # Add the nodes
    workflow.add_node("identify_role", identify_role_node)
    workflow.add_node("generate_m_language_spec", generate_m_language_spec_node)
    workflow.add_node("execute_swarm", execute_swarm_node)
    workflow.add_node("create_final_result", create_final_result_node)
    
    # Set the entry point
    workflow.set_entry_point("identify_role")
    
    # Add edges
    workflow.add_edge("identify_role", "generate_m_language_spec")
    workflow.add_edge("generate_m_language_spec", "execute_swarm")
    workflow.add_edge("execute_swarm", "create_final_result")
    workflow.add_edge("create_final_result", END)
    
    # Compile the graph
    app = workflow.compile()
    
    logger.debug("Auto orchestrate agent created successfully")
    return app


def run_auto_orchestrate_agent(command: str) -> tuple[Dict[str, Any], str]:
    """
    Run the auto orchestrate agent with a command and return response and summary.
    """
    logger.debug(f"Starting auto orchestrate agent with command: '{command}'")
    
    if not command:
        logger.warning("No command provided")
        return {}, "No command to process."
    
    agent = create_auto_orchestrate_agent()
    
    # Create initial state
    initial_state = AutoOrchestrateState(
        messages=[],
        command=command,
        identified_role="",
        m_language_spec="",
        swarm_result={},
        final_result=""
    )
    
    logger.debug("Invoking auto orchestrate agent...")
    # Run the agent
    result = agent.invoke(initial_state)
    
    logger.debug(f"Auto orchestrate agent result: {result}")
    
    # Extract the final result
    final_result = result.get("final_result", "No result generated")
    logger.debug(f"Final auto orchestrate result: {final_result}")
    
    # Create response object
    response = {
        "identified_role": result.get("identified_role", ""),
        "m_language_spec": result.get("m_language_spec", ""),
        "swarm_result": result.get("swarm_result", {}),
        "processing_steps": [
            "Role identification",
            "M Language specification generation", 
            "Swarm execution",
            "Result compilation"
        ]
    }
    
    return response, final_result 