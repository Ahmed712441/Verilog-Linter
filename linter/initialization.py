from linter.helpers import *

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

def block_assignment(statements:list,blocks:list,registers:dict)-> dict:
    
    '''
    used for infer latch detection
    '''

    blocks_dict = create_blocks_dictonary(blocks,registers)
    print(blocks_dict)
    # block , start_line , end_line = blocks.pop()
    # for statement,line in statements:
    #     if line < start_line:
    #         continue
        
    #     i =  statement.index('=')+1
        