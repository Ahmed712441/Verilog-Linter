from linter.helpers import report

def filterVariable(var:str):

    if 'b' in var:
        return var[3:]
    else:
        return var

def get_all_combinations(size,arr:list,added:str=''):
    if size == 1:
        arr.append(added+'0')
        arr.append(added+'1')
    else:
        get_all_combinations(size-1,arr,added+'0')
        get_all_combinations(size-1,arr,added+'1')

def value_has_in(value:str,arr:list):
    for char in value:
        if char in arr:
            return True
    return False

def get_all_dontCareComb(value:str,arr:list,added:str="",dontCareVal:list = ['x','X','z','Z']) -> list:
    
    if not value_has_in(value,dontCareVal) :
        arr.append(added + value)
        return
    
    for i in range(len(value)):
        char = value[i]
        if char in dontCareVal:
            get_all_dontCareComb(value[i+1:],arr,added+'0',dontCareVal)
            get_all_dontCareComb(value[i+1:],arr,added+'1',dontCareVal)
            break
        else:
            added += char

def createDict(arr:list):
    output = dict()
    for element in arr:
        output[element] = 0
    return output

class CaseNode:

    def __init__(self,line,size,name,children,varname):
        self.line = line
        self.size = size
        self.name = name
        self.children = children
        self.varname = varname

    def __repr__(self) -> str:
        return self.children.__repr__() + ' ' +self.name + '_' + str(self.line) + '_' + str(self.size) + '_' + str(self.varname)

    def check(self):
        arr = []
        get_all_combinations(self.size,arr,'')
        self.map = createDict(arr)
        self.propagate()
        self.parrell_check()
        self.full_check()

    def propagate(self):
        for child, _ , _ in self.children:
            val = filterVariable(child)
            values = []
            get_all_dontCareComb(val,values)
            for value in values:
                self.map[value] += 1

    def parrell_check(self):
        for value in self.map.keys():
            matches = self.map[value]
            if matches > 1:
                # print(f'Parallel Case Warning in {self.name} at line {self.line} , value: {value} has {matches} matches')
                report.append(f'Parallel Case Warning in {self.name} at line {self.line} , value: {value} has {matches} matches')

    def full_check(self):
        for value in self.map.keys():
            matches = self.map[value]
            if matches == 0:
                # print(f'Full Case Warning in {self.name} at line {self.line} , value: {value} has no matches')
                report.append(f'Full Case Warning in {self.name} at line {self.line} , value: {value} has no matches')


def get_variable_size(tokens:list,i:int,variables:dict):

    if tokens[i+1] == '[' and tokens[i+3] == ':' :
        start = int(tokens[i+2])
        end = int(tokens[i+4])
        size = abs(start-end) + 1
        return size 
    elif tokens[i+1] == '[' :
        return 1
    else:
        return variables[tokens[i]]

def getChildren(tokens:list,i:int,current_line:int):
    
    children = []
    prev_child = None
    start_line = None
    end_line = None
    while i < len(tokens):
        token = tokens[i]
        if token == '\n':
            current_line+=1
        elif token == ':' and tokens[i+1] == 'begin':
            prev_child = tokens[i-1]
            start_line = current_line
            # children.append()
            i+=1
        elif token == 'end':
            end_line = current_line
            children.append((prev_child,start_line,end_line))
            prev_child = None
            start_line = None
            end_line = None
        elif token == 'endcase':
            break
        i+=1
    
    return children , i

def getCases(tokens:list,variables:dict)->list:

    cases = []
    i = 0
    current_line = 1
    while i < len(tokens):
        token = tokens[i]
        if token == '\n':
            current_line += 1
        elif token in ['case','casex','casez'] :
            i+=2
            caseSize = get_variable_size(tokens,i,variables)
            varname = tokens[i]
            caseName = token
            line = current_line
            children , i = getChildren(tokens,i,current_line)
            caseNode = CaseNode(line,caseSize,caseName,children,varname)
            cases.append(caseNode)
        i+=1
 
    return cases


def getCasesErrors(cases:list):
    
    # cases = getCases(tokens,variables)
    for casee in cases:
        casee.check()