
class Borg:
    __shared_state = {}
    def __init__(self, var):
        self.__dict__ = self.__shared_state
        self.var = var

    def get_var(self):
        return self.var

test = Borg("Test")
test2 = Borg("Another Test")
test3 = Borg("And another")
test.var = "Testtest"
test3.var2 = "World!"
test4 = Borg("Hello")
print(test3.var)          #<---"Hello"
print(test4.var2)         #<---"World!"
