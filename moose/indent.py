#!/usr/env/python3
import re
def indent(string):

    new_string = string.split('\n')
    indent_count = 0
    for idx,line in enumerate(new_string):
        increments = re.findall('\[.+?\]',line)
        decrements = re.findall('\[\]',line)

        if decrements:
            indent_count = indent_count - 2
  
        if indent_count > 0:
            new_string[idx] = " "*indent_count + line
        
        if increments:
            indent_count = indent_count + 2
        
    print('\n'.join(new_string))       
    #split_string = re.split('\[.*?\]',string)
    #matches = re.findall('\[.*?\]',string)
    
    #print(split_string)
    #print(matches)

            

string = "[test]\n[test2]\nblah\nblah\n[]\n[test3]\nblah\nblah\n[]\n[]\n"
print(string)
indent(string)
