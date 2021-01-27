import ply.yacc as yacc
from AnalizadorLexico import tokens
import re
import sys
import ply.lex as lex 

resultado_gramatica = []
#ASIGNACIÓN DE LA PRECEDENCIA (IZQUIERDA DERECHA) CON MAYOR INDICE DE IMPORTANCIA
precedence = (
    ('right', 'IF','ELSE','FOR'),
    ('left', 'PARENTIZQ','PARENTDER'),
    ('right', 'PTCOMA'),
    ('left', 'SUMA', 'MENOS'),
    ('left', 'MULTIPLICAR', 'DIVISION'),
    ('right', 'NUMBER'),
    ('right', 'IGUALQUE'),
    ('right', 'ID')
)

nombres = {}
#RECONOCIMIENTO PARA OPERACIONES BÁSICAS (DECLARADAS EN LA PRECENDENCIA)
def p_declaracion_asignar(t):
    'declaracion :  TIPO ID IGUALQUE expresion PTCOMA'
    nombres[t[1]] = t[3]

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

#RECONOCIMIENTO DE LAS EXPRESIONES BÁSICAS Y ASIGNACIÓN DE POSICIONES EN LA ENTRADA
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

#RECONOCIMIENTO DE PARENTESIS
def p_expresion_grupo(t):
    '''
    expresion  : PARENTIZQ expresion PARENTDER
                | CORCHETEIZQ expresion CORCHETEDER
    '''
    t[0] = t[2]
#RECONOCIMEINTO DE LOS BUCLES IF ELSE Y FOR
def p_expresion_bucle(t):
    '''
    expresion : IF PARENTIZQ expresion MENORIGUALQUE expresion PARENTDER PARENTIZQ expresion IGUALIGUAL expresion PTCOMA PARENTDER ELSE PARENTIZQ expresion IGUALIGUAL expresion PTCOMA PARENTDER
                |  FOR PARENTIZQ expresion IGUALQUE expresion PTCOMA expresion MAYORQUE expresion PTCOMA expresion MASMAS PARENTDER PARENTIZQ ID PARENTDER
    '''
#RECONOCIMIENTO DE LAS OPERACIONES LÓGICAS Y SU POSICIÓN
def p_expresion_logicas(t):
    '''
    expresion   :  expresion MENORQUE expresion 
                |  expresion MAYORQUE expresion 
                |  expresion MENORIGUALQUE expresion 
                |   expresion MAYORIGUALQUE expresion 
                |   expresion IGUALQUE expresion 
                |   IF PARENTIZQ expresion MENORQUE expresion PARENTDER CORCHETEIZQ expresion PTCOMA CORCHETEDER
                |   IF PARENTIZQ expresion MAYORQUE expresion PARENTDER CORCHETEIZQ expresion PTCOMA CORCHETEDER
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
    
#DECLARACIÓN DE ALGUNAS ESTRUCTURAS DE RECONOCIMIENTO ESPECIFICO    
def p_expresion_int(t):
    'expresion : TIPO ID IGUALQUE NUMBER PTCOMA'
    t[0] = t[1]


def p_expresion_deci(t):
    'expresion : TIPO ID IGUALQUE DECIMAL SUMA DECIMAL PTCOMA'
    t[0] = t[1]

def p_expresion_id(t):
    'expresion : ID'
    t[0] = t[1]

def p_expresion_cori(t):
    'expresion : CORCHETEIZQ'
    t[0] = t[1]

def p_expresion_cord(t):
    'expresion : CORCHETEDER'
    t[0] = t[1]

def p_expresion_cont(t):
    'expresion : ID IGUALQUE ID SUMA NUMBER PTCOMA'
    t[0] = t[1]

def p_expresion_intd(t):
    'expresion : TIPO ID PTCOMA'
    t[0] = t[1]

def p_expresion_intm(t):
    'expresion : TIPO ID IGUALQUE ID MENOS NUMBER PTCOMA'
    t[0] = t[1]

def p_expresion_intt(t):
    'expresion : TIPO ID IGUALQUE ID MULTIPLICAR ID PTCOMA'
    t[0] = t[1]

def p_expresion_intc(t):
    'expresion : TIPO ID IGUALQUE ID PTCOMA'
    t[0] = t[1]

def p_expresion_number(t):
    'expresion : NUMBER'
    t[0] = t[1]

def p_expresion_dec(t):
    'expresion : INT'
    t[0] = t[1]

#CON LA EXISTENCIA DE ERROR SE PRESENTA EL TIPO DE ERROR
def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {:4} en el valor {:4}".format(
            str(t.type), str(t.value))
    else:
        resultado = "Error sintactico {}".format(t)
    resultado_gramatica.append(resultado)

parser = yacc.yacc()
#IMPRIMIR LOS RESULTADOS
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
print('----PRUEBA----')
print("")
print('\n'.join(list(map(''.join, resultado_gramatica))))