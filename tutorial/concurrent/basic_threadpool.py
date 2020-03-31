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
import time
from concurrent.futures import ThreadPoolExecutor


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
print(task1.result())
