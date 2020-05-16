import lexer
import parser
import ply.lex as lex
import ply.yacc as yacc
import sys

var_env = {}

def eval_exp(tree):
    global var_env
    print(tree)
    if type(tree) is int:
        return tree
    elif type(tree) is float:
        return tree
    elif tree[0] == "declaration":
        name = tree[2]
        if name in var_env:
            print("Error variable already declared!!!")
        else:
            typeval = tree[1]
            val = tree[3]
            var_env[name] = {typeval: eval_exp(val)}
            print(var_env)
    elif tree[0] == "+":
        return eval_exp(tree[1]) + eval_exp(tree[2])

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        f = open(filename, "r")
        code = f.read()
        filelex = lex.lex(module = lexer)
        filelex.input(code)
        fileparse = yacc.yacc(module=parser)
        filetree = fileparse.parse(code, lexer=filelex)
        for x in filetree:
            eval_exp(x)
