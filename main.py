from linter.helpers import *
from linter.arithmeticOverflow import *
from linter.initialization import * 
from linter.DrivenBus import *
from linter.caseDetection import *
from linter.FSM import *
from parser.tokenizer import *
import os
import json
import argparse

parser = argparse.ArgumentParser(description='Verliog Linter')

parser.add_argument('--file_path', type=str,
                    help='your verliog code file that you want to make analysis on')

parser.add_argument('--config_path', type=str,
                    help='your configuration file which has the configuration of the lint')

parser.add_argument('--output_path', type=str,
                    help='your configuration file which has the configuration of the lint')

args = parser.parse_args()
# print(args.file_path , args.config_path , args.output_path)

path = args.file_path if args.file_path else os.path.join(BASE_DIR , 'data','testfile5.v')
output_path = args.output_path if args.output_path else os.path.join(BASE_DIR,'reports','report.txt')
config_path = args.config_path if args.config_path else os.path.join(BASE_DIR , 'config','config.json')
stream = None 
config = None

with open(path) as f:
    stream = f.read()

with open(config_path) as f:
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


writeOutFile(output_path)