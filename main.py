from linter.helpers import *
from linter.arithmeticOverflow import *
from linter.initialization import * 
# from linter.inferLatches import *
from linter.caseDetection import *
from parser.tokenizer import *

stream = None 
with open('E:/EDA 2/Project phase2/data/testfile3.v') as f:
    stream = f.read()

tokens = get_tokens(stream)
variables , registers = get_variables(tokens)
all_variables = variables | registers
statements = get_statements(tokens)
# blocks = get_blocks(tokens)
# print(blocks)
# filtered = list(filter(filterBlocks, blocks))
# dontCareAssignment(statements)
# detectOverflow(statements,variables)
# get_assignment_errors(statements,registers,all_variables)
# getCases(tokens,all_variables)
print()
# infer_latch(statements,blocks,registers,all_variables)
# arr = []
# get_all_dontCareComb('01011',arr,'','x')
# print(arr)
# '00011'
# '00001'
# '01001'
# '01011'