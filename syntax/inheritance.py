class A:
    def work(self):
        print("A")

class B(A):
    def work(self):
        print("B")

    def doworks(self):
        #self.work()  #当然是调用B的work，能执行到这里说明self是B类型
        super(B,self).work()#调用父类的work方法
        super().work() #调用父类的方法


if __name__ == '__main__':
    b = B()
    b.work()
    b.doworks()

'''
执行结果：
B
A
A
'''

