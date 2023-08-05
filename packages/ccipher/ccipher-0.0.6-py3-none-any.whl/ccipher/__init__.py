
import string
from typing_extensions import LiteralString


alphabet: LiteralString = string.ascii_lowercase
numbers: string = '0123456789'

from .decrypt import *
from .encrypt import *
from .commons import *

__all__ = [
    "alphabet",
    "numbers"
]

def decrypt(string: string, key: int) -> str: ...
def decrypt(string: string, key: int) -> str: ...


