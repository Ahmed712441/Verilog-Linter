from linter.helpers import *
from linter.arithmeticOverflow import *
from linter.initialization import * 
from linter.DrivenBus import *
from linter.caseDetection import *
from linter.FSM import *
from parser.tokenizer import *
from pathlib import Path
import os
import json



stream = None 
config = None

with open(os.path.join(BASE_DIR , 'data','testfile6.v')) as f:
    stream = f.read()

with open(os.path.join(BASE_DIR , 'config','config.json')) as f:
    config = json.load(f)

tokens = get_tokens(stream)
all_variables = get_variables(tokens)
outputs_dict = get_dictonary_variables(list(filter(lambda x: x.direction == 'output',all_variables)))
registers_dict = get_dictonary_variables(list(filter(lambda x: x.type == 'reg',all_variables)))
all_variables_dict = get_dictonary_variables(all_variables)
output_wires_dict = get_dictonary_variables(list(filter(lambda x: x.type == 'wire' and x.direction == 'output' ,all_variables)))

statements , intialized_reg_stat = get_statements(tokens)
cases = getCases(tokens,all_variables_dict)
initialized_registers = getIntializedRegisters(intialized_reg_stat)
# initOutFile()

if config and config["Donot Care Assignment"]:
    dontCareAssignment(statements)

if config and config["Overflow"]:
    detectOverflow(statements,all_variables_dict)

if config and config["Intialization"]:
    get_assignment_errors(statements,outputs_dict,all_variables_dict)

if config and config["Non Full/Parallel Cases"]:
    getCasesErrors(cases)

if config and config["DrivenBus"]:
    DrivenBus(statements,output_wires_dict,all_variables_dict)

if config and config["UnreachableFSM and deadlocks"]:
    getUnreachableFSM(statements,cases,initialized_registers)


writeOutFile()