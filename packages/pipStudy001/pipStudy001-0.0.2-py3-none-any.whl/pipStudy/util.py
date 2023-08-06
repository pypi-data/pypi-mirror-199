import json
import requests


# 根据产品名称查询产品下的设备数
def quary_DeviceId_Underproduct(productName):
    url = "http://49.235.105.4:8500/mach/device/instance/_query"
    payload = json.dumps({
        "terms": [
            {
                "termType": "eq",
                "column": "product_id",
                "value": productName
            }
        ],
        "includes": [
            "id"
        ]
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': "49.235.105.4:8500",
        'Connection': 'keep-alive'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    device_list = []
    if response:
        json_dic = response.json()
        result = json_dic["result"]
        number = result["total"]

        for i in range(number):
            device_list.append(result["data"][i]["id"])
        print(device_list)
        print(response.text)
    return device_list
