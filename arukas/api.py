from http.client import HTTPSConnection, HTTPException, HTTPResponse
from base64 import b64encode
import json

from .exception import *
from .service import *


class ArukasJsonReply():
    def __init__(self, resp: HTTPResponse):
        self.code = resp.code
        self.res = json.loads(resp.read())
        if self.code == 200:
            pass
        elif self.code == 401:
            raise ArukasAPINotAuthorizedException(self)
        elif self.code == 404:
            raise ArukasAPINotFoundException(self)
        elif self.code == 422:
            raise ArukasAPIParamError(self)
        else:
            raise ArukasAPIRemoteException(self)


class ArukasClient():
    '''Main Arukas API Wrapper

    Args:
        token (bytes/str):Arukas API token
        secret (bytes/str):Arukas API secret
        apihost="app.arukas.io":arukas api domain
        useragent="XMLHttpRequest":default user agent
        fail_retry=3:retries for HTTPException

    '''

    def __init__(self,
                 token,
                 secret,
                 apihost="app.arukas.io",
                 useragent="XMLHttpRequest",
                 fail_retry=3):
        self.host = apihost
        self.ua = useragent
        self.retry = fail_retry
        if type(token) == str:
            token = token.encode("utf-8")
        if type(secret) == str:
            secret = secret.encode("utf-8")
        self.authstr = "Basic " + b64encode(token + b":" + secret).decode(
            "ascii")
        self._init_conn()

    def _init_conn(self):
        self.conn = HTTPSConnection(self.host)

    def sendCustomData(self,
                       method,
                       uri,
                       data=None,
                       mime="application/json",
                       extraheader={}):
        if type(data) == str:
            data = data.encode("utf-8")
        elif type(data) == dict:
            data = json.dumps(data).encode("utf-8")
        elif type(data) == bytes:
            pass
        elif data == None:
            pass
        else:
            raise NotImplementedError("Unknown data type: {}".format(
                type(data)))

        for _ in range(self.retry):
            try:
                self.conn.request(
                    method,
                    uri,
                    body=data,
                    headers={
                        "Accept": "application/vnd.api+json",
                        "Content-Type": mime,
                        "User-Agent": self.ua,
                        "Authorization": self.authstr,
                        **extraheader,
                    })
                resp = self.conn.getresponse()
                break
            except HTTPException as e:
                error = e
                self._init_conn()

        if resp:
            return ArukasJsonReply(resp)
        else:
            raise ArukasNetFailException(str(error))

    def getAllApp(self):
        resp = self.sendCustomData("GET", "/api/apps")
        return [ArukasApp._fromapi(dat) for dat in resp.res['data']]

    def createApp(self, app: ArukasApp):
        self.sendCustomData("POST", "/api/apps", app._getdata())

    def getAppByID(self, appid):
        resp = self.sendCustomData("GET", "/api/apps/" + appid)
        return ArukasApp._fromapi(resp.res['data'])

    def delAppByID(self, appid):
        self.sendCustomData("DELETE", "/api/apps/" + appid)

    def getAllService(self):
        resp = self.sendCustomData("GET", "/api/services")
        return [ArukasService._fromapi(dat) for dat in resp.res['data']]

    def getServiceByID(self, id):
        self.sendCustomData("DELETE", "/api/services/" + id)

    def updateService(self, service: ArukasService):
        self.sendCustomData("PATCH", "/api/services/" + service.id,
                            service._getdata())

    def powerOnService(self, id):
        self.sendCustomData("POST", "/api/services/{}/power".format(id))

    def powerOffService(self, id):
        self.sendCustomData("DELETE", "/api/services/{}/power".format(id))
