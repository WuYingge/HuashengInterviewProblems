"""
题目一


MyCustomException类定义了一个异常类，可以根据内容打印不同的信息，并包含错误码。
func1 调用func2，func2调用func3，func3抛出的异常，func2捕获后可以做一些处理，然后重新抛出，同理func1也是。

如果每一步不需要特殊处理，func1和func2可以不做捕获，直接完全在main方法里捕获。

"""

class MyCustomException(Exception):  
    def __init__(self, message, error_code=None):  
        self.message = message  
        self.error_code = error_code  
        super().__init__(self.message)  
  
    def __str__(self):  
        if self.error_code:  
            return f"MyCustomException({self.error_code}): {self.message}"  
        else:  
            return f"MyCustomException: {self.message}"


def func1():
    try:
        func2()
    except MyCustomException as e:
        # 一些清理资源的工作
        
        # 重新抛出异常
        raise

    
    
def func2():
    try:
        func3()
    except MyCustomException as e:
        # 记录日志 清理资源等
        print(f"Caught exception: {e}")
        # 重新抛出异常MycustomException
        raise
    
    
def func3():
    raise MyCustomException("func3 error", error_code=500)


def main():
    try:
        func1()
    except MyCustomException as e:
        print(f"Caught exception in main: {e}")
    
    

if __name__ == "__main__":
    main()
