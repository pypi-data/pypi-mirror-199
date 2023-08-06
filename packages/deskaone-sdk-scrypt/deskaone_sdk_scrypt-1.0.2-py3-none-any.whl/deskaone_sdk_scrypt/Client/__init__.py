import json, requests
from deskaone_sdk_scrypt.Internal import API, Internal
from deskaone_sdk_scrypt.Exceptions import Error, PrintError, ParseError
from deskaone_sdk_scrypt.Utils import Typer, Color, Crypto
from typing import Optional
from requests.exceptions import ConnectionError, ConnectTimeout, SSLError, RequestException, HTTPError, ProxyError, Timeout, ReadTimeout, JSONDecodeError, TooManyRedirects, ChunkedEncodingError
from urllib.parse import urlencode

class Client:
    
    def __init__(self, RPC: str, secretKey: str, TimeOut: int, DEBUG: bool = False) -> None:
        """A Internal Requests.
        
        Basic Usage::

            Client(
                secretKey   = str,
                DEBUG       = bool (Optional)
            )
            
        params 
        """
        self.RPC, self.secretKey, self.TimeOut, self.DEBUG = RPC, secretKey, TimeOut, DEBUG
        self.CR = Crypto.AES()
        self.CR.randomIv()
        self.CR.randomKey()
        
    def getCredits(self):
        self.CR.setData_FromString(json.dumps(dict(request = 'GET', secret = self.secretKey)))
        sub = f'{len(self.CR.getIv_to_Hex())}_{len(self.CR.getKey_to_Hex())}_{len(self.CR.encrypt_to_hex())}'
        Params = json.dumps(dict(sub = sub, data = self.CR.getKey_to_Hex() + self.CR.getIv_to_Hex() + self.CR.encrypt_to_hex()), separators=(',', ':'))
        sendApi = API(self.secretKey, self.RPC).Credits(Params, self.TimeOut)
        return int(dict(sendApi.get('data')).get('credits'))
    
    def setRequest(self, Params: dict, ParamsType: str, command: Optional[str] = None, IpPort: Optional[str] = None, Type: Optional[str] = None, TimeOut: Optional[int] = None):
        """A Internal Requests.
        
        Basic Usage::

            setRequest(
                Params  = dict,
                ParamsType  = str | JSON or URLENCODE,
                command = str | GET or POST or PUT or DELETE,
                IpPort  = str | None, example 127.0.0.1:8080
                Type    = str | HTTP | HTTPS | SOCKS4 | SOKCS5 | None, example SOCKS5
                TimeOut = int | if Mode INTERNAL
            )
            
        params is 
        """
        while True:
            try:
                if ParamsType.upper() == 'JSON':
                    self.CR.setData_FromString(json.dumps(Params, separators=(',', ':')))
                    sub = f'{len(self.CR.getIv_to_Hex())}_{len(self.CR.getKey_to_Hex())}_{len(self.CR.encrypt_to_hex())}'
                    POST = json.dumps(dict(sub = sub, data = self.CR.getKey_to_Hex() + self.CR.getIv_to_Hex() + self.CR.encrypt_to_hex()), separators=(',', ':'))
                elif ParamsType.upper() == 'URLENCODE':
                    self.CR.setData_FromString(urlencode(Params))
                    sub = f'{len(self.CR.getIv_to_Hex())}_{len(self.CR.getKey_to_Hex())}_{len(self.CR.encrypt_to_hex())}'
                    POST = json.dumps(dict(sub = sub, data = self.CR.getKey_to_Hex() + self.CR.getIv_to_Hex() + self.CR.encrypt_to_hex()), separators=(',', ':'))
                else:
                    raise ParseError('ParamsType required')
                sendApi = API(self.secretKey, self.RPC).sender(Params=POST, TimeOut=self.TimeOut)
                if sendApi.get('status') is True:
                    if command.upper() == 'EXTERNAL':
                        return True, sendApi
                    else:
                        data    = dict(sendApi.get('data'))
                        return True, Internal(URL=data.get('url'), PARAMS=data.get('data'), HEADER=data.get('headers')).Setup(IpPort=IpPort, Type=Type, Mode=data.get('methods'), TimeOut=TimeOut)
                else:
                    return False, sendApi
            except Error as e:
                raise Error(str(e))
        