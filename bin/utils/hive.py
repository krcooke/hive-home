"""
Hive class

"""

import os
import requests
import logging
import json
from utils.config import get_hive_username, get_hive_password
logger = logging.getLogger('hive')

session_id = ""
node_id = ""
headers = {
        'Accept': 'application/vnd.alertme.zoo-6.4+json',
        'Content-Type': 'application/json',
        'X-Omnia-Client': 'Hive Web Dashboard'
    }

# Login
def login():
    #url = 'https://api.hivehome.com/v5/login'
    global headers
    global session_id
    global node_id
    username = get_hive_username()
    password = get_hive_password()
    #logger.debug("Username: %s", username)
    #logger.debug("Password: %s", password)
    url = 'https://api-prod.bgchprod.info:443/omnia/auth/sessions'
    payload = {
        'sessions': [
            {
                'username': username,
                'password': password,
                'caller': 'WEB'
            }
        ]
    }
    #logger.debug("Payload: %s", payload)
    headers.pop("X-Omnia-Access-Token", None)

    response = requests.post(url, data=json.dumps(payload), headers = headers)
    #logger.debug("Response: %s", response.text)
    json_response = response.json()
    session_id = json_response['sessions'][0]['sessionId']
    headers['X-Omnia-Access-Token'] = session_id
    node_id = _get_node_id()
    

# Get the node_id of the receiver
def _get_node_id():
    url = 'https://api-prod.bgchprod.info:443/omnia/nodes/'
    response = _issue_request(url, method = 'get')
    json_response = response.json()
    #logger.debug("Response: %s", response.text)
    nodes = json_response['nodes']
    logger.debug("Number of nodes: %s", len(nodes))
    node_id = ""
    for i in range(0, len(nodes)):
        node_id = json_response['nodes'][i]['id']
        if json_response['nodes'][i]['name'] == 'Your Receiver' and 'schedule' in json_response['nodes'][i]['attributes']:
            break
    logger.debug("Node_id: %s", node_id)
    return node_id

# Get the current mode
def get_mode():
    global node_id
    url = 'https://api-prod.bgchprod.info:443/omnia/nodes/' + node_id
    logger.debug("URL: %s", url)
    response = _issue_request(url, method = 'get')
    #logger.debug("Response: %s", response.text)
    json_response = response.json()
    activeHeatCoolMode = json_response['nodes'][0]['attributes']['activeHeatCoolMode']['targetValue']
    logger.debug("activeHeatCoolMode: %s", activeHeatCoolMode)
    return activeHeatCoolMode

# Sets the heating mode
def set_mode(mode):
    global node_id
    global headers
    global session_id
    activeScheduleLock = {
        "OFF": "true",
        "HEAT": "false"
    }
    logger.debug("Control: %s", mode)
    url = 'https://api-prod.bgchprod.info:443/omnia/nodes/' + node_id
    payload = {
        'nodes': [
            { 'attributes':
                {
                    "activeHeatCoolMode": {
                        "targetValue": mode,
                    },
                    "activeScheduleLock": {
                        "targetValue": activeScheduleLock[mode]
                    }
                }
            }
        ]
    }
    headers['X-Omnia-Access-Token'] = session_id
    response = _issue_request(url, method = 'put', data = json.dumps(payload))
    logger.debug("Response: %s", response.text)
    return response

# Logout
def logout():
    global headers
    global session_id
    url = 'https://api-prod.bgchprod.info:443/omnia/logout'
    headers['X-Omnia-Access-Token'] = session_id
    response = requests.put(url, headers = headers)
    json_response = response.json()

    #url = 'https://my.hivehome.com/logout'

def _issue_request(url, method, data = {}):
    global headers
    action = getattr(requests, method);
    response = action(url, headers = headers, data = data)
    #logger.debug("Issue_request Response: %s", response.text)
    json_response = response.json()
    if 'errors' in json_response and json_response['errors'][0]['code'] == 'NOT_AUTHORIZED':
        login()
        response = action(url, headers = headers, data = data)
    return response
    


