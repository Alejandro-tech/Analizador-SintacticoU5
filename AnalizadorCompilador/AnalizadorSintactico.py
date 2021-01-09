import ply.yacc as yacc
from AnalizadorLexico import tokens
import re
import sys
import ply.lex as lex 

resultado_gramatica = []

precedence = (
    ('right', 'IF','ELSE'),
    ('left', 'PARENTIZQ','PARENTDER'),
    ('right', 'PTCOMA'),
    ('left', 'SUMA', 'MENOS'),
    ('left', 'MULTIPLICAR', 'DIVISION'),
    ('right', 'NUMBER'),
    ('right', 'IGUALQUE'),
    ('right', 'ID')
)

nombres = {}

def p_declaracion_coditionif(t):
    'declaracion : IF'
    t[0] = t[1]

def p_declaracion_EQUALS(t):
    'declaracion : IGUALQUE'
    t[0] = t[1]

def p_declaracion_coditionelse(t):
    'declaracion : ELSE'
    t[0] = t[1]

def p_declaracion_comma(t):
    'expresion :  PTCOMA'
    t[0] = t[1]

def p_declaracion_expr(t):
    'declaracion : expresion'
    t[0] = t[1]


def p_expresion_operaciones(t):
    '''
    expresion  :   expresion SUMA expresion
                |   expresion MENOS expresion
                |   expresion MULTIPLICAR expresion
                |   expresion DIVISION expresion
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    if t[2] == '-':
        t[0] = t[1] + t[3]
    if t[2] == '*':
        t[0] = t[1] + t[3]
    if t[2] == '/':
        t[0] = t[1] + t[3]

def p_expresion_grupo(t):
    '''
    expresion  : PARENTIZQ expresion PARENTDER
                | CORCHETEIZQ expresion CORCHETEDER
    '''
    t[0] = t[2]

def p_expresion_logicas(t):
    '''
    expresion   :  expresion MENORQUE expresion 
                |  expresion MAYORQUE expresion 
                |  expresion MENORIGUALQUE expresion 
                |   expresion MAYORIGUALQUE expresion 
                |   expresion IGUALQUE expresion 
                |   PARENTIZQ expresion MENORQUE expresion PARENTDER
                |   IF PARENTIZQ expresion MAYORQUE expresion PARENTDER
                |   PARENTIZQ expresion MENORIGUALQUE expresion PARENTDER
                |   PARENTIZQ expresion MAYORIGUALQUE expresion PARENTDER
                |   PARENTIZQ expresion IGUALQUE expresion PARENTDER

    '''
    if t[2] == "<":
        t[0] = t[1] < t[3]
    elif t[2] == ">":
        t[0] = t[1] > t[3]
    elif t[2] == "<=":
        t[0] = t[1] <= t[3]
    elif t[2] == ">=":
        t[0] = t[1] >= t[3]
    elif t[2] == "=":
        t[0] = t[1] is t[3]
    elif t[3] == "<":
        t[0] = t[2] < t[4]
    elif t[2] == ">":
        t[0] = t[2] > t[4]
    elif t[3] == "<=":
        t[0] = t[2] <= t[4]
    elif t[3] == ">=":
        t[0] = t[2] >= t[4]
    elif t[3] == "=":
        t[0] = t[2] is t[4]
    
def p_expresion_numero(t):
    'expresion : NUMBER'
    t[0] = t[1]

def p_expresion_int(t):
    'expresion : INT ID IGUALQUE NUMBER PTCOMA'
    t[0] = t[1]

def p_expresion_intd(t):
    'expresion : INT ID PTCOMA'
    t[0] = t[1]

def p_expresion_intt(t):
    'expresion : INT ID IGUALQUE ID MULTIPLICAR ID PTCOMA'
    t[0] = t[1]

def p_expresion_intc(t):
    'expresion : INT ID IGUALQUE ID PTCOMA'
    t[0] = t[1]

def p_expresion_id(t):
    'expresion : ID'
    t[0] = t[1]

def p_expresion_end(t):
    'expresion : END'
    t[0] = t[1]

def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {:4} en el valor {:4}".format(
            str(t.type), str(t.value))
    else:
        resultado = "Error sintactico {}".format(t)
    resultado_gramatica.append(resultado)

parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
   
    for item in data.splitlines():
        if item:
            gram = parser.parse(item)
            if gram:
                resultado_gramatica.append(str(gram))
        else:
            print("")
    return resultado_gramatica

try:
    file_name = sys.argv[1]
    archivo = open(file_name, "r")
except:
    print("el archivo no se encontro")
    quit()

text = ""
for linea in archivo:
    text += linea

prueba_sintactica(text)
print("")
print('>>>>> COMPROBACIÓN DE ERRORES <<<<<')
print('>>>>> NONE MARCA QUE NO EXISTE ERRORES <<<<<')
print("")
print('\n'.join(list(map(''.join, resultado_gramatica))))
print('-------------------------------------------------')