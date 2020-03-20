from typing import Any

class TestClass():
    def __init__(self):
        pass

    def __getattribute__(self, name:str)->Any:
        if name == 'print':
            print('Print Called')
        return super().__getattribute__(name)

    def print(self):
        print("This is the print method")

    def run(self, arg):
        print(arg)

t = TestClass()

t.print()
t.run("hello world")