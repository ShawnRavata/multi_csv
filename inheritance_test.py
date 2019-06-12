class ClassA(object):
    def __init__(self):
        self.var1 = 1
        self.var2 = 2
    def method(self):
        self.var1 = self.var1 + self.var2
        return self.var1

class ClassB(ClassA):
    def __init__(self):
        ClassA.__init__(self)

object1 = ClassA()

object2 = ClassB()
sum = object2.method()
print(object2.var2, object2.var1)