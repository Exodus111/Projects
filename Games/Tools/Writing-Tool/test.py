

class A:
    def s(self):
        print("test")

    def b(self, call=self.s):
        call()

a = A
a.b()
