"""
Workflow agent that spawns individual regular agents for each command.
"""

import logging
from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from config import Config
from .regular_agent import run_agent

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class WorkflowState(TypedDict):
    """State schema for the workflow agent."""
    messages: list[BaseMessage]
    responses: list[str]
    current_index: int
    commands: list[str]


def create_summary_llm():
    """
    Create an LLM instance for creating summaries.
    """
    # Validate configuration
    Config.validate()
    
    logger.debug(f"Creating summary LLM with model: {Config.DEFAULT_LLM_MODEL}, temperature: {Config.LLM_TEMPERATURE}")
    
    # Create LLM instance using config
    llm = ChatOpenAI(
        model=Config.DEFAULT_LLM_MODEL, 
        temperature=Config.LLM_TEMPERATURE,
        api_key=Config.OPENAI_API_KEY
    )
    
    return llm


def create_summary(responses: List[str]) -> str:
    """
    Create a summary of all responses using LLM.
    """
    if not responses:
        return "No responses to summarize."
    
    # Create a prompt for summarization
    responses_text = "\n".join([f"Response {i+1}: {response}" for i, response in enumerate(responses)])
    
    summary_prompt = f"""Please provide a concise summary of the following responses:

{responses_text}

Summary:"""
    
    try:
        logger.debug("Creating summary using LLM...")
        llm = create_summary_llm()
        
        logger.debug(f"Invoking LLM for summary with {len(responses)} responses")
        llm_response = llm.invoke(summary_prompt)
        
        logger.debug(f"Raw LLM summary response type: {type(llm_response)}")
        logger.debug(f"Raw LLM summary response: {llm_response}")
        
        # Convert the response to string
        if hasattr(llm_response, 'content'):
            summary = llm_response.content
            logger.debug(f"Extracted summary content: {summary}")
        elif isinstance(llm_response, str):
            summary = llm_response
            logger.debug(f"Summary is already string: {summary}")
        else:
            summary = str(llm_response)
            logger.debug(f"Converted summary to string: {summary}")
            
    except Exception as e:
        # Fallback summary if LLM fails
        error_msg = f"Error creating summary: {str(e)}"
        logger.error(f"LLM summary creation failed: {str(e)}")
        summary = error_msg
    
    return summary


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


def run_workflow_agent(commands: List[str]) -> tuple[List[str], str]:
    """
    Run the workflow agent with a list of commands and return responses and summary.
    """
    logger.debug(f"Starting workflow agent with {len(commands)} commands")
    
    if not commands:
        logger.warning("No commands provided")
        return [], "No commands to process."
    
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
    
    # Get the list of responses
    responses = result["responses"]
    logger.debug(f"Final workflow responses: {responses}")
    
    # Create summary of all responses
    logger.debug("Creating summary of all responses...")
    finalized_result = create_summary(responses)
    logger.debug(f"Finalized result: {finalized_result}")
    
    return responses, finalized_result 