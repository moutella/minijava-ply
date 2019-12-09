from minijavaparse import result, table
from symbol_table import *

conta_chamada_atual = 0
def conta_parametros(node, counter):
    global conta_chamada_atual
    if type(node) == tuple:
        for item in node:
            conta_parametros(item, conta_chamada_atual)
    if node == 'exp':
        conta_chamada_atual += 1
def semantics_check(node):
    if type(node) == tuple:
        if node[0] == "main":
            add_symbol_to_scope(node[12])
            new_scope()
            semantics_check(node[15])
            pop_scope()
            pop_scope()
        elif node[0] == "classe":
            new_scope()
            if len(node) == 10:
                semantics_check(node[6])
                semantics_check(node[7])
            else:
                semantics_check(node[4])
                semantics_check(node[5])
            pop_scope()
        elif node[0] == "pexp":
            
            if type(node[1])!=tuple:
                if len(node)==5:
                    semantics_check(node[1])
                    symbol_lookup(node[1], node[-1])
                    search_method(node[1],node[3],node[-1])
                elif len(node)==8:
                    symbol_lookup(node[1], node[-1])
                    search_method(node[1][2],node[3],node[-1])
                    semantics_check(node[1])
                elif len(node)==7:
                    semantics_check(node[1])
                    symbol_lookup(node[1], node[-1])
                    search_method(node[1],node[3],node[-1])
                elif len(node)==6:
                    semantics_check(node[1])
                    symbol_lookup(node[2], node[-1])
                elif len(node)==5:
                    semantics_check(node[1])
                    pass
            else:
                if len(node)==8:
                    search_method(node[1][2],node[3],node[-1])
                    conta_parametros(node[5], 0)
                    global conta_chamada_atual
                    verify_method_params(conta_chamada_atual, node[3], node[1][2], node[-1])
                    conta_chamada_atual = 0
                    
                else:
                    semantics_check(node[1])
        elif node[0] == "cmd":
            if len(node)==6:
                symbol_lookup(node[1],node[-1])
            elif len(node)==9:
                if node[1]!="if":
                    symbol_lookup(node[1],node[-1])
            elif len(node) == 7:
                semantics_check(node[3])
        elif node[0] == "var":
            if type(node[1]) != tuple:
                symbol_lookup(node[1], node[-1])
            add_symbol_to_scope(node[2])
        
        else:
            for item in node:
                semantics_check(item)
    else:
        pass
        # if type(entrada) == str:
        #     cgenstring(entrada)
        # else:
        #     cgenint(entrada)



check_dependencies()
new_scope()    
semantics_check(result)