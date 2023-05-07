
# Name: Andrew Danial
# NetID: ADANIAL
# SBUID: 113338469

# Name: Christopher Lee
# NetID: lee111
# SBUID: 113378397
import decaf_ast as ast

def type_check(program):
    class_list = program.class_list
    global curr
    curr = class_list.val
    while curr:
        for method in curr.methods:
            return_type = method.returnType
            for stmt in method.body.stmts:
                if not isinstance(stmt, ast.VarDecl):
                    # print(type(stmt))
                    print(stmt.typeCheck())
        # for constructor in curr.constructors:
        #     for stmt in constructor.body.stmts:
        #         if not isinstance(stmt, ast.VarDecl):
        #             print(vars(curr))
        #             print(type(stmt))
        #             print(stmt.typeCheck())
        class_list = class_list.next
        curr = class_list.val

# ***** EXPRESSIONS *****

    def getType(self):
        #TODO figure out the type of the var
        pass
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

# class ClassReferenceExpr():
#     def getType(self):
#         #TODO check name resolution
#         if (self.type == None):
#             self.type = Type(self.classRef, isLiteral=True)
#         return self.type