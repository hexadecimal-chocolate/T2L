# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 13:48:01 2020

@author: Daniel
"""
import sys

syntaxerror = "SyntaxError"
eoferror = "EOFError"
valueerror = "ValueError"

def Raise(e, m):
    print(e + ": " + m)
    sys.exit(1)