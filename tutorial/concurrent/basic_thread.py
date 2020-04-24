# 参考 https://www.runoob.com/python3/python3-multithreading.html
# Python3 多线程
# 线程可以分为:
# --内核线程：由操作系统内核创建和撤销。
# --用户线程：不需要内核支持而在用户程序中实现的线程。

# Python3 线程中常用的两个模块为：
# --_thread
# --threading(推荐使用)

# thread 模块已被废弃。用户可以使用 threading 模块代替。
# 所以，在 Python3 中不能再使用"thread" 模块。
# 为了兼容性，Python3 将 thread 重命名为 "_thread"。

# 开始学习Python线程
# Python中使用线程有两种方式：函数或者用类来包装线程对象。
# 函数式：调用 _thread 模块中的start_new_thread()函数来产生新线程。语法如下:
# _thread.start_new_thread ( function, args[, kwargs] )

# 参数说明:
# --function - 线程函数。
# --args - 传递给线程函数的参数,他必须是个tuple类型。
# --kwargs - 可选参数。

# 实例
# 为线程定义一个函数
import _thread
import queue
import threading
import time

# 为线程定义一个函数
from queue import Queue


def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (threadName, time.ctime(time.time())))


def a_simple_demo():
    try:
        _thread.start_new_thread(print_time, ("Thread-1", 2,))
        _thread.start_new_thread(print_time, ("Thread-2", 4,))
    except:
        print("Error: 无法启动线程")
    while 1:
        pass


# 创建两个线程
# a_simple_demo()

print("==============================================")

# 线程模块
# Python3 通过两个标准库 _thread 和 threading 提供对线程的支持。
# _thread 提供了低级别的、原始的线程以及一个简单的锁，它相比于 threading 模块的功能还是比较有限的。
# threading 模块除了包含 _thread 模块中的所有方法外，还提供的其他方法：
# --threading.currentThread(): 返回当前的线程变量。
# --threading.enumerate(): 返回一个包含正在运行的线程的list。
# 正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
# --threading.activeCount(): 返回正在运行的线程数量，与len(threading.enumerate())有相同的结果。

# 除了使用方法外，线程模块同样提供了Thread类来处理线程，Thread类提供了以下方法:
# --run(): 用以表示线程活动的方法。
# --start():启动线程活动。
# --join([time]): 等待至线程中止。
# 这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生。
# --isAlive(): 返回线程是否活动的。
# --getName(): 返回线程名。
# --setName(): 设置线程名。

# 使用 threading 模块创建线程
# 我们可以通过直接从 threading.Thread 继承创建一个新的子类，
# 并实例化后调用 start() 方法启动新线程，即它调用了线程的 run() 方法：

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print("退出线程：" + self.name)


def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("退出主线程")
print("==============================================")


# 线程同步
# 如果多个线程共同对某个数据修改，则可能出现不可预料的结果，为了保证数据的正确性，需要对多个线程进行同步。
# 使用 Thread 对象的 Lock 和 Rlock 可以实现简单的线程同步，这两个对象都有 acquire 方法和 release 方法，
# 对于那些需要每次只允许一个线程操作的数据，可以将其操作放到 acquire 和 release 方法之间。
class MyThreadLock():

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开启线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁，开启下一个线程
        threadLock.release()


threadLock = threading.Lock()
threads = []

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)

# 等待所有线程完成
for t in threads:
    t.join()
print("退出主线程")

print("==============================================")
# 线程优先级队列（ Queue）
# Python 的 Queue 模块中提供了同步的、线程安全的队列类，
# 包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列 PriorityQueue。
# 这些队列都实现了锁原语，能够在多线程中直接使用，可以使用队列来实现线程间的同步。
# Queue 模块中的常用方法:
# --Queue.qsize() 返回队列的大小
# --Queue.empty() 如果队列为空，返回True,反之False
# --Queue.full() 如果队列满了，返回True,反之False
# --Queue.full 与 maxsize 大小对应
# --Queue.get([block[, timeout]])获取队列，timeout等待时间
# --Queue.get_nowait() 相当Queue.get(False)
# --Queue.put(item) 写入队列，timeout等待时间
# --Queue.put_nowait(item) 相当Queue.put(item, False)
# --Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
# --Queue.join() 实际上意味着等到队列为空，再执行别的操作

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.name, self.q)
        print("退出线程：" + self.name)


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            print('get {0} into workQueue'.format(data))
            queueLock.release()
            print("%s processing %s" % (threadName, data))
        else:
            queueLock.release()
        time.sleep(1)


threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
    print('put {0} into workQueue'.format(word))
queueLock.release()
print('all work have put')

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出，此例中所有任务添加完成
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()

print("退出主线程")
print("==============================================")
