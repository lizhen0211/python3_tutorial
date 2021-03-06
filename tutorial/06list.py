# 列表
# 创建一个列表，只要把逗号分隔的不同的数据项使用方括号括起来即可
list1 = ['Google', 'Runoob', 1997, 2000]
list2 = [1, 2, 3, 4, 5]
list3 = ["a", "b", "c", "d"]
print("=============================================================")
# =============================================================
# 访问列表中的值
# !/usr/bin/python3
list1 = ['Google', 'Runoob', 1997, 2000]
list2 = [1, 2, 3, 4, 5, 6, 7]
print("list1[0]: ", list1[0])
print("list2[1:5]: ", list2[1:5])
print("=============================================================")
# =============================================================
# 更新列表
# !/usr/bin/python3

list5 = ['Google', 'Runoob', 1997, 2000]

print("第三个元素为 : ", list5[2])
list5[2] = 2001
print("更新后的第三个元素为 : ", list5[2])
print("=============================================================")
# =============================================================
# 添加元素
list1 = ['Google', 'Runoob', 1997, 2000]
list1.append('123')
print(list1)
print("=============================================================")
# =============================================================
# 删除列表元素
# !/usr/bin/python3

list6 = ['Google', 'Runoob', 1997, 2000]

print("原始列表 : ", list6)
del list6[2]
print("删除第三个元素 : ", list6)
print("=============================================================")
# =============================================================
# Python列表脚本操作符
# 列表对 + 和 * 的操作符与字符串相似。+ 号用于组合列表，* 号用于重复列表。
print(len([1, 2, 3]))  # 长度
print([1, 2, 3] + [4, 5, 6])  # 组合
print(['Hi!'] * 4)  # 重复
print(3 in [1, 2, 3])  # 元素是否存在于列表中
for x in [1, 2, 3]:  # 迭代
    print(x, end=" ")
print()
print("=============================================================")
# =============================================================
# Python列表截取与拼接
L = ['Google', 'Runoob', 'Taobao']
print(L[2])  # 读取第三个元素
print(L[-2])  # 从右侧开始读取倒数第二个元素: count from the right
print(L[1:])  # 输出从第二个元素开始后的所有元素
print("=============================================================")
# =============================================================
# 嵌套列表
a = ['a', 'b', 'c']
n = [1, 2, 3]
x = [a, n]
print(x)
print(x[0])
print(x[0][1])
print("=============================================================")
# =============================================================
# Python列表函数&方法
# len() 方法返回列表元素个数。
list1 = ['Google', 'Runoob', 'Taobao']
print(len(list1))
list2 = list(range(5))  # 创建一个 0-4 的列表
print(len(list2))
print("=============================================================")
# =============================================================
# Python3 List max()方法 # max() 方法返回列表元素中的最大值。
list1, list2 = ['Google', 'Runoob', 'Taobao'], [456, 700, 200]
print("list1 最大元素值 : ", max(list1))
print("list2 最大元素值 : ", max(list2))
list1, list2 = ['Google', 'Runoob', 'Taobao'], [456, 700, 200]
# Python3 List min()方法 min() 方法返回列表元素中的最小值。
print("list1 最小元素值 : ", min(list1))
print("list2 最小元素值 : ", min(list2))
# Python3 List list()方法 #list() 方法用于将元组或字符串转换为列表
aTuple = (123, 'Google', 'Runoob', 'Taobao')
list1 = list(aTuple)
print("列表元素 : ", list1)

