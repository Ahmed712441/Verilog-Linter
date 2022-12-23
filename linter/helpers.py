def get_variables(tokens:list)-> dict:

    '''
    return all variables in the verliog module as dictory key is variable name value is variable size
    '''

    variables = dict()
    i = 0
    while i < len(tokens): 
        token = tokens[i]
        if token == 'input' or token == 'output' or token == 'reg':
            if tokens[i+1] == 'reg':
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
            
            variables[var] = abs(start-end)+1
        i+=1
    return variables

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
            statement = ([tokens[i-1],tokens[i]],current_line) 
            i += 1
            while tokens[i] != ';':
                statement[0].append(tokens[i])
                i+=1
            statements.append(statement)
        i+=1
    return statements