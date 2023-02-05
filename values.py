from errors import *
from runtime import RTResult
from context import Context
from symboltable import SymbolTable
import os, time, math, random
from args import BUILTIN_ARGS,BUILTIN_OBJS,REAL_BUILTIN_ARGS

interpreter = None
main_run = None

class Value:
    typename = "any"
    def __init__(self):
        self.set_pos()
        self.set_context()
        self.parent_obj = None
        
    def set_obj(self,obj):
        self.parent_obj = obj
        return self

    def set_pos(self, ps=None, pe=None):
        self.pos_start = ps
        self.pos_end = pe
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()
        
    def set_context(self,context=None):
        self.context = context
        return self
    
    def copy(self):
        raise Exception("No copy method defined")
    
    def is_true(self):
        return False
    
    def illegal_operation(self,other=None):
        if not other: other = self
        return RTError(
            self.pos_start,other.pos_end,
            "Illegal operation",self.context
        )
        
    def execute(self):
        pass

class Number(Value):
    typename = "number"
    def __init__(self, value):
        super().__init__()
        self.value = value

    def set_pos(self, ps=None, pe=None):
        self.pos_start = ps
        self.pos_end = pe
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value+other.value).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value-other.value).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value*other.value).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Division by zero",
                    self.context
                )
            return Number(self.value/other.value).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
        
    def set_context(self,context=None):
        self.context = context
        return self
    
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        return self.value != 0
        
    def __repr__(self) -> str:
        return str(self.value)
    
Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)

class String(Value):
    typename = "string"
    def __init__(self,value):
        super().__init__()
        self.value = value
        
    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)
        
    def get_comparison_ne(self, other):
        if isinstance(other, String):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None,self.illegal_operation(other)
        
    def added_to(self, other):
        if isinstance(other,String):
            return String(self.value+other.value).set_context(self.context),None
        else:
            return None,self.illegal_operation(other)
        
    def multed_by(self, other):
        if isinstance(other,Number):
            return String(self.value*other.value).set_context(self.context),None
        else:
            return None,self.illegal_operation(other)
        
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start,self.pos_end)
        return copy
    
    def __repr__(self) -> str:
        return f'"{self.value}"'
    
    def __str__(self):
        return self.value

class Object(Value):
    typename = "object"
    def __init__(self,vars):
        super().__init__()
        self.vars:dict = vars
        
    def check(self,context):
        for val in self.vars.values():
            if isinstance(val,Function):
                count = 0
                for arg in val.arg_names:
                    if arg == "this":
                        count += 1
                if count > 1:
                    return RTResult().failure(RTError(
                        self.pos_start,self.pos_end,
                        "'this' is a reserved parameter name",context
                    ))
        return RTResult().success(self)
        
    def finish(self):
        for name,val in self.vars.items():
            if isinstance(val,Function):
                val.arg_names.insert(0,"this")
                val.name = f"<<object>.{name}>"
        return self
        
    def added_to(self, other):
        new_obj = self.copy()
        new_obj.vars.update(other.vars)
        return new_obj,None
    
    def copy(self):
        copy = Object(self.vars)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self) -> str:
        return ', '.join([str(n)+" = "+str(v) for n,v in self.vars.items()])
    
    def __repr__(self) -> str:
        return "{"+', '.join([str(n)+" = "+str(v) for n,v in self.vars.items()])+"}"

