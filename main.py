from linter.helpers import *
from linter.arithmeticOverflow import *
from parser.tokenizer import *


stream = None 
with open('E:/EDA 2/Project phase2/data/testfile2.v') as f:
    stream = f.read()

tokens = get_tokens(stream)
variables = get_variables(tokens)
statements = get_statements(tokens)
# print(statements)
# print(tokens)
detectOverflow(statements,variables)