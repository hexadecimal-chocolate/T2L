# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 09:58:12 2020

@author: Daniel
"""

import parse as p
import exec as ex
import lexer as l
import error as er

def Run(file, env={}):
    lexed = l.Lex().tokenize(file)
    #print(lexed)
    #for tok in lexed:
    #    print(tok)
    parser = p.Parse()
    parsed = parser.parse(lexed)
    try:
        pass
        #print(parsed, "\n\n\n")
    except Exception:
        pass
    execute = ex.Exec()
    execute.env = env
    try:
        execute.Walk(parsed)
    except TypeError:
        er.Raise(er.syntaxerror, "Expected semicolon")
        
    print("\n\n")
    print(execute.env)
    print("\n\n")
    return (parsed, execute.env)

with open("t2lcode/main.t2l", "r") as f:
    ps, env = Run(f.read())

with open("test.t2l", "r") as f:
    #env["test"] = {"Hi": "Hi"}
    ps, e = Run(f.read(), env)