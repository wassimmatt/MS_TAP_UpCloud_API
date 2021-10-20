import upcloud_api
from upcloud_api import Server, Storage, Tag, login_user_block
import paramiko
# from upcloud_api.storage import BackupDeletionPolicy
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime
import logs


# class Logs:
#     def __init__(self):
#         logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctimes:%(levelname)s:%(message)s')

class Upcloud_API:
    def __init__(self):
        self.mylogger = logs.Logs()
        self.manager = upcloud_api.CloudManager('tapaug2021ee', 'gr4D334uG2021')
        self.manager.authenticate()

        self.login_user = self.key_pair_login()
        self.planList = ["1xCPU-2GB", "1xCPU-1GB", "2xCPU-4GB", "4xCPU-8GB", "6xCPU-16GB", "8xCPU-32GB", "12xCPU-48GB",
                         "16xCPU-64GB", "20xCPU-96GB", "20xCPU-128G"]

    # login user
    def key_pair_login(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        # generate the public key
        public_key = private_key.public_key().public_bytes(serialization.Encoding.OpenSSH,
                                                           serialization.PublicFormat.OpenSSH)
        public_key = public_key.decode(encoding='UTF-8')
        # get private key in PEM container format
        pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                        encryption_algorithm=serialization.NoEncryption())
        login_user = login_user_block(
            username='root',
            ssh_keys=[public_key],
            create_password=False
        )
        self.mylogger.info_logger('A private_key.pem file is generated and stored for user: root.')
        with open('private_key.pem', 'wb') as f:
            f.write(pem)
        return login_user

    def get_zones(self):
        zones = self.manager.get_zones()['zones']['zone']
        zone_list = []
        for zone in zones:
            zone_list.append(zone['id'])
        return zone_list

    def get_templates(self):
        templates = self.manager.get_templates()
        return templates

    # new server creation
    def create_server(self, plan, zone, hostname, os, os_size):
        server = Server(
            plan=plan,
            hostname=hostname,
            zone=zone,  # All available zones with ids can be retrieved by using manager.get_zones()
            storage_devices=[
                Storage(os=os, size=os_size),
            ],
            login_user=self.login_user  # user and ssh-keys
        )
        server = self.manager.create_server(server)
        server_uuid = server.to_dict()['uuid']
        server_name = server.to_dict()['hostname']
        self.mylogger.info_logger(server_name + ' with uuid:' +server_uuid+' was created at' + str(datetime.now()))
        self.server_status(server)
        return server

    # get current server status
    def server_status(self, uuid):
        server_status = self.manager.get_server(uuid).to_dict()['state']
        server_name = self.manager.get_server(uuid).to_dict()['hostname']
        self.mylogger.info_logger('The status of Server:' + server_name + ':' + uuid+' is '+server_status + ' at '+str(datetime.now()))
        return "Current status of server: " + server_name + ":" + uuid + "  is " + server_status

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

    def access_console(self, uuid):
        try:
            server = self.manager.get_server(uuid).to_dict()
            ip_addr = server['ip_addresses']
            for ip in ip_addr:
                if ip['access'] == 'public' and ip['family'] == 'IPv4':
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip['address'], port=22, username='test_user', key_filename='.\private_key.pem')
                    command = 'uname -r '
                    stdin, stdout, stderr = ssh.exec_command(command)
                    lines = stdout.readlines()
                    print(lines)
                    break
        except Exception as e:
            raise e

    # check the performance of linux server
    def perform_statistic_linux(self, uuid):
        try:
            server = self.manager.get_server(uuid).to_dict()
            ip_addr = server['ip_addresses']
            perform_info = []
            for ip in ip_addr:
                if ip['access'] == 'public' and ip['family'] == 'IPv4':
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip['address'], port=22, username='root', key_filename='private_key.pem')
                    command = 'export TERM=xterm && top -n 1 -b'
                    # command = 'export TERM=xterm && mpstat'
                    stdin, stdout, stderr = ssh.exec_command(command)
                    lines = stdout.readlines()
                    err_lines = stderr.readlines()
                    break
            if err_lines:
                return err_lines
            else:
                return lines
        except Exception as e:
            raise e

    def server_stop(self,uuid):
        server = self.manager.get_server(uuid)
        if server.to_dict()['state'] != 'stopped':
            server.shutdown(hard=True)
        self.mylogger.info_logger('Server: '+ uuid + ' has been stopped.')

    # delete a vm based on the uuid
    def rm_server(self, uuid):
        try:
            self.manager.delete_server(uuid)
            self.mylogger.info_logger('Server' +uuid + ' has been deleted.')
            return "SUCCESS"
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    # log = Logs()
    ins = Upcloud_API()
    # login_user = ins.key_pair_login()
    # print(ins.server_list())
    # print(ins.get_zones())
    # print(ins.get_templates())
    # print(ins.single_server('00effc4b-47f5-4394-a357-0750c810b096'))
    # print(ins.access_console('00effc4b-47f5-4394-a357-0750c810b096'))
    # print(ins.server_list())
    print(ins.server_status('003f72ce-62b2-4f97-aba7-889b8bb483bf'))
    # print(ins.perform_statistic_linux('00e3d773-a32e-4cea-9653-1df3543710fa'))
    # print(ins.create_server("2xCPU-4GB","uk-lon1","maggie.win.com", "01000000-0000-4000-8000-000030200200", "10",login_user))
    # ins.rm_server("0021e1da-be14-4440-8de6-f04b0650926b")
# get server details
# print(self.manager.get_server("0021e1da-be14-4440-8de6-f04b0650926b").to_dict())
# get server states
# print(manager.get_server("0021e1da-be14-4440-8de6-f04b0650926b").to_dict()['state'])
# delete vms (stop first)
