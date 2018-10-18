## @file
## @brief in-memory knowledge/graph/object database

import os,sys,time

## @ingroup interp
## @{

try:
    ## source code file
    SRCFILE = sys.argv[1]
except IndexError:
    SRCFILE = 'src.src'

## init file will be parser on start
SRC = open(SRCFILE).read()

## @}

## @ingroup db
## @{

try:
    ## persistent database file (vocabulary snapshot)
    DBFILE = sys.argv[2]
except IndexError:
    DBFILE = sys.argv[0]+'.db'
    
## @}

## @defgroup sym Symbolic class system
## @dot
## digraph {
## rankdir=LR;
## Object -> Primitive;
## Object -> Container;
## Object -> Active;
## Object -> Doc;
## }
## @enddot
## @{

## base generic object
class Object:
    
    ## constructor
    def __init__(self,V):
        ## class/type tag
        self.type = self.__class__.__name__.lower()
        ## single primitive value
        self.value = V

    ## @defgroup print print/dump
    ## @brief represent any object in text forms
    ## @{
    
    ## represent any object in text form
    def __repr__(self):
        return self.dump()
    
    ## full dump of any object in tree form 
    def dump(self,depth=0):
        return self.head()
    
    ## short dump of any object: header only
    def head(self,prefix=''):
        return '%s<%s:%s>'%(prefix,self.type,self.value)
    
    ## @}

## @defgroup prim primitives
## @brief close to machine-level or VM implementation language  
## @{

## machine-level primitives
class Primitive(Object): pass

## @}

## @defgroup cont containers
## @brief data elements grouping
## @{

## data container
class Container(Object): pass

## ordered vector
class Vector(Container): pass

## LIFO stack
class Stack(Container): pass

## associative array
class Map(Container): pass

## @}

## @defgroup active active objects
## @brief has execution semantics
## @{

## callable objects has execution semantics
class Active(Object): pass

## @}

## @defgroup doc documenting
## @{

## documenting
class Doc(Object): pass

## @}

## @}

## @defgroup fvm FORTH Virtual Machine
## @{

## @defgroup stack stack
## @{

## data stack
S = Stack('DATA')

## @}

## @defgroup voc vocabulary
## @}

## @}

## @}

## @defgroup parser Syntax parser
## @{

import ply.lex  as lex
import ply.yacc as yacc

## token list will be parsed
tokens = ['SYM']

## ignore spaces
t_ignore = ' \t\r'

## ignore comments
t_ignore_COMMENT = '\#.*'

## increment line counter
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

## symbol
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    return t

## lexer error callback
def t_error(t): raise SyntaxError(t)

## syntax lexer
lexer = lex.lex()

## @}

## @defgroup interp interpreter
## @ingroup fvm
## @{

## interpret given string
def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        token = lexer.token()
        if not token: break
        print '<%s>' % token

INTERPRET(SRC)

print S

## @}

## @defgroup web Web interface
## @{

## @defgroup serv server
## @brief (web)server
## @ingroup sym
## @{

import socket

## (web)server
class Server(Object):
    ## tcp/ip address to bind
    IP   = '127.0.0.1'
    ## tcp/ip port to bind
    PORT = 8888
    ## response template
    RESP = 'HTTP/1.0 200 OK\nContent-type: text/plain\nContent-length: %i\n\n%s'
    def __init__(self,V):
        Object.__init__(self, V)
        self.sock = socket.socket()
        self.sock.bind((self.IP,self.PORT))
        self.sock.listen(0)
        client,(ip,port) = self.sock.accept()
        client.sendall(self.RESP % (len(self.dump()),self.dump()))
        
print Server('web')

## @}

## @}
