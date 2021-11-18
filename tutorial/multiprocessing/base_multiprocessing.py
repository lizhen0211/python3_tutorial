"""
https://docs.python.org/zh-cn/3/library/multiprocessing.html

multiprocessing 是一个用于产生进程的包，具有与 threading 模块相似API。
multiprocessing 包同时提供本地和远程并发，使用子进程代替线程，有效避免 Global Interpreter Lock 带来的影响。
因此， multiprocessing 模块允许程序员充分利用机器上的多核。可运行于 Unix 和 Windows 。

multiprocessing 模块还引入了在 threading 模块中没有的API。
一个主要的例子就是 Pool 对象，它提供了一种快捷的方法，赋予函数并行化处理一系列输入值的能力，
可以将输入数据分配给不同进程处理（数据并行）。下面的例子演示了在模块中定义此类函数的常见做法，
以便子进程可以成功导入该模块。这个数据并行的基本例子使用了 Pool ，
"""
from multiprocessing.context import Process
from multiprocessing.pool import Pool


def f(x):
    return x * x


def pool():
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))


print("==============================================")

"""
    Process 类
    在 multiprocessing 中，通过创建一个 Process 对象然后调用它的 start() 方法来生成进程。
     Process 和 threading.Thread API 相同。 一个简单的多进程程序示例是:
"""


def f(name):
    print('hello', name)


p = Process(target=f, args=('bob',))
p.start()
p.join()

if __name__ == '__main__':
    # pool();
    pass
