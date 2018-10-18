## @file

import os,sys,time

try:                SRCFILE = sys.argv[1]
except IndexError:  SRCFILE = 'src.src'

## init file will be parser on start
SRC = open(SRCFILE).read()

try:                DBFILE = sys.argv[2]
except IndexError:  DBFILE = sys.argv[0]+'.db'

## @defgroup parser Syntax parser
## @{

import ply.lex  as lex
import ply.yacc as yacc

tokens = ['SYM']

t_ignore_COMMENT = '\#.*'

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    return t

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()
lexer.input(SRC)

## @}

def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        token = lexer.token()
        if not token: break
        print '<%s>' % token

INTERPRET(SRC)
