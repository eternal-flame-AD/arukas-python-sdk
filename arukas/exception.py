class ArukasAPIException(Exception):
    def __init__(self, message):
        super().__init__("Arukas API Error: " + message + ".")


class ArukasAPIRemoteException(ArukasAPIException):
    def __init__(self, errresp):
        
        res = ""
        for error in errresp.res['errors']:
            code = errresp.code
            if "status" in error:
                code = error['status']
            elif "code" in error:
                code = error['code']
            info = ""
            if "detail" in error:
                info = error['detail']
            elif "title" in error:
                info = error['title']
            res += "{}: {}\n".format(code, info)
        
        super().__init__(res[:-1])


class ArukasAPILocalException(ArukasAPIException):
    def __init__(self, message):
        super().__init__(message)


class ArukasNetFailException(ArukasAPILocalException):
    def __init__(self, message):
        super().__init__("Failed to make a request: " + message)


class ArukasAPITypeError(ArukasAPILocalException):
    def __init__(self, message):
        super().__init__("TypeError: " + message)


class ArukasAPIParamCheckError(ArukasAPILocalException):
    def __init__(self, message):
        super().__init__("Param incorrect: " + message)


class ArukasAPINotAuthorizedException(ArukasAPIRemoteException):
    pass


class ArukasAPINotFoundException(ArukasAPIRemoteException):
    pass


class ArukasAPIParamError(ArukasAPIRemoteException):
    pass
