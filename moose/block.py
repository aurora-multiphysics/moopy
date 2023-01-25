#!/usr/env/python3

""" A block is a class of a particular type, which has contents which are
a name, the list of potential keys and the contents dictionary
"""
class Block():
    def __init__(self, name = "", keys={}, contents={}):
        self.name = name
        self.keys = keys
        self.contents = contents

    def __str__(self):
        string = f'[{self.name}]\n'
        for key in self.keys:
            if key in self.contents.keys():
                string += f'  {key} = {self.contents[key]}\n' 
        string += '[]\n'
        return string
