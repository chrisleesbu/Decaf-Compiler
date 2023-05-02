
# Name: Andrew Danial
# NetID: ADANIAL
# SBUID: 113338469

# Name: Christopher Lee
# NetID: lee111
# SBUID: 113378397
import decaf_ast as ast

def type_check(program):
    class_list = program.class_list
    curr = class_list.val
    while curr:
        for method in curr.methods:
            return_type = method.returnType
            for stmt in method.body.stmts:
                if isinstance(stmt, ast.IfStmt):
                    check_if_condition(stmt.expr)
        class_list = class_list.next
        curr = class_list.val
    
def check_if_condition(expr):
    if not isinstance(expr, ast.BinaryExpr):
        print(f"Error: {expr} does not resolve to a boolean")
        exit(1)
    scope_stack = expr.operand1.scope_stack
    var1_type = ""
    var2_type = ""
    for i in reversed(scope_stack):
        for j in i.keys():
            print
            if expr.operand1.idVar in j and not var1_type:
                var1_type = j[0]
            if expr.operand2.idVar in j and not var2_type:
                var2_type = j[0]
                
    if not var1_type or not var2_type:
        print("Error: Var not found")   
        exit(1) 
    if not isSubtype(var1_type, var2_type):
        print("Error: Type mismatch")
        exit(1)
    if not expr.operator in ["<", ">", ">=", "<=", "==", "!="]:
        print("Error: Expression does not evaluate to boolean")
    
def isSubtype(self, otherType):
    #Type T is a subtype of itself
    if (self == otherType):
        return True

    #int is a subtype of float
    if (self == "int" and otherType == "float") or (self == "float" and otherType == "int"):
        return True

    # #user(A) is a subtype of user(B) if A is a subclass of B.
    # if (self.category == "user" and otherType.category == "user"):
    #     return self.isSubclass(otherType.type)

    # #null is a subtype of user(A) for any class A
    # if (self.type == "null" and self.category == "user"):
    #     return True

    # #class-literal(A) is a subtype of class-literal(B) if A is a subclass of B
    # if (self.category == "classLiteral" and otherType.category == "classLiteral"):
    #     return self.type.isSubclass(otherType.type)
    
    return False
class IfStmtCheck():
    def typeCheck(if_stmt): 
        if (if_stmt.typeCorrect == None):
            if (if_stmt.expr != "boolean" or if_stmt.thenStmt.typeCheck() == False or if_stmt.elseStmt.typeCheck() == False):
                if_stmt.typeCorrect = False
            else:
                if_stmt.typeCorrect = True
        return if_stmt.typeCorrect

class WhileStmtCheck():
    def typeCheck(while_stmt): 
        if (while_stmt.typeCorrect == None):
            if (while_stmt.expr != "boolean" or while_stmt.stmt.typeCheck() == False):
                while_stmt.typeCorrect = False
            else:
                while_stmt.typeCorrect = True
        return while_stmt.typeCorrect

class ForStmtCheck():
    def typeCheck(self): 
        if (self.typeCorrect == None):
            if (self.loopExpr != "boolean" or self.initializerExpr.typeCheck() == False or self.updateExpr.typeCheck() == False or self.stmt.typeCheck() == False):
                self.typeCorrect = False
            else:
                self.typeCorrect = True
        return self.typeCorrect

class ReturnStmtCheck():
    def typeCheck(self): 
        if (self.typeCorrect == None):
            #If the expression is empty, then the declared return type of the method must be void (and viceversa).
            #TODO
            pass
        return self.typeCorrect

class ExprStmtCheck(): 
    def typeCheck(self): 
        if (self.typeCorrect == None):
            if (self.expr.typeCheck() == False):
                self.typeCorrect = False
            else:
                self.typeCorrect = True
        return self.typeCorrect

