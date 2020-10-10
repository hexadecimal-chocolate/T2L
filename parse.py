# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 17:09:46 2020

@author: Daniel
"""

from sly import Parser
from sly.yacc import SlyLogger
from lexer import Lex
from tree import Op, Func, Int, Str, Var, DeclaredVar
from tree import Compare, Wrapper, DeclaredFunc, OtherFunc
import error
import exec as e
import io

class Parse(Parser):
    log = SlyLogger(io.StringIO())
    debugfile = 'parser.out'
    
    start = 'stmt'
    
    tokens = Lex.tokens
    
    precedence = (
       ('nonassoc', LT, GT, LE, GE, EQ, NE),
       ('left', PLUS, MINUS),
       ('left', TIMES, DIVIDE),
       ('right', 'UMINUS')
    )
    
    def __init__(self):
        self.parse_list = []

    # Grammar rules and actions
    @_('expr PLUS expr')
    def expr(self, p):
        return Op('+', p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return Op('-', p.expr0, p.expr1)

    @_('expr TIMES expr')
    def expr(self, p):
        return Op('*', p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return Op('/', p.expr0, p.expr1)
    
    @_('expr LE expr')
    @_('expr GE expr')
    @_('expr NE expr')
    @_('expr EQ expr')
    @_('expr LT expr')
    @_('expr GT expr')
    @_('expr AND expr')
    @_('expr OR expr')
    def expr(self, p):
        return Compare(p.expr0, p[1], p.expr1)

    @_('NUMBER')
    def expr(self, p):
        return Int(p.NUMBER)
    
    @_('STRING')
    def expr(self, p):
        return Str(p.STRING)
    
    @_('ID "." ID')
    def expr(self, p):
        return p.ID0 + "." + p.ID1
    
    @_('ID "." expr')
    def expr(self, p):
        #print(type(p.expr))
        if type(p.expr) != str:
            print(p.lineno)
            error.Raise(error.syntaxerror, "Variable name cannot be a non function or keyword")
        return p.ID + "." + p.expr
    
    @_('expr "." expr')
    def expr(self, p):
        if type(p.expr0) != str or type(p.expr1) != str:
            error.Raise(error.syntaxerror, "Variable name cannot be a non function or keyword")
        return p.expr0 + "." + p.expr1
    
    @_('expr "." ID')
    def expr(self, p):
        if type(p.expr) != str:
            error.Raise(error.syntaxerror, "Variable name cannot be a non function or keyword")
        return p.expr + "." + p.ID
    
    @_('ID')
    def expr(self, p):
        return DeclaredVar(p.ID)
    
    @_('ID "(" param ")"')
    @_('ID "(" expr ")"')
    def expr(self, p):
        if type(p[2]) != list:
            d = [p[2].value]
        else:
            d = list(p[2])
        return DeclaredFunc(p.ID, d)
    
    @_('ID "(" ")"')
    def expr(self, p):
        return DeclaredFunc(p.ID, [])
    
    @_('ID "=" expr')
    @_('expr "=" expr')
    @_('PRINT "(" expr ")"')
    def stmt(self, p):
        #print(p.expr)
        if p[1] == "(":
            return Func(print, [p.expr], builtin=True)
        else:
            return Var(p[0], p[2])
    
    @_('RETURN expr')
    def stmt(self, p):
        return OtherFunc("return", p.expr)
    
    @_('PRINT')
    @_('INPUT')
    def expr(self, p):
        if p[0] == "print":
            f = print
        else:
            f = input
        return Wrapper("func", ["txt"], [Func(f, ["txt"], builtin=True)])
    
    @_('INPUT "(" expr ")"')
    def expr(self, p):
        return Func(e.Input, [p.expr], builtin=True, returns=True)
    
    @_('OBJECT')
    def expr(self, p):
        return {}
    
    @_('WHILE expr "{" stmt "}"')
    def stmt(self, p):
        return Wrapper("while", p.expr, p.stmt)
    
    @_('IF expr "{" stmt "}"')
    def stmt(self, p):
        return Wrapper("if", p.expr, p.stmt)
    
    @_('IF expr "{" stmt "}" ELSE "{" stmt "}"')
    def stmt(self, p):
        return Wrapper("if", p.expr, p.stmt0, ["else"], [p.stmt1])
    
    @_('FUNC ID param "{" stmt "}"')
    @_('FUNC ID expr "{" stmt "}"')
    def stmt(self, p):
        if type(p[2]) != list and type(p[2]) != Str:
            error.Raise(error.syntaxerror, "Func only takes strings as parameters")
        elif type(p[2]) == Str:
            d = [p[2].value]
        else:
            d = list(p[2])
        return Wrapper("func", d, p.stmt, [p.ID])
    @_('FUNC ID "{" stmt "}"')
    def stmt(self, p):
        return Wrapper("func", [], p.stmt, [p.ID])
    
    @_('expr "," expr')
    def param(self, p):
        return [p.expr0, p.expr1]
    
    @_('expr "," param')
    def param(self, p):
        d = [p.expr]
        d.extend(p.param)
        return d
    
    @_('param "," param')
    def param(self, p):
        d = p.param0
        d.extend(p.param1)
        return d
    
    @_('stmt ";" stmt')
    def stmt(self, p):
        l = [p.stmt0]
        l.extend(p.stmt1)
        return l
    
    @_('stmt ";"')
    def stmt(self, p):
        l = [p.stmt]
        return l
    
    @_('expr ";" stmt')
    def stmt(self, p):
        l = [p.expr]
        l.extend(p.stmt)
        return l
    
    @_('expr ";"')
    def stmt(self, p):
        l = [p.expr]
        return l
    
    @_('MINUS expr %prec UMINUS') 
    def expr(self, p): 
        return Int(-p.expr.value)
    
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr
    
    def error(self, p):
        if p:
            error.Raise(error.syntaxerror, "Syntax error at token " + p.type + " line " + str(p.lineno))
        else:
            error.Raise(error.eoferror, "Syntax error at EOF")