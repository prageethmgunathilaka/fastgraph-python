"""
M Language Lexer
Tokenizes M language syntax for agent swarm specifications
"""

import re
from enum import Enum
from typing import List, Tuple, Optional
from dataclasses import dataclass


class TokenType(Enum):
    """Token types for M language"""
    # Keywords
    AGENT = "AGENT"
    SWARM = "SWARM"
    WORKFLOW = "WORKFLOW"
    PARALLEL = "PARALLEL"
    SEQUENTIAL = "SEQUENTIAL"
    CONDITIONAL = "CONDITIONAL"
    LOOP = "LOOP"
    ROLE = "ROLE"
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    TRANSFORM = "TRANSFORM"
    FILTER = "FILTER"
    MERGE = "MERGE"
    SPLIT = "SPLIT"
    WAIT = "WAIT"
    TIMEOUT = "TIMEOUT"
    RETRY = "RETRY"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    CAPABILITIES = "CAPABILITIES"
    INPUTS = "INPUTS"
    OUTPUTS = "OUTPUTS"
    CONFIG = "CONFIG"
    MODEL = "MODEL"
    TEMPERATURE = "TEMPERATURE"
    
    # Data types
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"
    
    # Operators
    ASSIGN = "ASSIGN"
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"
    COLON = "COLON"
    ARROW = "ARROW"
    PIPE = "PIPE"
    
    # Special
    IDENTIFIER = "IDENTIFIER"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    EOF = "EOF"


@dataclass
class Token:
    """Token with type, value, and position"""
    type: TokenType
    value: str
    line: int
    column: int


class MLexer:
    """Lexer for M language"""
    
    def __init__(self):
        # Define token patterns
        self.patterns = [
            # Keywords
            (TokenType.AGENT, r'\bagent\b'),
            (TokenType.SWARM, r'\bswarm\b'),
            (TokenType.WORKFLOW, r'\bworkflow\b'),
            (TokenType.PARALLEL, r'\bparallel\b'),
            (TokenType.SEQUENTIAL, r'\bsequential\b'),
            (TokenType.CONDITIONAL, r'\bconditional\b'),
            (TokenType.LOOP, r'\bloop\b'),
            (TokenType.ROLE, r'\brole\b'),
            (TokenType.INPUT, r'\binput\b'),
            (TokenType.OUTPUT, r'\boutput\b'),
            (TokenType.TRANSFORM, r'\btransform\b'),
            (TokenType.FILTER, r'\bfilter\b'),
            (TokenType.MERGE, r'\bmerge\b'),
            (TokenType.SPLIT, r'\bsplit\b'),
            (TokenType.WAIT, r'\bwait\b'),
            (TokenType.TIMEOUT, r'\btimeout\b'),
            (TokenType.RETRY, r'\bretry\b'),
            (TokenType.ERROR, r'\berror\b'),
            (TokenType.SUCCESS, r'\bsuccess\b'),
            (TokenType.FAILURE, r'\bfailure\b'),
            (TokenType.CAPABILITIES, r'\bcapabilities\b'),
            (TokenType.INPUTS, r'\binputs\b'),
            (TokenType.OUTPUTS, r'\boutputs\b'),
            (TokenType.CONFIG, r'\bconfig\b'),
            (TokenType.MODEL, r'\bmodel\b'),
            (TokenType.TEMPERATURE, r'\btemperature\b'),
            
            # Boolean literals
            (TokenType.BOOLEAN, r'\btrue\b|\bfalse\b'),
            
            # Numbers
            (TokenType.NUMBER, r'\d+\.?\d*'),
            
            # Strings (single or double quoted)
            (TokenType.STRING, r'"[^"]*"|\'[^\']*\''),
            
            # Operators
            (TokenType.ASSIGN, r'='),
            (TokenType.EQUALS, r'=='),
            (TokenType.NOT_EQUALS, r'!='),
            (TokenType.GREATER, r'>'),
            (TokenType.LESS, r'<'),
            (TokenType.GREATER_EQUAL, r'>='),
            (TokenType.LESS_EQUAL, r'<='),
            (TokenType.AND, r'&&'),
            (TokenType.OR, r'\|\|'),
            (TokenType.NOT, r'!'),
            
            # Delimiters
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
            (TokenType.LBRACE, r'\{'),
            (TokenType.RBRACE, r'\}'),
            (TokenType.LBRACKET, r'\['),
            (TokenType.RBRACKET, r'\]'),
            (TokenType.SEMICOLON, r';'),
            (TokenType.COMMA, r','),
            (TokenType.DOT, r'\.'),
            (TokenType.COLON, r':'),
            (TokenType.ARROW, r'->'),
            (TokenType.PIPE, r'\|'),
            
            # Comments
            (TokenType.COMMENT, r'//.*|/\*.*?\*/'),
            
            # Whitespace
            (TokenType.WHITESPACE, r'\s+'),
            (TokenType.NEWLINE, r'\n'),
            
            # Identifiers
            (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ]
        
        # Compile patterns
        self.compiled_patterns = [(token_type, re.compile(pattern, re.IGNORECASE)) 
                                 for token_type, pattern in self.patterns]
    
    def tokenize(self, source: str) -> List[Token]:
        """Tokenize the source code"""
        tokens = []
        line = 1
        column = 1
        pos = 0
        
        while pos < len(source):
            match = None
            match_token_type = None
            
            # Try to match each pattern
            for token_type, pattern in self.compiled_patterns:
                match = pattern.match(source, pos)
                if match:
                    match_token_type = token_type
                    break
            
            if not match:
                # No pattern matched - this is an error
                raise SyntaxError(f"Unexpected character at line {line}, column {column}: '{source[pos]}'")
            
            # Extract the matched text
            text = match.group(0)
            token_length = len(text)
            
            # Skip whitespace and comments
            if match_token_type not in [TokenType.WHITESPACE, TokenType.COMMENT]:
                # Create token
                token = Token(
                    type=match_token_type,
                    value=text,
                    line=line,
                    column=column
                )
                tokens.append(token)
            
            # Update position
            pos += token_length
            
            # Update line and column
            if match_token_type == TokenType.NEWLINE:
                line += 1
                column = 1
            else:
                column += token_length
        
        # Add EOF token
        tokens.append(Token(TokenType.EOF, "", line, column))
        
        return tokens
    
    def tokenize_file(self, file_path: str) -> List[Token]:
        """Tokenize a file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        return self.tokenize(source) 