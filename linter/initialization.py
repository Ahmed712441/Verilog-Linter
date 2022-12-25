from linter.helpers import *
from linter.arithmeticOverflow import verify_statement

def hasDontCare(token:str)-> bool:

    if token[0] > '0' and token[0] <= '9':
        return 'x' in token  or 'X' in token
    else:
        return False
        
def dontCareAssignment(statements:list):

    for statement,line in statements:
        i =  statement.index('=')+1
        while i < len(statement):
            token = statement[i]
            if hasDontCare(token):
                print(f"X-ASSIGNMENT at line {line} , statement : {' '.join(statement)}")
                break
            i+=1

def assign_bits(arr:list,start:int,end:int,size:int):

    end = start+size if end-start > size else end+1
    for i in range(start , end):
        arr[i] = 1

def assign_register(start_left:int,end_left:int,size:int,error_dict:dict,register_name:str):
    
    if keyExists(error_dict,register_name):
        arr = error_dict[register_name]
        assign_bits(arr,start_left,end_left,size)
    

def get_left_hand_bits(statement:list,start_bit:int,end_bit:int):
    
    if statement[1] != '[':
        return (start_bit,end_bit)
    elif statement[1] == '[' and statement[3] == ':':
        start = int(statement[2])
        end = int(statement[4])
        return (min(start,end),max(start,end))
    elif statement[1] == '[' :
        return (int(statement[0]),int(statement[1]))



def statement_assignment(statements:list,registers:dict,variables:dict)-> dict:   
    '''
    used for initialization detection
    '''
    blocks_dict = create_register_dictonary(registers) #create_blocks_dictonary(blocks,registers)
    for statement in statements:
        register_size = registers[statement[0][0]]
        _ , right_hand_size = verify_statement(statement[0],variables)
        start_left , end_left = get_left_hand_bits(statement[0],0,register_size-1)
        assign_register(start_left,end_left,right_hand_size,blocks_dict,statement[0][0])
    
    return blocks_dict

def get_assignment_errors(statements:list,registers:dict,variables:dict):

    assignment_errors = statement_assignment(statements,registers,variables)
    registers_names = list(registers.keys())

    for reg in registers_names:
        arr = assignment_errors[reg]
        for i in range(len(arr)):
            if arr[i] == 0:
                print(f'OverAll Assignment error in register: {reg} bit {i} will never get a value')