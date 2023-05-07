
# Name: Andrew Danial
# NetID: ADANIAL
# SBUID: 113338469

# Name: Christopher Lee
# NetID: lee111
# SBUID: 113378397
from decaf_checker import *
import decaf_typecheck

class_record = dict()
field_ids = {1}

constructor_ids = set()
constructors = set()

methods = set()
methods_ids = set()

curr_vars = dict()
curr_var_ids = set()

scope_stack = []
var_counter = 1

class Program():
    def __init__(self, class_list):
        self.class_list = class_list 
    
    def __str__(self):
        if self.class_list:
            return str(self.class_list)
        else:
            return ""

class ClassDeclList(): 
    def __init__(self, val, n):
        self.val = val
        self.next = n
                
        global class_record
        out_decls = ClassBodyDeclList(ClassBodyDecl(Method(Modifier(first="public"), Type("void"), "print", Formal(Type("constant"), Variable("")), None)), None)
       
        scan_int = ClassBodyDecl(Method(Modifier(first="public"), Type("int"), "scan_int", None, None))
        scan_float = ClassBodyDecl(Method(Modifier(first="public"), Type("float"), "scan_float", None, None))
        in_decls = ClassBodyDeclList(scan_int, ClassBodyDeclList(scan_float, None))
        class_record["In"] = Class("In", decls=in_decls)
        class_record["Out"] = Class("Out", decls=out_decls)
    
    def __str__(self):
        s = ""
        curr = self
        
        while curr:
            s += str(curr.val) if curr.val else ""
            curr = curr.next
        if s:
            s += "--------------------------------------------------------------------------"
        return s

class Class():
    def __init__(self, name, super_class = None, decls = None) :
        self.type = "class"
        self.name = name
        self.super_class = super_class
        self.decls = decls
        self.fields = []
        self.constructors = []
        self.methods = []
        
        curr = decls
        while curr:
            if isinstance(curr.curr.decl, Field):
                self.fields.append(curr.curr.decl)
            elif isinstance(curr.curr.decl, Constructor):
                self.constructors.append(curr.curr.decl)
            else:
                self.methods.append(curr.curr.decl)
            curr = curr.next
            
        
        
    def __str__(self):
        s = f"--------------------------------------------------------------------------\nClass Name: {self.name}\n"
        s += f'Superclass Name: {self.super_class}\n' if self.super_class else f'Superclass Name:\n'
        s += 'Fields:\n'
        field_declarations = {0}
        for fields in self.fields:
            a = fields.get_data()
            modifier = a[0].get_data()
            vis = "public" if modifier[0] == "public" else "private"
            modifier = "static" if modifier[1] or modifier[0] == "static" else "instance"
            var_decls = a[1]
            
            type = var_decls.type.type
            var_decls_list = var_decls.vars
            
            curr = var_decls_list
            while curr:
                if curr.current.name in field_declarations:
                    print(f"Error: {curr.current.name} already declared")
                    exit(1)
                field_declarations.add(curr.current.name)
                s += f'FIELD {len(field_ids)}, {curr.current.name}, {self.name}, {vis}, {modifier}, {type if type == "int" or type == "float" or type == "boolean" else f"user({type})"}\n'
                field_ids.add(len(field_ids) + 1)
                curr = curr.next

        s += "Constructors:\n"
        for constructor in self.constructors:
            formals_declared = {0}
            vars_declared = {0}
            curr = constructor.formals
            while curr:
                if curr.current.variable.name in formals_declared:
                    print(f"Error: {curr.current.variable.name} already declared")
                    exit(1)
                formals_declared.add(curr.current.variable.name)
                curr = curr.next
            for i in constructor.block.var_decls:
                curr = i.vars
                while curr:
                    if curr.current.name in field_declarations or curr.current.name in vars_declared or curr.current.name in formals_declared:
                        print(f"Error: {curr.current.name} already declared")
                        exit(1)
                    vars_declared.add(curr.current.name)
                    curr = curr.next
            s += str(constructor)
            
        s += "Methods:\n"
        
        for method in self.methods:
            modifier = method.visibility if method.visibility else "private"
            formals_declared = {0}
            vars_declared = {0}
            curr = method.parameters
            
            while curr:
                if curr.current.variable.name in formals_declared:
                    print(f"Error: {curr.current.variable.name} already declared")
                    exit(1)
                formals_declared.add(curr.current.variable.name)
                curr = curr.next
            
            for i in method.body.var_decls:
                curr = i.vars
                while curr:
                    if curr.current.name in field_declarations or curr.current.name in vars_declared or curr.current.name in formals_declared:
                        print(f"Error: {curr.current.name} already declared")
                        exit(1)
                    vars_declared.add(curr.current.name)
                    curr = curr.next
            applicability = "static" if method.applicability else "instance"
            s += f'METHOD: {method.id}, {method.name}, {self.name}, {modifier}, {applicability}, {method.returnType}\n'
            s += str(method)
            
        return s
    
    def isSubclass(self, otherClass):
        if (self.name == otherClass.name):
            return True
        elif (self.super_class != None):
            if (self.super_class != otherClass): 
                return self.super_class.isSubclass(otherClass)
            else:
                return True
        return False
    
