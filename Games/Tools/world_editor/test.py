from collections import OrderedDict


class TestA:
    def setup(self):
        t1 = TestB("Test B1")
        t2 = TestB("Test B2")
        t3 = TestB("Test B3")
        runner = TestC(t1, t2, t3)
        my_list = [t1, t2, t3]
        name_run = runner.run()
        for i in my_list:
            print("{}--->{}".format(name_run.next(), i.name))

class TestB:
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)

class TestC:
    def __init__(self, *args):
        self.dict_of = OrderedDict((tuple([i.name,i]) for i in args))
        self.num = 1

    def run(self):
        for l in self.dict_of:
            self.dict_of[l].name = "New Name {}".format(self.num)
            self.num += 1
            yield self.dict_of[l].name

if __name__ == "__main__":
    s = TestA()
    s.setup()
