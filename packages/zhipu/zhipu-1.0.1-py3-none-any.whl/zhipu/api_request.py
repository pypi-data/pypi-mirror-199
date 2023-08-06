# -*- coding:utf-8 -*-
import json
import time
from zhipu.base_request import sendPost, sendGet, postStream
from zhipu.utils.rsa_util import rsa_encode
from zhipu.utils.sse_util import SSEClient

BASE_URL = "https://maas.aminer.cn/api/paas"

ENGINES_PATH = "/model/v1/open/engines/"

ENGINES_PATH_V2 = "/model/v2/open/engines/"

TOKEN_PATH = "/passApiToken/createApiToken"

QUERY_ORDER_RESULT = "/request-task/query-request-task-result"


def getToken(api_key, public_key):
    content = str(int(round(time.time() * 1000)))
    crypto = rsa_encode(content.encode("utf-8"), public_key)
    params = {"apiKey": api_key,
              "encrypted": crypto
              }
    data = sendPost(BASE_URL + TOKEN_PATH, params)
    data = json.loads(data)
    return data


def chat(ability_type, engine_type, auth_token, params):
    req_engine_api_url = BASE_URL + "/model/v1/open/" + ability_type + "/" + engine_type
    data = sendPost(req_engine_api_url, params, auth_token)
    data = json.loads(data)
    return data


def chatRoleCreate(auth_token, params):
    req_engine_api_url = BASE_URL + "/model/v1/open/chat/role-create"
    data = sendPost(req_engine_api_url, params, auth_token)
    data = json.loads(data)
    return data


def executeEngine(ability_type, engine_type, auth_token, params, timeout=3600):
    req_engine_api_url = BASE_URL + ENGINES_PATH + ability_type + "/" + engine_type
    data = sendPost(req_engine_api_url, params, auth_token, timeout)
    data = json.loads(data)
    return data


def executeEngineV2(ability_type, engine_type, auth_token, params, timeout=36000):
    req_engine_api_url = BASE_URL + ENGINES_PATH_V2 + ability_type + "/" + engine_type
    data = sendPost(req_engine_api_url, params, auth_token, timeout)
    data = json.loads(data)
    return data


def executeSSE(ability_type, engine_type, auth_token, params):
    req_engine_api_url = BASE_URL + ENGINES_PATH + "sse/" + ability_type + "/" + engine_type
    response = postStream(req_engine_api_url, auth_token, params)
    return SSEClient(response)


def executeRiskSSE(ability_type, engine_type, auth_token, params):
    req_engine_api_url = BASE_URL + ENGINES_PATH + "sse/risk/" + ability_type + "/" + engine_type
    response = postStream(req_engine_api_url, auth_token, params)
    return SSEClient(response)


def queryTaskResult(auth_token, taskOrderNo):
    api_url = BASE_URL + QUERY_ORDER_RESULT + "/" + taskOrderNo
    task_data = sendGet(api_url, auth_token)
    data = json.loads(task_data)
    return data