class ClassBodyDeclList():
    def __init__(self, curr, n):
        self.curr = curr 
        self.next = n
        
class ClassBodyDecl():
    def __init__(self, decl) -> None:
        self.decl = decl

class Field():
    def __init__(self, modifier, var_decl):
        self.modifier = modifier
        self.var_decl = var_decl
    
    def get_data(self):
        return [self.modifier, self.var_decl]
    
class Modifier():
    def __init__(self, first = None, second = None):
        self.first = first
        self.second = second
    
    def get_data(self):
        return [self.first, self.second]

class VarDecl():
    def __init__(self, type, vars) -> None:
        self.type = type
        self.vars = vars

class Type():
    def __init__(self, type, isLiteral=False) -> None:
        self.type = type
        self.category = None

        if (self.type in ["int", "float", "boolean", "string", "void", "error", "null"]):
            self.category = "elementary"
        elif (isLiteral):
            self.category = "classLiteral"
        else:
            self.category = "user"

    def __str__(self):
        return f'{self.type}'
    
    def isSubtype(self, otherType):
        #Type T is a subtype of itself
        if (self.type == otherType.type):
            return True

        #int is a subtype of float
        if (self.type == "int" and otherType.type == "float") or (self.type == "float" and otherType.type == "int"):
            return True

        #user(A) is a subtype of user(B) if A is a subclass of B.
        if (self.category == "user" and otherType.category == "user"):
            return self.isSubclass(otherType.type)

        #null is a subtype of user(A) for any class A
        if (self.type == "null" and self.category == "user"):
            return True

        #class-literal(A) is a subtype of class-literal(B) if A is a subclass of B
        if (self.category == "classLiteral" and otherType.category == "classLiteral"):
            return self.type.isSubclass(otherType.type)
        
        return False
    
class Variables():
    def __init__(self, current = None, n = None) -> None:
        self.current = current
        self.next = n

    def getList(self):
        variablesList = []
        head = self.current
        next = self.next
        while (head != None):
            variablesList.append(head)
            if (next == None):
                break
            head = next.current
            next = next.next
        return variablesList
        
class VariablesCont():
    def __init__(self, current = None, n = None) -> None:
        self.current = current
        self.next = n
        
class Variable():
    def __init__(self, name) -> None:
        self.name = name
    def __str__(self) -> str:
        return f'{self.name}'
    
class Constructor():
    def __init__(self, modifier, name, formals, block) -> None:
        self.id = len(constructor_ids) + 1
        constructor_ids.add(len(constructor_ids) + 1)
        self.modifier = modifier
        self.name = name
        self.formals = formals
        self.block = block
        self.current_table = curr_vars
        curr_vars.clear()
        curr_var_ids.clear()
    def __str__(self) -> str:
        s = ""
        modifier = self.modifier.get_data()
        modifier = modifier[0] if modifier[0] == "public" else "private"
        s += f'CONSTRUCTOR: {self.id}, {modifier}\n'
        
        formals_table = []
        var_table = []
        curr = self.formals
        param_counter = 0
        while curr:
            param_counter += 1
            formals_table.append([curr.current.type, curr.current.variable])
            curr = curr.next
        s += f"Constructor Parameters:"
        for i in range(1, len(formals_table) + 1):
            if i == 1:
                s += " " 
                s += str(i)
            else:
                s += f', {i}'
        s += "\n"
        s += "Variable Table:\n"
        for i, var in enumerate(formals_table):
            s += f"VARIABLE {i+1}, {var[1]}, formal, {var[0]}\n"
        
        index = 0
        for i in self.block.var_decls:
            print(i)
            curr = i.vars
            length = 0
            var_table.append([i.type])
            while curr:
                var_table[index].append(curr.current.name)
                length += 1
                curr = curr.next
            index += 1

        counter = len(formals_table) + 1 
        for i, var in enumerate(var_table):
            for x, element in enumerate(var):
                if x == 0:
                    continue
                s += f"VARIABLE {counter}, {element}, local, {var[0]}\n"
                counter += 1
        
        s += "Constructor Body:"
        s += str(self.block) + "\n"
        return s
    
