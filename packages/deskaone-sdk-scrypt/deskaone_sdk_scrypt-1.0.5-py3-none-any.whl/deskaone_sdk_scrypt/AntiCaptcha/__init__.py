import json
import time
from deskaone_sdk_scrypt.Client import Client

class AntiCaptcha:
    
    def __init__(self, *args, **kwargs) -> None:
        """A Internal Requests.
        
        Basic Usage::

            AntiCaptcha(
                API_KEY = str || AntiCaptcha,
                URL_API = str || Server Scrypt,
                SECRET_KEY = str || Server Scrypt
            )
            
        params is Json/urlencode for POST/PUT or urlencode for GET
        """
        #RPC: str, secretKey: str, TimeOut: int, DEBUG: bool = False
        self.API_KEY, self.URL_API, self.SECRET_KEY = kwargs.get('API_KEY'), kwargs.get('URL_API'), kwargs.get('SECRET_KEY')
        self.client = Client(f'{self.URL_API}AntiCaptcha', self.SECRET_KEY, 60, False)
    
    def __setParams__(self, *args, **kwargs):
        return dict(**kwargs)
    
    def __setRequest__(self, *args, **kwargs):
        while True:
            try:
                return self.client.setRequest(Params = kwargs, ParamsType = 'JSON', command = 'INTERNAL')
            except ConnectionError:
                time.sleep(1)
    
    @staticmethod
    def __ParseResult__(Result: any):
        try:
            return True, Result if type(Result) == dict else json.loads(Result)
        except:
            return False, dict()
                
    def getBalance(self):
        Status, Result = self.__setRequest__(API_KEY =  self.API_KEY, request = 'getBalance')
        return self.__ParseResult__(Result)
    
    def createTask(self, *args, **kwargs):
        """A Internal Requests.
        
        Basic Usage::

            createTask(
                type = str || ex : RecaptchaV2TaskProxyless,
                websiteURL = str || ex : http://makeawebsitehub.com/recaptcha/test.php,
                websiteKey = str || ex : 6LfI9IsUAAAAAKuvopU0hfY8pWADfR_mogXokIIZ
            )
            
        params is Json/urlencode for POST/PUT or urlencode for GET
        """
        Status, Result = self.__setRequest__(**dict(API_KEY =  self.API_KEY, request = 'createTask', **kwargs))
        return self.__ParseResult__(Result)
    
    def getTaskResult(self, taskId: int):
        Status, Result = self.__setRequest__(API_KEY =  self.API_KEY, request = 'getTaskResult', taskId = taskId)
        return self.__ParseResult__(Result)
    
    def getQueueStats(self, queueId: int):
        Status, Result = self.__setRequest__(API_KEY =  self.API_KEY, request = 'getQueueStats', queueId = queueId)
        return self.__ParseResult__(Result)
    
    def reportIncorrectImageCaptcha(self, taskId: int):
        Status, Result = self.__setRequest__(API_KEY =  self.API_KEY, request = 'reportIncorrectImageCaptcha', taskId = taskId)
        return self.__ParseResult__(Result)
    
    def reportIncorrectRecaptcha(self, taskId: int):
        Status, Result = self.__setRequest__(API_KEY =  self.API_KEY, request = 'reportIncorrectRecaptcha', taskId = taskId)
        return self.__ParseResult__(Result)
    
    def reportCorrectRecaptcha(self, taskId: int):
        Status, Result = self.__setRequest__(API_KEY =  self.API_KEY, request = 'reportCorrectRecaptcha', taskId = taskId)
        return self.__ParseResult__(Result)
    
    def reportIncorrectHcaptcha(self, taskId: int):
        Status, Result = self.__setRequest__(API_KEY =  self.API_KEY, request = 'reportIncorrectHcaptcha', taskId = taskId)
        return self.__ParseResult__(Result)