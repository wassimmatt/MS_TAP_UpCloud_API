import json

from app import app
from Upcloud_API import Upcloud_API
from flask import request, jsonify

api = Upcloud_API()

sample_start_server = [
    {
        "plan": "2xCPU-4GB",
        "zone": "uk-lon1",
        "hostname": "jwm-jason",
        "os": "01000000-0000-4000-8000-000050010300",
        "size": 80
    },
    {
        "plan": "2xCPU-4GB",
        "zone": "uk-lon1",
        "hostname": "jwm-jason",
        "os": "01000000-0000-4000-8000-000050010300",
        "size": 80
    }
]


# 006a7b12-3e1b-45a2-9f71-0aa217cf67b4

@app.route('/server', methods=['POST'])
def create_server():
    json_data = request.get_json()
    print(json_data)
    server = json.loads(json_data)
    new_server = api.create_server(server['plan'], server['zone'], server['hostname'], server['os'], int(server['size']))
    new_server_dict = new_server.to_dict()
    return jsonify({
        "state": new_server_dict['state'],
        "hostname": new_server_dict['hostname'],
        "uuid": new_server_dict['uuid']
    })


@app.route('/server', methods=['GET'])
def get_all_server():
    details = api.server_list()
    return jsonify(details)


@app.route('/server/<uuid>', methods=['GET'])
def get_server_uuid(uuid):
    details = api.single_server(uuid)
    return jsonify(details)


@app.route('/server/hostname/<hostname>', methods=['GET'])
def get_server_hostname(hostname):
    details = api.server_list()
    for server in details:
        if server['hostname'] == hostname:
            return jsonify(server)


# TODO: Proper response
@app.route('/server/<uuid>', methods=['DELETE'])
def delete_server(uuid):
    api.rm_server(uuid)
    return "Successfully deleted server"
