# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 17:09:46 2020

@author: Daniel
"""

from sly import Lexer

class Lex(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, ID, WHILE, IF, ELSE, PRINT,
               PLUS, MINUS, TIMES, DIVIDE,
               EQ, LT, LE, GT, GE, NE, STRING, INPUT,
               AND, OR, FUNC, RETURN, OBJECT }


    literals = { '(', ')', '{', '}', ';', '=', ',', '.' }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['print'] = PRINT
    ID['input'] = INPUT
    ID['func'] = FUNC
    ID['return'] = RETURN
    ID['object'] = OBJECT
    
    AND = r'&&'
    OR = r'\|\|'

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += t.value.count('\n')
        #self.index = 0
        #print("hai")

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
    
    @_(r'\{')
    def lbrace(self, t):
        t.type = '{'      # Set token type to the expected literal
        self.nesting_level += 1
        return t

    @_(r'\}')
    def rbrace(self, t):
        t.type = '}'      # Set token type to the expected literal
        self.nesting_level -=1
        return t
    
    #@_(r"'[a-zA-Z_][a-zA-Z0-9_]*'")
    #@_(r'"[a-zA-Z_][a-zA-Z0-9_]*"')
    @_(r"'[^']*'")
    @_(r'"[^"]*"')
    def STRING(self, t):
        t.value = t.value[1:][:-1]
        return t
    
    def __init__(self):
        self.nesting_level = 0

if __name__ == "__main__":
    for tok in Lex().tokenize("\'hiasdasd\'"):
        print(tok)