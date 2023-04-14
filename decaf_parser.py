
# Name: Andrew Danial
# NetID: ADANIAL
# SBUID: 113338469

# Name: Christopher Lee
# NetID: lee111
# SBUID: 113378397

import sys
from decaf_lexer import *
from decaf_ast import *
names = {}

precedence = (('right', 'ASSIGN'),
              ('left', 'OR'),
              ('left', 'AND'),
              ('nonassoc', 'EQ', 'NOT_EQ'),
              ('nonassoc', 'LT', 'LTE', 'GT', 'GTE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'STAR', 'F_SLASH'),
              ('right', 'UMINUS', 'UPLUS', 'NOT')
              )

new_scope_created = False

def p_program(p):
    'program : class_decl_list'
    p[0] = Program(p[1])
    return True

def p_class_decl_list(p):
    '''class_decl_list : class_decl class_decl_list
                       | empty'''
    if p[1]:
        p[0] = ClassDeclList(p[1], p[2])
    else:
        p[0] = ClassDeclList(None, None)
    pass

def p_class_decl(p):
    '''class_decl : CLASS ID LEFT_CB new_scope class_body_decl_list RIGHT_CB end_scope
                  | CLASS ID EXTENDS ID LEFT_CB new_scope class_body_decl_list RIGHT_CB end_scope'''
    if p[3] != "extends":
        a = Class(p[2], decls=p[5])
        p[0] = a
        if p[0] in class_record.keys():
            print(f"Error: Duplicate class name `{p[2]}` detected")
            exit(1)
        class_record[p[2]] = a
    else:
        b = Class(p[2], p[4], decls=p[7])
        p[0] = b
        if p[0] in class_record.keys():
            print(f"Error: Duplicate class name `{p[2]}` detected")
            exit(1)
        class_record[p[2]] = b
    pass

def p_class_body_decl_list(p):
    '''class_body_decl_list : class_body_decl class_body_decl_list
                            | empty '''
    if p[1]:
        p[0] = ClassBodyDeclList(p[1], p[2])
    pass

# def p_class_body_decl_cont(p):
#     '''class_body_decl_cont : class_body_decl class_body_decl_cont
#                             | empty'''
#     pass

def p_class_body_decl(p):
    '''class_body_decl : field_decl
                       | method_decl
                       | constructor_decl'''
                       
    p[0] = ClassBodyDecl(p[1])
    pass

def p_field_decl(p):
    'field_decl : modifier var_decl'
    p[0] = Field(p[1], p[2])
    pass

def p_modifier(p):
    '''modifier : PUBLIC STATIC
                | PRIVATE STATIC
                | PUBLIC
                | PRIVATE
                | STATIC
                | empty'''
    if len(p) == 3:
        p[0] = Modifier(p[1], p[2])
    elif len(p) == 2:
        p[0] = Modifier(p[1])
    pass

def p_var_decl(p):
    'var_decl : type variables SEMI_COLON'
    
    p[0] = VarDecl(p[1], p[2])
    
    
    pass

def p_type(p):
    '''type : TYPE_INT
            | TYPE_FLOAT
            | TYPE_BOOLEAN
            | ID'''
            
    p[0] = Type(p[1])
    pass

def p_variables(p):
    'variables : variable variables_cont'
    if p[1]:
        p[0] = Variables(p[1], p[2])
    pass

def p_variables_cont(p):
    '''variables_cont : COMMA variable variables_cont
                      | empty'''
    if p[1]:
        p[0] = VariablesCont(p[2], p[3])
    pass

def p_variable(p):
    'variable : ID'
    p[0] = Variable(p[1])
    global var_counter
    scope_stack[-1][p[0].name] = var_counter
    var_counter += 1
    pass

def p_method_decl(p):
    '''method_decl : modifier type ID LEFT_PN new_scope formals RIGHT_PN block
                   | modifier TYPE_VOID ID LEFT_PN new_scope formals RIGHT_PN block'''
    if (p[2] == "VOID"):
        p[0] = Method(p[1], Type("VOID"), p[3], p[6], p[8])
    else: 
        p[0] = Method(p[1], p[2], p[3], p[6], p[8])
    
    pass

def p_constructor_decl(p):
    'constructor_decl : modifier ID LEFT_PN new_scope formals RIGHT_PN block'
    p[0] = Constructor(p[1], p[2], p[5], p[7])
    pass

def p_formals(p):
    '''formals : formal_param formals_cont
               | empty'''
    if p[1]:
        p[0] = FormalList(p[1], p[2])
    pass

def p_formals_cont(p):
    '''formals_cont : COMMA formal_param formals_cont
                    | empty'''
    if p[1]:
        p[0] = FormalCont(p[2], p[3])
    pass

def p_formal_param(p):
    'formal_param : type variable'
    p[0] = Formal(p[1], p[2])
    curr_vars[p[2].name] = len(curr_var_ids) + 1
    curr_var_ids.add(len(curr_var_ids) + 1)
    global var_counter
    scope_stack[-1][p[2].name] = var_counter
    var_counter += 1
    pass

def p_block(p):
    'block : LEFT_CB block_new_scope stmt_list RIGHT_CB end_scope'
    p[0] = BlockStmt(p[3], p.lineno(3), p.lineno(3))
    pass

def p_new_scope(p):
    "new_scope :"
    
    global new_scope_created
    new_scope_created = True
    scope_stack.append(dict())

def p_block_new_scope(p):
    "block_new_scope :"
    global new_scope_created
    if not new_scope_created:
        scope_stack.append(dict())
    new_scope_created = False 

def p_end_scope(p):
    "end_scope :"
    
    global var_counter, new_scope_created
    scope_stack.pop()
    var_counter -= 1
    new_scope_created = False
    
def p_stmt_list(p):
    'stmt_list : stmt stmt_list'
    p[0] = [p[1]] + p[2]  #add stmt to stmt_list
    pass

def p_stmt_list_empty(p):
    'stmt_list : empty'
    p[0] = []
    pass

# def p_stmt(p):
#     '''stmt : IF LEFT_PN expr RIGHT_PN stmt 
#             | IF LEFT_PN expr RIGHT_PN stmt ELSE stmt
#             | WHILE LEFT_PN expr RIGHT_PN stmt
#             | FOR LEFT_PN for_cond1 SEMI_COLON for_cond2 SEMI_COLON for_cond3 RIGHT_PN stmt
#             | RETURN return_val SEMI_COLON
#             | stmt_expr SEMI_COLON
#             | BREAK SEMI_COLON
#             | CONTINUE SEMI_COLON
#             | block
#             | var_decl
#             | SEMI_COLON'''

def p_stmt_if(p):
    'stmt : IF LEFT_PN expr RIGHT_PN stmt'
    p[0] = IfStmt(p[3], p[5], None, p.lineno(3), p.lineno(5)) 
    pass

def p_stmt_ifElse(p):
    'stmt : IF LEFT_PN expr RIGHT_PN stmt ELSE stmt'
    p[0] = IfStmt(p[3], p[5], p[7], p.lineno(3), p.lineno(7)) 
    pass

def p_stmt_while(p):
    'stmt : WHILE LEFT_PN expr RIGHT_PN stmt'
    p[0] = WhileStmt(p[3], p[5], p.lineno(3), p.lineno(5)) 
    pass

def p_stmt_for(p):
    'stmt : FOR LEFT_PN for_cond1 SEMI_COLON for_cond2 SEMI_COLON for_cond3 RIGHT_PN stmt'
    p[0] = ForStmt(p[3], p[5], p[7], p[9], p.lineno(3), p.lineno(9))
    pass

def p_stmt_break(p):
    'stmt : BREAK SEMI_COLON'
    p[0] = BreakStmt(p.lineno(1), p.lineno(1))
    pass

def p_stmt_continue(p):
    'stmt : CONTINUE SEMI_COLON'
    p[0] = ContinueStmt(p.lineno(1), p.lineno(1))
    pass

def p_stmt_return(p):
    'stmt : RETURN return_val SEMI_COLON'
    p[0] = ReturnStmt(p[2], p.lineno(2), p.lineno(2))
    pass

def p_stmt_stmtExpr(p):
    'stmt : stmt_expr SEMI_COLON'
    p[0] = ExprStmt(p[1], p.lineno(1), p.lineno(1))
    pass

def p_stmt_block(p):
    'stmt : block'
    p[0] = p[1]
    pass

def p_stmt_var_decl(p):
    'stmt : var_decl'
    p[0] = p[1]
    curr = p[1].vars
    while curr:
        curr_vars[curr.current.name] = len(curr_var_ids) + 1
        curr_var_ids.add(len(curr_var_ids) + 1)
        
        curr = curr.next
    pass

def p_stmt_semicolon(p):
    'stmt : SEMI_COLON'
    p[0] = p[1]
    pass

def p_for_cond1(p):
    '''for_cond1 : stmt_expr
                 | empty'''
    if (p[1]):
        p[0] = p[1]
    pass

def p_for_cond2(p):
    '''for_cond2 : expr
                 | empty'''
    if (p[1]):
        p[0] = p[1]
    pass

def p_for_cond3(p):
    '''for_cond3 : stmt_expr
                 | empty'''
    if (p[1]):
        p[0] = p[1]
    pass

def p_return_val(p):
    '''return_val : expr
                  | empty'''
    if (p[1]):
        p[0] = p[1]
    pass

# def p_literal(p):
#     '''literal : INT_CONST
#                | FLOAT_CONST
#                | STRING_CONST
#                | NULL
#                | TRUE
#                | FALSE'''
#     pass

def p_literal_int_const(p):
    'literal : INT_CONST'
    p[0] = ConstantExpr("Integer", int(p[1]), p.lineno(1), p.lineno(1), "int")
    pass

def p_literal_float_const(p):
    'literal : FLOAT_CONST'
    p[0] = ConstantExpr("Float", float(p[1]), p.lineno(1), p.lineno(1), "float")
    pass

def p_literal_string_const(p):
    'literal : STRING_CONST'
    p[0] = ConstantExpr("String", str(p[1]), p.lineno(1), p.lineno(1), "string")
    pass

def p_literal_null(p):
    'literal : NULL'
    p[0] = ConstantExpr("Null", None, p.lineno(1), p.lineno(1), "null")
    pass

def p_literal_true(p):
    'literal : TRUE'
    p[0] = ConstantExpr("True", None, p.lineno(1), p.lineno(1), "boolean")
    pass

def p_literal_false(p):
    'literal : FALSE'
    p[0] = ConstantExpr("False", None, p.lineno(1), p.lineno(1), "boolean")
    pass

# def p_primary(p):
#     '''primary : literal
#                | THIS
#                | SUPER
#                | LEFT_PN expr RIGHT_PN
#                | NEW ID LEFT_PN arguments RIGHT_PN
#                | lhs
#                | method_invocation'''
#     pass

def p_primary_literal(p):
    'primary : literal'
    p[0] = p[1]
    pass

def p_primary_this(p):
    'primary : THIS'
    p[0] = ThisExpr(p.lineno, p.lineno)
    pass

def p_primary_super(p):
    'primary : SUPER'
    p[0] = SuperExpr(p.lineno, p.lineno)
    pass

def p_primary_paren_expr(p):
    'primary : LEFT_PN expr RIGHT_PN'
    p[0] = p[2]
    pass

def p_primary_new_object(p):
    'primary : NEW ID LEFT_PN arguments RIGHT_PN'
    p[0] = NewObjectExpr(p[2], p[4], p.lineno(1), p.lineno(1))
    pass

def p_primary_lhs(p):
    'primary : lhs'
    p[0] = p[1]
    pass

def p_primary_method_invocation(p):
    'primary : method_invocation'
    p[0] = p[1]
    pass

def p_arguments(p):
    '''arguments : expr arguments_cont
                 | empty'''
    if (p[1]):
        p[0] = p[1]
    pass

def p_arguments_cont(p):
    '''arguments_cont : COMMA expr arguments_cont
                      | empty'''
    if (p[1]):
        p[0] = p[3] + [p[2]]
    pass

def p_lhs(p):
    'lhs : field_access'
    
    p[0] = p[1]
    pass

def p_field_access(p):
    '''field_access : primary DOT ID
                    | ID'''
    #print(len(p))
    if (len(p) == 4): #primary DOT ID
        var = p[3]
        found = False
        p[0] = FieldAccessExpr(p[1], p[3], p.lineno, p.lineno)
        # for i in reversed(scope_stack):
        #     if var in i:
        #         found = True
        #         break
        # if not found:
        #     print(f"Error: Variable {var} cannot be found")
        #     exit(1)
    else: #ID
        var = p[1]
        found = False
        for i in reversed(scope_stack):
            if var in i:
                found = True
                break
           
        if (p[1] in curr_vars):
            p[0] = VarExpr(p[1], p.lineno, p.lineno, curr_vars[p[1]]) # bandaid fix that isnt really a fix: curr_vars[p[1]] if p[1] in curr_vars else None
            
        else:
            p[0] = ClassReferenceExpr(p[1], p.lineno, p.lineno)
            
        if not found:
            print(f"Error: Variable {var} cannot be found")
            exit(1)
            
    pass

def p_method_invocation(p):
    'method_invocation : field_access LEFT_PN arguments RIGHT_PN'
    #p[1] should be a FieldAccessExpr
    p[0] = MethodCallExpr(p[1].base, p[1].fieldName, p[3], p.lineno, p.lineno)
    pass

def p_expr(p):
    '''expr : primary
            | assign'''
    p[0] = p[1]
    pass
    
#def p_expr(p):
#   '''expr : primary
#            | assign
#            | expr arith_op expr
#            | expr bool_op expr
#            | unary_op expr'''
#    pass

# def p_assign(p):
#     '''assign : lhs ASSIGN expr
#               | lhs INCREMENT
#               | INCREMENT lhs
#               | lhs DECREMENT
#               | DECREMENT lhs'''
#     pass

def p_assign_equals(p):
    'assign : lhs ASSIGN expr'
    p[0] = AssignExpr(p[1], p[3], p.lineno, p.lineno)
    pass

def p_assign_postInc(p):
    'assign : lhs INCREMENT'
    p[0] = AutoExpr(p[1], "inc", "post", p.lineno, p.lineno)
    pass

def p_assign_preInc(p):
    'assign : INCREMENT lhs'
    p[0] = AutoExpr(p[2], "inc", "pre", p.lineno, p.lineno)
    
    
def p_assign_postDec(p):
    'assign : lhs DECREMENT'
    p[0] = AutoExpr(p[1], "dec", "post", p.lineno, p.lineno)
    pass

def p_assign_preDec(p):
    'assign : DECREMENT lhs'
    p[0] = AutoExpr(p[2], "dec", "pre", p.lineno, p.lineno)
    pass

#def p_assign(p):
#    '''assign : lhs ASSIGN expr
#              | lhs PLUS PLUS
#              | PLUS PLUS lhs
#              | lhs MINUS MINUS
#              | MINUS MINUS lhs'''
#    pass

def p_add_expr(p):
    'expr : expr PLUS expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_sub_expr(p):
    'expr : expr MINUS expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_mult_exp(p):
    'expr : expr STAR expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_div_expr(p):
    'expr : expr F_SLASH expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_conj_expr(p):
    'expr : expr AND expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_disj_expr(p):
    'expr : expr OR expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_equals_expr(p):
    'expr : expr EQ expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_notequals_expr(p):
    'expr : expr NOT_EQ expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_lt_expr(p):
    'expr : expr LT expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_lte_expr(p):
    'expr : expr LTE expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_gt_expr(p):
    'expr : expr GT expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_gte_expr(p):
    'expr : expr GTE expr'
    p[0] = BinaryExpr(p[1], p[3], p[2], p.lineno(2), p.lineno(2))
    pass

def p_pos_expr(p):
    'expr : PLUS expr %prec UPLUS'
    p[0] = UnaryExpr(p[2], p[1], p.lineno(2), p.lineno(2))
    pass

def p_minus_expr(p):
    'expr : MINUS expr %prec UMINUS'
    p[0] = UnaryExpr(p[2], p[1], p.lineno(2), p.lineno(2))
    pass

def p_not_expr(p):
    'expr : NOT expr'
    p[0] = UnaryExpr(p[2], p[1], p.lineno(2), p.lineno(2))
    pass

#def p_arith_op(p):
#    '''arith_op : PLUS
#                | MINUS
#                | STAR
#                | F_SLASH'''
#    pass

#def p_bool_op(p):
#    '''bool_op : AND
#               | OR
#               | EQ
#               | NOT_EQ
#               | LT
#               | GT
#               | LTE
#       p_as        | GTE'''
#    pass

#def p_unary_op(p):
#    '''unary_op : PLUS
#                | MINUS
#                | NOT'''
#    pass

def p_stmt_expr(p):
    '''stmt_expr : assign
                 | method_invocation'''
    p[0] = p[1]
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print()
    if p:
        print("Syntax error at token,", p.type, ", line", p.lineno)
    else:
        print("Syntax error at EOF")
    print()
    sys.exit()
