import flask
# import flask_restplus
# import werkzeug

from flask import Flask
import http.client
import base64
import upcloud_api
from upcloud_api import Server, Storage, Tag, login_user_block


# from upcloud_api.storage import BackupDeletionPolicy


class Upcloud_api:
    def __init__(self):
        self.manager = upcloud_api.CloudManager('tapaug2021ee', 'gr4D334uG2021')
        self.manager.authenticate()
        self.tag = Tag('JWM_TEAM')

    def logon_user(self):
        login_user = login_user_block(
            username='test_user',
            ssh_keys=['ssh-rsa AAAAB3NzaC1yc2EAAptshi44x user@some.host'],
            create_password=False
        )
        return login_user

    # describe all plan here (hard code)
    # def get_plan(self):
    # self.PlanClass = upcloud_api.listPlans()
    # PlanClass.

    # return storage_size, storage_tire

    def create_server(self, plan, zone, hostname, os, os_size):
        server = Server(
            plan=plan,
            hostname=hostname,
            zone=zone,  # All available zones with ids can be retrieved by using manager.get_zones()
            storage_devices=[
                # OS: template storage UUID, all available os templates can be retrieved by calling manager.get_templates()
                # Note: the storage os template uuid:s will change when OS is updated. So check that the UUID is correct
                # default tier: maxIOPS, the 100k IOPS storage backend
                Storage(os=os, size=os_size),
                # secondary storage, hdd for reduced speed & cost
                # Storage(size=100, tier='hdd')
            ],
            # login_user=login_user  # user and ssh-keys
        )
        self.manager.create_server(server)
        # server.add_tags([self.tag])
        return server

    # get all server list
    def server_list(self):
        servers = self.manager.get_servers()
        server_list = []
        for server in servers:
            server_list.append(server.to_dict())
        return server_list

    # get one server details
    def single_server(self, uuid):
        server = self.manager.get_server(uuid).to_dict()
        return server

    # delete a vm based on the uuid
    def rm_server(self, uuid):
        server = self.manager.get_server(uuid)
        if server.to_dict()["state"] != "stopped":
            server.shutdown(hard=True)
        while self.manager.get_server(uuid).to_dict()["state"] != "stopped":
            pass
        self.manager.delete_server(uuid)
        return "Selected server deleted."

# ins = Upcloud_api()
# login_user=ins.logon_user()
# new_server=ins.server("2xCPU-4GB","uk-lon1","web1.example.com",login_user)
# ins.rm_server("0021e1da-be14-4440-8de6-f04b0650926b")

# get server details
# print(self.manager.get_server("0021e1da-be14-4440-8de6-f04b0650926b").to_dict())
# get server states
# print(manager.get_server("0021e1da-be14-4440-8de6-f04b0650926b").to_dict()['state'])
# delete vms (stop first)

# access the console of VM


# @app.route('/')
# class BaseAPI:
#     api = "api.upcloud.com"
#     api_version = "1.3"
#     token = base64.b64encode("tapaug2021ee:gr4D334uG2021".encode())
#
#     def get(self, endpoint):
#         conn = http.client.HTTPSConnection(self.api)
#         url = "/" + self.api_version + endpoint
#         headers = {
#             "Authorization": "Basic " + self.token.decode(),
#             "Content-Type": "application/json"
#         }
#         conn.request("GET", url, None, headers)
#         res = conn.getresponse()
#         self.printresponse(res.read())
#
#     def printresponse(self, res):
#         data = res.decode(encoding="UTF-8")
#         print(data)


# class account(BaseAPI):
#     endpoint = "/account"
#
#     def do(self):
#         self.get(self.endpoint)
#
# class plans(BaseAPI):
#     endpoint="/plan"
#     def do(self):
#         self.get(self.endpoint)
# #
# # class server(BaseAPI):
# #     endpoint="/server"
# #
# #     def do(self):
# #         self.get(self.endpoint)
# #
# if __name__ == '__main__':
#     plans().do()
#     # app.run(host='0.0.0.0')
