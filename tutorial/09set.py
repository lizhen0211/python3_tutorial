# Python3 集合
# 集合（set）是一个无序的不重复元素序列。
# 可以使用大括号 { } 或者 set() 函数创建集合，注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
# 创建格式：
# parame = {value01,value02,...}
# 或者
# set(value)
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(basket)  # 这里演示的是去重功能
print('orange' in basket)  # 快速判断元素是否在集合内
print('crabgrass' in basket)
print("=============================================================")
# =============================================================
# 下面展示两个集合间的运算.
a = set('abracadabra')
b = set('alacazam')
print(a)
print(b)
print(a - b)  # 集合a中包含而集合b中不包含的元素
print(a | b)  # 集合a或b中包含的所有元素
print(a & b)  # 集合a和b中都包含了的元素
print(a ^ b)  # 不同时包含于a和b的元素
print("=============================================================")
# =============================================================
# 集合的基本操作
# 1、添加元素
thisset = set(("Google", "Runoob", "Taobao"))
thisset.add("Facebook")
print(thisset)
# 还有一个方法，也可以添加元素，且参数可以是列表，元组，字典等，语法格式如下：
# s.update( x ) x 可以有多个，用逗号分开
thisset = set(("Google", "Runoob", "Taobao"))
# thisset.update({1, 3})
print(thisset)
thisset.update([1, 4], [5, 6])
print(thisset)
print("=============================================================")
# =============================================================
# 移除元素
# s.remove( x )
thisset = set(("Google", "Runoob", "Taobao"))
thisset.remove("Taobao")
print(thisset)
# thisset.remove("Facebook")  # 不存在会发生错误
# 此外还有一个方法也是移除集合中的元素，且如果元素不存在，不会发生错误
# s.discard( x )
thisset = set(("Google", "Runoob", "Taobao"))
thisset.discard("Facebook")  # 不存在不会发生错误
print(thisset)
# 我们也可以设置随机删除集合中的一个元素
# s.pop()
thisset = set(("Google", "Runoob", "Taobao", "Facebook"))
x = thisset.pop()  # 多次执行测试结果都不一样 set 集合的 pop 方法会对集合进行无序的排列，然后将这个无序排列集合的左面第一个元素进行删除
print(x)
print("=============================================================")
# =============================================================
# 计算集合元素个数
# len(s)
thisset = set(("Google", "Runoob", "Taobao"))
print(len(thisset))
# 清空集合
# s.clear()
thisset = set(("Google", "Runoob", "Taobao"))
thisset.clear()
print(thisset)
print("=============================================================")
# =============================================================
# 判断元素是否在集合中存在
# x in s 判断元素 x 是否在集合 s 中，存在返回 True，不存在返回 False。
thisset = set(("Google", "Runoob", "Taobao"))
print("Runoob" in thisset)
print("Facebook" in thisset)
print("=============================================================")
# =============================================================
# 集合内置方法完整列表
# https://www.runoob.com/python3/python3-set.html
# add()	为集合添加元素
# clear()	移除集合中的所有元素
# copy()	拷贝一个集合
# difference()	返回多个集合的差集
# difference_update()	移除集合中的元素，该元素在指定的集合也存在。
# discard()	删除集合中指定的元素
# intersection()	返回集合的交集
# intersection_update()	返回集合的交集。
# isdisjoint()	判断两个集合是否包含相同的元素，如果没有返回 True，否则返回 False。
# issubset()	判断指定集合是否为该方法参数集合的子集。
# issuperset()	判断该方法的参数集合是否为指定集合的子集
# pop()	随机移除元素
# remove()	移除指定元素
# symmetric_difference()	返回两个集合中不重复的元素集合。
# symmetric_difference_update()	移除当前集合中在另外一个指定集合相同的元素，并将另外一个指定集合中不同的元素插入到当前集合中。
# union()	返回两个集合的并集
# update()	给集合添加元素
