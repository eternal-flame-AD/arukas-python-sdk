from .exception import *


class ArukasService():
    '''Class representation of an Arukas service

    Args:
        None

    '''

    def __init__(self):
        self.__data = {
            "lid": "1",
            "type": "services",
            "attributes": {
                "command": "",
                "custom-domain": "",
                "image": None,
                "instances": "1",
                "ports": [],
                "environment": [],
                "subdomain": ""
            },
            "relationships": {
                "service-plan": {
                    "data": {
                        "type": "service-plans",
                        "id": "jp-tokyo/free",
                    },
                },
            },
        }

    def _checkparam(self):
        if not self.__data['attributes']['image']:
            raise ArukasAPIParamCheckError("Image name not set.")

    def _getdata(self):
        self._checkparam()
        return self.__data

    def setcmd(self, cmd: str):
        self.__data['attributes']['command'] = cmd

    def setCustomDomain(self, domain: str):
        self.__data['attributes']['custom-domain'] = domain

    def setImage(self, image: str):
        self.__data['attributes']['image'] = image

    def setInstanceCount(self, n: int):
        self.__data['attributes']['instances'] = n

    def setSubDomain(self, subdomain: str):
        self.__data['attributes']['subdomain'] = subdomain

    def setPlan(self, plan: str):
        plans_avail = [
            "jp-tokyo/free", "jp-tokyo/hobby", "jp-tokyo/standard-1",
            "jp-tokyo/standard-2"
        ]
        if plan not in plans_avail:
            raise ArukasAPIParamCheckError(
                "Plan must be either " + " or ".join(plans_avail))

    def addPortMap(self, port, protocol: str):
        self.__data['attributes']['ports'].append({
            "number": str(port),
            "protocol": protocol
        })

    def addENV(self, key: str, value: str):
        self.__data['attributes']['environment'].append({
            "key": key,
            "value": value
        })

    @classmethod
    def _fromapi(cls, apiresp):

        if apiresp['type'] != "services":
            raise ArukasAPITypeError(
                "Expected services Got " + apiresp['type'])

        self = cls()
        self._data = apiresp
        self.id = apiresp['id']
        self.appid = apiresp['relationships']['app']['data']['id']
        self.plan = apiresp['relationships']['service-plan']['data']['type'][
            'id']

        attr = apiresp['attributes']
        self.cmd = attr['command']
        self.image = attr['image']
        self.envireonment = attr['environment']
        self.instancecount = attr['instances']
        self.endpoint = attr['endpoint']
        self.customdomain = attr['custon-domain']
        self.ctime = attr['created-at']
        self.cpus = attr['cpus']
        self.last_fail_time = attr['last-instance-failed-at']
        self.last_fail_status = attr['last-instance-failed-status']
        self.memory = attr['memory']
        self.portmapping = attr['port-mappings']
        self.ports = attr['ports']
        self.status = attr['status']
        self.subdomain = attr['subdomain']
        self.updatetime = attr['updated-at']
        return self


class ArukasApp():
    '''Class representation of an Arukas app

    Args:
        name (str): name of the app
        service (arukas.ArukasService): the service bundled to this app

    '''

    def __init__(self, name: str, service: ArukasService):
        self.services = [service]
        self.__data = {
            "data": {
                "type": "apps",
                "attributes": {
                    "name": name,
                },
                "relationships": {
                    "service": {
                        "data": {
                            "lid": "1",
                            "type": "services",
                        },
                    },
                },
            },
            "included": [],
        }

    def _getdata(self):
        self.__data['included'] = [self.services[0]._getdata()]
        return self.__data

    @classmethod
    def _fromapi(cls, apiresp):

        if apiresp['type'] != "apps":
            raise ArukasAPITypeError("Expected apps Got " + apiresp['type'])

        self = cls("", None)
        self._data = apiresp
        self.appid = apiresp['id']
        self.name = apiresp['attributes']['name']
        self.ctime = apiresp['attributes']['created-at']
        self.updatetime = apiresp['attributes']['updated-at']
        self.services = [
            i['id'] for i in apiresp['relationships']['services']['data']
        ]
        self.userid = apiresp['relationships']['user']['data']['id']
        return self