class List(Value):
    typename = "list"
    def __init__(self,elements):
        super().__init__()
        self.elements = elements
        
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list,None
    
    def multed_by(self, other):
        if isinstance(other,List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list,None
        else:
            return None,self.illegal_operation(other)
        
    def subbed_by(self, other):
        if isinstance(other,Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list,None
            except:
                return None,RTError(
                    other.pos_start,other.pos_end,
                    "Element at index could not be removed because index is out of bounds",self.context
                )
        else:
            return None, self.illegal_operation(other)
        
    def dived_by(self, other):
        if isinstance(other,Number):
            try:
                return self.elements[other.value],None
            except:
                return None,RTError(
                    other.pos_start,other.pos_end,
                    "Element at index could not be retrieved because index is out of bounds",self.context
                )
        else:
            return None, self.illegal_operation(other)
        
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self) -> str:
        return ', '.join([str(x) for x in self.elements])
    
    def __repr__(self) -> str:
        return f"[{', '.join([str(x) for x in self.elements])}]"

class BaseFunction(Value):
    typename = "function"
    def __init__(self,name):
        super().__init__()
        self.name = name or "<anonymus>"
        
    def generate_new_context(self):
        new_context = Context(self.name,self.context,self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
    
    def check_args(self,arg_names,args):
        res = RTResult()
        errmsg = "allgood"
        if len(args) > len(arg_names):
            errmsg = f"{len(args)-len(arg_names)} too many args passed into {self.name}"
        elif len(args) < len(arg_names):
            errmsg = f"{len(arg_names)-len(args)} too few args passed into {self.name}"
        if errmsg != "allgood":
            return res.failure(RTError(
                self.pos_start,self.pos_end,errmsg,self.context
            ))
        return res.success(None)
    
    def populate_args(self,arg_names,args,exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name,arg_value)
            
    def check_and_populate_args(self,arg_names,args,exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names,args))
        if res.should_return(): return res
        self.populate_args(arg_names,args,exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self,name, body_node,arg_names,should_auto_return):
        super().__init__(name)
        
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return
        
    def execute(self,args):
        res = RTResult()
        interpreter_ = interpreter()
        exec_ctx = self.generate_new_context()
        
        res.register(self.check_and_populate_args(self.arg_names,args,exec_ctx))
        if res.should_return(): return res
        
        value = res.register(interpreter_.visit(self.body_node,exec_ctx))
        if res.should_return() and res.func_return_value == None: return res
        
        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)
    
    def copy(self):
        copy = Function(self.name,self.body_node,self.arg_names,self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start,self.pos_end)
        return copy
    
    def __repr__(self):
        return f"<function {self.name}>"
    
