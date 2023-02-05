from lexer import *
from parsing import *
from interpreter import *
from context import *
from symboltable import *
import values
from args import BUILTIN_ARGS,BUILTIN_OBJS

global_symbol_table = SymbolTable()
global_symbol_table.set("null",Number.null)
global_symbol_table.set("true",Number.true)
global_symbol_table.set("false",Number.false)

for name in BUILTIN_ARGS.keys():
    if not "_" in name:
        global_symbol_table.set(name,BuiltInFunction(name))
for obj in BUILTIN_OBJS.keys():
    global_symbol_table.set(obj,BuiltInObject(obj))

def run(fn,text,isfromfile=False):
    lexer = Lexer(fn,text)
    tokens,error = lexer.make_tokens()
    if error:return None,error
    
    parser = Parser(tokens)
    ast = parser.parse(isfromfile)
    if ast.error: return None,ast.error
    
    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node,context)
    
    return result.value,result.error

values.main_run = run