from linter.helpers import *
from linter.arithmeticOverflow import verify_statement

def get_block(stmt_line:int,blocks:list):
    Nested = []
    for block in blocks:
        start_line = block[1]
        end_line = block[2]
        if len(Nested) > 0:
            if block[0] in ['always','initial']:
                Nested.insert(0,block[0]+'_'+str(block[1])+'_'+str(block[2]))
                return Nested
        elif stmt_line >= start_line and stmt_line <= end_line:
            if block[0] in ['if','else','else if']:
                Nested.append(block[0]+'_'+str(block[1])+'_'+str(block[2]))
            else:
                return [block[0]+'_'+str(block[1])+'_'+str(block[2])]

def assign_bits(arr:list,start:int,end:int,size:int):

    end = start+size if end-start > size else end+1
    for i in range(start , end):
        arr[i] = 1

def assign_register(start_left:int,end_left:int,keys:list,size:int,blocks_dict:dict,register_name:str):
    
    selected_dict = blocks_dict
    for key in keys :
        selected_dict = selected_dict[key]
    
    if keyExists(selected_dict,register_name):
        arr = selected_dict[register_name]
        assign_bits(arr,start_left,end_left,size)
    else:
        for dict_key in selected_dict.keys():
            assign_bits(selected_dict[dict_key][register_name],start_left,end_left,size)

def get_left_hand_bits(statement:list,start_bit:int,end_bit:int):
    
    if statement[1] != '[':
        return (start_bit,end_bit)
    elif statement[1] == '[' and statement[3] == ':':
        start = int(statement[2])
        end = int(statement[4])
        return (min(start,end),max(start,end))
    elif statement[1] == '[' :
        return (int(statement[0]),int(statement[1]))

def block_assignment(statements:list,blocks:list,registers:dict,variables:dict)-> dict:   
    '''
    used for initialization detection
    '''
    blocks_dict = create_blocks_dictonary(blocks,registers)
    for statement in statements:
        keys = get_block(statement[1],blocks)
        if keys :
            register_size = registers[statement[0][0]]
            _ , right_hand_size = verify_statement(statement[0],variables)
            start_left , end_left = get_left_hand_bits(statement[0],0,register_size-1)
            assign_register(start_left,end_left,keys,right_hand_size,blocks_dict,statement[0][0])
    
    return blocks_dict


def get_assignment_errors(blocks_dict:dict,registers:dict):

    assignment_errors = create_register_dictonary(registers)
    registers_names = list(registers.keys())

    for key in blocks_dict.keys():
        selected_dict = blocks_dict[key]
        if not keyExists(selected_dict,registers_names[0]):
            for blocks in selected_dict.keys():
                for reg in registers_names:
                    add_two_arr(assignment_errors[reg],selected_dict[blocks][reg])
        else:
            for reg in registers_names:
                add_two_arr(assignment_errors[reg],selected_dict[reg])

    for reg in registers_names:
        arr = assignment_errors[reg]
        for i in range(len(arr)):
            if arr[i] == 0:
                print(f'OverAll Assignment error in register: {reg} bit {i} will never get a value')   

def infer_latch(statements:list,blocks:list,registers:dict,variables:dict):

    blocks_dict = block_assignment(statements,blocks,registers,variables)
    
    get_assignment_errors(blocks_dict,registers)
    