"""
Simple LangGraph agent implementation.
"""

from typing import Dict, Any, TypedDict
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """State schema for the agent."""
    messages: list[BaseMessage]


def agent_node(state: AgentState) -> AgentState:
    """
    Simple agent node that always returns "hello agent from langgraph".
    """
    # Always return the same response regardless of input
    response = "hello agent from langgraph"
    
    # Add the response to the state
    state["messages"].append(AIMessage(content=response))
    return state


def create_agent():
    """
    Create a simple LangGraph agent.
    """
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
    
    return app


def run_agent(input_text: str = "") -> str:
    """
    Run the agent with given input and return the response.
    """
    agent = create_agent()
    
    # Create initial state with the input message
    initial_state = AgentState(
        messages=[HumanMessage(content=input_text)]
    )
    
    # Run the agent
    result = agent.invoke(initial_state)
    
    # Extract the last AI message (the response)
    ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
    if ai_messages:
        return ai_messages[-1].content
    
    return "No response generated" 