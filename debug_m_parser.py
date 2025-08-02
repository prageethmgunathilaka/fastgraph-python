"""
Debug script for M Language parser
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.MParser import MLexer, MParser

def debug_parser():
    """Debug the parser with a simple M code example"""
    
    lexer = MLexer()
    parser = MParser()
    
    # Simple M code
    m_code = """
swarm test_swarm {
    agent test_agent {
        role: "Test agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
            temperature: 0.7
        }
    }
    
    workflow sequential {
        test_agent(input: "input", output: "output")
    }
}"""
    
    print("M Code:")
    print(m_code)
    print("\n" + "="*50)
    print("Tokenizing...")
    
    try:
        tokens = lexer.tokenize(m_code)
        print(f"Generated {len(tokens)} tokens:")
        
        for i, token in enumerate(tokens):
            print(f"{i:3d}: {token.type.value:15s} | '{token.value}' | line {token.line}, col {token.column}")
        
        print("\n" + "="*50)
        print("Parsing...")
        
        ast = parser.parse(tokens)
        print(f"✓ Parse successful!")
        print(f"  Swarm name: {ast.name}")
        print(f"  Agents: {len(ast.agents)}")
        print(f"  Workflow type: {ast.workflow.type}")
        print(f"  Workflow steps: {len(ast.workflow.steps)}")
        
        # Print agent details
        for i, agent in enumerate(ast.agents):
            print(f"  Agent {i+1}: {agent.name}")
            print(f"    Role: {agent.role}")
            print(f"    Capabilities: {agent.capabilities}")
            print(f"    Inputs: {agent.inputs}")
            print(f"    Outputs: {agent.outputs}")
            print(f"    Config: {agent.config}")
        
        # Print workflow details
        print(f"  Workflow steps:")
        for i, step in enumerate(ast.workflow.steps):
            print(f"    Step {i+1}: {step.agent_name}")
            print(f"      Inputs: {step.inputs}")
            print(f"      Outputs: {step.outputs}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_parser() 