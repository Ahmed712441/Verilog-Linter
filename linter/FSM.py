from linter.helpers import  report


def getIntializedRegisters(statements:list):

    registers = dict()
    for statement , _ in statements:
        index = statement.index('=')
        varname = statement[index-1]
        initialVal = statement[index+1]
        registers[varname] = initialVal

    return registers 

def getNewVal(statements,varName,start_line,end_line):
    
    val = None
    for statement , line in statements:
        if line >= start_line and line <= end_line:
            if len(statement) == 3 and statement[0] == varName:
                val = statement[2]
        elif line > end_line:
            break
    
    return val

def propagate_FSM(statements,case,val,varName):
    
    children = case.children
    states = [child[0] for child in case.children]
    prev_states = []
    end = False
    deadlock = False
    while len(prev_states) < len(states) :
        for state ,start_line ,end_line in children:
            if state == val:
                prev_states.append(val)
                newVal = getNewVal(statements,varName,start_line,end_line)
                if newVal == val or not newVal:
                    deadlock = val
                elif newVal in prev_states :
                    end = True
                else:
                    val = newVal
                break
        if end or deadlock:
            break
    
    return prev_states , deadlock

def analyzeCase(case,prev_states):
    states = [child[0] for child in case.children]
    for state in prev_states:
        states.remove(state) 

    for state in states:
        report.append(f"Unreachable FSM State {state} in {case.name} at line {case.line}")
        print(f"Unreachable FSM State {state} in {case.name} at line {case.line}")
        # writeToFile("reports.txt",f"Unreachable FSM State {state} in {case.name} at line {case.line}")
    
def getUnreachableFSM(statements:list,cases:list,registers:dict):
    '''
    registers : registers that has initial values if exits in registers ex: 'c' : '1'b000'
    cases : list of all cases 
    '''
    reg_names = list(registers.keys())

    for case in cases:
        if case.varname in reg_names:
            prev_states , deadlock = propagate_FSM(statements,case,registers[case.varname],case.varname)
            if deadlock :
                # writeToFile("reports.txt",f"Deadlock State Warning in {case.name} at line {case.line} when {case.varname} = {deadlock}")
                print(f"Deadlock State Warning in {case.name} at line {case.line} when {case.varname} = {deadlock}")
                report.append(f"Deadlock State Warning in {case.name} at line {case.line} when {case.varname} = {deadlock}")
            analyzeCase(case,prev_states)