class FormalList():
    def __init__(self, curr, n) -> None:
        self.current = curr
        self.next = n
        pass

    def getList(self):
        formalList = []
        head = self.current
        next = self.next
        while (head != None):
            formalList.append(head)
            if (next == None):
                break
            head = next.current
            next = next.next
        return formalList

    
class FormalCont():
    def __init__(self, curr, n) -> None:
        self.current = curr
        self.next = n
        pass
    
class Formal():
    def __init__(self, type, variable) -> None:
        self.type = type
        self.variable = variable

    def getList(self):
        return [self]
    
class StmtList():
    def __init__(self, current, n):
        self.current = current
        self.next = n
        pass
    
class Stmt():
    def __init__(self) -> None:
        pass
    
class Expr():
    def __init__(self, lhs = None, op = None, rhs = None) -> None:
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

class Method():
    def __init__(self, modifier, type, name, formals, block) -> None:
        self.name = name
        self.id = len(methods_ids) + 1
        methods_ids.add(len(methods_ids) + 1)
        self.visibility = modifier.first 
        self.applicability = modifier.second #this may not exist
        self.parameters = formals
        self.returnType = type
        self.body = block
        self.current_table = curr_vars
        curr_vars.clear()
        curr_var_ids.clear()
    def __str__(self) -> str:
        s = ""
        formals_table = []
        var_table = []
        curr = self.parameters
        param_counter = 0
        while curr:
            param_counter += 1
            formals_table.append([curr.current.type, curr.current.variable])
            curr = curr.next
        s += f"Method Parameters:"
        for i in range(1, len(formals_table) + 1):
            if i == 1:
                s += " "
                s += str(i)
            else:
                s += f', {i}'
        s += "\n"
        s += "Variable Table:\n"
        for i, var in enumerate(formals_table):
            s += f"VARIABLE {i+1}, {var[1]}, formal, {var[0]}\n"
            
        index = 0
        for i in self.body.var_decls:
            curr = i.vars
            length = 0
            var_table.append([i.type])
            while curr:
                var_table[index].append(curr.current)
                length += 1
                curr = curr.next
            index += 1
            
        var_map = dict()
        self.var_table = var_table
        counter = len(formals_table) + 1 
        for i, var in enumerate(var_table):
            for x, element in enumerate(var):
                if x == 0:
                    continue
                s += f"VARIABLE {counter}, {element.name}, local, {var[0]}\n"
                var_map[element.name] = counter
                counter += 1
        s += "Method Body:"
        s += str(self.body) + "\n"
        
        return s
# ***** STATEMENTS *****

class IfStmt():
    def __init__(self, expr, thenStmt, elseStmt, lineStart, lineEnd) -> None:
        self.expr = expr
        self.thenStmt = thenStmt
        self.elseStmt = elseStmt
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.typeCorrect = None

    def __str__(self):
        s = ""
        if (self.elseStmt == None): #if statement
            s = "If( " + str(self.expr) + ", " + str(self.thenStmt) + " )"
        else:
            if str(self.thenStmt) and str(self.elseStmt):
                s = "If( " + str(self.expr) + ", " + str(self.thenStmt) + ", " + "Else " + str(self.elseStmt) + " )" 
            if not str(self.elseStmt) and not str(self.thenStmt):
                s = "If( " + str(self.expr) + " )" 
            if str(self.elseStmt) and not str(self.thenStmt):
                #s = "If( " + str(self.expr) + ", " + str(self.thenStmt) + ", " + "Else " + str(self.elseStmt) + " )" 
                s = "If ( " + str(self.expr) + ",\nElse " + str(self.elseStmt) + " )"
        
        return s
    
    def typeCheck(self): 
        if (self.typeCorrect == None):
            if (str(self.expr.getType()) != "boolean" or (self.thenStmt and self.thenStmt.typeCheck() == False) or (self.elseStmt and self.elseStmt.typeCheck() == False)):
                self.typeCorrect = False
            else:
                self.typeCorrect = True
        return self.typeCorrect
        
