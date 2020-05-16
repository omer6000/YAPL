import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'ASSIGNMENT',
    'SEMICOLON',
    'DOUBLE',
    'INT',
    'STRING',
    'CHAR',
    'BOOL',
    'DOUBLE_TYPE',
    'INT_TYPE',
    'BOOL_TYPE',
    'CHARACTER_TYPE',
    'STRING_TYPE',
    'NAME'
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_ASSIGNMENT = r'\='
t_MULTIPLY = r'\*'
t_SEMICOLON = r'\;'
t_ignore = r' '

def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r"\"[^\"]*\""
    t.value = t.value[1:-1]
    return t

def t_CHAR(t):
    r"\'[^\']\'"
    t.value = t.value[1:-1]
    return t

def t_BOOL(t):
    r"true|false"
    return t

def t_DOUBLE_TYPE(t):
    r'double'
    return t

def t_INT_TYPE(t):
    r'int'
    return t

def t_BOOL_TYPE(t):
    r'bool'
    return t

def t_CHARACTER_TYPE(t):
    r'char'
    return t

def t_STRING_TYPE(t):
    r'string'
    return t

def t_NAME(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = "NAME"
    return t

def t_error(t):
    print("Illegal Characters!")
    t.lexer.skip(1)

lexer = lex.lex()
# lexer.input("\'h\' 12.54 35 \"how are you\" true false x")
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

def p_calc(p):
    '''
    calc : declaration
         | empty
    '''
            #  | redeclaration
    print(p[1])

def p_declaration(p):
    '''
    declaration : DOUBLE_TYPE NAME ASSIGNMENT double_expression SEMICOLON
                | INT_TYPE NAME ASSIGNMENT int_expression SEMICOLON
                | STRING_TYPE NAME ASSIGNMENT string_expression SEMICOLON
                | CHARACTER_TYPE NAME ASSIGNMENT CHAR SEMICOLON
                | BOOL_TYPE NAME ASSIGNMENT BOOL SEMICOLON

    '''
    p[0] = (p[1], p[2], p[4])

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

parser = yacc.yacc()

while True:
    try:
        s = input('')
    except EOFError:
        break
    parser.parse(s)