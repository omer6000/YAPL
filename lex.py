import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
    'INT',
    'DOUBLE',
    'STRING',
    'CHAR',
    'BOOL',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'NAME',
    'ASSIGNMENT'
]

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

# def t_BOOL(t):
#     r"true|false"
#     return t

def t_CHAR(t):
    r"\'[^\']\'"
    t.value = t.value[1:-1]
    return t

def t_NAME(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = "NAME"
    return t

def t_error(t):
    print("Illegal Characters!")
    t.lexer.skip(1)

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_ASSIGNMENT = r'\='
t_MULTIPLY = r'\*'
t_ignore = r' '

lexer = lex.lex()
# lexer.input("123.456")
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
    calc : number
         | var_assign
         | empty
    '''
    print(p[1])

def p_var_assign(p):
    '''
    var_assign : NAME ASSIGNMENT number
               | NAME ASSIGNMENT NAME
    '''
    p[0] = ("=", p[1], p[3])

def p_computation(p):
    '''
    number : number PLUS number
           | number MULTIPLY number
           | number DIVIDE number
           | number MINUS number
    '''
    p[0] = (p[2], p[1], p[3])

def p_number(p):
    '''
    number : INT
           | DOUBLE
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