class WhileStmt():
    def __init__(self, expr, stmt, lineStart, lineEnd) -> None:
        self.expr = expr #loop condition 
        self.stmt = stmt #loop body
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.typeCorrect = None

    def __str__(self):
        s = "While( " + str(self.expr) + ", " + str(self.stmt) + " )" if str(self.stmt) else "While( " + str(self.expr) + " )"
        return s
    
    def typeCheck(while_stmt): 
        if (while_stmt.typeCorrect == None):
            if (while_stmt.expr.getType().type != "boolean" or while_stmt.stmt.typeCheck() == False):
                while_stmt.typeCorrect = False
            else:
                while_stmt.typeCorrect = True
        return while_stmt.typeCorrect

class ForStmt():
    def __init__(self, initializerExpr, loopExpr, updateExpr, stmt, lineStart, lineEnd) -> None:
        self.initializerExpr = initializerExpr
        self.loopExpr = loopExpr #loop condition
        self.updateExpr = updateExpr 
        self.stmt = stmt
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.typeCorrect = None

    def __str__(self):
        s = "For( " + str(self.initializerExpr) + ", " + str(self.loopExpr) + ", " + str(self.updateExpr) + ", " + str(self.stmt) + " )"
        return s
    
    def typeCheck(self): 
        if (self.typeCorrect == None):
            if (self.loopExpr.getType().type != "boolean" or self.initializerExpr.getType().type == "error" or self.updateExpr.getType().type  == "error" or self.stmt.typeCheck() == False):
                self.typeCorrect = False
            else:
                self.typeCorrect = True
        return self.typeCorrect
class ReturnStmt():
    def __init__(self, returnValue, lineStart, lineEnd) -> None:
        self.returnValue = returnValue
        self.lineStart = lineStart
        self.lineEnd = lineEnd 
        self.typeCorrect = None

    def __str__(self):
        s = "Return( " + str(self.returnValue) + " )"
        return s

    def typeCheck(self): 
        if (self.typeCorrect == None):
            #If the expression is empty, then the declared return type of the method must be void (and viceversa).
            #TODO
            pass
        return self.typeCorrect

class ExprStmt():
    def __init__(self, expr, lineStart, lineEnd) -> None:
        self.expr = expr
        self.lineStart = lineStart
        self.lineEnd = lineEnd   
        self.typeCorrect = None

    def __str__(self):
        s = "Expr( " + str(self.expr) + " )"
        return s 
    
    def typeCheck(self): 
        if (self.typeCorrect == None):
            if (self.expr.getType().category == "error"):
                self.typeCorrect = False
            else:
                self.typeCorrect = True
        return self.typeCorrect

class BlockStmt():
    def __init__(self, stmts, lineStart, lineEnd) -> None:
        self.stmts = stmts
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.var_decls = []
        self.typeCorrect = None
        for stmt in self.stmts:
            if isinstance(stmt, VarDecl):
                self.var_decls.append(stmt)
        
    def __str__(self):
        if not self.stmts:
            return ""
        s = "\nBlock([\n" 
        for i, stmt in enumerate(self.stmts):
            if not isinstance(stmt, VarDecl):
                if i != len(self.stmts) - 1:
                    s += str(stmt) + ", "
                else: 
                     s += str(stmt)
            else:
                self.var_decls.append(stmt)
        s += "\n])"
        return s 
    
    def typeCheck(self): 
        
        if (self.typeCorrect == None):
            self.typeCorrect = True
            for stmt in self.stmts:
                if not isinstance(stmt, VarDecl):
                    if (stmt.typeCheck() == False):
                        self.typeCorrect = False
        return self.typeCorrect

class BreakStmt():
    def __init__(self, lineStart, lineEnd) -> None:
        self.lineStart = lineStart
        self.lineEnd = lineEnd  
    
    def __str__(self):
        s = "Break( " + " )"
        return s 

