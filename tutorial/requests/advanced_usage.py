# https://requests.readthedocs.io/zh_CN/latest/user/advanced.html
import requests
from requests import Session, Request


def ssl_cert_verification():
    """SSL 证书验证"""
    # Requests 可以为 HTTPS 请求验证 SSL 证书，就像 web 浏览器一样。
    # SSL 验证默认是开启的，如果证书验证失败，Requests 会抛出 SSLError:

    # r = requests.get('https://requestb.in')
    # print(r)

    # requests.exceptions.SSLError: hostname 'requestb.in' doesn't match either of '*.herokuapp.com', 'herokuapp.com'

    print("==============================================")
    # 在该域名上我没有设置 SSL，所以失败了。但 Github 设置了 SSL:

    # r1 = requests.get('https://github.com', verify=True)
    # print(r1)

    # 你可以为 verify 传入 CA_BUNDLE 文件的路径，或者包含可信任 CA 证书文件的文件夹路径：
    # requests.get('https://github.com', verify='/path/to/certfile')

    # 或者将其保持在会话中：
    s = requests.Session()
    s.verify = '/path/to/certfile'
    # 如果 verify 设为文件夹路径，文件夹必须通过 OpenSSL 提供的 c_rehash 工具处理。
    # 你还可以通过 REQUESTS_CA_BUNDLE 环境变量定义可信任 CA 列表。
    print("==============================================")
    # 如果你将 verify 设置为 False，Requests 也能忽略对 SSL 证书的验证。

    # r2 =  requests.get('https://kennethreitz.org', verify=False)
    # print(r2)

    # 默认情况下， verify 是设置为 True 的。选项 verify 仅应用于主机证书。
    # # 对于私有证书，你也可以传递一个 CA_BUNDLE 文件的路径给 verify。
    # 你也可以设置 # REQUEST_CA_BUNDLE 环境变量。


def prepared_requests():
    """准备的请求"""
    # 当你从 API 或者会话调用中收到一个 Response 对象时，
    # request 属性其实是使用了 PreparedRequest。
    # 有时在发送请求之前，你需要对 body 或者 header （或者别的什么东西）做一些额外处理。

    url = 'http://httpbin.org/post'
    data = {'key': 'value'}
    header = {'user-agent': 'my-app/0.0.1'}
    s = Session()
    req = Request('GET', url,
                  data=data,
                  headers=header
                  )
    prepped = req.prepare()
    # do something with prepped.body
    # do something with prepped.headers

    # resp = s.send(prepped,
    #               stream=stream,
    #               verify=verify,
    #               proxies=proxies,
    #               cert=cert,
    #               timeout=timeout
    #               )
    #
    # print(resp.status_code)

    # 由于你没有对 Request 对象做什么特殊事情，
    # 你立即准备和修改了 PreparedRequest 对象，
    # 然后把它和别的参数一起发送到 requests.* 或者 Session.*。

    # 然而，上述代码会失去 Requests Session 对象的一些优势， 尤其 Session 级别的状态，
    # 例如 cookie 就不会被应用到你的请求上去。
    # 要获取一个带有状态的 PreparedRequest，
    # 请用 Session.prepare_request() 取代 Request.prepare() 的调用，如下所示：

    # s = Session()
    # req = Request('GET', url,
    #               data=data
    # headers = headers
    # )
    #
    # prepped = s.prepare_request(req)
    #
    # # do something with prepped.body
    # # do something with prepped.headers
    #
    # resp = s.send(prepped,
    #               stream=stream,
    #               verify=verify,
    #               proxies=proxies,
    #               cert=cert,
    #               timeout=timeout
    #               )
    #
    # print(resp.status_code)


def request_and_response_objects():
    """请求与响应对象"""
    # 任何时候进行了类似 requests.get() 的调用，你都在做两件主要的事情。
    # 其一，你在构建一个 Request 对象， 该对象将被发送到某个服务器请求或查询一些资源。
    # 其二，一旦 requests 得到一个从服务器返回的响应就会产生一个 Response 对象。
    # 该响应对象包含服务器返回的所有信息，也包含你原来创建的 Request 对象。
    # 如下是一个简单的请求，从 Wikipedia 的服务器得到一些非常重要的信息：
    r = requests.get('http://www.baidu.com')
    # 如果想访问服务器返回给我们的响应头部信息，可以这样做：
    print(r.headers)
    # 然而，如果想得到发送到服务器的请求的头部，
    # 我们可以简单地访问该请求，然后是该请求的头部：
    print(r.request.headers)


def session_objects():
    """会话对象"""
    # 会话对象让你能够跨请求保持某些参数。
    # 它也会在同一个 Session 实例发出的所有请求之间保持 cookie，
    # 期间使用 urllib3 的 connection pooling 功能。
    # 所以如果你向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。 (参见 HTTP persistent connection).

    # 会话对象具有主要的 Requests API 的所有方法。
    # 我们来跨请求保持一些 cookie:
    s1 = requests.Session()
    r = s1.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
    print(r.text)
    print("==============================================")
    r1 = s1.get("http://httpbin.org/cookies")
    print(r1.text)
    print("==============================================")
    # 会话也可用来为请求方法提供缺省数据。这是通过为会话对象的属性提供数据来实现的：
    s2 = requests.Session()
    s2.auth = ('user', 'pass')
    s2.headers.update({'x-test': 'true'})

    # both 'x-test' and 'x-test2' are sent
    r2 = s2.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
    print(r2.text)
    print("==============================================")

    # 任何你传递给请求方法的字典都会与已设置会话层数据合并。
    # 方法层的参数 覆盖 会话的参数。
    # 不过需要注意，就算使用了会话，方法级别的参数也不会被跨请求保持。
    # 下面的例子只会和第一个请求发送 cookie ，而非第二个：
    s3 = requests.Session()
    r3 = s3.get('http://httpbin.org/cookies', cookies={'from-my': 'browser'})
    print(r3.text)

    r4 = s3.get('http://httpbin.org/cookies')
    print(r4.text)
    print("==============================================")
    # 如果你要手动为会话添加 cookie，就使用 Cookie utility 函数 来操纵 Session.cookies。
    # 会话还可以用作前后文管理器：
    with requests.Session() as s:
        r5 = s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
        print(r5.text)

    # 包含在一个会话中的所有数据你都可以直接使用。学习更多细节请阅读 会话 API 文档。


# 会话对象
# session_objects()

# 请求与响应对象
# request_and_response_objects()

# 准备的请求
# prepared_requests()

# SSL 证书验证
ssl_cert_verification()
