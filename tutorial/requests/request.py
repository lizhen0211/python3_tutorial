# https://requests.readthedocs.io/zh_CN/latest/
import json

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


def raw_response_content():
    """原始响应内容"""
    # 在罕见的情况下，你可能想获取来自服务器的原始套接字响应，那么你可以访问 r.raw。
    # 果你确实想这么干，那请你确保在初始请求中设置了 stream=True。
    r = requests.get('https://api.github.com/events', stream=True)
    print(r.raw)

    print(r.raw.read(10))

    # 但一般情况下，你应该以下面的模式将文本流保存到文件：
    # with open(filename, 'wb') as fd:
    #     for chunk in r.iter_content(chunk_size):
    #         fd.write(chunk)

    # 使用 Response.iter_content 将会处理大量你直接使用 Response.raw 不得不处理的。
    # 当流下载时，上面是优先推荐的获取内容方式。
    # Note that chunk_size can be freely adjusted to a number that may better fit your use cases.


def custom_headers():
    """定制请求头"""
    # 如果你想为请求添加 HTTP 头部，只要简单地传递一个 dict 给 headers 参数就可以了。
    # 例如，在前一个示例中我们没有指定 content-type:
    url = 'https://api.github.com/some/endpoint'
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers=headers)
    print(r)

    # 注意: 定制 header 的优先级低于某些特定的信息源，例如：
    # 如果在 .netrc 中设置了用户认证信息，使用 headers= 设置的授权就不会生效。而如果设置了 auth= 参数，``.netrc`` 的设置就无效了。
    # 如果被重定向到别的主机，授权 header 就会被删除。
    # 代理授权 header 会被 URL 中提供的代理身份覆盖掉。
    # 在我们能判断内容长度的情况下，header 的 Content-Length 会被改写。
    # 更进一步讲，Requests 不会基于定制 header 的具体情况改变自己的行为。只不过在最后的请求中，所有的 header 信息都会被传递进去。

    # 注意: 所有的 header 值必须是 string、bytestring 或者 unicode。尽管传递 unicode header 也是允许的，但不建议这样做。


def more_complicated_post_requests():
    """更加复杂的 POST 请求"""
    # 通常，你想要发送一些编码为表单形式的数据——非常像一个 HTML 表单。
    # 要实现这个，只需简单地传递一个字典给 data 参数。你的数据字典在发出请求时会自动编码为表单形式：
    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.post("http://httpbin.org/post", data=payload)
    print(r.text)
    print("==============================================")
    # 你还可以为 data 参数传入一个元组列表。
    # 在表单中多个元素使用同一 key 的时候，这种方式尤其有效：
    payload = (('key1', 'value1'), ('key1', 'value2'))
    r = requests.post('http://httpbin.org/post', data=payload)
    print(r.text)
    print("==============================================")
    # 很多时候你想要发送的数据并非编码为表单形式的。
    # 如果你传递一个 string 而不是一个 dict，那么数据会被直接发布出去。
    url = 'http://httpbin.org/post'
    payload = {'some': 'data'}
    r = requests.post(url, data=json.dumps(payload))
    print(r.text)
    print("==============================================")
    # 此处除了可以自行对 dict 进行编码，你还可以使用 json 参数直接传递，然后它就会被自动编码。
    # 这是 2.4.2 版的新加功能：
    url = 'http://httpbin.org/post'
    payload = {'some': 'data'}
    r = requests.post(url, json=payload)
    print(r.text)
    print("==============================================")


def post_a_multipart_encoded_file():
    """POST一个多部分编码(Multipart-Encoded)的文件"""
    # Requests 使得上传多部分编码文件变得很简单：
    url = 'http://httpbin.org/post'
    files = {'file': open('../../../report.xls', 'rb')}
    r = requests.post(url, files=files)
    print(r.text)
    print("==============================================")
    # 你可以显式地设置文件名，文件类型和请求头：
    url = 'http://httpbin.org/post'
    files = {'file': ('report.xls', open('../../../report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
    r = requests.post(url, files=files)
    print(r.text)
    print("==============================================")
    # 如果你想，你也可以发送作为文件来接收的字符串：
    url = 'http://httpbin.org/post'
    files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
    r = requests.post(url, files=files)
    print(r.text)
    print("==============================================")
    # 如果你发送一个非常大的文件作为 multipart/form-data 请求，你可能希望将请求做成数据流。
    # 默认下 requests 不支持, 但有个第三方包 requests-toolbelt 是支持的。
    # 你可以阅读 toolbelt（链接） 文档 来了解使用方法。
    # 在一个请求中发送多文件参考 高级用法（链接） 一节。
    # 警告:
    # 我们强烈建议你用二进制模式(binary mode)打开文件。
    # 这是因为 Requests 可能会试图为你提供 Content-Length header，在它这样做的时候，这个值会被设为文件的字节数（bytes）。
    # 如果用文本模式(text mode)打开文件，就可能会发生错误。


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
# json_response_content()

# 原始响应内容
# raw_response_content()

# 定制请求头
# custom_headers()

# 更加复杂的 POST 请求
# more_complicated_post_requests()

# POST一个多部分编码(Multipart-Encoded)的文件
post_a_multipart_encoded_file()
