class Variable:

    def __init__(self,name,size,direction,type):
        self.name = name
        self.size  = size
        self.direction = direction
        self.type = type
 
    def __repr__(self) -> str:
        return self.name + '_' + str(self.size) + '_' +  self.direction + '_' + self.type

def get_dictonary_variables(variables:list):
    output = dict()

    for var in variables:
        output[var.name] = var.size 

    return output

def get_variables(tokens:list)-> tuple:

    '''
    return all variables , registers in the verliog module as dictory key is variable name value is variable size
    '''

    all_variables = []

    variables = dict()
    registers = dict()
    i = 0
    while i < len(tokens): 
        token = tokens[i]
        if token == 'input' or token == 'output' :
            direction = token
            typee = 'wire' 
            if tokens[i+1] == 'reg':
                typee = 'reg' 
                i+=1
            if tokens[i+1] == '[':
                start = int(tokens[i+2])
                end = int(tokens[i+4])
                var = tokens[i+6]
                i+=6
            else:
                start = 0
                end = 0
                var = tokens[i+1]
                i+=1
            all_variables.append(Variable(var,abs(start-end)+1,direction,typee))
        elif token  == 'reg':
            direction = 'output'
            typee = 'reg'
            if tokens[i+1] == '[':
                start = int(tokens[i+2])
                end = int(tokens[i+4])
                var = tokens[i+6]
                i+=6
            else:
                start = 0
                end = 0
                var = tokens[i+1]
                i+=1
            all_variables.append(Variable(var,abs(start-end)+1,direction,typee)) 
        i+=1
    
    return all_variables

def get_statements(tokens:list)->list :

    '''
    return all assign statements in verliog module in list of tuples [([statement],line_number),([statement],line_number),.....]
    '''

    i = 0
    statements = []
    current_line = 1
    while i < len(tokens):
        if tokens[i] == '\n':
            current_line += 1
        if tokens[i] == '=':
            statement = ([],current_line) 
            j = i
            while not tokens[j] in [';','begin','end','\n'] :
                statement[0].insert(0,tokens[j])
                j-=1
            i += 1
            while tokens[i] != ';':
                statement[0].append(tokens[i])
                i+=1
            statements.append(statement)
        i+=1
    return statements

def get_blocks(tokens:list) -> list:

    '''
    returns all initial , always , if-else block start and end lines
    '''

    i = 0
    blocks = []
    blocks_stack = []
    current_line = 1
    while i < len(tokens):
        if tokens[i] == '\n':
            current_line += 1
        if tokens[i] in ['always','initial','if','else','else if'] : 
            blocks_stack.append((tokens[i],current_line))
        elif tokens[i] in ['end']:
            block , start_line = blocks_stack.pop()
            blocks.append((block , start_line,current_line))
        i+=1
    
    return blocks

def filterBlocks(block:list):
    
    if block[0] in ['if','else','else if'] :
        return True
    else:
        return False

def add_two_arr(arr1:list,arr2:list):
    for i in range(len(arr1)):
        arr1[i] += arr2[i]

def create_register_dictonary(registers:dict):
    
    output = dict()
    for key in registers.keys():
        output[key] = [0 for i in range(registers[key])]
    return output

def create_blocks_dictonary(blocks:list,registers:dict):

    output = dict()
    toback = 0
    for i in range(len(blocks)):
        block  = blocks[i]
        if block[0] in ['if','else','else if']:
            toback += 1
        else:
            block_dict = dict() 
            while toback > 0:
                old_block = blocks[i-toback]
                block_dict[old_block[0]+'_'+str(old_block[1])+'_'+str(old_block[2])] = create_register_dictonary(registers)
                toback -= 1
            if len(block_dict) == 0:
                output[block[0]+'_'+str(block[1])+'_'+str(block[2])] = create_register_dictonary(registers)
            else:
                output[block[0]+'_'+str(block[1])+'_'+str(block[2])] = block_dict
    return output


def keyExists(dictonary:dict,key:str):

    try:
        dictonary[key]
        return True
    except:
        return False
