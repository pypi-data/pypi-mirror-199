server_url = 'http://localhost'
server_key = 'demo_key'
import json
import requests

def LOGIN(url=server_url, key=server_key):
    global server_key
    global server_url
    server_url = url
    server_key = key

def optimize(data, timelimit=60, parameters=""):
    try:
        req = {
            'timelimit': timelimit,
            'key': server_key,
            'parameters': parameters
        }
        req.update(data)
        solution = json.loads(
            requests.put(server_url, data=json.dumps(req), headers={"Content-Type": "application/json"}).text)
        return solution
    except Exception as err:
        return {"status": f'error: connecting to server {err}'}