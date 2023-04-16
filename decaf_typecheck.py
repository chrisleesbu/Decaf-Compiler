from decaf_ast import *

class Type():    
    def isSubtype(self, otherType):
        #Type T is a subtype of itself
        if (self.type == otherType.type):
            return True

        #int is a subtype of float
        if (self.type == "int" and otherType.type == "float"):
            return True

        #user(A) is a subtype of user(B) if A is a subclass of B.
        if (self.category == "user" and otherType.category == "user"):
            return self.type.isSubclass(otherType.type)

        #null is a subtype of user(A) for any class A
        if (self.type == "null" and self.category == "user"):
            return True

        #class-literal(A) is a subtype of class-literal(B) if A is a subclass of B
        if (self.category == "classLiteral" and otherType.category == "classLiteral"):
            return self.type.isSubclass(otherType.type)
        
        return False


# ***** EXPRESSIONS *****

class ConstantExpr():
    def getType(self): #tyoe is already in here
        return self.type
    
class VarExpr():
    def getType(self):
        #TODO figure out the type of the var
        pass

class UnaryExpr():
    def getType(self):
        if (self.type == None):
            if (self.unary == '!'):
                if (self.operand.getType() == "boolean"):
                    self.type = Type("boolean")
                else:
                    print("Error: Unary type error")
                    self.type = Type("error")
            elif(self.unary == "-"): 
                if (self.unary == '-'):
                    if (self.operand.getType() == "int"):
                        self.type = Type("int")
                    elif (self.operand.getType() == "float"):
                        self.type = Type("float")
                    else:
                      print("Error: Unary type error")  
                      self.type = Type("error")
        return self.type
    
class BinaryExpr():
    def getType(self):
        if (self.type == None): 
            if(self.operator in ["+", "-", "*", "/"]): #arithmetic operations
                if (self.operand1.getType() == "int" and self.operand2.getType() == "int"):
                    self.type = Type("int")
                elif (self.operand1.getType() == "float" or self.operand2.getType() == "float"):
                    self.type = Type("float")
                else:
                    print("Error: Binary type error (arithmetic operations)")
                    self.type = Type("error")
            elif (self.operator in ["&&", "||"]): #boolean operations
                if (self.operand1.getType() == "boolean" and self.operand2.getType() == "boolean"):
                    self.type = Type("boolean")
                else:
                    print("Error: Binary type error (boolean operations)")
                    self.type = Type("error")
            elif (self.operator in [">", ">=", "<", "<="]): #arithmetic comparisons
                if ((self.operand1.getType() == "int" or self.operand1.getType() == "float")
                    and (self.operand2.getType() == "int" or self.operand2.getType() == "float")):
                    self.type = Type('boolean')
                else:
                    print("Error: Binary type error (arithmetic comparisons)")
                    self.type = Type("error")
            elif (self.operator in ["==","!="]): #equality comparisons
                #TODO figure out how to get subtype
                print("Error: Binary type error (equality comparisons)")
                self.type = Type("error")
        return self.type
        
    
class AssignExpr():
    def getType(self):
        if(self.type == None):
            if (self.leftExpr.getType() != "error" and self.rightExpr.getType() != "error"):
                if (self.rightExpr.getType().isSubtype(self.leftExpr.getType())):
                    self.type = self.rightExpr.getType()
                else:
                    print("Error: Assign type error (not subtype)")
                    self.type = Type("error")
            else:
                print("Error: Assign type error")
                self.type = Type("error")
        return self.type
    
class AutoExpr():
    def getType(self):
        if(self.type == None):
            if (self.operand.getType() == "int" or self.operand.getType() == "float"):
                self.type = self.operand.getType()
            else:
                print("Auto type error")
                self.type = Type("error")
        return self.type
    
class FieldAccessExpr():
    def getType(self):
        #TODO
        pass

class MethodCallExpr():
    def getType(self):
        #TODO
        pass

class NewObjectExpr():
    def getType(self):
        #TODO
        pass

class ThisExpr():
    def getType(self):
        #TODO
        pass

class SuperExpr():
    def getType(self):
        #TODO
        pass

class ClassReferenceExpr():
    def getType(self):
        #TODO check name resolution
        if (self.type == None):
            self.type = Type(self.classRef, isLiteral=True)
        return self.type