import json
import base64
import requests

# 获取打卡用户配置：打卡开关、打卡地点
def get_config():
    url = "http://api.heclouds.com/devices/1133712873/datastreams/clown"
    payload={}
    headers = {
    'api-key': 'q8xOJuPNLebskj9DhHiuz1on1jY=',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Accept': '*/*',
    'Host': 'api.heclouds.com',
    'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    
    # 解析返回的JSON数据
    data = json.loads(response.text)
    config = data['data']['current_value']
    json_config = json.loads(config)
    return json_config

# 发送打卡成功信息
def send_message(message):
    token = '32252f4813174ec7a743f601adc1c827' #在pushplus网站中可以找到
    title= '数据天中考勤系统' #改成你要的标题内容
    url = 'http://www.pushplus.plus/send'
    data = {
        "token":token,
        "title":title,
        "content":message
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    requests.post(url,data=body,headers=headers)
