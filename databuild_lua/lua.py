import functools
import warnings

from lupa import LuaRuntime

from databuild import settings
from databuild.loader import load_module

from databuild.environments.base import BaseEnvironment


class LuaEnvironment(BaseEnvironment):
    def __init__(self, book):
        lua_runtime = LuaRuntime()
        functions = []
        [functions.extend(load_module(module)) for module in settings.FUNCTION_MODULES]
        lua_globals = lua_runtime.globals()

        for fn in functions:
            if fn.__name__ not in lua_globals:
                lua_globals[fn.__name__] = functools.partial(fn, self, book)
            else:
                warnings.warn("Function '%s' already present in Lua Environment. Skipping.")

        self.runtime = lua_runtime
        super(LuaEnvironment, self).__init__(book)

    def lua_copy(self):
        return self.runtime.eval("""
function(L)
    local t = {}
    for index, item in python.enumerate(L) do
        t[ index+1 ] = item
    end
    return t
end
        """)

    def add_to_globals(self, iterable):
        lua_globals = self.runtime.globals()
        for k, v in iterable:
            lua_globals[k] = self.copy(v)

    def copy(self, value):
        if isinstance(value, (list, tuple, dict)):
            return self.lua_copy(value)
        return value

    def eval(self, expression, context):
        func = 'function(row) %s end' % expression
        return self.runtime.eval(func)
