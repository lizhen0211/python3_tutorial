# 16.Python 列表推导式(经典代码)
# 一.什么是推导式
# 推导式是从一个或者多个迭代器快速简洁地创建数据类型的一种方法，它将循环和条件判断结合，
# 从而避免语法冗长的代码，提高代码运行效率。能熟练使用推导式也可以间接说明你已经超越了python初学者的水平。

# 二.条件推导式
# 1.语法
'''
value1：如果条件表达式condition成立，返回value1 ； 如果条件表达式不成立，返回value2 ；
condition：条件表达式
Value2：如果条件表达式condition成立，返回value1 ； 如果条件表达式不成立，返回value2 ；

'''

# value1 if condition else Value2

# 2.实战练习
# 判断一个数字是奇数还是偶数？
# 新手代码
import time

x = 10
if x % 2 == 0:
    print("新手说：x是偶数")
else:
    print("新手说：x是奇数")

# 老司机
x = 15
print("老司机说：x是偶数") if x % 2 == 0 else print("老司机说：x是奇数")

# 三.列表推导式
# 列表推导式是条件推导式和循环一起配合使用，并返回一个列表，并且整个表达式需要在[]内，因为返回值也是列表。
# 1.语法

'''
语法一：
    exp1：在for循环中，如果x的值满足条件表达式condition(即条件表达式成立)，返回exp1；条件表达式不成立则不返回
    x：for循环中变量
    data：一个序列（比如：列表/元组/字符串等）
    condition：条件表达式
    [exp1 for x in data if condition]
'''

'''
语法二：
    exp1：在for循环中，如果x的值满足条件表达式condition(即条件表达式成立)，返回exp1；条件表达式不成立则返回exp2
    condition：条件表达式
    exp2：在for循环中，如果x的值满足条件表达式condition(即条件表达式成立)，返回exp1；条件表达式不成立则返回exp2
    x：for循环中变量
    data：个序列（比如：列表/元组/字符串等）
    [exp1 if condition else exp2 for x in data]
'''

# 获取0~20的所有偶数并且乘以10，并返回所有计算之后的结果。
list1 = [x * 10 for x in range(0, 21) if x % 2 == 0]
print(list1)

# 将0~20的偶数乘以10，奇数乘以100，并返回所有计算之后的结果。
list2 = [x * 10 if x % 2 == 0 else x * 100 for x in range(0, 21)]
print(list2)

# 3.效率对比
# 使用列表推导式的效率远远高于for循环，可能执行一句print(“helloworld”)对于cpu而已只需要0.0002秒，
# 你可能感觉不到差距，如果需要输出一亿次helloworld呢？往往细节觉得成败！
# 假如有一个需求：将0~10000000(一亿)以内的所有整数存到列表中，对比一下列表推导式和for循环耗时情况：
# 一共添加10000000次数据到列表中
total_num = 10000000
# 使用列表推导式
start_time = time.time()
list1 = [x for x in range(0, total_num)]  # 列表推导式
end_time = time.time()
print("使用列表推导式耗时：{}秒".format(end_time - start_time))

# 使用普通for循环
start_time = time.time()
list2 = list()
for x in range(0, total_num):  # for循环
    list2.append(x)
end_time = time.time()
print("使用普通for循环耗时：{}秒".format(end_time - start_time))
