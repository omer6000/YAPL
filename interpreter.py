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
        if len(tree[1]) > 0:
            print(tree[1][0],"", end="")
            arr = tree[1][1:]
            eval_exp(("print", arr))
    elif tree[0] == "dowhile":
        print(tree)
    elif tree[0] == "assignment":
        name = tree[2]
        if name in var_env:
            print("Error variable already declared!!!")
        else:
            typeval = tree[1]
            val = tree[3]
            if typeval == 'bool' and val == "false":
                var_env[name] = [typeval, False]
            elif typeval == 'bool' and val == "true":
                var_env[name] = [typeval, True]
            else:
                var_env[name] = [typeval, eval_exp(val)]
    elif tree[0] == "declaration":
        name = tree[2]
        if name in var_env:
            print("Error variable already declared!!!")
        else:
            typeval = tree[1]
            var_env[name] = [typeval, ""]
    elif tree[0] == "variable_update":
        name = tree[1]
        val = tree[2]
        if name in var_env:
            typeval = var_env[name][0]
            if typeval == 'bool' and val == "false":
                var_env[name] = [typeval, False]
            elif typeval == 'bool' and val == "true":
                var_env[name] = [typeval, True]
            else:
                var_env[name] = [typeval, eval_exp(val)]
        else:
            print("Variable does not exist!!")
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
    elif tree[0] == "^":
        return eval_exp(tree[1]) ** eval_exp(tree[2])
    elif tree[0] == "%":
        return eval_exp(tree[1]) % eval_exp(tree[2])
    elif tree[0] == ">":
        return eval_exp(tree[1]) > eval_exp(tree[2])
    elif tree[0] == ">=":
        return eval_exp(tree[1]) >= eval_exp(tree[2])
    elif tree[0] == "<":
        return eval_exp(tree[1]) < eval_exp(tree[2])
    elif tree[0] == "<=":
        return eval_exp(tree[1]) <= eval_exp(tree[2])
    elif tree[0] == "==":
        return eval_exp(tree[1]) <= eval_exp(tree[2])
    elif tree[0] == "&&":
        val_left = None
        val_right = None
        if tree[1] == "false":
            val_left = False
        elif tree[1] == "true":
            val_left = True
        else:
            val_left = eval_exp(tree[1])
        if tree[2] == "false":
            val_right = False
        elif tree[2] == "true":
            val_right = True
        else:
            val_right = eval_exp(tree[2])
        return val_left and val_right
    elif tree[0] == "||":
        val_left = None
        val_right = None
        if tree[1] == "false":
            val_left = False
        elif tree[1] == "true":
            val_left = True
        else:
            val_left = eval_exp(tree[1])
        if tree[2] == "false":
            val_right = False
        elif tree[2] == "true":
            val_right = True
        else:
            val_right = eval_exp(tree[2])
        return val_left or val_right
    elif tree[0] == "not":
        if tree[1] == "false":
            return True
        elif tree[1] == "true":
            return False
        else:
            return not eval_exp(tree[1])
 
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
