#!/usr/bin/env python
# -*- coding: utf-8 -*-

####
#CI3725 - Etapa 1 - Análisis Lexicográfico
#Fabio, Castro, 10-10132
#Antonio, Scaramazza 11-10957
####
import ply.lex as lex

# Palabras reservadas del lenguaje
RESERVED = {
    # lenguaje
    'program' : 'PROGRAM',

    # tipos
    'int' : 'INT',
    'bool' : 'BOOL',
    'set' : 'SET',

    ## valores
    'true' : 'TRUE',
    'false' : 'FALSE',

    # instrucciones
    'using' : 'USING',
    'in' : 'IN',

    ## condicionales
    'if' : 'IF',
    'else' : 'ELSE',

    ## lazos
    'repeat' : 'REPEAT',
    'while' : 'WHILE',

    'do': 'DO',

    'for' : 'FOR',

    # Especiales del FOR

    'min':'MIN',
    'max':'MAX',

    ## entrada/salida
    'scan' : 'SCAN',

    'print' : 'PRINT',
    'println' : 'PRINTLN',

    # expresiones/operadores
    'or' : 'OR',
    'and' : 'AND',
    'not' : 'NOT',

    ## funciones
    #'def' : 'DEF',
    #'return': 'RETURN'
}

# Tokens a ser reconocidos
tokens = [
    # Lenguaje
    'NUMBER',
    'COMMA',
    'SEMICOLON',
    'ASSIGN',

    # IDENTIFICADORES
    'ID',

    # INSTRUCCIONES
    'STRING',

    # EXPRESIONES/OPERADORES
        # OPERADORES DE CONJUNTOS
            'SETPLUS',
            'SETMINUS',
            'SETTIMES',
            'SETMOD',
            'SETDIVITION',
            'SETMAX',
            'SETMIN',
            'SETLEN',
            'SETINTERSECTION',
            'SETUNION',
            'SETDIFFERENCE',
        # OPERADORES DE Enteros
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'MODULE',
        #  OPERADORES BOOLEANOS
            'LESS',
            'LESSEQ',
            'GREAT',
            'GREATEQ',
            'EQUAL',
            'UNEQUAL',
            # OPERADORES BOOLEANOS SOBRE CONJUNTOS
                'SETBELONG',   
        #  PARENTIZACION
           'OPENPAREN',
           'CLOSEPAREN',
           'OPENCURLY',
           'CLOSECURLY'
] + list(RESERVED.values())


# Token de Entero
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'%'

# Token de Set

t_LESS = r'\<'
t_GREAT = r'\>'

# Token de Separacion

t_COMMA = r','
t_SEMICOLON = r';'

# Token de Asignacion
t_ASSIGN = r'='

# Token de Parentizacion
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'

def t_OPENCURLY(token):
    r'\{'
    token.endlexpos = token.lexpos + len(token.value) - 1
    return token

def t_CLOSECURLY(token):
    r'\}'
    token.endlexpos = token.lexpos + len(token.value) - 1
    return token

def t_NUMBER(token):
    r'\d+'
    val = int(token.value)
    if val > 2147483648:
        error_NUMBER(token)

    token.endlexpos = token.lexpos + len(token.value) - 1
    token.value = val
    return token

def t_ID(token):
    r'\w[\w\d]*'
    # If there are no reserved words that match, it's an ID
    token.type = RESERVED.get(token.value, 'ID')
    token.endlexpos = token.lexpos + len(token.value) - 1
    return token

# Los Strings almacenan toda entrada sin importar los saltos de linea
# Siempre que estas esten entre " "

def t_STRING(token):
    r'\"([^\\\n]|(\\(n|"|\\)))*?\"'
    token.endlexpos = token.lexpos + len(token.value) - 1
    return token

# token de conjuntos
def t_SETPLUS(token): 
    r'\<\+\>'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETMINUS(token):
    r'\<\-\>'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETTIMES(token):
    r'\<\*\>'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETDIVITION(token):
    r'\<\/\>'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETMOD(token):
    r'\<\%\>'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETMAX(token):
    r'\>\?'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETMIN(token):
    r'\<\?'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETLEN(token):
    r'\$\?'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETINTERSECTION(token):
    r'\>\<'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETUNION(token):
    r'\+\+'
    token.endlexpos = token.lexpos + 1
    return token

def t_SETDIFFERENCE(token):
    r'\\'
    token.endlexpos = token.lexpos + 1
    return token

# token de booleano

def t_LESSEQ(token):
    r'\<\='
    token.endlexpos = token.lexpos + 1
    return token

def t_GREATEQ(token):
    r'\>\='
    token.endlexpos = token.lexpos + 1
    return token

def t_EQUAL(token):
    r'\=\='
    token.endlexpos = token.lexpos + 1
    return token

def t_UNEQUAL(token):
    r'\/\='
    token.endlexpos = token.lexpos + 1
    return token


#token de booleano sobre entero
def t_SETBELONG(token):
    r'\@'
    token.endlexpos = token.lexpos + 1
    return token

# Ignora espacion, tabuladores y comentarios en formato C
t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

# The only new line character considered is \n
def t_newline(token):
    r'\n+'
    token.lexer.lineno += token.value.count('\n')


# To find the column number of the current line
def find_column(text, lexpos):
    last_new = text.rfind('\n', 0, lexpos)
    if last_new < 0:
        last_new = -1
    column = lexpos - last_new
    return column


# Error to be shown if the lexer finds an "Unexpected" character
def t_error(token):
    text = token.lexer.lexdata
    message = "ERROR: unexpected character '%s' at line %d, column %d"
    data = token.value[0], token.lineno, find_column(text, token.lexer.lexpos)
    lexer_error.append(message % data)
    token.lexer.skip(1)


# Error to be shown if the lexer finds a number that's too large
def error_NUMBER(token):
    text = token.lexer.lexdata
    message = "ERROR: overflow for int '%s' at line %d, column %d"
    data = token.value, token.lineno, find_column(text, token.lexer.lexpos)
    lexer_error.append(message % data)

# Build the lexer
lexer = lex.lex()
lexer_error = []

###############################################################################


# The file (stored in a Python String)
# goes through the lexer and returns the list of tokens
def lexing(file_string, debug=0):

    lexer = lex.lex()
    tokens_list = []

    lexer.input(file_string, debug=debug)

    # Pass entire file through lexer
    for tok in lexer:
        tokens_list.append(tok)

    # If no "Unexpected character" or "Overflow" was found
    if not lexer_error:
        return tokens_list
    else:
        # Print all the errors
        for error in lexer_error:
            print error

        # Empty list to indicate error
        return []


# Only to be called if this is the main module
def main(argv=None):
    import sys      # argv, exit

    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        print "ERROR: No input file"
        return
    elif len(argv) > 3:
        print "ERROR: Invalid number of arguments"
        return

    if len(argv) == 3:
        debug = argv[2]
    else:
        debug = 0

    # Opens file to interpret
    file_string = open(argv[1], 'r').read()

    # Reads the file and passes it to the Lexer
    tokens_list = lexing(file_string, debug)

    for tok in tokens_list:
        print 'tok(' + str(tok.type) + ')' + '            '[:-(len(tok.type))],
        print 'val(' + str(tok.value) + ')',
        print 'at line ' + str(tok.lineno) + ',',
        print 'column ' + str(find_column(file_string, tok))


# If this is the module running
if __name__ == "__main__":
    main()