class BlockStmtCheck():
    def typeCheck(self): 
        if (self.typeCorrect == None):
            self.typeCorrect = True
            for stmt in self.stmts:
                if (stmt.typeCheck() == False):
                    self.typeCorrect = False
        return self.typeCorrect




# ***** EXPRESSIONS *****

class ConstantExpr():
    def getType(self): #tyoe is already in here
        return self.type
    
class VarExpr():
    def getType(self):
        #TODO figure out the type of the var
        pass

# class UnaryExpr():
#     def getType(self):
#         if (self.type == None):
#             if (self.unary == '!'):
#                 if (self.operand.getType() == "boolean"):
#                     self.type = Type("boolean")
#                 else:
#                     print("Error: Unary type error")
#                     self.type = Type("error")
#             elif(self.unary == "-"): 
#                 if (self.unary == '-'):
#                     if (self.operand.getType() == "int"):
#                         self.type = Type("int")
#                     elif (self.operand.getType() == "float"):
#                         self.type = Type("float")
#                     else:
#                       print("Error: Unary type error")  
#                       self.type = Type("error")
#         return self.type
    
# class BinaryExpr():
#     def getType(self):
#         if (self.type == None): 
#             if(self.operator in ["+", "-", "*", "/"]): #arithmetic operations
#                 if (self.operand1.getType() == "int" and self.operand2.getType() == "int"):
#                     self.type = Type("int")
#                 elif (self.operand1.getType() == "float" or self.operand2.getType() == "float"):
#                     self.type = Type("float")
#                 else:
#                     print("Error: Binary type error (arithmetic operations)")
#                     self.type = Type("error")
#             elif (self.operator in ["&&", "||"]): #boolean operations
#                 if (self.operand1.getType() == "boolean" and self.operand2.getType() == "boolean"):
#                     self.type = Type("boolean")
#                 else:
#                     print("Error: Binary type error (boolean operations)")
#                     self.type = Type("error")
#             elif (self.operator in [">", ">=", "<", "<="]): #arithmetic comparisons
#                 if ((self.operand1.getType() == "int" or self.operand1.getType() == "float")
#                     and (self.operand2.getType() == "int" or self.operand2.getType() == "float")):
#                     self.type = Type('boolean')
#                 else:
#                     print("Error: Binary type error (arithmetic comparisons)")
#                     self.type = Type("error")
#             elif (self.operator in ["==","!="]): #equality comparisons
#                 #TODO figure out how to get subtype
#                 print("Error: Binary type error (equality comparisons)")
#                 self.type = Type("error")
#         return self.type
        
    
# class AssignExpr():
#     def getType(self):
#         if(self.type == None):
#             if (self.leftExpr.getType() != "error" and self.rightExpr.getType() != "error"):
#                 if (self.rightExpr.getType().isSubtype(self.leftExpr.getType())):
#                     self.type = self.rightExpr.getType()
#                 else:
#                     print("Error: Assign type error (not subtype)")
#                     self.type = Type("error")
#             else:
#                 print("Error: Assign type error")
#                 self.type = Type("error")
#         return self.type
    
# class AutoExpr():
#     def getType(self):
#         if(self.type == None):
#             if (self.operand.getType() == "int" or self.operand.getType() == "float"):
#                 self.type = self.operand.getType()
#             else:
#                 print("Auto type error")
#                 self.type = Type("error")
#         return self.type
    
# class FieldAccessExpr():
#     def getType(self):
#         #TODO
#         pass

# class MethodCallExpr():
#     def getType(self):
#         #TODO
#         pass

# class NewObjectExpr():
#     def getType(self):
#         #TODO
#         pass

# class ThisExpr():
#     def getType(self):
#         #TODO
#         pass

# class SuperExpr():
#     def getType(self):
#         #TODO
#         pass

# class ClassReferenceExpr():
#     def getType(self):
#         #TODO check name resolution
#         if (self.type == None):
#             self.type = Type(self.classRef, isLiteral=True)
#         return self.type