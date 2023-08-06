from pydantic import BaseModel
import copy

from ..DIP_Environment import Environment
from ..settings import Format
from ..datatypes import Type

class FunctionSolver(BaseModel):

    env: Environment

    def __init__(self, env:Environment=None, **kwargs):
        if env:
            kwargs['env'] = env
        else:
            kwargs['env'] = Environment()
        super().__init__(**kwargs)
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass

    def solve(self, fn_name:str, in_units=None):
        fn = self.env.functions[fn_name]
        data = copy.deepcopy(self.env.data(format=Format.TYPE))
        result = fn(data)
        if isinstance(result, Type):
            if in_units:
                result.convert(in_units)
            return result.value
        else:
            return result
