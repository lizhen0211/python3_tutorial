# 列表
# 创建一个列表，只要把逗号分隔的不同的数据项使用方括号括起来即可
list1 = ['Google', 'Runoob', 1997, 2000];
list2 = [1, 2, 3, 4, 5];
list3 = ["a", "b", "c", "d"];
print("=============================================================")
# =============================================================
# 访问列表中的值
# !/usr/bin/python3
list1 = ['Google', 'Runoob', 1997, 2000];
list2 = [1, 2, 3, 4, 5, 6, 7];
print("list1[0]: ", list1[0])
print("list2[1:5]: ", list2[1:5])
print("=============================================================")
# =============================================================
# 更新列表
# !/usr/bin/python3

list = ['Google', 'Runoob', 1997, 2000]

print("第三个元素为 : ", list[2])
list[2] = 2001
print("更新后的第三个元素为 : ", list[2])
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

list = ['Google', 'Runoob', 1997, 2000]

print("原始列表 : ", list)
del list[2]
print("删除第三个元素 : ", list)
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
