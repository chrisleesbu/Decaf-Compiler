
# Name: Andrew Danial
# NetID: ADANIAL
# SBUID: 113338469

# Name: Christopher Lee
# NetID: lee111
# SBUID: 113378397

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
                s += f'FIELD {len(field_ids)}, {curr.current.name}, {self.name}, {vis}, {modifier}, {type if type == "int" or type == "float" or type == "boolean" else f"user({type})"}\n'
                field_ids.add(len(field_ids) + 1)
                curr = curr.next
            
        s += "Constructors:\n"
        for constructor in self.constructors:
            s += str(constructor)
            
        s += "Methods:\n"
            
        for method in self.methods:
            modifier = method.visibility if method.visibility else "private"
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
    
class Variables():
    def __init__(self, current = None, n = None) -> None:
        self.current = current
        self.next = n
        
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
    
class FormalCont():
    def __init__(self, curr, n) -> None:
        self.current = curr
        self.next = n
        pass
    
class Formal():
    def __init__(self, type, variable) -> None:
        self.type = type
        self.variable = variable
    
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
        #print(scope_stack)
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
            
        var_map = dict();
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
    
class ReturnStmt():
    def __init__(self, returnValue, lineStart, lineEnd) -> None:
        self.returnValue = returnValue
        self.lineStart = lineStart
        self.lineEnd = lineEnd 
        self.typeCorrect = None

    def __str__(self):
        s = "Return( " + str(self.returnValue) + " )"
        return s


class ExprStmt():
    def __init__(self, expr, lineStart, lineEnd) -> None:
        self.expr = expr
        self.lineStart = lineStart
        self.lineEnd = lineEnd   
        self.typeCorrect = None

    def __str__(self):
        s = "Expr( " + str(self.expr) + " )"
        return s 

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

class VarExpr():
    def __init__(self, idVar, lineStart, lineEnd, unique_id, stack=None) -> None:
        self.idVar = idVar
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.unique_id = unique_id
        self.scope_stack = stack
        self.type = None #TODO 
        
    def __str__(self):
        s = "Variable(" + str(self.unique_id) + ")"
        return s

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
            s = "Method-call(" + str(self.base) + ", " + str(self.methodName) + ", " + str(self.exprs) + ")"
        return s 

class NewObjectExpr():
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
            s = "New-object(" + str(self.baseClassName) + ", " + str(self.exprs) + ")"
        return s    

class ThisExpr():
    def __init__(self, lineStart, lineEnd) -> None:
        self.lineStart = lineStart
        self.lineEnd = lineEnd  
        self.type = None

    def __str__(self):
        return "This"

class SuperExpr():
    def __init__(self, lineStart, lineEnd) -> None:
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None  

    def __str__(self):
        return "Super"

class ClassReferenceExpr():
    def __init__(self, classRef, lineStart, lineEnd) -> None:
        self.classRef = classRef
        self.lineStart = lineStart
        self.lineEnd = lineEnd
        self.type = None

    def __str__(self):
        s = "Class-reference( " + str(self.classRef) + " )"
        return s