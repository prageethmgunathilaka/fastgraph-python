# M Language: Agent Swarm Programming Language

## Overview

M Language is a specialized programming language designed for LLM-to-workflow agent communication. It enables LLMs to specify complex agent swarms with precise control over agent creation, roles, data flow, and execution patterns.

## Key Features

- **Declarative Syntax**: Simple, readable syntax for defining agent swarms
- **Multiple Agent Types**: Support for LLM, MCP, and hybrid agents
- **Flexible Workflows**: Sequential, parallel, conditional, and loop execution patterns
- **Data Flow Control**: Explicit input/output specification and data transformations
- **Error Handling**: Built-in retry, skip, and abort mechanisms
- **Nested Swarms**: Support for complex hierarchical agent structures

## Language Components

### 1. Lexer (`m_lexer.py`)
- Tokenizes M language source code
- Supports keywords, operators, delimiters, and literals
- Handles comments and whitespace

### 2. Parser (`m_parser.py`)
- Builds Abstract Syntax Tree (AST) from tokens
- Validates syntax and structure
- Supports nested agent definitions

### 3. Compiler (`m_compiler.py`)
- Converts AST to executable specifications
- Generates execution plans
- Creates Python code templates

### 4. Executor (`m_executor.py`)
- Executes compiled swarm specifications
- Handles different workflow types
- Manages agent execution and data flow

### 5. Runtime (`m_runtime.py`)
- Complete interface for LLM-to-workflow communication
- Provides high-level API for swarm execution
- Includes MCP tool integration

## Syntax Guide

### Basic Swarm Structure

```m
swarm swarm_name {
    agent agent_name {
        role: "Agent role description"
        capabilities: "llm,mcp,research,analysis"
        inputs: "input1,input2"
        outputs: "output1,output2"
        config: {
            model: "gpt-4"
            temperature: 0.7
            timeout: 300
        }
    }
    
    workflow sequential|parallel|conditional|loop {
        agent_name(input: "input_data", output: "output_data")
    }
}
```

### Agent Definition

```m
agent agent_name {
    role: "Agent role description"
    capabilities: "llm,mcp,research,analysis"
    inputs: "input1,input2"
    outputs: "output1,output2"
    config: {
        model: "gpt-4"
        temperature: 0.7
        timeout: 300
        retry: 3
    }
}
```

### Workflow Types

#### Sequential Workflow
```m
workflow sequential {
    agent1(input: "data1", output: "result1")
    agent2(input: "result1", output: "result2")
}
```

#### Parallel Workflow
```m
workflow parallel {
    agent1(input: "data", output: "result1")
    agent2(input: "data", output: "result2")
    merger(input: "result1,result2", output: "final_result")
}
```

#### Conditional Workflow
```m
workflow conditional {
    analyzer(input: "data", output: "analysis,score")
    simple_agent(input: "data,analysis", output: "simple_result")
    advanced_agent(input: "data,analysis", output: "advanced_result")
    conditional: ["score < 5", "score >= 5"]
}
```

#### Loop Workflow
```m
workflow loop {
    optimizer(input: "current", output: "optimized")
    evaluator(input: "optimized", output: "score")
    checker(input: "score", output: "continue")
    loop: 10
}
```

### Data Flow Control

#### Input/Output Specification
```m
agent_name(input: "input_data", output: "output_data")
```

#### Data Transformation
```m
agent_name(input: "data", output: "result", transform: "to_string")
```

#### Data Filtering
```m
agent_name(input: "data", output: "result", filter: "non_empty")
```

#### Error Handling
```m
agent_name(input: "data", output: "result", error: "retry")
```

### Configuration Options

#### LLM Configuration
```m
config: {
    model: "gpt-4"
    temperature: 0.7
    max_tokens: 1000
}
```

#### MCP Configuration
```m
config: {
    timeout: 300
    retry: 3
    tools: ["file_search", "web_search"]
}
```

#### Execution Configuration
```m
config: {
    timeout: 600
    retry: 5
    error_handler: "retry"
}
```

## Agent Types

### LLM Agents
- Use language models for reasoning and generation
- Support various models (GPT-4, GPT-3.5-turbo, etc.)
- Configurable temperature and other parameters

### MCP Agents
- Use Model Context Protocol tools
- Support file operations, web search, code analysis
- Configurable timeouts and retry mechanisms

### Hybrid Agents
- Combine LLM and MCP capabilities
- Can use both reasoning and tool execution
- Flexible configuration options

## Workflow Execution Strategies

### Sequential Execution
- Agents execute in order
- Data flows from one agent to the next
- Suitable for linear processes

### Parallel Execution
- Multiple agents execute concurrently
- Independent agents can run simultaneously
- Results are merged at the end

### Conditional Execution
- Agents execute based on conditions
- Dynamic workflow paths
- Conditional branching support

### Loop Execution
- Agents execute repeatedly
- Termination conditions
- Iterative optimization support

## Data Flow Mechanisms

### Input Mapping
- Map data sources to agent inputs
- Support for multiple input sources
- Dynamic input resolution

### Output Processing
- Transform agent outputs
- Filter and validate results
- Map outputs to next agents

### Data Transformation
- Built-in transformation functions
- Custom transformation support
- Data format conversion

### Error Handling
- Retry mechanisms
- Skip failed steps
- Abort entire workflow
- Custom error handlers

