# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 19:41:45 2020

@author: Daniel
"""
import error

class Op():
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Func():
    def __init__(self, method, parameters, loc=None, builtin=False, returns=False):
        self.loc = loc
        self.builtin = builtin
        self.method = method
        self.parameters = parameters
        self.returns = returns
    
    def Run(self, params):
        return self.method(*params)

class OtherFunc():
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class DefinedFunc():
    def __init__(self, stmt, parameters):
        self.stmt = stmt
        self.parameters = parameters

class DeclaredFunc():
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

class Int():
    def __init__(self, value):
        self.value = value
    
    def Int(self, err=True):
        return self
    
    def Str(self):
        return Str(str(self.value))
    
    def Bool(self):
        if self.value <= 0:
            return Bool(False)
        return Bool(True)

class Str():
    def __init__(self, value):
        self.value = value
    
    def Int(self, err=True):
        try:
            return Int(int(self.value))
        except ValueError as e:
            pass
        if err:
            error.Raise(error.valueerror, "Cannot make string " + self.value + " into int")
        else:
            return None
    
    def Str(self):
        return self
    
    def Bool(self):
        if self.value == "":
            return Bool(False)
        return Bool(True)

class Bool():
    def __init__(self, value):
        self.value = value
    
    def Bool(self):
        return self
    
    def Str(self):
        return Str(str(self.value))
    
    def Int(self, err=True):
        if err:
            error.Raise(error.valueerror, "Cannot make bool " + str(self.value) + " into int")
        return None

class Var():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class DeclaredVar():
    def __init__(self, name):
        self.name = name
        
class Compare():
    def __init__(self, left, comp, right):
        self.left = left
        self.right = right
        self.comp = comp

class Wrapper():
    def __init__(self, t, expr, stmt, extra=[], extra_stmt=[]):
        self.type = t
        self.expr = expr
        self.stmt = stmt
        self.extra = extra
        self.extra_stmt = extra_stmt