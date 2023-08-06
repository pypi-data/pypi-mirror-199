from requests.auth import AuthBase
import time, base64, hmac, requests
from typing import Optional

class __Auth__(AuthBase):
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp   = str(int(time.time() * 1000))
        message     = str(timestamp + request.method + request.path_url + (request.body or ''))
        signature   = base64.b64encode(hmac.new(self.secret_key.encode(), message.encode(), 'SHA256').digest()).decode()
        request.headers.update({
            'SIGNATURE'     : signature,
            'TIMESTAMP'     : timestamp,
            'VERSION'       : '1.0.0'
        })
        return request

class API:
    
    def __init__(self, secret_key: str, RPC: str) -> None:
        self.Session    = requests.Session()
        self.secret_key = secret_key
        self.__url__    = RPC
    
    def setProxy(self, IpPort: Optional[str] = None, Type: Optional[str] = None):
        if IpPort is not None and Type is not None:
            if Type.upper() == 'HTTP' or Type.upper() == 'HTTPS':
                Proxies = dict(http=f"http://{IpPort}", https=f"http://{IpPort}")
            elif Type.upper() == 'SOCKS4':
                Proxies = dict(http=f"socks4://{IpPort}", https=f"socks4://{IpPort}")
            elif Type.upper() == 'SOCKS5':
                Proxies = dict(http=f"socks5://{IpPort}", https=f"socks5://{IpPort}")
            else:
                Proxies = dict(http=f"http://{IpPort}", https=f"http://{IpPort}"
                )
            self.Session.proxies     = Proxies
    
    def sender(self, Params: str, TimeOut: int, IpPort: Optional[str] = None, Type: Optional[str] = None):
        return dict(self.Session.post(self.__url__, data=Params, auth=__Auth__(self.secret_key), timeout=TimeOut).json())
    
    def Credits(self, Params: str, TimeOut: int):
        return dict(self.Session.post(self.__url__.split('/')[0] + '//' + self.__url__.split('/')[2] + '/' + 'SecretV2', data=Params, auth=__Auth__(self.secret_key), timeout=TimeOut).json())