"""
Orchestrate agent that handles hierarchical workflows and agents.
"""

import logging
from typing import TypedDict, List, Union, Any
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from config import Config
from .regular_agent import run_agent
from .workflow_agent import run_workflow_agent

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class OrchestrateState(TypedDict):
    """State schema for the orchestrate agent."""
    messages: list[BaseMessage]
    responses: list[Any]
    current_index: int
    tasks: list[Any]
    workflow_results: list[Any]


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


def create_summary(responses: List[Any]) -> str:
    """
    Create a summary of all responses using LLM.
    """
    if not responses:
        return "No responses to summarize."
    
    # Create a prompt for summarization
    responses_text = "\n".join([f"Response {i+1}: {response}" for i, response in enumerate(responses)])
    
    summary_prompt = f"""Please provide a concise summary of the following orchestrated responses:

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
        
        # Create a simple fallback summary
        if len(responses) == 1:
            summary = f"Single response: {responses[0]}"
        else:
            summary = f"Processed {len(responses)} tasks successfully. Individual responses: " + "; ".join([str(r) for r in responses])
    
    return summary


def process_task(task: Any) -> Any:
    """
    Process a single task - could be a string (agent) or list (workflow).
    """
    if isinstance(task, str):
        # This is a string, send to regular agent
        logger.debug(f"Processing string task with regular agent: {task}")
        return run_agent(task)
    elif isinstance(task, list):
        # This is a list, could be workflow or nested structure
        if all(isinstance(item, str) for item in task):
            # All items are strings, this is a simple workflow
            logger.debug(f"Processing list task with workflow agent: {task}")
            workflow_responses, finalized_result = run_workflow_agent(task)
            return {
                "type": "workflow",
                "responses": workflow_responses,
                "finalized_result": finalized_result
            }
        else:
            # This is a nested structure, process recursively
            logger.debug(f"Processing nested task structure: {task}")
            nested_results = []
            for item in task:
                nested_result = process_task(item)
                nested_results.append(nested_result)
            
            # Create a summary for this nested workflow
            if nested_results:
                # Extract text responses for summary
                text_responses = []
                for result in nested_results:
                    if isinstance(result, str):
                        text_responses.append(result)
                    elif isinstance(result, dict) and "finalized_result" in result:
                        text_responses.append(result["finalized_result"])
                    else:
                        text_responses.append(str(result))
                
                nested_summary = create_summary(text_responses)
                return {
                    "type": "nested_workflow",
                    "responses": nested_results,
                    "finalized_result": nested_summary
                }
            else:
                return "No nested tasks to process"
    else:
        # Fallback for unexpected types
        logger.warning(f"Unexpected task type: {type(task)}")
        return f"Unsupported task type: {type(task)}"


def orchestrate_node(state: OrchestrateState) -> OrchestrateState:
    """
    Orchestrate node that processes tasks hierarchically.
    """
    tasks = state["tasks"]
    current_index = state["current_index"]
    responses = state["responses"]
    
    # Check if we've processed all tasks
    if current_index >= len(tasks):
        logger.debug("All tasks processed, ending orchestration")
        return state
    
    # Get the current task
    current_task = tasks[current_index]
    logger.debug(f"Processing task {current_index + 1}/{len(tasks)}: {current_task}")
    
    # Process the current task
    try:
        logger.debug(f"Processing task: {current_task}")
        task_result = process_task(current_task)
        
        logger.debug(f"Task result: {task_result}")
        
    except Exception as e:
        # Fallback response if task processing fails
        error_msg = f"Error processing task '{current_task}': {str(e)}"
        logger.error(f"Task processing failed for task {current_index}: {str(e)}")
        task_result = error_msg
    
    # Add the result to the list
    responses.append(task_result)
    logger.debug(f"Added response to list: {task_result}")
    
    # Move to next task
    state["current_index"] = current_index + 1
    
    # Add the interaction to messages for tracking
    state["messages"].append(HumanMessage(content=str(current_task)))
    state["messages"].append(AIMessage(content=str(task_result)))
    
    return state


def create_orchestrate_agent():
    """
    Create a LangGraph orchestrate agent that handles hierarchical tasks.
    """
    logger.debug("Creating LangGraph orchestrate agent...")
    
    # Create the graph with state schema
    workflow = StateGraph(OrchestrateState)
    
    # Add the orchestrate node
    workflow.add_node("orchestrate", orchestrate_node)
    
    # Set the entry point
    workflow.set_entry_point("orchestrate")
    
    # Add conditional edge - continue processing if more tasks, otherwise end
    workflow.add_conditional_edges(
        "orchestrate",
        lambda state: "orchestrate" if state["current_index"] < len(state["tasks"]) else END
    )
    
    # Compile the graph
    app = workflow.compile()
    
    logger.debug("Orchestrate agent created successfully")
    return app


def run_orchestrate_agent(tasks: List[List[Union[str, List[Union[str, List[str]]]]]]) -> tuple[List[Any], str]:
    """
    Run the orchestrate agent with hierarchical tasks and return responses and summary.
    """
    logger.debug(f"Starting orchestrate agent with {len(tasks)} task groups")
    
    if not tasks:
        logger.warning("No tasks provided")
        return [], "No tasks to process."
    
    agent = create_orchestrate_agent()
    
    # Create initial state
    initial_state = OrchestrateState(
        messages=[],
        responses=[],
        current_index=0,
        tasks=tasks,
        workflow_results=[]
    )
    
    logger.debug("Invoking orchestrate agent...")
    # Run the agent
    result = agent.invoke(initial_state)
    
    logger.debug(f"Orchestrate agent result: {result}")
    
    # Get the list of responses
    responses = result["responses"]
    logger.debug(f"Final orchestrate responses: {responses}")
    
    # Create summary of all responses
    logger.debug("Creating summary of all responses...")
    finalized_result = create_summary(responses)
    logger.debug(f"Finalized result: {finalized_result}")
    
    return responses, finalized_result 