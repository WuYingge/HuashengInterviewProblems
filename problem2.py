"""
自定义迭代器定义：可以从指定位置开始按照指定步长遍历list

EvenIterable继承StepIterable，遍历列表的偶数位
OddIterable，遍历列表的奇数位

给定列表[1,2,3,4,5,6,7,8,9]，定义新列表类，新增返回奇数迭代器和偶数迭代的方法，用zip打包遍历并输出成对的奇数偶数项
"""


class StepIterator:
    
    def __init__(self, data, start_index, step):
        self.data = data
        self.step = step
        self.index = start_index
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            res = self.data[self.index]
            self.index += self.step
            return res
        else:
            raise StopIteration()


class EvenIterableClass(StepIterator):
    
    def __init__(self, data):
        super().__init__(data, 0, 2)
        

class OddIterableClass(StepIterator):
    
    def __init__(self, data):
        super().__init__(data, 1, 2)


class CustomList(list):
    
    def odd_iter(self):
        return OddIterableClass(self)
    
    def even_iter(self):
        return EvenIterableClass(self)
    

if __name__ == '__main__':
    cl = CustomList([1,2,3,4,5,6,7,8,9])
    for even, odd in zip(cl.even_iter(), cl.odd_iter()):
        print(even, odd)
