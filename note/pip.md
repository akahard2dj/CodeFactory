pip 설치시 아래와 같은 SSL 인증 문제 발생시에
```bash
  Could not fetch URL https://pypi.python.org/simple/django/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host='pypi.python.org', port=443): Max retries exceeded with url: /simple/django/ (Caused by SSLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:833)'),)) - skipping
  ```
pip 내의 sessions.py 수정을 통해서 해결이 가능하다.

일반적으로 설치된 python 폴더내에서

\Lib\site-packages\pip\_vendor\requests\sessions.py

파일을 수정한다.

```py
#: SSL Verification default.
        self.verify = True
```

이부분을 False 로 변경할 경우 SSL 인증을 하지 않고 pip 설치가 
