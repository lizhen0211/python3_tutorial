var1 = 'Hello World!'
var2 = "Runoob"
# Python 访问子字符串，可以使用方括号来截取字符串，如下实例：
print("var1[0]: ", var1[0])
print("var2[1:5]: ", var2[1:5])
print("=============================================================")
# =============================================================
# Python 字符串更新
# 你可以截取字符串的一部分并与其他字段拼接，如下实例：
var1 = 'Hello World!'
print("已更新字符串 : ", var1[:6] + 'Runoob!')
print("=============================================================")
# =============================================================
# Python字符串运算符
# + 	字符串连接
# !/usr/bin/python3
a = "Hello"
b = "Python"
print("a + b 输出结果：", a + b)  # +	字符串连接
print("a * 2 输出结果：", a * 2)  # * 重复输出字符串
print("a[1] 输出结果：", a[1])  # [] 通过索引获取字符串中字符
print("a[1:4] 输出结果：", a[1:4])  # [:]截取字符串中的一部分，遵循左闭右开原则，str[0,2] 是不包含第 3 个字符的。

if "H" in a:
    print("H 在变量 a 中")
else:
    print("H 不在变量 a 中")

if "M" not in a:
    print("M 不在变量 a 中")
else:
    print("M 在变量 a 中")
print(r'\n')
print(R'\n')
print("=============================================================")
# =============================================================
# Python字符串格式化
# !/usr/bin/python3
print("我叫 %s 今年 %d 岁!" % ('小明', 10))
print("=============================================================")
# =============================================================
# 字符串内建函数
# capitalize()将字符串的第一个字母变成大写,其他字母变小写。
str = "this is string Example From runoob....wow!!!"
print("str.capitalize() : ", str.capitalize())

# center() 方法返回一个指定的宽度 width 居中的字符串，fillchar 为填充的字符，默认为空格。
str = "[www.runoob.com]"
print("str.center(40, '*') : ", str.center(40, '*'))
# str.count(sub, start= 0,end=len(string))
str = "www.runoob.com"
sub = 'o'
print("str.count('o') : ", str.count(sub))
# str.count(sub, start= 0,end=len(string))
sub = 'run'
print("str.count('run', 0, 10) : ", str.count(sub, 0, 10))

# !/usr/bin/python3
# encode() 方法以指定的编码格式编码字符串。errors参数可以指定不同的错误处理方案。
str = "菜鸟教程";
str_utf8 = str.encode("UTF-8")
str_gbk = str.encode("GBK")

print(str)

print("UTF-8 编码：", str_utf8)
print("GBK 编码：", str_gbk)
# decode() 方法以指定的编码格式解码 bytes 对象。默认编码为 'utf-8'。
print("UTF-8 解码：", str_utf8.decode('UTF-8', 'strict'))
print("GBK 解码：", str_gbk.decode('GBK', 'strict'))
print("=============================================================")
# =============================================================
"""
    更多内建函数 见 https://www.runoob.com/python3/python3-string.html
"""
