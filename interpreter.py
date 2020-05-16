import lexer
import parser
import ply.lex as lex
import ply.yacc as yacc
import sys

var_env = {}

def eval_exp(tree):
    global var_env
    if type(tree) is int:
        return tree
    elif type(tree) is float:
        return tree
    elif type(tree) is str:
        return tree
    elif (type(tree) is tuple) and tree[0] == "print":
        print(eval_exp(tree[1]))
    elif tree[0] == "assignment":
        name = tree[2]
        if name in var_env:
            print("Error variable already declared!!!")
        else:
            typeval = tree[1]
            val = tree[3]
            var_env[name] = [typeval, eval_exp(val)]
    elif tree[0] == "declaration":
        name = tree[2]
        if name in var_env:
            print("Error variable already declared!!!")
        else:
            typeval = tree[1]
            var_env[name] = []
    elif tree[0] == "variable":
        if tree[1] in var_env:
            return var_env[tree[1]][1]
        else:
            print("Error!!!")
    elif tree[0] == "+":
        return (eval_exp(tree[1]) + eval_exp(tree[2]))
    elif tree[0] == "-":
        return eval_exp(tree[1]) - eval_exp(tree[2])
    elif tree[0] == "*":
        return eval_exp(tree[1]) * eval_exp(tree[2])
    elif tree[0] == "/":
        return eval_exp(tree[1]) / eval_exp(tree[2])

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
