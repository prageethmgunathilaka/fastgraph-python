"""
Workflow agent that spawns individual regular agents for each command.
"""

import logging
from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END
from config import Config
from agent import run_agent

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class WorkflowState(TypedDict):
    """State schema for the workflow agent."""
    messages: list[BaseMessage]
    responses: list[str]
    current_index: int
    commands: list[str]


def workflow_node(state: WorkflowState) -> WorkflowState:
    """
    Workflow node that spawns a regular agent for each command.
    """
    commands = state["commands"]
    current_index = state["current_index"]
    responses = state["responses"]
    
    # Check if we've processed all commands
    if current_index >= len(commands):
        logger.debug("All commands processed, ending workflow")
        return state
    
    # Get the current command
    current_command = commands[current_index]
    logger.debug(f"Processing command {current_index + 1}/{len(commands)}: {current_command}")
    
    # Spawn a regular agent for this command
    try:
        logger.debug(f"Spawning regular agent for command: {current_command}")
        agent_response = run_agent(current_command)
        
        logger.debug(f"Regular agent response: {agent_response}")
        
    except Exception as e:
        # Fallback response if agent fails
        error_msg = f"Error processing command '{current_command}': {str(e)}"
        logger.error(f"Regular agent failed for command {current_index}: {str(e)}")
        agent_response = error_msg
    
    # Add the response to the list
    responses.append(agent_response)
    logger.debug(f"Added response to list: {agent_response}")
    
    # Move to next command
    state["current_index"] = current_index + 1
    
    # Add the interaction to messages for tracking
    state["messages"].append(HumanMessage(content=current_command))
    state["messages"].append(AIMessage(content=agent_response))
    
    return state


def create_workflow_agent():
    """
    Create a LangGraph workflow agent that spawns regular agents.
    """
    logger.debug("Creating LangGraph workflow agent...")
    
    # Create the graph with state schema
    workflow = StateGraph(WorkflowState)
    
    # Add the workflow node
    workflow.add_node("workflow", workflow_node)
    
    # Set the entry point
    workflow.set_entry_point("workflow")
    
    # Add conditional edge - continue processing if more commands, otherwise end
    workflow.add_conditional_edges(
        "workflow",
        lambda state: "workflow" if state["current_index"] < len(state["commands"]) else END
    )
    
    # Compile the graph
    app = workflow.compile()
    
    logger.debug("Workflow agent created successfully")
    return app


def run_workflow_agent(commands: List[str]) -> List[str]:
    """
    Run the workflow agent with a list of commands and return responses.
    """
    logger.debug(f"Starting workflow agent with {len(commands)} commands")
    
    if not commands:
        logger.warning("No commands provided")
        return []
    
    agent = create_workflow_agent()
    
    # Create initial state
    initial_state = WorkflowState(
        messages=[],
        responses=[],
        current_index=0,
        commands=commands
    )
    
    logger.debug("Invoking workflow agent...")
    # Run the agent
    result = agent.invoke(initial_state)
    
    logger.debug(f"Workflow agent result: {result}")
    
    # Return the list of responses
    responses = result["responses"]
    logger.debug(f"Final workflow responses: {responses}")
    return responses 