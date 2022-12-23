# from linter.helpers import *

current_state = 0

def clean(string:str,values:list = ['\t']):
    output = ''
    for char in string:
        if not char in values:
            output += char

    return output

def get_string_tokens(stream:str):
    output = []
    old_str = ''
    i = 0
    while i < len(stream):
        char = stream[i]
        if char == ' ':
            if old_str != '':
                output.append(old_str)
                old_str = ''
        elif i < len(stream)-2 and stream[i:i+3] in ['===','!==']:
            op = stream[i:i+3]
            i += 2
            if old_str != '':
                output.append(old_str)
                old_str = ''
            output.append(op)
        elif i < len(stream)-1 and stream[i:i+2] in ['&&','||','==','!=','>=','<=']:
            op = stream[i:i+2]
            i += 1
            if old_str != '':
                output.append(old_str)
                old_str = ''
            output.append(op)
        elif char in ['+','-','&','|','=','^','>','<','(',')',';','@','?',':','[',']','\n']:
            if old_str != '':
                output.append(old_str)
                old_str = ''
            output.append(char)
        else:
            old_str += char
        i+=1
    return output



def get_tokens(stream:str):

    new_stream = clean(stream) 
    tokens = get_string_tokens(new_stream)
    return tokens


if __name__ == '__main__':
    stream = None 
    with open('E:/EDA 2/Project phase2/data/testfile2.v') as f:
        stream = f.read()

    tokens = get_tokens(stream)