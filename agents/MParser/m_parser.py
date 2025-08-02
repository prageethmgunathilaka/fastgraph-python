"""
M Language Parser
Builds Abstract Syntax Tree (AST) from tokens
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from .m_lexer import Token, TokenType


@dataclass
class ASTNode:
    """Base AST node"""
    node_type: str
    line: int
    column: int


@dataclass
class AgentDefinition(ASTNode):
    """Agent definition node"""
    name: str
    role: str
    capabilities: List[str]
    inputs: List[str]
    outputs: List[str]
    config: Dict[str, Any]
    body: Optional['SwarmDefinition'] = None


@dataclass
class SwarmDefinition(ASTNode):
    """Swarm definition node"""
    name: str
    agents: List[AgentDefinition]
    workflow: 'WorkflowDefinition'
    config: Dict[str, Any]


@dataclass
class WorkflowDefinition(ASTNode):
    """Workflow definition node"""
    type: str  # 'sequential', 'parallel', 'conditional', 'loop'
    steps: List['WorkflowStep']
    conditions: Optional[List[str]] = None
    max_iterations: Optional[int] = None


@dataclass
class WorkflowStep(ASTNode):
    """Workflow step node"""
    agent_name: str
    inputs: List[str]
    outputs: List[str]
    transform: Optional[str] = None
    filter: Optional[str] = None
    timeout: Optional[int] = None
    retry: Optional[int] = None
    error_handler: Optional[str] = None


@dataclass
class DataFlow(ASTNode):
    """Data flow definition"""
    source: str
    target: str
    transform: Optional[str] = None
    condition: Optional[str] = None


@dataclass
class Expression(ASTNode):
    """Expression node"""
    operator: str
    left: Optional['Expression'] = None
    right: Optional['Expression'] = None
    value: Optional[Any] = None


class MParser:
    """Parser for M language"""
    
    def __init__(self):
        self.tokens: List[Token] = []
        self.current = 0
        self.errors: List[str] = []
    
    def parse(self, tokens: List[Token]) -> SwarmDefinition:
        """Parse tokens into AST"""
        self.tokens = tokens
        self.current = 0
        self.errors = []
        
        try:
            return self.parse_swarm()
        except Exception as e:
            self.errors.append(f"Parse error: {str(e)}")
            raise
    
    def current_token(self) -> Token:
        """Get current token"""
        if self.current >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[self.current]
    
    def peek(self, offset: int = 1) -> Token:
        """Peek at token ahead"""
        if self.current + offset >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[self.current + offset]
    
    def advance(self) -> Token:
        """Advance to next token"""
        if self.current < len(self.tokens):
            token = self.tokens[self.current]
            self.current += 1
            return token
        return self.tokens[-1]  # EOF token
    
    def match(self, expected_type: TokenType) -> Token:
        """Match and consume expected token type"""
        token = self.current_token()
        if token.type == expected_type:
            return self.advance()
        else:
            raise SyntaxError(f"Expected {expected_type.value}, got {token.type.value} at line {token.line}")
    
    def check(self, expected_type: TokenType) -> bool:
        """Check if current token matches expected type"""
        return self.current_token().type == expected_type
    
    def parse_swarm(self) -> SwarmDefinition:
        """Parse swarm definition"""
        token = self.current_token()
        
        if token.type == TokenType.SWARM:
            self.advance()  # consume 'swarm'
            name = self.match(TokenType.IDENTIFIER).value
            
            self.match(TokenType.LBRACE)
            
            agents = []
            workflow = None
            config = {}
            
            while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
                if self.check(TokenType.AGENT):
                    agents.append(self.parse_agent())
                elif self.check(TokenType.WORKFLOW):
                    workflow = self.parse_workflow()
                elif self.check(TokenType.IDENTIFIER):
                    config.update(self.parse_config())
                else:
                    self.advance()  # skip unknown tokens
            
            self.match(TokenType.RBRACE)
            
            return SwarmDefinition(
                node_type="swarm",
                line=token.line,
                column=token.column,
                name=name,
                agents=agents,
                workflow=workflow,
                config=config
            )
        else:
            raise SyntaxError(f"Expected 'swarm', got {token.type.value}")
    
    def parse_agent(self) -> AgentDefinition:
        """Parse agent definition"""
        token = self.current_token()
        self.advance()  # consume 'agent'
        
        name = self.match(TokenType.IDENTIFIER).value
        
        self.match(TokenType.LBRACE)
        
        role = ""
        capabilities = []
        inputs = []
        outputs = []
        config = {}
        body = None
        
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            if self.check(TokenType.ROLE):
                self.advance()
                self.match(TokenType.COLON)
                role = self.match(TokenType.STRING).value.strip('"\'')
            elif self.check(TokenType.CAPABILITIES):
                self.advance()
                self.match(TokenType.COLON)
                value = self.match(TokenType.STRING).value.strip('"\'')
                capabilities = [cap.strip() for cap in value.split(',')]
            elif self.check(TokenType.INPUTS):
                self.advance()
                self.match(TokenType.COLON)
                value = self.match(TokenType.STRING).value.strip('"\'')
                inputs = [inp.strip() for inp in value.split(',')]
            elif self.check(TokenType.OUTPUTS):
                self.advance()
                self.match(TokenType.COLON)
                value = self.match(TokenType.STRING).value.strip('"\'')
                outputs = [out.strip() for out in value.split(',')]
            elif self.check(TokenType.CONFIG):
                self.advance()
                self.match(TokenType.COLON)
                config.update(self.parse_config())
            elif self.check(TokenType.SWARM):
                body = self.parse_swarm()
            else:
                self.advance()  # skip unknown tokens
        
        self.match(TokenType.RBRACE)
        
        return AgentDefinition(
            node_type="agent",
            line=token.line,
            column=token.column,
            name=name,
            role=role,
            capabilities=capabilities,
            inputs=inputs,
            outputs=outputs,
            config=config,
            body=body
        )
    
    def parse_workflow(self) -> WorkflowDefinition:
        """Parse workflow definition"""
        token = self.current_token()
        self.advance()  # consume 'workflow'
        
        workflow_type = "sequential"  # default
        if self.check(TokenType.SEQUENTIAL):
            self.advance()
            workflow_type = "sequential"
        elif self.check(TokenType.PARALLEL):
            self.advance()
            workflow_type = "parallel"
        elif self.check(TokenType.CONDITIONAL):
            self.advance()
            workflow_type = "conditional"
        elif self.check(TokenType.LOOP):
            self.advance()
            workflow_type = "loop"
        elif self.check(TokenType.IDENTIFIER):
            workflow_type = self.advance().value
        
        self.match(TokenType.LBRACE)
        
        steps = []
        conditions = None
        max_iterations = None
        
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            if self.check(TokenType.IDENTIFIER):
                steps.append(self.parse_workflow_step())
            elif self.check(TokenType.CONDITIONAL):
                self.advance()
                conditions = self.parse_conditions()
            elif self.check(TokenType.LOOP):
                self.advance()
                max_iterations = int(self.match(TokenType.NUMBER).value)
            else:
                self.advance()  # skip unknown tokens
        
        self.match(TokenType.RBRACE)
        
        return WorkflowDefinition(
            node_type="workflow",
            line=token.line,
            column=token.column,
            type=workflow_type,
            steps=steps,
            conditions=conditions,
            max_iterations=max_iterations
        )
    
    def parse_workflow_step(self) -> WorkflowStep:
        """Parse workflow step"""
        token = self.current_token()
        agent_name = self.advance().value
        
        inputs = []
        outputs = []
        transform = None
        filter_expr = None
        timeout = None
        retry = None
        error_handler = None
        
        if self.check(TokenType.LPAREN):
            self.advance()
            while not self.check(TokenType.RPAREN):
                if self.check(TokenType.INPUT):
                    self.advance()
                    self.match(TokenType.COLON)
                    inputs = [inp.strip() for inp in self.match(TokenType.STRING).value.strip('"\'').split(',')]
                elif self.check(TokenType.OUTPUT):
                    self.advance()
                    self.match(TokenType.COLON)
                    outputs = [out.strip() for out in self.match(TokenType.STRING).value.strip('"\'').split(',')]
                elif self.check(TokenType.TRANSFORM):
                    self.advance()
                    self.match(TokenType.COLON)
                    transform = self.match(TokenType.STRING).value.strip('"\'')
                elif self.check(TokenType.FILTER):
                    self.advance()
                    self.match(TokenType.COLON)
                    filter_expr = self.match(TokenType.STRING).value.strip('"\'')
                elif self.check(TokenType.TIMEOUT):
                    self.advance()
                    self.match(TokenType.COLON)
                    timeout = int(self.match(TokenType.NUMBER).value)
                elif self.check(TokenType.RETRY):
                    self.advance()
                    self.match(TokenType.COLON)
                    retry = int(self.match(TokenType.NUMBER).value)
                elif self.check(TokenType.ERROR):
                    self.advance()
                    self.match(TokenType.COLON)
                    error_handler = self.match(TokenType.STRING).value.strip('"\'')
                else:
                    self.advance()  # skip unknown tokens
                
                if self.check(TokenType.COMMA):
                    self.advance()
            
            self.match(TokenType.RPAREN)
        
        return WorkflowStep(
            node_type="workflow_step",
            line=token.line,
            column=token.column,
            agent_name=agent_name,
            inputs=inputs,
            outputs=outputs,
            transform=transform,
            filter=filter_expr,
            timeout=timeout,
            retry=retry,
            error_handler=error_handler
        )
    
    def parse_conditions(self) -> List[str]:
        """Parse conditional expressions"""
        conditions = []
        self.match(TokenType.LBRACKET)
        
        while not self.check(TokenType.RBRACKET):
            if self.check(TokenType.STRING):
                conditions.append(self.advance().value.strip('"\''))
            if self.check(TokenType.COMMA):
                self.advance()
        
        self.match(TokenType.RBRACKET)
        return conditions
    
    def parse_config(self) -> Dict[str, Any]:
        """Parse configuration key-value pairs"""
        config = {}
        
        self.match(TokenType.LBRACE)
        
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            if self.check(TokenType.MODEL):
                self.advance()
                self.match(TokenType.COLON)
                config["model"] = self.match(TokenType.STRING).value.strip('"\'')
            elif self.check(TokenType.TEMPERATURE):
                self.advance()
                self.match(TokenType.COLON)
                number_token = self.match(TokenType.NUMBER)
                config["temperature"] = float(number_token.value)
            elif self.check(TokenType.IDENTIFIER):
                key = self.advance().value
                self.match(TokenType.COLON)
                if self.check(TokenType.STRING):
                    config[key] = self.advance().value.strip('"\'')
                elif self.check(TokenType.NUMBER):
                    config[key] = float(self.advance().value)
                elif self.check(TokenType.BOOLEAN):
                    config[key] = self.advance().value.lower() == 'true'
            else:
                self.advance()  # skip unknown tokens
        
        self.match(TokenType.RBRACE)
        
        return config 