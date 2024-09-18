import json

import requests
from user_login import user_login


def user_add(data: dict, headers: dict):
    return requests.post(
        url="https://test-erp-cn.p6sai.com/p6s/api/mgr/lite/v1/cloud/user-add",
        headers=headers,
        json=data
    )


if __name__ == "__main__":
    token = user_login("13638601129", "cx123456").json().get("data").get("token")
    headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json",
               "token": token}
    data = {"did": "IOTDDD-298852-BMMTC",
            "deviceModel": "T5AI/IPG-5950PCS-AI",
            "boardId": "0x20F1", "iccid": "",
            "versions": "2.2.0-20240911_message",
            "account": "13638601129",
            "region": "CN",
            "type": "AD",
            "details": "添加不了\n",
            "contact": "13638601129",
            "problemTime": 1726042080000,
            "pictureUrl": "{\"list\":[]}",
            "allow": 0,
            "lag": "zh_CN"}
    res = user_add(headers=headers, data=data)
    print(res.json())