class ContinueStmt():
    def __init__(self, lineStart, lineEnd) -> None:
        self.lineStart = lineStart
        self.lineEnd = lineEnd 

    def __str__(self):
        s = "Continue( " + " )"
        return s 

class SkipStmt():
    def __init__(self, lineStart, lineEnd) -> None:
        self.lineStart = lineStart
        self.lineEnd = lineEnd 

    def __str__(self):
        s = "Skip( " + " )"
        return s 
    
# ***** EXPRESSIONS *****

class ConstantExpr():
    def __init__(self, version, info, lineStart, lineEnd, type) -> None:
        self.version = version
        self.info = info
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = Type(type) #already in the parameter

    def __str__(self):
        s = ""
        if (self.info == None):
            s = "Constant(" + str(self.version) + ")"
        else:
            s = "Constant(" + str(self.version) + "-constant(" + str(self.info) + ")" + ")"
        return s
    
    def getType(self):
        return self.type

class VarExpr():
    def __init__(self, idVar, lineStart, lineEnd, unique_id, stack=None) -> None:
        self.idVar = idVar
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.unique_id = unique_id
        self.scope_stack = stack
        self.type = None
        
    def __str__(self):
        s = "Variable(" + str(self.unique_id) + ")"
        return s
    
    def getType(self):
        if (self.type == None):
            for i in reversed(self.scope_stack):
                for j in i.keys():
                    if self.idVar in j:
                        self.type = Type(j[0])
        return self.type

class UnaryExpr():
    def __init__(self, operand, unary, lineStart, lineEnd) -> None:
        self.operand = operand
        self.unary = unary
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None
        
    def __str__(self):
        s = ""
        if (self.unary == "+"):
            s = "Variable(" + str(self.operand) + ")"
        else:
            s = "Unary(" + str(self.unary) + str(self.operand) + ")"   
        return s
    
    def getType(self):
        if (self.type == None):
            if (self.unary == '!'):
                if (self.operand.getType().type == "boolean"):
                    self.type = Type("boolean")
                else:
                    print("Error: Unary type error")
                    self.type = Type("error")
            elif(self.unary == "-" or self.unary =="+"): 
                if (self.operand.getType().type == "int"):
                    self.type = Type("int")
                elif (self.operand.getType().type == "float"):
                    self.type = Type("float")
                else:
                    print("Error: Unary type error")  
                    self.type = Type("error")
        return self.type
    
class BinaryExpr():
    def __init__(self, operand1, operand2, operator, lineStart, lineEnd) -> None:
        self.operand1 = operand1
        self.operand2 = operand2
        self.operator = operator
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.operator_table = {"+": "add", "-": "sub", "*": "mul", "/": "div", 
                               "&&": "and", "||": "or", 
                               "==": "eq", "!=": "neq", 
                               "<": "lt", ">": "gt",
                               "<=": "leq", ">=": "geq"}
        self.type = None
        
        
    def __str__(self):
        s = "Binary(" + str(self.operator_table[self.operator]) + ", " + str(self.operand1) + ", " + str(self.operand2) + ")"
        return s
    
    def getType(self):
        if (self.type == None): 
            if(self.operator in ["+", "-", "*", "/"]): #arithmetic operations
                if (self.operand1.getType().type == "int" and self.operand2.getType().type == "int"):
                    self.type = Type("int")
                elif (self.operand1.getType().type == "float" or self.operand2.getType().type == "float"):
                    self.type = Type("float")
                else:
                    print("Error: Binary type error (arithmetic operations)")
                    self.type = Type("error")
                    
            elif (self.operator in ["&&", "||"]): #boolean operations
                if (self.operand1.getType().type == "boolean" and self.operand2.getType().type == "boolean"):
                    self.type = Type("boolean")
                else:
                    print("Error: Binary type error (boolean operations)")
                    self.type = Type("error")
                    exit(1)
            elif (self.operator in [">", ">=", "<", "<="]): #arithmetic comparisons
                print(self.operand1.getType().type)
                print(self.operand2.getType().type)
                if ((self.operand1.getType().type == "int" or self.operand1.getType().type == "float")
                    and (self.operand2.getType().type == "int" or self.operand2.getType().type == "float")):
                    self.type = Type('boolean')
                else:
                    print("Error: Binary type error (arithmetic comparisons)")
                    self.type = Type("error")
                    exit(1)
            elif (self.operator in ["==","!="]): #equality comparisons
                if ((self.operand1.getType().type == "int" or self.operand1.getType().type == "float")
                    and (self.operand2.getType().type == "int" or self.operand2.getType().type == "float")):
                    self.type = Type('boolean')
                else:
                    print("Error: Binary type error (equality comparisons)")
                    self.type = Type("error")
                    exit(1)
        return self.type
    
