def get_size(token:str,variables:dict):

    if token[0] >= '0' and token[0] <= '9':
        return int(token[0])      
    else:
        return variables[token]

def get_start(statement:list,variables:dict):
    '''
    function returns the size of left_hand_size variable and index of the equal sign
    '''
    print(statement)
    if len(statement) > 6 and statement[1] == '[' and statement[3] == ':' :
        start = int(statement[2])
        end = int(statement[4])
        size = abs(start-end) + 1
        return size , 6 
    elif len(statement) > 4 and statement[1] == '[' and statement[3] == ']':
        return 1 , 4
    else:
        return variables[statement[0]] , 1

def verify_statement(statement:list,variables:dict):
    
    # left_hand_size , index =  #get_start(statement,variables)
    left_hand_size = variables[statement[0]]
    right_hand_size = variables[statement[2]]
    i = 3
    while i < len(statement):
        token = statement[i]
        if token in [ '^','&','|','-','/']:
            right_hand_size = max(right_hand_size,get_size(statement[i+1],variables))
            i+=1
        elif token == '+':
            right_hand_size = max(right_hand_size,get_size(statement[i+1],variables))+1
            i+=1
        elif token == '*':
            right_hand_size = right_hand_size+get_size(statement[i+1],variables)
            i+=1
        i+=1
    return left_hand_size , right_hand_size

def detectOverflow(statements,variables):
   
    for statement in statements:
        left_hand_size , right_hand_size = verify_statement(statement[0],variables)
        if right_hand_size > left_hand_size:
            print(f"Assignment Overflow Warning on line {statement[1]} statement : {' '.join(statement[0])} left-hand size is {left_hand_size} and right-hand size might be {right_hand_size}")