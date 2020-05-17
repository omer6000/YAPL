import lexer
import parser
import ply.lex as lex
import ply.yacc as yacc
import sys

var_env = {}
var_struct = {}
def eval_exp(tree):
    global var_env
    global var_struct
    # print(tree)
    if type(tree) is int:
        return tree
    elif type(tree) is float:
        return tree
    elif type(tree) is str:
        return tree
    elif (type(tree) is tuple) and tree[0] == "print":
        arr = tree[1]
        if len(arr) > 0:
            for x in arr:
                try:
                    print(eval_exp(x),"",end="")
                except:
                    print("TypeError")
                    sys.exit()
            print("")
    elif tree[0] == "struct":
        # print(tree)
        name = tree[1]
        if name in var_struct:
            print("Structure already declared!!")
            sys.exit()
        else:
            var_struct[name] = []
            for var in tree[2]:
                var_struct[name].append((var[1], var[2]))
    elif tree[0] == "dowhile":
        pass
        # print(tree[1])
        pass
        while True:
            code_inside = tree[1]
            for x in code_inside:
                eval_exp(x)
            condition = tree[2]
            condition_tuple = (condition[1], condition[2], condition[3])
            for x in code_inside: # Removing variables
                if x[0] == "assignment":
                    del var_env[x[2]]
            if not eval_exp(condition_tuple):
                break
    elif tree[0] == "assignment":
        name = tree[2]
        if name in var_env:
            print("RedeclarationError")
            sys.exit()
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
        typeval = tree[1]
        if (typeval in var_struct) == False:
            print("Wrong data type!")
            sys.exit()
        elif typeval in var_struct:
            var_env[name] = {}
        elif name in var_env:
            print("RedeclarationError")
            sys.exit()
        else:
            var_env[name] = [typeval, ""]
    elif tree[0] == "variable_update":
        name = tree[1]
        val = tree[2]
        if ("." in name) and (name.split(".")[0] in var_env):
            struct_name = name.split(".")[0]
            variable_name = name.split(".")[1]
            var_env[struct_name][variable_name] = val
            # print(var_env)
        elif name in var_env:
            typeval = var_env[name][0]
            if typeval == 'bool' and val == "false":
                var_env[name] = [typeval, False]
            elif typeval == 'bool' and val == "true":
                var_env[name] = [typeval, True]
            else:
                var_env[name] = [typeval, eval_exp(val)]
        else:
            print("Variable does not exist!!")
            sys.exit()
    elif tree[0] == "variable":
        if tree[1] in var_env:
            return var_env[tree[1]][1]
        elif ("." in tree[1]) and (tree[1].split(".")[0] in var_env) and (tree[1].split(".")[1] in var_env[tree[1].split(".")[0]]):
            return var_env[tree[1].split(".")[0]][tree[1].split(".")[1]]
        else:
            print("AttributeError")
            sys.exit()
    elif tree[0] == "increment":
        if tree[1][0] == 'variable' and (tree[1][1] in var_env):
            var_env[tree[1][1]][1] = var_env[tree[1][1]][1] + 1
    elif tree[0] == "decrement":
        if tree[1][0] == 'variable' and (tree[1][1] in var_env):
            var_env[tree[1][1]][1] = var_env[tree[1][1]][1] - 1
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
        return eval_exp(tree[1]) == eval_exp(tree[2])
    elif tree[0] == "!=":
        return eval_exp(tree[1]) != eval_exp(tree[2])
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