class AssignExpr():
    def __init__(self, leftExpr, rightExpr, lineStart, lineEnd) -> None:
        self.leftExpr = leftExpr
        self.rightExpr = rightExpr
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None

    def __str__(self):
        s = "Assign(" + str(self.leftExpr) + ", " + str(self.rightExpr) + ")"
        return s
    
    def getType(self):
        # print("left")
        # print(self.leftExpr)
        # print("right")
        # print(self.rightExpr.getType())
        if(self.type == None):
            if (self.leftExpr.getType().type != "error" and self.rightExpr.getType().type != "error"):
                if (self.rightExpr.getType().isSubtype(self.leftExpr.getType())):
                    self.type = self.rightExpr.getType()
                else:
                    print("Error: Assign type error (not subtype)")
                    self.type = Type("error")
                    exit(1)
            else:
                print("Error: Assign type error")
                self.type = Type("error")
                exit(1)
        return self.type

class AutoExpr():
    def __init__(self, operand, incOrDec, preOrPost, lineStart, lineEnd) -> None:
        self.operand = operand
        self.incOrDec = incOrDec
        self.preOrPost = preOrPost
        self.lineStart = lineStart
        self.lineEnd = lineEnd 
        self.type = None

    def __str__(self):
        s = "Auto(" + str(self.operand) + ", " + str(self.incOrDec) + ", " + str(self.preOrPost) + ")"
        return s
    
    def getType(self):
        if(self.type == None):
            if (self.operand.getType().type == "int" or self.operand.getType().type == "float"):
                self.type = self.operand.getType()
            else:
                print("Auto type error")
                self.type = Type("error")
        return self.type
    
class FieldAccessExpr():
    def __init__(self, base, fieldName, lineStart, lineEnd) -> None:
        self.base = base
        self.fieldName = fieldName
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None

    def __str__(self):
        s = "Field-access(" + str(self.base) + ", " + str(self.fieldName) + ")"
        return s
    
    def getType(self):
        #p's type is user(A), and z is a non-static field.
        #p's type is class-literal(A) and z is a static field.
        if (self.type == None):
            if(self.base.getType().category == "user" or self.base.getType().category == "classLiteral"):
                if(self.base.getType().category == "user"):
                    if isinstance(self.base, ThisExpr):
                        fieldResolve = self.fieldResolution(self.base.getType().type, self.fieldName, None) #it really should be instance
                    else:
                        fieldResolve = self.fieldResolution(class_record[self.base.getType().type], self.fieldName, None) #it really should be instance
                    if (fieldResolve == None):
                        self.type = Type("error")
                        print("Field resolve failed")
                    else:
                        self.type = fieldResolve.var_decl.type
                else:
                    fieldResolve = self.fieldResolution(self.base.getType().type, self.fieldName, "static") 
                    if (fieldResolve == None):
                        self.type = Type("error")
                        print("Field resolve failed")
                    else:
                        self.type = fieldResolve.var_decl.type
                    pass
            else:
                print("Field access type error")
                self.type = Type("error")
        return self.type

    def fieldResolution(self, fieldClass, fieldName, applicability):
        currentClass = fieldClass
        while (currentClass):
            for field in currentClass.fields:
                varsList = field.var_decl.vars.getList()
                for var in varsList:
                    if (var.name == fieldName):
                        if (field.modifier.first == "public" and field.modifier.second == applicability):
                            return field
            currentClass = currentClass.super_class
        return None