class BuiltInFunction(BaseFunction):
    def __init__(self,name,object_name=""):
        super().__init__(name)
        if object_name:
            self.name = f"{object_name}_{self.name}"
        
    def execute(self,args):
        res = RTResult()
        exec_ctx = self.generate_new_context()
        
        method_name = f"execute_{self.name}"
        method = getattr(self,method_name,self.no_execute_method)
        res.register(self.check_and_populate_args(REAL_BUILTIN_ARGS[self.name],args,exec_ctx))
        if res.should_return(): return res
        
        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        
        return res.success(return_value)
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start,self.pos_end)
        return copy
        
    def no_execute_method(self,context):
        raise Exception(f"No execute_{self.name} method defined")
    
    def __repr__(self) -> str:
        return f"<built-in function {self.name}>".replace("_",".")
    
    def check_types(self,values,types,ctx):
        for i,val in enumerate(values):
            if type(val) != types[i]:
                typestr = ', '.join(['\''+t.typename+'\'' for t in types])
                details = f"Arguments must be respectively of type: {typestr}"
                return RTResult().failure(RTError(
                    self.pos_start,self.pos_end,details,ctx
                ))
        return None
    
    def check_type(self,value,type_,ctx):
        if type(value) != type_:
            details = f"Argument must be of type: '{type_.typename}'"
            return RTResult().failure(RTError(
                self.pos_start,self.pos_end,details,ctx
            ))
        return None
    
    def get_values(self,ctx):
        return [ctx.symbol_table.get(arg) for arg in BUILTIN_ARGS[self.name]] if len(BUILTIN_ARGS[self.name]) > 1 else ctx.symbol_table.get(BUILTIN_ARGS[self.name][0])
    
    def return_null(self):
        return RTResult().success(Number.null)
    
    # BUILTINS
    
    def execute_log(self,ctx):
        value = self.get_values(ctx)
        print(str(value))
        return self.return_null()
    
    def execute_exit(self,ctx):
        value = str(self.get_values(ctx))
        return RTResult().failure(ExitError(value))
    
    def execute_quit(self,ctx):
        return self.execute_exit(ctx)
    
    def execute_input(self,ctx):
        text = input(str(self.get_values(ctx)))
        return RTResult().success(String(text))
    
    def execute_clear(self,ctx):
        os.system("cls" if os.name == "nt" else "clear")
        return self.return_null()
    
    def execute_cls(self,ctx):
        return self.execute_clear(ctx)
    
    def execute_istype(self,ctx):
        value,type_ = self.get_values(ctx)
        type_ = str(type_)
        typ = None
        specialtype = None
        if type_ == "string": typ = String
        elif type_ == "list": typ = List
        elif type_ == "function": typ = BaseFunction
        elif type_ == "int": typ = Number;specialtype=int
        elif type_ == "float":typ = Number;specialtype=float
        is_number = isinstance(value,typ)
        if specialtype:
            is_number = isinstance(value.value,specialtype)
        return RTResult().success(Number.true if is_number else Number.false)
    
    def execute_list(self,ctx):
        return RTResult().success(List(list()))
    
    def execute_string(self,ctx):
        return RTResult().success(String(""))
    
    def execute_range(self,ctx):
        start,end,step = self.get_values(ctx)
        err = self.check_types((start,end,step),(Number,Number,Number),ctx)
        if err != None:
            return err
        return RTResult().success(List([Number(i) for i in range(start.value,end.value,step.value)]))
    
    def execute_error(self,ctx):
        name,desc = self.get_values(ctx)
        return RTResult().failure(CustomError(f"{str(name)}: {str(desc)}"))
    
    def execute_len(self,ctx):
        value = self.get_values(ctx)
        res = RTResult()
        
        if isinstance(value,List):
            return res.success(Number(len(value.elements)))
        elif isinstance(value,String):
            return res.success(Number(len(value.value)))
        elif isinstance(value,(Number)):
            return res.success(Number(value.value))
        else:
            return res.success(Number.null)
    
    def execute_run(self,ctx):
        fn = self.get_values(ctx)
        err = self.check_type(fn,String,ctx)
        if err: return err
        fn = fn.value
        try:
            with open(fn,"r") as f:
                script = f.read()
        except:
            return RTResult().failure(RTError(
                self.pos_start,self.pos_end,
                f"Failed to load script '{fn}'",ctx
            ))
        if not ".sol" in fn:
            print("WARNING: scripts written in Solace should be inside '.sol' files")
        _,err = main_run(fn,script,True)
        if err:
            return RTResult().failure(RTError(
                self.pos_start,self.pos_end,
                f"Failed to finish executing script '{fn}'\n"+err.as_string(),ctx
            ))
        return RTResult().success(Number.null)
    
    def execute_String_replace(self,ctx):
        string,old,new,count = self.get_values(ctx)
        err = self.check_types((string,old,new,count),(String,String,String,Number),ctx)
        if err: return err
        return RTResult().success(String(string.value.replace(old.value,new.value,int(count.value))))
    
    def execute_String_toint(self,ctx):
        string = self.get_values(ctx)
        err = self.check_type(string,String,ctx)
        if err: return err
        try:
            return RTResult().success(Number(int(string.value)))
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Could not convert '{string}' to 'int'",ctx))
        
    def execute_String_tostring(self,ctx):
        value = self.get_values(ctx)
        return RTResult().success(String(str(value)))
        
    def execute_String_tofloat(self,ctx):
        string = self.get_values(ctx)
        err = self.check_type(string,String,ctx)
        if err: return err
        try:
            return RTResult().success(Number(float(string.value)))
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Could not convert '{string}' to 'float'",ctx))
        
    def execute_String_tolist(self,ctx):
        string = self.get_values(ctx)
        err = self.check_type(string,String,ctx)
        if err: return err
        return RTResult().success(List([String(val) for val in string.value]))
    
    def execute_String_empty(self,ctx):
        return RTResult().success(String(""))
    
    def execut_String_split(self,ctx):
        string,sep,count = self.get_values(ctx)
        err = self.check_types((string,sep,count),(String,String,Number),ctx)
        if err: return err
        return RTResult().success(List([String(val) for val in string.value.split(sep.value,count.value)]))
    
    def execute_String_lower(self,ctx):
        string = self.get_values(ctx)
        err = self.check_type(string,String,ctx)
        if err: return err
        return RTResult().success(String(string.value.lower()))
    
    def execute_String_upper(self,ctx):
        string = self.get_values(ctx)
        err = self.check_type(string,String,ctx)
        if err: return err
        return RTResult().success(String(string.value.upper()))
    
    def execute_String_title(self,ctx):
        string = self.get_values(ctx)
        err = self.check_type(string,String,ctx)
        if err: return err
        return RTResult().success(String(string.value.title()))
    
    def execute_String_capitalize(self,ctx):
        string = self.get_values(ctx)
        err = self.check_type(string,String,ctx)
        if err: return err
        return RTResult().success(String(string.value.capitalize()))
    
    def execute_String_count(self,ctx):
        string,substring = self.get_values(ctx)
        err = self.check_types((string,substring),(String,String),ctx)
        if err: return err
        return RTResult().success(Number(string.value.count(substring.value)))
    
    def execute_String_startswith(self,ctx):
        string,substring = self.get_values(ctx)
        err = self.check_types((string,substring),(String,String),ctx)
        if err: return err
        return RTResult().success(Number.true if string.value.startswith(substring.value) else Number.false)
    
    def execute_String_endswith(self,ctx):
        string,substring = self.get_values(ctx)
        err = self.check_types((string,substring),(String,String),ctx)
        if err: return err
        return RTResult().success(Number.true if string.value.endswith(substring.value) else Number.false)
    
    def execute_String_find(self,ctx):
        string,substring = self.get_values(ctx)
        err = self.check_types((string,substring),(String,String),ctx)
        if err: return err
        return RTResult().success(Number(string.value.find(substring.value)))
    
    def execute_String_rfind(self,ctx):
        string,substring = self.get_values(ctx)
        err = self.check_types((string,substring),(String,String),ctx)
        if err: return err
        return RTResult().success(Number(string.value.rfind(substring.value)))
    
    def execute_Float_toint(self,ctx):
        float_ = self.get_values(ctx)
        err = self.check_type(float_,Number,ctx)
        if err: return err
        return RTResult().success(Number(int(float_.value)))
    
    def execute_Time_now(self,ctx):
        return RTResult().success(Number(time.time()))
    
    def execute_Time_delta(self,ctx):
        last = self.get_values(ctx)
        err = self.check_type(last,Number,ctx)
        if err: return err
        return RTResult().success(Number(time.time()-last.value))
    
    def execute_File_read(self,ctx):
        name = self.get_values(ctx)
        err = self.check_type(name,String,ctx)
        if err: return err
        try:
            with open(name.value,"r") as file:
                return RTResult().success(String(file.read()))
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Cannot read from file '{name}'. Check if the file exists",ctx))
        
    def execute_File_write(self,ctx):
        name,content = self.get_values(ctx)
        err = self.check_types((name,content),(String,String),ctx)
        if err: return err
        try:
            with open(name.value,"w") as file:
                file.write(content.value)
                return self.return_null()
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Cannot write to file '{name}'. Check if the file exists",ctx))
        
    def execute_File_remove(self,ctx):
        name = self.get_values(ctx)
        err = self.check_type(name,String,ctx)
        if err: return err
        try:
            os.remove(name.value)
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Cannot remove file '{name}'. Check if the file exists",ctx))
        
    def execute_File_exists(self,ctx):
        name = self.get_values(ctx)
        err = self.check_type(name,String,ctx)
        if err: return err
        return RTResult().success(Number.true if os.path.exists(name.value) else Number.false)
    
    def execute_File_listdir(self,ctx):
        name = self.get_values(ctx)
        err = self.check_type(name,String,ctx)
        if err: return err
        try:
            return RTResult().success(List([String(val) for val in os.listdir(name.value)]))
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Cannot list the directory '{name}'. Check if it exists",ctx))
        
    def execute_List_add(self,ctx):
        list_,value = self.get_values(ctx)
        err = self.check_type(list_,List,ctx)
        if err: return err
        list_.elements.append(value)
        return RTResult().success(list_)
    
    def execute_List_extend(self,ctx):
        lista,listb = self.get_values(ctx)
        err = self.check_types((lista,listb),(List,List),ctx)
        if err: return err
        lista.elements.extend(listb.elements)
        return RTResult().success(lista)
    
    def execute_List_insert(self,ctx):
        list_,index,value = self.get_values(ctx)
        err = self.check_types((list_,index),(List,Number),ctx)
        if err: return err
        list_.elements.insert(index.value,value)
        return RTResult().success(list_)
    
    def execute_List_get(self,ctx):
        list_,index = self.get_values(ctx)
        err = self.check_types((list_,index),(List,Number),ctx)
        if err: return err
        try:
            return RTResult().success(list_.elements[index.value])
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Cannot get value at index '{index}' because it's out of bounds",ctx))
        
    def execute_List_set(self,ctx):
        list_,index,value = self.get_values(ctx)
        err = self.check_types((list_,index),(List,Number),ctx)
        if err: return err
        try:
            list_.elements[index.value]= value
            return RTResult().success(list_)
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Cannot set value at index '{index}' because it's out of bounds",ctx))
        
    def execute_List_pop(self,ctx):
        list_,index = self.get_values(ctx)
        err = self.check_types((list_,index),(List,Number),ctx)
        if err: return err
        try:
            list_.elements.pop(index.value)
            return RTResult().success(list_)
        except:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,f"Cannot pop value at index '{index}' because it's out of bounds",ctx))
        
    def execute_help(self,ctx):
        return RTResult().success(String(str(BUILTIN_ARGS).replace("{","").replace("{","").replace("'","")))
    
    def execute_Math_round(self,ctx):
        number,decimals = self.get_values(ctx)
        err = self.check_types((number,decimals),(Number,Number),ctx)
        if err: return err
        return RTResult().success(Number(round(number.value,decimals.value)))
    
    def execute_Math_floor(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.floor(number.value)))
    
    def execute_Math_cos(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.cos(number.value)))
    
    def execute_Math_sin(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.sin(number.value)))
    
    def execute_Math_tan(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.tan(number.value)))
    
    def execute_Math_acos(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.acos(number.value)))
    
    def execute_Math_asin(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.asin(number.value)))
    
    def execute_Math_atan(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.atan(number.value)))
    
    def execute_Math_pow(self,ctx):
        number,exponent = self.get_values(ctx)
        err = self.check_types((number,exponent),(Number,Number),ctx)
        if err: return err
        return RTResult().success(Number(math.pow(number.value,exponent.value)))
    
    def execute_Math_factorial(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.factorial(number.value)))
    
    def execute_Math_degrees(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.degrees(number.value)))
    
    def execute_Math_radians(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.radians(number.value)))
    
    def execute_Math_log(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        return RTResult().success(Number(math.log(number.value)))
    
    def execute_Math_sqrt(self,ctx):
        number = self.get_values(ctx)
        err = self.check_type(number,Number,ctx)
        if err: return err
        if number.value < 0:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,"Cannot take the square root of a negative number",ctx))
        return RTResult().success(Number(math.sqrt(number.value)))
    
    def execute_Random_randint(self,ctx):
        rangea,rangeb = self.get_values(ctx)
        err = self.check_types((rangea,rangeb),(Number,Number),ctx)
        if err: return err
        return RTResult().success(Number(random.randint(int(rangea.value),int(rangeb.value))))
    
    def execute_Random_randfloat(self,ctx):
        rangea,rangeb = self.get_values(ctx)
        err = self.check_types((rangea,rangeb),(Number,Number),ctx)
        if err: return err
        return RTResult().success(Number(random.uniform(rangea.value,rangeb.value)))
    
    def execute_Random_choice(self,ctx):
        list_ = self.get_values(ctx)
        err = self.check_type(list_,List,ctx)
        if len(list_.elements) <= 0:
            return RTResult().failure(RTError(self.pos_start,self.pos_end,"Cannot choose from an empty list",ctx))
        if err: return err
        return RTResult().success(Number(random.choice(list_.elements)))
    
class BuiltInObject(Object):
    def __init__(self,name):
        vars_ = {}
        for func in BUILTIN_OBJS[name]:
            vars_[func] = BuiltInFunction(func,name)
        super().__init__(vars_)