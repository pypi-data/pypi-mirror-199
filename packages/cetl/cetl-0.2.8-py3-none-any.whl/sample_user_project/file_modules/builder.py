import sys, os
sys.path.insert(0, os.path.join(".."))


from cetl.utils.registry import Registry
from cetl.utils.builder import add_register


FILE_TRANSFORMERS = Registry("file")
add_register(register=FILE_TRANSFORMERS)