## Integration with Existing System

### Workflow Agent Integration
```python
from agents.MParser import MRuntime

runtime = MRuntime()
result = runtime.process_llm_request(llm_response, user_command)
```

### MCP Tool Registration
```python
runtime.executor.register_mcp_tool("custom_tool", custom_function)
```

### Custom Agent Factories
```python
runtime.executor.register_agent_factory("custom_type", custom_factory)
```

## Examples

### Simple Research Swarm
```m
swarm research_swarm {
    agent research_agent {
        role: "Research and analysis specialist"
        capabilities: "llm,research,analysis"
        inputs: "user_query,context"
        outputs: "research_results,insights"
        config: {
            model: "gpt-4"
            temperature: 0.7
        }
    }
    
    workflow sequential {
        research_agent(input: "user_query", output: "research_results")
    }
}
```

### File Analysis Swarm
```m
swarm file_analysis_swarm {
    agent file_reader {
        role: "File reading specialist"
        capabilities: "mcp,file_operations"
        inputs: "file_path"
        outputs: "file_content"
        config: {
            timeout: 60
        }
    }
    
    agent content_analyzer {
        role: "Content analysis specialist"
        capabilities: "llm,analysis"
        inputs: "file_content"
        outputs: "analysis_results"
        config: {
            model: "gpt-4"
            temperature: 0.3
        }
    }
    
    workflow sequential {
        file_reader(input: "file_path", output: "file_content")
        content_analyzer(input: "file_content", output: "analysis_results")
    }
}
```

### Parallel Web Research
```m
swarm web_research_swarm {
    agent web_searcher_1 {
        role: "Primary web search specialist"
        capabilities: "mcp,web_search"
        inputs: "search_query"
        outputs: "search_results_1"
        config: {
            timeout: 120
        }
    }
    
    agent web_searcher_2 {
        role: "Secondary web search specialist"
        capabilities: "mcp,web_search"
        inputs: "search_query"
        outputs: "search_results_2"
        config: {
            timeout: 120
        }
    }
    
    agent result_merger {
        role: "Result merging specialist"
        capabilities: "llm,merge,analysis"
        inputs: "search_results_1,search_results_2"
        outputs: "merged_results"
        config: {
            model: "gpt-4"
            temperature: 0.4
        }
    }
    
    workflow parallel {
        web_searcher_1(input: "search_query", output: "search_results_1")
        web_searcher_2(input: "search_query", output: "search_results_2")
        result_merger(input: "search_results_1,search_results_2", output: "merged_results")
    }
}
```

## Usage Patterns

### LLM-to-Workflow Communication
1. User provides command to workflow agent
2. Workflow agent calls LLM for swarm specification
3. LLM responds with M language code
4. Workflow agent parses and executes the swarm
5. Results are returned to user

### Direct M Language Execution
```python
from agents.MParser import MRuntime

runtime = MRuntime()
m_code = """
swarm my_swarm {
    agent my_agent {
        role: "My agent"
        capabilities: "llm"
        inputs: "input"
        outputs: "output"
        config: {
            model: "gpt-4"
        }
    }
    
    workflow sequential {
        my_agent(input: "input", output: "output")
    }
}
"""

result = runtime.execute_m_code(m_code, {"input": "Hello, world!"})
```

### Template Generation
```python
template = runtime.generate_m_code_template("Research task")
print(template)
```

### Validation
```python
validation = runtime.validate_m_code(m_code)
if validation["valid"]:
    print(f"Valid code with {validation['agents_count']} agents")
else:
    print(f"Invalid code: {validation['error']}")
```

## Advanced Features

### Nested Swarms
- Agents can contain nested swarm definitions
- Hierarchical agent structures
- Complex workflow compositions

### Custom Transformations
- Extensible transformation system
- Custom filter functions
- Data processing pipelines

### Error Recovery
- Automatic retry mechanisms
- Graceful degradation
- Error reporting and logging

### Monitoring and Debugging
- Execution tracking
- Performance metrics
- Debug information

## Best Practices

### Agent Design
- Keep agents focused on specific roles
- Use clear input/output specifications
- Configure appropriate timeouts and retries

### Workflow Design
- Choose appropriate workflow types
- Consider data dependencies
- Plan for error scenarios

### Performance Optimization
- Use parallel execution when possible
- Minimize data transformations
- Configure appropriate timeouts

### Error Handling
- Implement proper error handlers
- Use retry mechanisms for transient failures
- Provide fallback options

## Future Enhancements

### Planned Features
- Advanced data flow patterns
- Dynamic agent creation
- Real-time monitoring
- Performance optimization
- Extended MCP tool support

### Language Extensions
- More workflow types
- Advanced conditionals
- Custom functions
- Template system

### Integration Improvements
- Better LLM integration
- Enhanced MCP support
- Monitoring and analytics
- Debugging tools

## Conclusion

M Language provides a powerful and flexible way for LLMs to communicate complex agent swarm specifications to workflow agents. Its declarative syntax, comprehensive feature set, and integration capabilities make it an ideal solution for building sophisticated multi-agent systems.

The language enables rapid development of complex solutions while maintaining clarity and maintainability. Whether used by LLMs or humans, M Language provides the tools needed to build and execute agent swarms with unlimited complexity. 