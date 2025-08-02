"""
LangGraph agent with LLM capabilities.
"""

import logging
from typing import TypedDict
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from config import Config

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State schema for the agent."""
    messages: list[BaseMessage]


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


def agent_node(state: AgentState) -> AgentState:
    """
    Agent node that uses LLM to generate responses.
    """
    # Get the last human message
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    if not human_messages:
        response = "No input provided"
        logger.debug("No human message found, using fallback response")
    else:
        # Get the user's input
        user_input = human_messages[-1].content
        logger.debug(f"Processing user input: {user_input}")
        
        # Use the LLM to get response
        try:
            logger.debug("Creating LLM instance...")
            llm = create_llm()
            
            logger.debug("Invoking LLM...")
            llm_response = llm.invoke(user_input)
            
            logger.debug(f"Raw LLM response type: {type(llm_response)}")
            logger.debug(f"Raw LLM response: {llm_response}")
            
            # Convert the response to string
            if hasattr(llm_response, 'content'):
                response = llm_response.content
                logger.debug(f"Extracted content from response: {response}")
            elif isinstance(llm_response, str):
                response = llm_response
                logger.debug(f"Response is already string: {response}")
            else:
                response = str(llm_response)
                logger.debug(f"Converted response to string: {response}")
                
        except Exception as e:
            # Fallback response if LLM fails
            error_msg = f"Sorry, I encountered an error: {str(e)}. Please check your API key configuration."
            logger.error(f"LLM invocation failed: {str(e)}")
            response = error_msg
    
    logger.debug(f"Final response: {response}")
    
    # Add the response to the state
    state["messages"].append(AIMessage(content=response))
    return state


def create_agent():
    """
    Create a LangGraph agent with LLM capabilities.
    """
    logger.debug("Creating LangGraph agent...")
    
    # Create the graph with state schema
    workflow = StateGraph(AgentState)
    
    # Add the agent node
    workflow.add_node("agent", agent_node)
    
    # Set the entry point
    workflow.set_entry_point("agent")
    
    # Set the end point
    workflow.add_edge("agent", END)
    
    # Compile the graph
    app = workflow.compile()
    
    logger.debug("Agent created successfully")
    return app


def run_agent(input_text: str = "") -> str:
    """
    Run the agent with given input and return the LLM response.
    """
    logger.debug(f"Starting agent with input: '{input_text}'")
    
    agent = create_agent()
    
    # Create initial state with the input message
    initial_state = AgentState(
        messages=[HumanMessage(content=input_text)]
    )
    
    logger.debug("Invoking agent...")
    # Run the agent
    result = agent.invoke(initial_state)
    
    logger.debug(f"Agent result: {result}")
    
    # Extract the last AI message (the response)
    ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
    if ai_messages:
        final_response = ai_messages[-1].content
        logger.debug(f"Final agent response: {final_response}")
        return final_response
    
    logger.warning("No AI messages found in result")
    return "No response generated" 