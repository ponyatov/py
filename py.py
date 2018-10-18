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

## @defgroup web Web interface
## @{

## @defgroup serv server
## @brief (web)server
## @ingroup sym
## @{

# https://www.junian.net/python-http-server-client/
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket,ssl,threading

## http(s) (web)server
class Server(Object):

    ## tcp/ip address to bind
    IP   = '127.0.0.1'

    ## tcp/ip port to bind
    PORT = 8885

    ## http(s) GET handler
    class HTTPhandler(BaseHTTPRequestHandler):
        ## GET handler
        ## @param[in] self.path URL
        def do_GET(self):
            # response header
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            # body
            self.wfile.write('%s\n---------------\n%s' % (self.path, S.dump()))
            return
    
    ## constructor with name
    def __init__(self,V):
        Object.__init__(self, V)
        ## wrapped HTTP server
        self.server = HTTPServer((self.IP,self.PORT), self.HTTPhandler)
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ## wrapped thread in background
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon=True
        self.thread.start()
    ## stop server
    def stop(self):
        self.server.shutdown()
        self.server.server_close()
    ## warp in HTTPS
    def https(self):
        server.socket = ssl.wrap_socket(self.server.socket, keyfile='./key.pem', certfile='./cert.pem', server_side=True)
        
print Server('web')

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

while True:
    print S
    INTERPRET(raw_input('> '))

## @}

## @}
