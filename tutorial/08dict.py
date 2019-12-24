# Python3 字典
# 字典是另一种可变容器模型，且可存储任意类型对象。
# 字典的每个键值(key=>value)对用冒号(:)分割，每个对之间用逗号(,)分割，整个字典包括在花括号({})中 ,格式如下所示：
# d = {key1 : value1, key2 : value2 }
print("=============================================================")
# =============================================================
# 访问字典里的值
dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
print("dict['Name']: ", dict['Name'])
print("dict['Age']: ", dict['Age'])
# 如果用字典里没有的键访问数据，会输出错误如下：
dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
# print("dict['Alice']: ", dict['Alice'])
print("=============================================================")
# =============================================================
# 修改字典
# 向字典添加新内容的方法是增加新的键/值对，修改或删除已有键/值对如下实例:
dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
dict['Age'] = 8  # 更新 Age
dict['School'] = "菜鸟教程"  # 添加信息
print("dict['Age']: ", dict['Age'])
print("dict['School']: ", dict['School'])
print("=============================================================")
# =============================================================
# 删除字典元素
# 能删单一的元素也能清空字典，清空只需一项操作。
dict1 = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
del dict1['Name']  # 删除键 'Name'
print(dict1)
dict1.clear()  # 清空字典
print(dict1)
del dict1  # 删除字典
# print(dict1) 但这会引发一个异常，因为用执行 del 操作后字典不再存在：
print("=============================================================")
# =============================================================
# 字典键的特性
# 字典值可以是任何的 python 对象，既可以是标准的对象，也可以是用户定义的，但键不行
# 1）不允许同一个键出现两次。创建时如果同一个键被赋值两次，后一个值会被记住
dict = {'Name': 'Runoob', 'Age': 7, 'Name': '小菜鸟'}
print("dict['Name']: ", dict['Name'])
# 2）键必须不可变，所以可以用数字，字符串或元组充当，而用列表就不行
# dict = {['Name']: 'Runoob', 'Age': 7}
# print("dict['Name']: ", dict['Name'])
print("=============================================================")
# =============================================================
# 字典内置函数&方法
# Python字典包含了以下内置函数
dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
print(len(dict))  # 计算字典元素个数，即键的总数
print("=============================================================")
# =============================================================
dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
print(str(dict))  # 输出字典，以可打印的字符串表示
print("=============================================================")
# =============================================================
dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
print(type(dict))  # type(variable) 返回输入的变量类型，如果变量是字典就返回字典类型
print("=============================================================")
# =============================================================
# Python字典包含了以下内置方法
# 字典 clear()方法
dict = {'Name': 'Zara', 'Age': 7}
print("字典长度 : %d" % len(dict))
dict.clear()
print("字典删除后长度 : %d" % len(dict))
print("=============================================================")
# =============================================================
# https://www.runoob.com/w3cnote/python-understanding-dict-copy-shallow-or-deep.html
# 字典 copy()方法
dict1 = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
print(id(dict1))
dict2 = dict1.copy()  # copy() 函数返回一个字典的浅复制
print("新复制的字典为 : ", dict2)
print(id(dict2))
print("=============================================================")
# =============================================================
# 字典浅拷贝
a = {1: [1, 2, 3], 'a_key': 'a_val'}
b = a.copy()
print(a, b)
a[1].append(4)
a['a_key'] = 'b_val'
print(a)
print(b)
print("=============================================================")
# =============================================================
import copy

a = [1, 2, 3, 4, ['a', 'b']]  # 原始对象
b = a  # 赋值，传对象的引用
c = copy.copy(a)  # 对象拷贝，浅拷贝
d = copy.deepcopy(a)  # 对象拷贝，深拷贝

a.append(5)  # 修改对象a
a[4].append('c')  # 修改对象a中的['a', 'b']数组对象
print('a = ', a)
print(('a的子对象ID:') + '' + str(id(a[4])))
print('b = ', b)  # 赋值
print('b的子对象ID:' + str(id(b[4])))
print('c = ', c)  # 对象拷贝，浅拷贝 拷贝父对象，不会拷贝对象的内部的子对象
print('c的子对象ID:' + str(id(c[4])))
print('d = ', d)  # copy 模块的 deepcopy 方法，完全拷贝了父对象及其子对象
print('d的子对象ID:' + str(id(d[4])))
print("=============================================================")
# =============================================================
# 字典 fromkeys() 方法
# Python 字典 fromkeys() 函数用于创建一个新字典，以序列 seq 中元素做字典的键，value 为字典所有键对应的初始值。
seq = ('name', 'age', 'sex')

