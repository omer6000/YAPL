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
    'EQUALS'
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

def t_BOOL(t):
    r"true|false|0|1"
    return t

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
t_EQUALS = r'\='
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
    calc : expression
         | empty
    '''
    print(p[1])

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
               | NAME EQUALS NAME
    '''
    p[0] = ("=", p[1], p[3])

def p_expression(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_number(p):
    '''
    expression : INT
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