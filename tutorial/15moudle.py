# Python3 模块
# 模块是一个包含所有你定义的函数和变量的文件，其后缀名是.py。模块可以被别的程序引入，
# 以使用该模块中的函数等功能。这也是使用 python 标准库的方法。
# 下面是一个使用 python 标准库中模块的例子。
import sys

print('命令行参数如下:')
for i in sys.argv:
    print(i)
print('\n\nPython 路径为：', sys.path, '\n')
# 1、import sys 引入 python 标准库中的 sys.py 模块；这是引入某一模块的方法。
# 2、sys.argv 是一个包含命令行参数的列表。
# 3、sys.path 包含了一个 Python 解释器自动查找所需模块的路径的列表。
# ============================================================
print("=============================================================")
# import 语句
# 想使用 Python 源文件，只需在另一个源文件里执行 import 语句，语法如下：
# import module1[, module2[,... moduleN]
# 搜索路径是一个解释器会先进行搜索的所有目录的列表。如想要导入模块 support，需要把命令放在脚本的顶端：
# 见 tutorial/moudle/test.py