dict = dict.fromkeys(seq)
print("新的字典为 : %s" % str(dict))

dict = dict.fromkeys(seq, 10)
print("新的字典为 : %s" % str(dict))
print("=============================================================")
# =============================================================
# 字典 get() 方法
# 字典 get() 函数返回指定键的值，如果值不在字典中返回默认值 None
dict = {'Name': 'Runoob', 'Age': 27}

print("Age 值为 : %s" % dict.get('Age'))
print("Sex 值为 : %s" % dict.get('Sex', "NA"))
print("tel 值为 : %s" % dict.get('tel'))
print("=============================================================")
# =============================================================
# 字典 in 操作符
# Python 字典 in 操作符用于判断键是否存在于字典中，如果键在字典 dict 里返回 true，否则返回 false。
# 而 not in 操作符刚好相反，如果键在字典 dict 里返回 false，否则返回 true。
dict = {'Name': 'Runoob', 'Age': 7}
# 检测键 Age 是否存在
if 'Age' in dict:
    print("键 Age 存在")
else:
    print("键 Age 不存在")

# 检测键 Sex 是否存在
if 'Sex' in dict:
    print("键 Sex 存在")
else:
    print("键 Sex 不存在")

# 检测键 Age 是否存在
if 'Age' not in dict:
    print("键 Age 不存在")
else:
    print("键 Age 存在")
print("=============================================================")
# =============================================================
# Python3 字典 items() 方法
# 返回可遍历的(键, 值) 元组数组。
dict = {'Name': 'Runoob', 'Age': 7}
print("Value : %s" % dict.items())
for _ in dict.items():
    print(_)
print("=============================================================")
# =============================================================
# Python3 字典 keys() 方法
# Python3 字典 keys() 方法返回一个可迭代对象，可以使用 list() 来转换为列表。
dict = {'Name': 'Runoob', 'Age': 7}
print(dict.keys())
print(list(dict.keys()))
print("=============================================================")
# =============================================================
# Python3 字典 values() 方法
# Python 字典 values() 方法返回一个迭代器，可以使用 list() 来转换为列表，列表为字典中的所有值。
dict = {'Sex': 'female', 'Age': 7, 'Name': 'Zara'}
print(dict.values())
print("字典所有值为 : ", list(dict.values()))
print("=============================================================")
# =============================================================
# Python3 字典 setdefault() 方法
# Python 字典 setdefault() 方法和 get()方法 类似, 如果键不已经存在于字典中，将会添加键并将值设为默认值。
dict = {'Name': 'Runoob', 'Age': 7}

print("Age 键的值为 : %s" % dict.setdefault('Age', None))
print("Sex 键的值为 : %s" % dict.setdefault('Sex', 'Na'))
print("新字典为：", dict)
print("=============================================================")
# =============================================================
# Python3 字典 update() 方法
# Python 字典 update() 函数把字典参数 dict2 的 key/value(键/值) 对更新到字典 dict 里。
dict = {'Name': 'Runoob', 'Age': 7}
dict2 = {'Sex': 'female'}
dict.update(dict2)
print("更新字典 dict : ", dict)
print("=============================================================")
# =============================================================
# Python3 字典 pop() 方法
# Python 字典 pop() 方法删除字典给定键 key 所对应的值，返回值为被删除的值。key值必须给出。 否则，返回default值。
site = {'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'}
pop_obj = site.pop('name')
print(pop_obj)
# pop_obj = site.pop('age',18)
# print(pop_obj)
print(site)
print("=============================================================")
# =============================================================
# Python3 字典 popitem() 方法
# Python 字典 popitem() 方法随机返回并删除字典中的最后一对键和值。
# 返回一个键值对(key,value)形式，按照 LIFO（Last In First Out 后进先出法） 顺序规则，即最末尾的键值对。
site = {'name': '菜鸟教程', 'alexa': 10000, 'url': 'www.runoob.com'}
pop_obj = site.popitem()
print(pop_obj)
print(site)
