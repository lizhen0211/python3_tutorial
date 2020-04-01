# 17.Python 字典推导式(经典代码)
# 字典推导式使用方法其实也类似，也是通过循环和条件判断表达式配合使用，
# 不同的是字典推导式返回值是一个字典，所以整个表达式需要写在{}内部。

# 一.字典推导式语法


"""
语法一：
    key：字典中的key
    value：字典中的value
    dict.items()：序列
    condition：条件表达式
    key_exp：在for循环中，如果条件表达式condition成立(即条件表达式成立)，返回对应的key,value并作key_exp,value_exp处理
    value_exp：在for循环中，如果条件表达式condition成立(即条件表达式成立)，返回对应的key,value并作key_exp,value_exp处理

    {key_exp: value_exp for key, value in dict.items() if condition}
"""

'''
语法二：
    key：字典中的key 
    value：字典中的value 
    dict.items()：序列 
    condition：条件表达式 
    key_exp：在for循环中，如果条件表达式condition成立(即条件表达式成立)，返回对应的key,value并作key_exp,value_exp处理 
    value_exp1：在for循环中，如果条件表达式condition成立(即条件表达式成立)，返回对应的key,value并作key_exp,value_exp1处理
    value_exp2：在for循环中，如果条件表达式condition不成立(即条件表达式不成立)，返回对应的key,value并作key_exp,value_exp2处理
    
    {key_exp: value_exp1 if condition else value_exp2 for key, value in dict.items()}
'''

# 二.字典推导式实战
# 1.在字典中提取或者修改数据，返回新的字典
# 案例一：获取字典中key值是小写字母的键值对
dict1 = {"a": 10, "B": 20, "C": True, "D": "hello world", "e": "python教程"}
dict2 = {key: value for key, value in dict1.items() if key.islower()}
print(dict2)

# 案例二：将字典中的所有key设置为小写
dict3 = {key.lower(): value for key, value in dict1.items()}
print(dict3)

# 案例三：将字典中所有key是小写字母的value统一赋值为'error'
dict4 = {key: value if key.isupper() else "error" for key, value in dict1.items()}
print(dict4)

# 2.在字符串中提取数据，返回新的字典
# 在后期的爬虫课程中，我们需要获取cookies并以字典的形式传参，
# 如果cookies是字符串则需要转换为字典，经典代码案例如下：

cookies = "anonymid=jy0ui55o-u6f6zd; depovince=GW; _r01_=1; JSESSIONID=abcMktGLRGjLtdhBk7OVw; ick_login=a9b557b8-8138-4e9d-8601-de7b2a633f80; _ga=GA1.2.1307141854.1562980962; _gid=GA1.2.201589596.1562980962; _c1=-100; first_login_flag=1; ln_uact=18323008898; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; jebe_key=88f1340c-592c-4dd6-a738-128a76559f45%7Cad33b3c730fcdc8df220648f0893e840%7C1562981108370%7C1%7C1562981106763; jebe_key=88f1340c-592c-4dd6-a738-128a76559f45%7Cad33b3c730fcdc8df220648f0893e840%7C1562981108370%7C1%7C1562981106765; jebecookies=793eb32e-92c6-470d-b9d0-5f924c335d30|||||; _de=E77807CE44886E0134ABF27E72CFD74F; p=a00d65b1f779614cd242dc719e24c73e0; t=292ba8729a4151c1a357e176d8d91bff0; societyguester=292ba8729a4151c1a357e176d8d91bff0; id=969937120; xnsid=1700b2cc; ver=7.0; loginfrom=null; wp_fold=0"
# 字典推导式
cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
print(cookies)

# 字典推导式和列表推导式的效率均比普通的for循环效率更高，注意字典推导式与列表推导式的区别：
#
# 1.列表推导式返回列表，表达式在中括号[]中
#
# 2.字典推导式返回字典，表达式在大括号{}中