str = "Hello World"
list2 = list(str)
print("列表元素 : ", list2)
print("=============================================================")
# =============================================================
# Python3 List append()方法
# append() 方法用于在列表末尾添加新的对象。
list1 = ['Google', 'Runoob', 'Taobao']
list1.append('Baidu')
print("更新后的列表 : ", list1)
print("=============================================================")
# =============================================================
# Python3 List count()方法
# count() 方法用于统计某个元素在列表中出现的次数。
aList = [123, 'Google', 'Runoob', 'Taobao', 123]
print("123 元素个数 : ", aList.count(123))
print("Runoob 元素个数 : ", aList.count('Runoob'))
print("=============================================================")
# =============================================================
# Python3 List extend()方法
# extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）。
list1 = ['Google', 'Runoob', 'Taobao']
list2 = list(range(5))  # 创建 0-4 的列表
list1.extend(list2)  # 扩展列表
print("扩展后的列表：", list1)
print("=============================================================")
# =============================================================
# Python3 List insert()方法
# insert() 函数用于将指定对象插入列表的指定位置。
list1 = ['Google', 'Runoob', 'Taobao']
list1.insert(1, 'Baidu')
print('列表插入元素后为 : ', list1)
print("=============================================================")
# =============================================================
# Python3 List index()方法
# index() 函数用于从列表中找出某个值第一个匹配项的索引位置。
# 语法 list.index(x[, start[, end]]) x-- 查找的对象。start-- 可选，查找的起始位置。end-- 可选，查找的结束位置。
list1 = ['Google', 'Runoob', 'Taobao']
print('Runoob 索引值为', list1.index('Runoob'))
print('Taobao 索引值为', list1.index('Taobao'))
print("=============================================================")
# =============================================================
# pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
# Python3 List pop()方法
# 语法 list.pop([index=-1])
# index -- 可选参数，要移除列表元素的索引值，不能超过列表总长度，默认为 index=-1，删除最后一个列表值。
list1 = ['Google', 'Runoob', 'Taobao']
result1 = list1.pop()
print("列表现在为 : ", list1)
print("返回结果为 : ", result1)

result2 = list1.pop(1)
print("列表现在为 : ", list1)
print("返回结果为 : ", result2)
print("=============================================================")
# =============================================================
# Python3 List remove()方法
# remove() 函数用于移除列表中某个值的 第一个 匹配项。
list1 = ['Google', 'Runoob', 'Taobao', 'Baidu', 'Taobao', 'Badidu', 'Baidu']
result1 = list1.remove('Taobao')
print("列表现在为 : ", list1)
print("返回结果为 : ", result1)
result2 = list1.remove('Baidu')
print("列表现在为 : ", list1)
print("返回结果为 : ", result2)
print("=============================================================")
# =============================================================
# Python3 List reverse()方法
# reverse() 函数用于反向列表中元素。
list1 = ['Google', 'Runoob', 'Taobao', 'Baidu']
list1.reverse()
print("列表反转后: ", list1)
print("=============================================================")
# =============================================================
# Python3 List sort()方法
# sort() 函数用于对原列表进行排序，如果指定参数，则使用比较函数指定的比较函数。
# key -- 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
# reverse -- 排序规则，reverse = True 降序， reverse = False 升序（默认）。

# 以下实例展示了 sort() 函数的使用方法：
aList = ['Google', 'Runoob', 'Taobao', 'Facebook']
aList.sort()
print("List : ", aList)
# 以下实例降序输出列表：
# 列表
vowels = ['e', 'a', 'u', 'o', 'i']
# 降序
vowels.sort(reverse=True)
# 输出结果
print('降序输出:', vowels)


# 以下实例演示了通过指定列表中的元素排序来输出列表：
# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]


# 列表
random = [(2, 2), (3, 4), (4, 1), (1, 3)]
# 指定第二个元素排序
random.sort(key=takeSecond)
# 输出类别
print('排序列表：', random)
print("=============================================================")
# =============================================================
# Python3 List clear()方法
# clear() 函数用于清空列表，类似于 del a[:]。
# list.clear()
list1 = ['Google', 'Runoob', 'Taobao', 'Baidu']
# del list1[:]
list1.clear()
print("列表清空后 : ", list1)
print("=============================================================")
# =============================================================
# Python3 List copy()方法
# copy() 函数用于复制列表，类似于 a[:]。
list1 = ['Google', 'Runoob', 'Taobao', 'Baidu']
list2 = list1.copy()
print("list2 列表: ", list2)

list3 = list2[:]
print("list3 列表: ", list3)
