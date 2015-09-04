import base64
import datetime
import hashlib
import json
from random import choice
import string
import requests

__author__ = 'hason'


def get_start_end(req, number_per_page):
    """
    从请求里获取index转化成start和end
    :param req:
    :return:
    """
    index = req.GET.get("index", '1')
    try:
        index = int(index)
    except (ValueError, TypeError):
        index = 1
    start = (index - 1) * number_per_page
    end = start + number_per_page
    return start, end, index


def get_token(length=6, chars=string.digits):
    return ''.join([choice(chars) for _ in range(length)])


accountSid = '8a48b5514f73ea32014f86abc50f216d'
# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID。

accountToken = '99dba7ab907347cdb3f8291da70d78fb'
# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN。

appId = '8a48b5514f73ea32014f86ad28342177'
# 说明：应用Id，如果是在沙盒环境开发，请配置"控制台-应用-测试DEMO"中的APPID。
# 如切换到生产环境，请使用自己创建应用的APPID.

serverIP = 'https://sandboxapp.cloopen.com'
# 说明：请求地址。沙盒环境配置成sandboxapp.cloopen.com，生产环境配置成app.cloopen.com。

serverPort = '8883'
# 说明：请求端口 ，无论生产环境还是沙盒环境都为8883.

softVersion = '2013-12-26'  # 说明：REST API版本号保持不变。


class MsgSender:
    def __init__(self, server_ip, server_port, server_version, account_token, account_sid, app_id):
        self.app_id = app_id
        self.account_token = account_token
        self.account_sid = account_sid
        self.ServerIP = server_ip
        self.ServerPort = server_port
        self.SoftVersion = server_version

    def send_msg(self, to, datas, tempId):
        nowdate = datetime.datetime.now()
        batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.account_sid + self.account_token + batch
        sig = hashlib.md5(signature.encode()).hexdigest().upper()
        url = self.ServerIP + ":" + self.ServerPort + "/" + self.SoftVersion + "/Accounts/" \
              + self.account_sid \
              + "/SMS/TemplateSMS?sig=" + sig
        src = self.account_sid + ":" + batch
        auth = base64.encodebytes(src.encode()).strip().decode()
        headers = {'Authorization': auth,
                   'Content-Type': 'application/json;charset=utf-8;', "Accept": "application/json"}
        body = json.dumps({"to": to, "datas": datas, "templateId": tempId, "appId": self.app_id})
        rep = requests.post(url, data=body, headers=headers)
        result = rep.json()
        print(result)
        return result["statusCode"] == "000000"


def send_template_sms(to, datas):
    sender = MsgSender(serverIP, serverPort, softVersion, accountToken, accountSid, appId)
    return sender.send_msg(to, datas, "1")
