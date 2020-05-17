import ply.yacc as yacc
from lexer import tokens
import sys

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'MOD', 'POWER'),
)

def p_calc(p):
    '''
    calc : assignment SEMICOLON
         | assignment SEMICOLON calc
         | declaration SEMICOLON
         | declaration SEMICOLON calc
         | variable_update SEMICOLON
         | variable_update SEMICOLON calc
         | expression SEMICOLON
         | expression SEMICOLON calc
         | printoutput SEMICOLON
         | printoutput SEMICOLON calc
         | dowhile_expression SEMICOLON
         | dowhile_expression SEMICOLON calc
         | increment SEMICOLON
         | increment SEMICOLON calc
         | decrement SEMICOLON
         | decrement SEMICOLON calc
         | struct SEMICOLON
         | struct SEMICOLON calc
    '''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_var(p):
    '''
    var : NAME
    '''
    p[0] = ("variable", p[1])

def p_printstatement(p):
    '''
    printoutput : PRINT LB printexpression RB
    '''
    p[0] = ("print", p[3])

def p_printexpression(p):
    '''
    printexpression : expression
                    | expression COMMA printexpression
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_expression(p):
    '''
    expression : var
               | CHAR
               | double_expression
               | int_expression
               | string_expression
               | bool_expression
    '''
    p[0] = p[1]

def p_declaration(p):
    '''
    declaration : DOUBLE_TYPE NAME
                | INT_TYPE NAME
                | STRING_TYPE NAME
                | CHARACTER_TYPE NAME
                | BOOL_TYPE NAME
                | NAME NAME
                | empty
    '''
    p[0] = ("declaration", p[1], p[2])

def p_assignment(p):
    '''
    assignment : DOUBLE_TYPE NAME ASSIGNMENT double_expression 
               | INT_TYPE NAME ASSIGNMENT int_expression 
               | STRING_TYPE NAME ASSIGNMENT string_expression 
               | CHARACTER_TYPE NAME ASSIGNMENT CHAR 
               | BOOL_TYPE NAME ASSIGNMENT bool_expression
               | empty
    '''
    p[0] = ("assignment",p[1], p[2], p[4])

def p_variable_update(p):
    '''
    variable_update : NAME ASSIGNMENT double_expression 
                    | NAME ASSIGNMENT int_expression 
                    | NAME ASSIGNMENT string_expression 
                    | NAME ASSIGNMENT CHAR 
                    | NAME ASSIGNMENT bool_expression
                    
    '''
    p[0] = ("variable_update", p[1], p[3])

def p_double_number(p):
    '''
    double_expression : DOUBLE
                      | INT
                      | var
    '''
    p[0] = p[1]

def p_double_expression(p):
    '''
    double_expression : double_expression PLUS double_expression
                      | double_expression MINUS double_expression
                      | double_expression MULTIPLY double_expression
                      | double_expression DIVIDE double_expression
                      | double_expression MOD double_expression
                      | double_expression POWER double_expression
                      | MINUS double_expression
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1], 0, p[2])

def p_double_bracket(p):
    '''
    double_expression : LB double_expression RB
    '''
    p[0] = p[2]

def p_int_number(p):
    '''
    int_expression : INT
                   | var
    '''
    p[0] = p[1]

def p_int_expression(p):
    '''
    int_expression : int_expression PLUS int_expression
                   | int_expression MINUS int_expression
                   | int_expression MULTIPLY int_expression
                   | int_expression DIVIDE int_expression
                   | int_expression MOD int_expression
                   | int_expression POWER int_expression
                   | MINUS int_expression
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1], 0, p[2])

def p_int_bracket(p):
    '''
    int_expression : LB int_expression RB
    '''
    p[0] = p[2]

def p_bool(p):
    '''
    bool_expression : BOOL
                    | var 
    '''
    p[0] = p[1]

def p_bool_expression(p):
    '''
    bool_expression : bool_expression OR bool_expression
                    | bool_expression AND bool_expression
                    | expression LESS expression
                    | expression LESSEQUAL expression
                    | expression GREATER expression
                    | expression GREATEREQUAL expression
                    | expression EQUALITY expression
                    | expression NOTEQUAL expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_bool_not(p):
    '''
    bool_expression : NOT bool_expression
    '''
    p[0] = ("not", p[2])

def p_bool_bracket(p):
    '''
    bool_expression : LB bool_expression RB
    '''
    p[0] = p[2]

def p_string(p):
    '''
    string_expression : STRING
                      | var
    '''
    p[0] = p[1]

def p_string_expression(p):
    '''
    string_expression : string_expression PLUS string_expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_string_bracket(p):
    '''
    string_expression : LB string_expression RB
    '''
    p[0] = p[2]

def p_code(p):
    '''
    code : assignment SEMICOLON
         | declaration SEMICOLON
         | variable_update SEMICOLON
         | increment SEMICOLON
         | decrement SEMICOLON
         | printoutput SEMICOLON
    '''
    p[0] = p[1]

def p_insidewhile(p):
    '''
    insidewhile : code
                | code insidewhile 
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_comparison_operators(p):
    '''
    operator : LESS
             | LESSEQUAL
             | GREATER
             | GREATEREQUAL
             | EQUALITY
             | NOTEQUAL
    '''
    p[0] = p[1]

def p_loop_condition(p):
    '''
    condition : int_expression operator int_expression
              | LB condition RB
    '''
    p[0] = ("dowhole condition" ,p[2], p[1], p[3])

def p_dowhile(p):
    '''
    dowhile_expression : DO LP insidewhile RP WHILE LB condition RB
    '''
    p[0] = ("dowhile", p[3], p[7])

def p_struct_code(p):
    '''
    structcode : declaration SEMICOLON
               | assignment SEMICOLON
    '''
    p[0] = p[1]

def p_insidestruct(p):
    '''
    insidestruct : structcode
                 | structcode insidestruct
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_struct(p):
    '''
    struct : STRUCT NAME LP insidestruct RP
    '''
    p[0] = ("struct", p[2], p[4])

def p_increment(p):
    '''
    increment : int_expression INCREMENT
    '''
    p[0] = ("increment", p[1])

def p_decrement(p):
    '''
    decrement : int_expression DECREMENT
    '''
    p[0] = ("decrement", p[1])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    print("TypeError")