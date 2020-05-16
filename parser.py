import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

def p_calc(p):
    '''
    calc : declaration SEMICOLON
         | declaration SEMICOLON calc
         | variable_update SEMICOLON
         | variable_update SEMICOLON calc
    '''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_declaration(p):
    '''
    declaration : DOUBLE_TYPE NAME ASSIGNMENT double_expression 
                | INT_TYPE NAME ASSIGNMENT int_expression 
                | STRING_TYPE NAME ASSIGNMENT string_expression 
                | CHARACTER_TYPE NAME ASSIGNMENT CHAR 
                | BOOL_TYPE NAME ASSIGNMENT BOOL 
                | empty

    '''
    p[0] = ("declaration",p[1], p[2], p[4])

def p_variable_update(p):
    '''
    variable_update : NAME ASSIGNMENT double_expression 
                    | NAME ASSIGNMENT int_expression 
                    | NAME ASSIGNMENT string_expression 
                    | NAME ASSIGNMENT CHAR 
                    | NAME ASSIGNMENT BOOL 
                    
    '''
    p[0] = ("variable_update", p[1], p[3])

def p_double_expression(p):
    '''
    double_expression : double_expression PLUS double_expression
                      | double_expression MINUS double_expression
                      | double_expression MULTIPLY double_expression
                      | double_expression DIVIDE double_expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_double_number(p):
    '''
    double_expression : DOUBLE
    '''
    p[0] = p[1]

def p_int_expression(p):
    '''
    int_expression : int_expression PLUS int_expression
                   | int_expression MINUS int_expression
                   | int_expression MULTIPLY int_expression
                   | int_expression DIVIDE int_expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_int_number(p):
    '''
    int_expression : INT
    '''
    p[0] = p[1]

def p_string_expression(p):
    '''
    string_expression : string_expression PLUS string_expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_string(p):
    '''
    string_expression : STRING
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    print("Syntax error in input!")
# parser = yacc.yacc()

# while True:
#     try:
#         s = input('')
#     except EOFError:
#         break
#     parser.parse(s)