"""
Debug script for M Language lexer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.MParser import MLexer

def debug_lexer():
    """Debug the lexer with a simple M code example"""
    
    lexer = MLexer()
    
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
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_lexer() 