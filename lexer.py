import ply.lex as lex
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
    'NAME',
    'PRINT',
    'LB',
    'RB',
    'COMMA',
    'POWER',
    'MOD',
    'INCREMENT',
    'DECREMENT',
    'AND',
    'OR',
    'LESS',
    'LESSEQUAL',
    'GREATER',
    'GREATEREQUAL',
    'NOT',
    'EQUALITY',
    'NOTEQUAL',
    'DO',
    'WHILE',
    'LP',
    'RP',
    'STRUCT'
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
t_MOD = r'\%'
t_POWER = r'\^'
t_LESS = r'\<'
t_GREATER = r'\>'
t_LP = "\{"
t_RP = "\}"
t_ignore = ' \t\v\r'

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

def t_PRINT(t):
    r'print'
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_EQUALITY(t):
    r'\=\='
    return t
def t_NOTEQUAL(t):
    r'\!\='
    return t

def t_DO(t):
    r'do'
    return t

def t_STRUCT(t):
    r'struct'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_LESSEQUAL(t):
    r'\<\='
    return t

def t_GREATEREQUAL(t):
    r'\>\='
    return t

def t_NOT(t):
    r'not'
    return t

def t_INCREMENT(t):
    r'\+\+'
    return t

def t_DECREMENT(t):
    r'\-\-'
    return t

def t_AND(t):
    r'\&\&'
    return t

def t_OR(t):
    r'\|\|'
    return t

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

def t_NAME(t):
    r'[a-zA-Z_][_a-zA-Z0-9.]*'
    t.type = "NAME"
    return t

def t_error(t):
    print("TypeError")
    t.lexer.skip(1)

lexer = lex.lex()

