# https://www.runoob.com/python3/python3-date-time.html
# https://docs.python.org/zh-cn/3/tutorial/stdlib.html#dates-and-times

# Python3 日期和时间
# Python 程序能用很多方式处理日期和时间，转换日期格式是一个常见的功能。
# Python 提供了一个 time 和 calendar 模块可以用于格式化日期和时间。
# 时间间隔是以秒为单位的浮点小数。
# 每个时间戳都以自从 1970 年 1 月 1 日午夜（历元）经过了多长时间来表示。

# Python 的 time 模块下有很多函数可以转换常见日期格式。如函数 time.time() 用于获取当前时间戳, 如下实例:
import calendar
import datetime
import time
from datetime import date

ticks = time.time()
print("当前时间戳为:", ticks)
# 时间戳单位最适于做日期运算。但是1970年之前的日期就无法以此表示了。太遥远的日期也不行，UNIX和Windows只支持到2038年。

# 获取当前时间
# 从返回浮点数的时间戳方式向时间元组转换，只要将浮点数传递给如localtime之类的函数。

# 不传参数为当前时间:
print(time.localtime())
# 传参数为指定时间、返回 struct_time
localtime = time.localtime(time.time())
print(type(localtime))
print("本地时间为 :", localtime)

# 获取格式化的时间
# 你可以根据需求选取各种格式，但是最简单的获取可读的时间模式的函数是asctime():
# Python time asctime() 函数接受时间元组并返回一个可读的形式为"Tue Dec 11 18:07:14 2008"
localtime = time.asctime(time.localtime(time.time()))
print(type(localtime))
print("本地时间为 :", localtime)

# 格式化日期
# 我们可以使用 time 模块的 strftime 方法来格式化日期，：
# time.strftime(format[, t])

# 格式化成2016-03-20 11:45:39形式
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(type(datetime.datetime.now()))
# 时间加减
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 3 * 24 * 60 * 60)))
# 时间计算
print(datetime.date.today() - datetime.timedelta(days=3))
threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=3))
print(threeDayAgo)
# struct_time
print(threeDayAgo.timetuple())
# 转换为时间戳
timeStamp = int(time.mktime(threeDayAgo.timetuple()))
print(timeStamp)

# 格式化成Sat Mar 28 22:24:24 2016形式
print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
# Python time strptime() 函数根据指定的格式把一个时间字符串解析为时间元组。
# 语法
# time.strptime(string[, format])
struct_time = time.strptime(a, "%a %b %d %H:%M:%S %Y")

# Python time mktime() 函数执行与gmtime(), localtime()相反的操作，它接收struct_time对象作为参数，返回用秒数来表示时间的浮点数。
print(time.mktime(struct_time))

# python中时间日期格式化符号：

# %y 两位数的年份表示（00-99）
# %Y 四位数的年份表示（000-9999）
# %m 月份（01-12）
# %d 月内中的一天（0-31）
# %H 24小时制小时数（0-23）
# %I 12小时制小时数（01-12）
# %M 分钟数（00=59）
# %S 秒（00-59）
# %a 本地简化星期名称
# %A 本地完整星期名称
# %b 本地简化的月份名称
# %B 本地完整的月份名称
# %c 本地相应的日期表示和时间表示
# %j 年内的一天（001-366）
# %p 本地A.M.或P.M.的等价符
# %U 一年中的星期数（00-53）星期天为星期的开始
# %w 星期（0-6），星期天为星期的开始
# %W 一年中的星期数（00-53）星期一为星期的开始
# %x 本地相应的日期表示
# %X 本地相应的时间表示
# %Z 当前时区的名称
# %% %号本身

# 获取某月日历
# Calendar 模块有很广泛的方法用来处理年历和月历，例如打印某月的月历：
cal = calendar.month(2016, 1)
print("以下输出2016年1月份的日历:")
print(cal)

# datetime 模块提供了以简单和复杂的方式操作日期和时间的类。虽然支持日期和时间算法，但实现的重点是有效的成员提取以进行输出格式化和操作。该模块还支持可感知时区的对象。
# 获取当前日期
now = date.today()
print(now)
print(now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B."))
# 获取指定日期
date = datetime.date(2003, 12, 2)
print(date)
print(date.strftime("%Y-%m-%d"))

# dates support calendar arithmetic
birthday = datetime.date(1964, 7, 31)
age = now - birthday
print(age)
print(age.days)
