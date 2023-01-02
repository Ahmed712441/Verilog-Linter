from linter.helpers import *
from linter.arithmeticOverflow import verify_statement
from linter.initialization import get_left_hand_bits

def create_wires_dict(outputWires:dict):
    output = dict()
    for key in outputWires.keys():
        output[key] = [[] for i in range(outputWires[key])]
    return output


def assign_bits(arr:list,start:int,end:int,size:int,line:int):

    end = start+size if end-start > size else end+1
    for i in range(start , end):
        arr[i].append(line) 


def DrivenBus(statements:list,outputWires:dict,all_variables:dict):
    
    outputWires_dict = create_wires_dict(outputWires)
    
    for statement in statements:
        statementt = statement[0]
        line = str(statement[1])
        if keyExists(outputWires,statementt[0]):
            register_size = outputWires[statementt[0]]
            arr = outputWires_dict[statementt[0]]
            _ , right_hand_size = verify_statement(statementt,all_variables)
            start_left , end_left = get_left_hand_bits(statement[0],0,register_size-1)
            assign_bits(arr,start_left,end_left,right_hand_size,line)

    for wire in outputWires_dict.keys():
        arr = outputWires_dict[wire]
        for i in range(len(arr)):
            if len(arr[i]) > 1:
                print(f'BUS_VALUE_CONFLICT at {wire}[{i}] as it is assigned multiple values concurrently at lines {",".join(arr[i])}')
                report.append(f'BUS_VALUE_CONFLICT at {wire}[{i}] as it is assigned multiple values concurrently at lines {",".join(arr[i])}')

