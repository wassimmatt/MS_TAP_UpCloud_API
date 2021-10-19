import flask
# import flask_restplus
# import werkzeug

from flask import Flask
import http.client
import base64
import upcloud_api
from upcloud_api import Server, Storage, Tag, login_user_block

# from upcloud_api.storage import BackupDeletionPolicy

import paramiko
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class Upcloud_API:
    def __init__(self):
        self.manager = upcloud_api.CloudManager('tapaug2021ee', 'gr4D334uG2021')
        self.manager.authenticate()
        self.tag = Tag('JWM_TEAM')
        self.plan1 = "1xCPU-2GB"
        self.plan2 = "1xCPU-1GB"
        self.plan3 = "2xCPU-4GB"
        self.plan4 = "4xCPU-8GB"
        self.plan5 = "6xCPU-16GB"
        self.plan6 = "8xCPU-32GB"
        self.plan7 = "12xCPU-48GB"
        self.plan8 = "16xCPU-64GB"
        self.plan9 = "20xCPU-96GB"
        self.plan10 = "20xCPU-128G"

    # login user
    def key_pair_login(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        #generate the public key
        public_key = private_key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
        public_key = public_key.decode(encoding='UTF-8')
        # get private key in PEM container format
        pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.TraditionalOpenSSL,
                                encryption_algorithm=serialization.NoEncryption())
        login_user = login_user_block(
            username='test_user',
            ssh_keys=[public_key],
            create_password=False
        )
        with open('private_key.pem','wb') as f:
            f.write(pem)
        return login_user


    # def get_zones(self):
    #     zones = self.manager.get_zones()['zones']['zone']
    #     # print(zones)
    #     zone_list = []
    #     for zone in zones:
    #         zone_list.append(zone['id'])
    #     return zone_list


    def get_templates(self):
        templates = self.manager.get_templates()
        print(templates)
        # # template_list=[]
        # print(templates[0].keys())
        # i = 0
        # while i < len(templates):
        #     if os == templates[i].keys():
        #         return templates[i][os]
        #         break
        #     else:
        #         continue
        #     i += 1


    #new server creation
    def create_server(self, plan, zone, hostname, os, os_size, sec_stg_size,sec_stg_tier,login_user):
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
                Storage(size=sec_stg_size, tier=sec_stg_tier)
            ],
            login_user=login_user  # user and ssh-keys
        )
        self.manager.create_server(server)
        # server.add_tags([self.tag])
        return server

    #get all server list
    def server_list(self):
        servers = self.manager.get_servers()
        server_list=[]
        for server in servers:
            server_list.append(server.to_dict())
        return server_list

    #get one server details
    def single_server(self,uuid):
        server = self.manager.get_server(uuid).to_dict()
        return server

    def access_console(self,uuid):
        try:
            server = self.manager.get_server(uuid).to_dict()
            ip_addr = server['ip_addresses']
            for ip in ip_addr:
                if ip['access'] =='public' and ip['family'] == 'IPv4':
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip['address'],port=22,username='test_user',key_filename='.\private_key.pem')
                    command = 'uname -r '
                    stdin, stdout, stderr = ssh.exec_command(command)
                    lines = stdout.readlines()
                    print(lines)
                    break
        except Exception as e:
            raise e


    #delete a vm based on the uuid
    def rm_server(self,uuid):
        server = self.manager.get_server(uuid)
        if server.to_dict()["state"] != "stopped":
            server.shutdown(hard=True)
        while self.manager.get_server(uuid).to_dict()["state"] != "stopped":
            pass
        self.manager.delete_server(uuid)
        return "Selected server deleted."

if __name__ == '__main__':
    ins = Upcloud_API()
    # login_user=ins.logon_user()
    # login_user = ins.key_pair_login()
    # print(ins.server_list())
    # print(ins.single_server('00effc4b-47f5-4394-a357-0750c810b096'))
    print(ins.access_console('00effc4b-47f5-4394-a357-0750c810b096'))
    # print(ins.server_list())
    # ins.get_templates()
    # ins.create_server("2xCPU-4GB","uk-lon1","maggie.example.com", "01000000-0000-4000-8000-000020060100", "10", "100", "hdd", login_user)
    # new_server=ins.server("2xCPU-4GB","uk-lon1","web1.example.com",login_user)
    # ins.rm_server("0021e1da-be14-4440-8de6-f04b0650926b")

#get server details
# print(self.manager.get_server("0021e1da-be14-4440-8de6-f04b0650926b").to_dict())
#get server states
# print(manager.get_server("0021e1da-be14-4440-8de6-f04b0650926b").to_dict()['state'])
#delete vms (stop first)

#access the console of VM


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
