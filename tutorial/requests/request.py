# https://requests.readthedocs.io/zh_CN/latest/
import requests


def simple_request():
    """一个简单的请求"""
    r = requests.get('https://api.github.com/user', auth=('[your username]', '[your password]'))
    # r = requests.get('https://www.baidu.com')
    print(r.status_code)
    print(r.headers['content-type'])
    print(r.encoding)
    print(r.text)
    print(r.json())


def make_a_request():
    """发送请求"""

    # 我们有一个名为 r 的 Response 对象。我们可以从这个对象中获取所有我们想要的信息。
    r = requests.get('https://api.github.com/events')
    print(r.json())
    print("==================以上是get请求结果============================")
    # 发送一个 HTTP POST 请求
    r = requests.post('http://httpbin.org/post', data={'key(see response)': 'value(see response)'})
    print(r.json())
    print("===================以上是post请求结果===========================")
    # 发送一个put请求
    r = requests.put('http://httpbin.org/put', data={'key': 'value'})
    print(r.json())
    print("===================以上是put请求结果===========================")
    # 发送一个delete请求
    r = requests.delete('http://httpbin.org/delete')
    print(r.json())
    print("===================以上是delete请求结果===========================")
    # 发送一个head请求
    r = requests.head('http://httpbin.org/get')
    print(r)
    print("===================以上是head请求结果===========================")
    # 发送一个options请求
    r = requests.options('http://httpbin.org/get')
    print(r)
    print("===================以上是options请求结果===========================")


def passing_parameters_in_urls():
    """传递 URL 参数"""
    # httpbin.org/get?key=val。Requests 允许你使用 params 关键字参数，以一个字符串字典来提供这些参数。
    # 如果你想传递 key1=value1 和 key2=value2 到 httpbin.org/get ，那么你可以使用如下代码：

    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.get("http://httpbin.org/get", params=payload)
    # http://httpbin.org/get?key2=value2&key1=value1
    print(print(r.url))

    # 你还可以将一个列表作为值传入：
    payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
    r = requests.get('http://httpbin.org/get', params=payload)
    # http://httpbin.org/get?key1=value1&key2=value2&key2=value3
    print(r.url)


def response_content():
    """响应内容"""
    r = requests.get('https://api.github.com/events')
    # Requests 会自动解码来自服务器的内容。大多数 unicode 字符集都能被无缝地解码。
    print(r.text)
    print("==============================================")
    # 请求发出后，Requests 会基于 HTTP 头部对响应的编码作出有根据的推测。
    # 当你访问 r.text 之时，Requests 会使用其推测的文本编码。
    # 你可以找出 Requests 使用了什么编码，并且能够使用 r.encoding 属性来改变它：
    print(r.encoding)
    print("==============================================")
    # 如果你改变了编码，每当你访问 r.text ，Request 都将会使用 r.encoding 的新值
    r.encoding = 'ISO-8859-1'
    print(r.text)
    print("==============================================")
    # 你可能希望在使用特殊逻辑计算出文本的编码的情况下来修改编码。比如 HTTP 和 XML 自身可以指定编码。
    # 这样的话，你应该使用 r.content 来找到编码，然后设置 r.encoding 为相应的编码。
    # 这样就能使用正确的编码解析 r.text 了。
    print(r.content)
    print("==============================================")


def binary_response_content():
    """二进制响应内容"""
    # Requests 会自动为你解码 gzip 和 deflate 传输编码的响应数据。
    # 如，以请求返回的二进制数据创建一张图片，你可以使用如下代码：
    # i = Image.open(BytesIO(r.content))
    pass


def json_response_content():
    """JSON 响应内容"""
    # Requests 中也有一个内置的 JSON 解码器，助你处理 JSON 数据：
    r = requests.get('https://api.github.com/events')
    print(r.json())
    # 如果 JSON 解码失败， r.json() 就会抛出一个异常。
    # 例如，响应内容是 401 (Unauthorized)，尝试访问 r.json() 将会抛出 ValueError: No JSON object could be decoded 异常。

    # 需要注意的是，成功调用 r.json() 并**不**意味着响应的成功。
    # 有的服务器会在失败的响应中包含一个 JSON 对象（比如 HTTP 500 的错误细节）。
    # 这种 JSON 会被解码返回。要检查请求是否成功，请使用 r.raise_for_status()
    # 或者检查 r.status_code 是否和你的期望相同。


# 一个简单的demo
# simple_request()

# 简单的get、post、put、delete、head、options
# make_a_request()

# 传递 URL 参数
# passing_parameters_in_urls()

# 响应内容
# response_content()

# 二进制响应内容
# binary_response_content()

# JSON 响应内容
json_response_content()
