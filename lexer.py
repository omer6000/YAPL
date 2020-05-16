import ply.lex as lex

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
    'NAME',
    'PRINT',
    'LB',
    'RB',
    'COMMA'
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_ASSIGNMENT = r'\='
t_MULTIPLY = r'\*'
t_SEMICOLON = r'\;'
t_LB = r'\('
t_RB = r'\)'
t_COMMA = r'\,'
t_ignore = ' \t\v\r'

def t_PRINT(t):
    r'print'
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

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
# # lexer.input("\'h\' 12.54 35 \"how are you\" true false x")
# # while True:
# #     tok = lexer.token()
# #     if not tok:
# #         break
# #     print(tok)

