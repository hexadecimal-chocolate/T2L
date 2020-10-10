# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 09:46:12 2020

@author: Daniel
"""
import tree
import error

class Exec():
    def __init__(self):
        self.env = {}
        self.curenv = "main"
        self.prevenv = "main"
        
        self.stack = []
    
    def Run(self, func):
        if type(func) == tree.Func:
            params = []
            
            for param in func.parameters:
                params.append(self.GetValue(param))
            
            return func.Run(params)
        elif type(func) == tree.Var:
            if self.curenv == "main":
                #if type(func.value) == tree.Func:
                if "." in func.name:
                    params = func.name.split(".")
                    current = self.GetValue(tree.DeclaredVar(params[0]))
                    if type(current) != dict:
                        #print("hai")
                        error.Raise(error.valueerror, "No object named " + func.name)
                    
                    for idex, i in enumerate(params):
                        if idex == 0:
                            continue
                        
                        #print(current, i, func.name)
                        
                        if i in current:
                            #print(type(current[i]) == dict)
                            if type(current[i]) == dict:
                                #print(i)
                                current = current[i]
                                continue
                
                    current[i] = self.GetValue(func.value)
                else:
                    self.env[func.name] = self.GetValue(func.value)
                #else:
                #    self.env[func.name] = func.value
        elif type(func) == tree.Wrapper:
            if func.type == "while":
                #sys.setrecursionlimit(100)
                while self.GetValue(func.expr):
                    #print(func.stmt)
                    return self.Walk(func.stmt)
            elif func.type == "if":
                if self.GetValue(func.expr):
                    return self.Walk(func.stmt)
                elif func.extra != []:
                    if func.extra[0] == "else":
                        return self.Walk(func.extra_stmt[0])
            elif func.type == "func":
                if self.curenv == "main":
                    self.env[func.extra[0]] = tree.DefinedFunc(func.stmt, func.expr)
        elif type(func) == tree.DeclaredFunc:
            if self.curenv == "main":
                if func.name not in self.env.keys():
                    error.Raise(error.valueerror, "No variable, function, or class called " + func.name)
                else:
                    if self.curenv == "main":
                        self.prevenv = self.curenv
                        self.curenv = {}
                        for idex, i in enumerate(self.env[func.name].parameters):
                            self.curenv[self.GetValue(i)] = self.RawToTree(self.GetValue(func.parameters[idex]))
                        self.Walk(self.env[func.name].stmt)
                        self.curenv = self.prevenv
            else:
                if func.name not in self.curenv.keys():
                    if func.name not in self.env.keys():
                        error.Raise(error.valueerror, "No variable, function, or class called " + func.name)
                    else:
                        self.prevenv = self.curenv
                        self.curenv = {}
                        for idex, i in enumerate(self.env[func.name].parameters):
                            self.curenv[self.GetValue(i)] = self.RawToTree(self.GetValue(func.parameters[idex]))
                        self.Walk(self.env[func.name].stmt)
                        self.curenv = self.prevenv
                else:
                    self.prevenv = self.curenv
                    self.curenv = {}
                    for idex, i in enumerate(self.env[func.name].parameters):
                        self.curenv[self.GetValue(i)] = self.RawToTree(self.GetValue(func.parameters[idex]))
                    self.Walk(self.curenv[func.name].stmt)
                    self.curenv = self.prevenv
        elif type(func) == tree.OtherFunc:
            if func.name == "return":
                return self.RawToTree(self.GetValue(func.expr))
    
    def Walk(self, node):
        #print("hai")
        try:
            if type(node) != list:
                error.Raise(error.syntaxerror, "Expected semicolon")
            for i in node:
                #print(i)
                r = self.Run(i)
                if r != None:
                    #print(self.curenv)
                    return r
        except TypeError:
            error.Raise(error.syntaxerror, "Expected semicolon")
    
    def GetValue(self, obj):
        #print(obj)
        if type(obj) == tree.Int or type(obj) == tree.Str:
            return obj.value
        elif type(obj) == tree.Op:
            
            left = obj.left
            right = obj.right
            
            if type(left) == tree.DeclaredVar:
                left = self.RawToTree(self.GetValue(left))
            if type(right) == tree.DeclaredVar:
                right = self.RawToTree(self.GetValue(right))
            
            if obj.op == "+":
                if left.Int(err=False) is None or right.Int(err=False) is None:
                    return self.GetValue(left.Str()) + self.GetValue(right.Str())
                else:
                    return self.GetValue(left.Int()) + self.GetValue(right.Int())
            elif obj.op == "-":
                return self.GetValue(left.Int()) - self.GetValue(right.Int())
            elif obj.op == "*":
                return self.GetValue(left.Int()) * self.GetValue(right.Int())
            elif obj.op == "/":
                return self.GetValue(left.Int()) / self.GetValue(right.Int())
        elif type(obj) == tree.DeclaredVar:
            #print("hai")
            if self.curenv == "main":
                if obj.name not in self.env.keys():
                    error.Raise(error.valueerror, "No variable, function, or class called " + obj.name)
                else:
                    return self.GetValue(self.env[obj.name])
            else:
                if obj.name not in self.curenv.keys():
                    if obj.name not in self.env.keys():
                        error.Raise(error.valueerror, "No variable, function, or class called " + obj.name)
                    else:
                        return self.GetValue(self.env[obj.name])
                else:
                    return self.GetValue(self.curenv[obj.name])
        elif type(obj) == tree.Func:
            if obj.builtin == True:
                return self.GetValue(self.Run(obj))
        elif type(obj) == tree.DeclaredFunc:
            func = obj
            if self.curenv == "main":
                if func.name not in self.env.keys():
                    error.Raise(error.valueerror, "No variable, function, or class called " + func.name)
                else:
                    if self.curenv == "main":
                        self.prevenv = self.curenv
                        self.curenv = {}
                        for idex, i in enumerate(self.env[func.name].parameters):
                            self.curenv[self.GetValue(i)] = self.RawToTree(self.GetValue(func.parameters[idex]))
                            #print(self.GetValue(i), self.GetValue(func.parameters[idex]))
                        t = self.Walk(self.env[func.name].stmt)
                        #print(t)
                        self.curenv = self.prevenv
                        return self.GetValue(t)
            else:
                if func.name not in self.curenv.keys():
                    if func.name not in self.env.keys():
                        error.Raise(error.valueerror, "No variable, function, or class called " + func.name)
                    else:
                        self.prevenv = self.curenv
                        self.curenv = {}
                        for idex, i in enumerate(self.env[func.name].parameters):
                            self.curenv[self.GetValue(i)] = self.RawToTree(self.GetValue(func.parameters[idex]))
                        t = self.Walk(self.env[func.name].stmt)
                        self.curenv = self.prevenv
                        return t
                else:
                    self.prevenv = self.curenv
                    self.curenv = {}
                    for idex, i in enumerate(self.env[func.name].parameters):
                        self.curenv[self.GetValue(i)] = self.RawToTree(self.GetValue(func.parameters[idex]))
                    t = self.Walk(self.curenv[func.name].stmt)
                    self.curenv = self.prevenv
                    return t
        elif type(obj) == tree.Compare:
            left = self.GetValue(self.RawToTree(self.GetValue(obj.left)))
            right = self.GetValue(self.RawToTree(self.GetValue(obj.right)))
            
            comp = obj.comp
            
            if obj.comp == "&&":
                comp = "and"
            elif obj.comp == "||":
                comp = "or"
            else:
                comp = obj.comp
                if type(left) == str:
                    left = self.GetValue(self.RawToTree(left).Int())
                if type(right) == str:
                    right = self.GetValue(self.RawToTree(right).Int())
            #print(left, obj.comp, right)
            d = {"left": left, "right": right}
            exec("a = left " + comp + " right", globals(), d)
            return d["a"]
        elif type(obj) == tree.Bool:
            return obj.value
        elif type(obj) == str:
            params = obj.split(".")
            if len(params) == 1:
                return obj
            current = self.GetValue(tree.DeclaredVar(params[0]))
            if type(current) != dict:
                #print("hai")
                error.Raise(error.valueerror, "No object named " + obj)
            
            for idex, i in enumerate(params):
                if idex == 0:
                    continue
                
                #print(current, i, obj)
                
                if i not in current.keys():
                    #print("hai")
                    error.Raise(error.valueerror, "No object named " + obj)
                
                if type(current[i]) == dict:
                    current = current[i]
                    continue
                
                #print(current[i])
                return self.GetValue(self.RawToTree(current[i]))
        else:
            return obj
    
    def RawToTree(self, obj):
        if type(obj) == str:
            return tree.Str(obj)
        elif type(obj) == int:
            return tree.Int(obj)
        else:
            return obj

def Input(obj):
    return tree.Str(input(obj))