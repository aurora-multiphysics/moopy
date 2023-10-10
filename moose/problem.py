#!/usr/env/python3

class ProblemType():
    def __init__(self, name = "", **kwargs):
        self.name = name
        self.problem_object_type = kwargs.pop('problem_object_type')

    def __str__(self):
        string = f'\n[{self.name}]\n'
        string += f'type={self.problem_object_type}\n'
        string += '[]\n\n'
        return string

