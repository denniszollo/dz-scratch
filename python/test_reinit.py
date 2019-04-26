
from traits.api import HasTraits, Str


class MyToy(HasTraits):
    def close(self):
        self.test.close()
    def __init__(self, test):
        self.test = open(test, 'w')

    def __repr__(self):
        return "object on class is :" + str(self.test) + ": id of that obj is" + str(id(self.test)) + ": id of self is" +  str(id(self))



if __name__ == '__main__':
   test = "HelloWorld.txt"
   a = MyToy(test)
   print a
   a.close()
   testb = "HelloWorld.txt"
   a.__init__(testb)
   print a

