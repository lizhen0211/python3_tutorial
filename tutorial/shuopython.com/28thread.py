# 28.Python 线程创建和传参
# 在以前的文章中虽然我们没有介绍过线程这个概念，但是实际上前面所有代码都是线程，
# 只不过是单线程，代码由上而下依次执行或者进入main函数执行，这样的单线程也称为主线程。

# 有了单线程的话，什么又是多线程？
# 可以这么理解：一个线程执行一个代码块，多个线程可以同时执行多个代码，使用多线程能让程序效率更高。

# 一.线程解释
# 线程是cpu最小调度单位，一个程序中至少有一个或者多个线程（至于进程暂时不做讲解，后面文章会有详细解释）！
# 在开发中使用线程可以让程序运行效率更高，多线程类似于同时执行多个不同代码块。

# 二.线程创建和启动
# 1.导入线程模块

# 导入线程threading模块
# import threading

# 2.创建线程并初始化线程
# 调用threading模块中的缺省函数Thread，创建并初始化线程，返回线程句柄。

# 创建并初始化线程，返回线程句柄
# t = threading.Thread(target=函数名)

# 3.启动线程
# 通过初始化返回的线程句柄调用start()函数，启动线程，
# 此时会自动执行在创建线程时target对应的函数内部的代码：

# 启动线程
# t.start()

# 综合上面三步,下面使用代码对python线程thread做详细讲解：
# 导入线程threading模块
import threading
# 导入内置模块time
import time


def wash_clothes():
    print("{0}:洗衣服开始...".format(threading.current_thread().name))
    # sleep 5 秒，默认以秒为单位
    time.sleep(5)
    print("{0}:洗衣服完成...".format(threading.current_thread().name))


def clean_room():
    print("{0}:打扫房间开始...".format(threading.current_thread().name))
    # sleep 5 秒，默认以秒为单位
    time.sleep(5)
    print("{0}:打扫房间完成...".format(threading.current_thread().name))


if __name__ == "__main__":
    # 创建线程并初始化 -- 该线程执行wash_clothes中的代码
    t1 = threading.Thread(target=wash_clothes)
    # 创建线程并初始化 -- 该线程执行clean_room中的代码
    t2 = threading.Thread(target=clean_room)

    t1.start()
    t2.start()

# 第一步:洗衣服开始和打扫房间开始几乎同时开始，两个事件同时执行.
# 第二步：程序停止5秒；
# 第三步:洗衣服和打扫房间几乎同时完成
print("==============================================")


def wash_clothes():
    print("{0}:洗衣服开始...".format(threading.current_thread().name))
    # sleep 5 秒，默认以秒为单位
    time.sleep(5)
    print("{0}:洗衣服完成...".format(threading.current_thread().name))


def clean_room():
    print("{0}:打扫房间开始...".format(threading.current_thread().name))
    # sleep 5 秒，默认以秒为单位
    time.sleep(5)
    print("{0}:打扫房间完成...".format(threading.current_thread().name))


if __name__ == "__main__":
    wash_clothes()
    clean_room()

# 第一步：洗衣服开始；
# 第二步：程序停止了5秒；
# 第三步：洗衣服完成，打扫房间开始
# 第四步：程序停止5秒；
# 第五步：打扫房间结束，程序结束；
print("==============================================")


# 三.线程传参
# threading.Thread()函数中有两个缺省参数 args 和 kwargs ，
# args 是元组类型，kwargs 是字典类型，缺省值默认为空，除此之外，
# 其实还可以设置线程的名字等，其函数声明如下：
def wash_clothes(*args, **kargcs):
    print("wash_clothes:", args)
    print("wash_clothes:", kargcs)


def clean_room(*args, **kargcs):
    print("clean_room:", args)
    print("clean_room:", kargcs)


if __name__ == "__main__":
    t1 = threading.Thread(target=wash_clothes,
                          args=(1, "猿说python"),  # args 传递元组，可以同时传递多个数据
                          kwargs={"a": 1, "b": False})  # kwargs 传递字典，可以同时传递多个键值对

    t2 = threading.Thread(target=clean_room,
                          args=(2, False),  # args 传递元组，可以同时传递多个数据
                          kwargs={"c": 0.2, "d": False})  # kwargs 传递字典，可以同时传递多个键值对

    t1.start()
    t2.start()

# 四.线程结束
# 线程一：__name__ == “__main__” 作为主线程；
# 线程二：t1 作为子线程；
# 线程三：t2 作为子线程；
# 注意：主程序会等待所有子程序结束之后才会结束！
print("==============================================")


# 五.相关函数介绍
# 1.threading.Thread() — 创建线程并初始化线程，可以为线程传递参数 ；
# 2.threading.enumerate() — 返回一个包含正在运行的线程的list；
# 3.threading.activeCount(): 返回正在运行的线程数量，与len(threading.enumerate())有相同的结果；
# 4.Thread.start() — 启动线程 ；
# 5.Thread.join() — 阻塞函数，一直等到线程结束为止 ；
# 6.Thread.isAlive() — 返回线程是否活动的；
# 7.Thread.getName() — 返回线程名；
# 8.Thread.setName() — 设置线程名；
# 9.Thread.setDaemon() — 设置为后台线程，这里默认是False，设置为True之后
# 则主线程不会再等待子线程结束才结束，而是主线程结束意味程序退出，子线程也立即结束，注意调用时必须设置在start()之前；

def wash_clothes(*args, **kargcs):
    time.sleep(2)
    print("wash_clothes:", args)
    time.sleep(2)
    print("wash_clothes:", kargcs)


def clean_room(*args, **kargcs):
    time.sleep(2)
    print("clean_room:", args)
    time.sleep(2)
    print("clean_room:", kargcs)


if __name__ == "__main__":
    t1 = threading.Thread(target=wash_clothes,
                          args=(1, "猿说python"),  # args 传递元组，可以同时传递多个数据
                          kwargs={"a": 1, "b": False})  # kwargs 传递字典，可以同时传递多个键值对

    t2 = threading.Thread(target=clean_room,
                          args=(2, False),  # args 传递元组，可以同时传递多个数据
                          kwargs={"c": 0.2, "d": False})  # kwargs 传递字典，可以同时传递多个键值对

    # setDaemon(True)意味着主线程退出，不管子线程执行到哪一步，子线程自动结束
    # t1.setDaemon(True)
    # t2.setDaemon(True)
    t1.start()
    t2.start()

    print("threading.enumerate():", threading.enumerate())
    print("threading.activeCount():", threading.activeCount())
    print("t1.isAlive():", t1.isAlive())
    print("t1.getName():", t1.getName())
    print("t2.isAlive():", t2.isAlive())
    t2.setName("my_custom_thread_2")
    print("t2.getName():", t2.getName())

# 六.重点总结
# 1.默认主线程会等待所有子线程结束之后才会结束，主线程结束意味着程序退出；
# 如果setDaemon设置为True,主线程则不会等待子线程，主线程结束，子线程自动结束；

# 2.threading模块除了以上常用函数，还有互斥锁Lock/事件Event/信号量Condition/队列Queue等
