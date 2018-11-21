import requests

class KongApi:
    __server_addr = {}

    def __init__(self, server_addr):
        self.__server_addr = server_addr

    def clear_all(self):
        resp = requests.get(self.__server_addr + "/routes/").json()
        for route in resp["data"]:
            self.delete_route(route['id'])

        resp = requests.get(self.__server_addr + "/services/").json()
        for srv in resp["data"]:
            self.delete_service(srv['id'])
        
        resp = requests.get(self.__server_addr + "/plugins/").json()
        for pl in resp["data"]:
            self.delete_plugin(pl['id'])

        resp = requests.get(self.__server_addr + "/consumers/").json()
        for cs in resp["data"]:
            self.delete_consumer(cs['id'])

    def add_service(self, service):
        resp = requests.post(self.__server_addr + "/services/", service)
        s = resp.json()
        return s["id"]

    def add_route(self, route):
        resp = requests.post(self.__server_addr + "/routes/", route)
        s = resp.json()
        return s["id"]

    def add_plugin(self, plugin):
        resp = requests.post(self.__server_addr + "/plugins/", plugin)
        s = resp.json()
        if "already " in s["name"]:
            return ""

        return s["id"]
    
    def add_consumer(self, consumer, credential):
        resp = requests.post(self.__server_addr + "/consumers/", consumer)
        s = resp.json()
        cr_addr = self.__server_addr + "/consumers/" + consumer["username"] + "/" + credential["type"]
        del credential["type"]
        resp = requests.post(cr_addr, credential)
        s = resp.json()

        return s["id"]

    def delete_service(self, key):
        resp = requests.get(self.__server_addr + "/services/" + key + "/routes")
        if resp.status_code != 404:
            for route in resp.json()["data"]:
                self.delete_route(route["id"])
          
        resp = requests.delete(self.__server_addr + "/services/" + key)
        return resp.status_code

    def delete_route(self, key):
        resp = requests.delete(self.__server_addr + "/routes/" + key)
        return resp.status_code

    def delete_plugin(self, key):
        resp = requests.delete(self.__server_addr + "/plugins/" + key)
        return resp.status_code

    def delete_consumer(self, key):
        resp = requests.delete(self.__server_addr + "/consumers/" + key)
        return resp.status_code