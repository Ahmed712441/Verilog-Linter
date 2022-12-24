from linter.helpers import *
from linter.arithmeticOverflow import *
from linter.initialization import * 
from parser.tokenizer import *

stream = None 
with open('E:/EDA 2/Project phase2/data/testfile4.v') as f:
    stream = f.read()

tokens = get_tokens(stream)
variables , registers = get_variables(tokens)
statements = get_statements(tokens)
blocks = get_blocks(tokens)
filtered = list(filter(filterBlocks, blocks))
# dontCareAssignment(statements)
# detectOverflow(statements,variables)
block_assignment(statements,filtered,registers)
# print(filtered)

# print(statements)
# print(tokens)