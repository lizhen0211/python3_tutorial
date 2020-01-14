# Python3 循环语句
# Python 中的循环语句有 for 和 while。
# 同样需要注意冒号和缩进。另外，在 Python 中没有 do..while 循环。
n = 100

sum = 0
counter = 1
while counter <= n:
    sum = sum + counter
    counter += 1

print("1 到 %d 之和为: %d" % (n, sum))
print("=============================================================")
# =============================================================
# 无限循环
# 我们可以通过设置条件表达式永远不为 false 来实现无限循环
# var = 1
# while var == 1:  # 表达式永远为 true
#     num = int(input("输入一个数字  :"))
#     print("你输入的数字是: ", num)
#
# print("Good bye!")
print("=============================================================")
# =============================================================
# while 循环使用 else 语句
# 在 while … else 在条件语句为 false 时执行 else 的语句块。
# 语法格式如下：
# while <expr>:
# #####<statement(s)>
# else:
# #####<additional_statement(s)>
count = 0
while count < 5:
    print(count, " 小于 5")
    count = count + 1
else:
    print(count, " 大于或等于 5")
print("=============================================================")
# =============================================================
# for 语句
# Python for循环可以遍历任何序列的项目，如一个列表或者一个字符串。
# for循环的一般格式如下：
# for <variable> in <sequence>:
# #### <statements>
# else:
# ### <statements>

# Python for 循环实例
languages = ["C", "C++", "Perl", "Python"]
for x in languages:
    print(x)
print("=============================================================")
# =============================================================
# 以下 for 实例中使用了 break 语句，break 语句用于跳出当前循环体：
sites = ["Baidu", "Google", "Runoob", "Taobao"]
for site in sites:
    if site == "Runoob":
        print("菜鸟教程!")
        break
    print("循环数据 " + site)
else:
    print("没有循环数据!")
print("完成循环!")
print("=============================================================")
# =============================================================
# range()函数
# 如果你需要遍历数字序列，可以使用内置range()函数。它会生成数列，例如:
for i in range(5):
    print(i)
print("=============================================================")
# =============================================================
# 你也可以使用range指定区间的值：
