from app import app
from main import Upcloud_api
from flask import request, jsonify

api = Upcloud_api()

sample_start_server = {
    "servers": [
        {
            "plan": "2xCPU-4GB",
            "zone": "uk-lon1",
            "hostname": "JWM_TEAM",
            "os": "01000000-0000-4000-8000-000030200200"
        }
    ]
}


# TODO: Parsing request body and proper response
@app.route('/server', methods=['POST'])
def create_server():
    json_data = request.get_json()
    login_user = api.logon_user()
    new_servers = []
    for server in json_data['servers']:
        server = api.create_server(server['plan'], server['zone'], server['hostname'], server['os'])
        new_servers.append(server.to_dict())
    return jsonify(new_servers)


# TODO: Proper response
@app.route('/server/<uuid>', methods=['GET'])
def get_server(uuid):
    details = api.get_server(uuid)
    return jsonify(details)


# TODO: Proper response
@app.route('/server/<uuid>', methods=['DELETE'])
def delete_server(uuid):
    api.rm_server(uuid)
    return "Success response"
