from linter.helpers import report

ARITHMETICPRECEDENCE = {
    '|' : 1,
    '^' : 2,
    '&' : 3,
    '+' : 4,
    '-' : 4,
    '*' : 5,
    '/' : 5,
}

def parse_variable_size(statement:list,variables:dict,index:int):

    '''
    gives you variable size and the index of the token after variable 
    '''
    if statement[index][0] >= '0' and statement[index][0] <= '9':
        return int(statement[index][0]) , index+1
    elif len(statement) >= index+6 and statement[index+1] == '[' and statement[index+3] == ':' :
        start = int(statement[index+2])
        end = int(statement[index+4])
        size = abs(start-end) + 1
        return size , index+6
    elif len(statement) >= index+4 and statement[index+1] == '['  :
        return 1 , index+4
    else:
        return variables[statement[index]],index+1

def verify_statement(statement:list,variables:dict):
    
    '''
    return the left_hand_size of the statement and the largest value right_hand_size can take
    '''  
    left_hand_size , i = parse_variable_size(statement,variables,0)
    right_hand_size , i = parse_variable_size(statement,variables,i+1) 
    
    while i < len(statement):
        token = statement[i]
        if token in [ '^','&','|','-','/']:
            size , i = parse_variable_size(statement,variables,i+1)
            right_hand_size = max(right_hand_size,size)
        elif token == '+':
            size , i = parse_variable_size(statement,variables,i+1)
            right_hand_size = right_hand_size+1
        elif token == '*':
            size , i = parse_variable_size(statement,variables,i+1)
            right_hand_size = right_hand_size+size
        else:
            i+=1
    return left_hand_size , right_hand_size

def detectOverflow(statements,variables):
   
    for statement in statements:
        # statementt = statement[0]
        
        left_hand_size , right_hand_size = verify_statement(statement[0],variables)
        if right_hand_size > left_hand_size:
            # print(f"Assignment Overflow Warning on line {statement[1]} statement : {' '.join(statement[0])} left-hand size is {left_hand_size} and right-hand size might be {right_hand_size}")
            report.append(f"Assignment Overflow Warning on line {statement[1]} statement : {' '.join(statement[0])} left-hand size is {left_hand_size} and right-hand size might be {right_hand_size}")