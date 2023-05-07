
# Name: Andrew Danial
# NetID: ADANIAL
# SBUID: 113338469

# Name: Christopher Lee
# NetID: lee111
# SBUID: 113378397
import decaf_ast as ast

curr_ast = None

def type_check(program):
    global curr_ast

    class_list = program.class_list
    curr_ast = class_list.val
    #print(curr_ast)
    while curr_ast:
        for constructor in curr_ast.constructors:
            for stmt in constructor.block.stmts:
                if not isinstance(stmt, ast.VarDecl):
                    stmt.typeCheck()
                    print("", end="")
        for method in curr_ast.methods:
            for stmt in method.body.stmts:
                if not isinstance(stmt, ast.VarDecl):
                    stmt.typeCheck()
                    print("", end="")
        class_list = class_list.next
        curr_ast = class_list.val