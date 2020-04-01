# 参考 http://www.shuopython.com/archives/1899
# https://docs.python.org/zh-cn/3/library/concurrent.futures.html

# 线程池ThreadPoolExecutor函数介绍

# 1.ThreadPoolExecutor构造实例的时候，传入max_workers参数来设置线程池中最多能同时运行的线程数目。

# 2.使用submit函数来提交线程需要执行的任务（函数名和参数）到线程池中，
# 并返回该任务的句柄（类似于文件、画图），注意submit()不是阻塞的，而是立即返回。

# 3.通过submit函数返回的任务句柄，能够使用done()方法判断该任务是否结束。下面的例子可以看出，
# 由于任务有2s的延时，在task1提交后立刻判断，task1还未完成，而在延时4s之后判断，task1就完成了。

# 4.使用cancel()方法可以取消提交的任务，如果任务已经在线程池中运行了，就取消不了。
# 这个例子中，线程池的大小设置为2，任务已经在运行了，所以取消失败。如果改变线程池的大小为1，那么先提交的是task1，task2还在排队等候，这是时候就可以成功取消。

# 5.使用result()方法可以获取任务的返回值，注意：这个方法是阻塞的。

# 线程池ThreadPoolExecutor简单使用

# 参数times用来模拟下载的时间
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED


def down_video(times):
    time.sleep(times)
    print("down video {}s finished".format(times))
    return times


executor = ThreadPoolExecutor(max_workers=2)
# 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
task1 = executor.submit(down_video, (3))
task2 = executor.submit(down_video, (2))
# done方法用于判定某个任务是否完成
print("任务1是否已经完成：", task1.done())
# cancel方法用于取消某个任务,该任务没有放入线程池中才能取消成功
print("取消任务2：", task2.cancel())
time.sleep(4)
print("任务1是否已经完成：", task1.done())
# result方法可以获取task的执行结果，注意：这个方法是阻塞的。
print(task1.result())  # down_video 返回值
print(task2.result())  # down_video 返回值
print("==============================================")


# 1.threadpool — 是一个比较老的模块了，现在虽然还有一些人在用，但已经不再是主流了；
# 2.concurrent.futures — 目前线程池主要使用这个模块，主流模块；
# ThreadPoolExecutor常用函数

# --1.as_completed
# 虽然 done() 函数提供了判断任务是否结束的方法，但是并不是太实用，
# 因为我们并不知道线程到底什么时候结束，需要一直判断每个任务有没有结束。
# 这时就可以使用 as_completed() 方法一次取出所有任务的结果。
# as_completed() 方法是一个生成器，在没有任务完成的时候，会阻塞，
# 在有某个任务完成的时候，就能继续执行for循环后面的语句，然后继续阻塞住，循环到所有的任务结束。

# 参数times用来模拟网络请求的时间
def download_video(index):
    time.sleep(2)
    print("download video {} finished at {}".format(index, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())))
    return index


executor = ThreadPoolExecutor(max_workers=2)
urls = [1, 2, 3, 4, 5]
all_task = [executor.submit(download_video, (url)) for url in urls]

for task in as_completed(all_task):
    data = task.result()
    print("任务{} down load success".format(data))

# 5个任务，2个线程，由于在线程池构造的时候允许同时最多执行2个线程，
# 所以同时执行任务1和任务2，重代码的输出结果来看，
# 任务1和任务2执行后，for循环进入阻塞状态，
# 直到任务1或者任务2结束之后才会for才会继续执行任务3/任务4，
# 并保证同时执行的最多只有两个任务

print("==============================================")


# 2--map
# 和as_completed() 方法不同的是：map()方法能保证任务的顺序性，
# 举个例子：如果同时下载5个视频，就算第二个视频比第一个视频先下载完成，
# 也会阻塞等待第一个视频下载完成并通知主线程之后，
# 第二个下载完成的视频才回通知主线程，保证按照顺序完成任务，下面举个例子说明一下：


# 参数times用来模拟网络请求的时间
def download_video(index):
    time.sleep(index)
    print("download video {} finished at {}".format(index, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())))
    return index


executor = ThreadPoolExecutor(max_workers=2)
urls = [3, 2, 1, 4, 5]

for data in executor.map(download_video, urls):
    print("任务{} down load success".format(data))

# 重上面的输出结果看来，即便任务2比任务3先完成，
# for循环输出的内容依旧是提示先完成的任务3再完成任务2，
# 根据列表urls顺序输出，保证任务的顺序性！
print("==============================================")


# 3.wait
# wait()方法有点类似线程的join()方法，能阻塞主线程，
# 直到线程池中的所有的线程都操作完成！实例代码如下：
# 参数times用来模拟网络请求的时间
def download_video(index):
    time.sleep(2)
    print("download video {} finished at {}".format(index, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())))
    return index


executor = ThreadPoolExecutor(max_workers=2)
urls = [1, 2, 3, 4, 5]
all_task = [executor.submit(download_video, (url)) for url in urls]

wait(all_task, return_when=ALL_COMPLETED)

print(threading.currentThread())

# wait方法接收3个参数，等待的任务序列、超时时间以及等待条件。
# 等待条件return_when默认为ALL_COMPLETED，表明要等待所有的任务都结束。
# 可以看到运行结果中，确实是所有任务都完成了，主线程才打印出main。
# 等待条件还可以设置为FIRST_COMPLETED，表示第一个任务完成就停止等待。
