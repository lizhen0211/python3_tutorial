# https://requests.readthedocs.io/zh_CN/latest/user/advanced.html
import requests


def session_objects():
    """会话对象"""
    # 会话对象让你能够跨请求保持某些参数。
    # 它也会在同一个 Session 实例发出的所有请求之间保持 cookie， 期间使用 urllib3 的 connection pooling 功能。
    # 所以如果你向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
    # (参见 HTTP persistent connection).
    # 我们来跨请求保持一些 cookie:
    s = requests.Session()
    r = s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
    print(r.text)
    r1 = s.get("http://httpbin.org/cookies")
    print(r1.text)
    print("==============================================")
    # 会话也可用来为请求方法提供缺省数据。这是通过为会话对象的属性提供数据来实现的：
    s1 = requests.Session()
    s1.auth = ('user', 'pass')
    s1.headers.update({'x-test': 'true'})
    # both 'x-test' and 'x-test2' are sent
    r2 = s1.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
    print(r2.text)
    # 任何你传递给请求方法的字典都会与已设置会话层数据合并。方法层的参数覆盖会话的参数。
    print("==============================================")


session_objects()
