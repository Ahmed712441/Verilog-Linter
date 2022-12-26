from linter.helpers import *
from linter.arithmeticOverflow import *
from linter.initialization import * 
from linter.DrivenBus import *
# from linter.inferLatches import *
from linter.caseDetection import *
from parser.tokenizer import *

stream = None 
with open('E:/EDA 2/Project phase2/data/testfile5.v') as f:
    stream = f.read()

tokens = get_tokens(stream)
# variables , registers = get_variables(tokens)
# all_variables = variables | registers

all_variables = get_variables(tokens)
outputs_dict = get_dictonary_variables(list(filter(lambda x: x.direction == 'output',all_variables)))
registers_dict = get_dictonary_variables(list(filter(lambda x: x.type == 'reg',all_variables)))
all_variables_dict = get_dictonary_variables(all_variables)
output_wires_dict = get_dictonary_variables(list(filter(lambda x: x.type == 'wire' and x.direction == 'output' ,all_variables)))

statements = get_statements(tokens)
# blocks = get_blocks(tokens)
# print(blocks)
# filtered = list(filter(filterBlocks, blocks))
dontCareAssignment(statements)
detectOverflow(statements,all_variables_dict)
get_assignment_errors(statements,outputs_dict,all_variables_dict)
getCases(tokens,all_variables)
DrivenBus(statements,output_wires_dict,all_variables_dict)
# print()
# infer_latch(statements,blocks,registers,all_variables)
# arr = []
# get_all_dontCareComb('01011',arr,'','x')
# print(arr)
# '00011'
# '00001'
# '01001'
# '01011'