class MethodCallExpr():
    def __init__(self, base, methodName, exprs, lineStart, lineEnd) -> None:
        self.base = base
        self.methodName = methodName
        self.exprs = exprs
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None

    def __str__(self):
        s = ""
        if (self.exprs == None):
            s = "Method-call(" + str(self.base) + ", " + str(self.methodName) + ", [])" 
        else:
            s = "Method-call(" + str(self.base) + ", " + str(self.methodName) 
            for x in self.exprs:
                s += ", " + str(x) + " "  
            s += ")"
        return s  
    
    def getType(self):
        # print("here")
        # print(self.base)
        if (self.type == None):
            if isinstance(self.base, ClassReferenceExpr):
                if (self.base.classRef == "Out" or self.base.classRef == "In"):
                    self.type = Type("builtin")
                    return self.type
            if (self.base.getType().category == "user"):
                methodResolve = self.methodResolution(class_record[self.base.getType().type], self.methodName, self.exprs, None) 
                if (methodResolve == None):
                    self.type = Type("error")
                    print("Method resolve failed")
                else:
                    self.type = methodResolve.returnType
            elif (self.base.getType().category == "classLiteral"):
                methodResolve = self.methodResolution(self.base.getType().type, self.methodName, self.exprs, "static") 
                if (methodResolve == None):
                    self.type = Type("error")
                    print("Method resolve failed")
                else:
                    self.type = methodResolve.returnType
            else:
                self.type = Type("error")
                print("Method call type error")
        return self.type

    def methodResolution(self, methodClass, methodName, methodParameters, applicability):
        #keep checking methods from base class to super class and if nothing is found return none
        currentClass = methodClass
        while (currentClass.methods):
            for method in currentClass.methods:
                if (method.parameters == None):
                    parameterList = []
                else:
                    parameterList = method.parameters.getList()
                if (method.name == methodName and len(parameterList) == len(methodParameters) and applicability == method.applicability):
                    for i in range(len(methodParameters)):
                        if not (methodParameters[i].getType().isSubtype(parameterList[i].type)):
                            break
                    return method
                else:
                    return None
            currentClass = currentClass.super_class
        return None
    
class NewObjectExpr(): #constructor
    def __init__(self, baseClassName, exprs, lineStart, lineEnd) -> None:
        self.baseClassName = baseClassName
        self.exprs = exprs
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None

    def __str__(self):
        s = ""
        if (self.exprs == None):
            s = "New-object(" + str(self.baseClassName) + ", [])" 
        else:
            s = "New-object(" + str(self.baseClassName)
            for x in self.exprs:
                s += ", " + str(x) + " "  
            s += ")"
        return s    
    
    def getType(self):
        global class_record

        if (self.type == None):
            constructorResolve = self.constructorResolution(class_record[self.baseClassName], self.exprs)
            if (constructorResolve == None):
                self.type = Type("error")
                print("New object expr type error")
            else: 
                self.type = Type(self.baseClassName)
        return self.type

    
    def constructorResolution(self, constructorClass, constructorParameters):
        currentClass = constructorClass
        while (currentClass):
            for constructor in currentClass.constructors:
                if (constructor.formals == None):
                    parameterList = []
                else:
                    parameterList = constructor.formals.getList()
                if (constructor.name == self.baseClassName and len(parameterList) == len(constructorParameters)):
                    for i in range(len(constructorParameters)):
                        if not (constructorParameters[i].getType().isSubtype(parameterList[i].type)):
                            break
                    return constructor
                else:
                    return None
            currentClass = currentClass.super_class
        return None
    

class ThisExpr():
    def __init__(self, lineStart, lineEnd) -> None:
        self.lineStart = lineStart
        self.lineEnd = lineEnd  
        self.type = None

    def __str__(self):
        return "This"
    
    def getType(self):
        if(self.type == None):
            self.type = Type(decaf_typecheck.curr_ast)
            print(self.type)
        return self.type


class SuperExpr():
    def __init__(self, lineStart, lineEnd) -> None:
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None  

    def __str__(self):
        return "Super"
    
    def getType(self):
        if(self.type == None):
            if (decaf_typecheck.curr_ast.super_class == None):
                self.type = Type("error")
                print("Super type error (no superclass)")
            else:
                self.type = Type(decaf_typecheck.curr_ast.super_class)
        return self.type

class ClassReferenceExpr():

    def __init__(self, classRef, lineStart, lineEnd) -> None:
        self.classRef = classRef
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None

    def __str__(self):
        s = "Class-reference( " + str(self.classRef) + " )"
        return s
    
    def getType(self):
        global class_record
        if (self.type == None):
            if (self.classRef not in class_record.keys()):
                self.type = Type("error")
                print("Class reference does not exist")
            else:
                self.type = Type(class_record[self.classRef], isLiteral=True)
        return self.type
    

