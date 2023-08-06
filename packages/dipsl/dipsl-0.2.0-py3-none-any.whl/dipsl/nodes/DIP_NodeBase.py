from typing import List
from pydantic import BaseModel

from ..DIP_Source import Source

class NodeBase(BaseModel):
    code: str 
    source: Source = None
    keyword: str = None
    dtype = str
    indent: int = 0
    name: str = None
    value_raw: str = None           # Raw value
    value_ref: str = None           # Reference
    value_fn: str = None            # Function
    value_expr: str = None          # Expression
    value_slice: List[tuple] = None # Slice
    units_raw: str = None           # Ras units
    defined: bool = False
    dimension: List[tuple] = None
    options: List[BaseModel] = None  
