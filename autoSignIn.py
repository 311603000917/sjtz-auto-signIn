import requests
from sendwx import send
import base64
import argparse
import json

class Location:
    def __init__(self, name, latitude, longitude,jmname):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.jmname = jmname

# 定义打卡地点数组
locations = [
    Location("IDC", 32.999749, 113.967228,"5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy66am.5Z!O5Yy65YiY6ZiB6KGX6YGT6auY5qW8"),
    Location("置地办公区",33.001344,113.98826,'5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy65reu5rKz5aSn6YGT6am.5Z!O5Yy6572u5Zywwrflm73pmYXlub.lnLoo5reu5rKz5aSn6YGT5YyXKQ::'),
    Location("市豫资办公区", 32.998817,114.016507,'5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy65paH5piO5aSn6YGT6am.5Z!O5Yy66am76ams5bqX6LSi5pS.5bGAKOmHkembgOi3r!WMlzUw57GzKQ::'),
    Location("大数据中心", 32.975491,114.020093,'KOmpu!mprOW6l!W4guaUv!WKoeacjeWKoeWSjOWkp!aVsOaNrueuoeeQhuWxgC3ljZfpl6go5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy66Kej5pS!5aSn6YGTNTQ25Y!36ZmE6L!RKSk:')
]

def main():
    # 创建解析器对象
    parser = argparse.ArgumentParser(description='一个简单的命令行参数示例')

    # 添加命令行参数
    parser.add_argument('--username', default='', help='指定用户名')
    parser.add_argument('--password', default='sj@1396', help='指定密码，默认为 sj@1396')
    parser.add_argument('--address', default='1', help='指定打卡地址，默认值为IDC')

    # 解析命令行参数
    args = parser.parse_args()

    # 获取用户名和密码
    if args.username == "":
        print("\r\n用户名不能为空，请重新运行程序")
        exit()

    return json.dumps({
        "username": args.username,
        "password": args.password,
        "address": args.address
    })

def login(username, password):
    url = "http://218.29.229.34:9001/api.php?a=check&m=login&cfrom=nppandroid"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip',
        'Charset': 'UTF-8',
        'Connection': 'Keep-Alive',
        'Host': '218.29.229.34:9001',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        "cfrom": "nppandroid",
        "device": "f6139b7dee",
        "ltype": 0,
        "pass": base64.b64encode(password.encode("utf-8")).decode("utf-8"),
        "token": "",
        "user": base64.b64encode(username.encode("utf-8")).decode("utf-8"),
        "web": "v1913avivo",
        "yanzm": ""
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # 如果请求不成功，会抛出异常
        return [response.headers['Set-Cookie'], response.json()]
    except requests.exceptions.RequestException as e:
        print("登录失败：", e)

def add_location(token, location,PHPSESSID):
    url = f"http://218.29.229.34:9001/api.php?m=weixin&a=addlocation&addminid=141&device=1693480732947&cfrom=mweb&token={token}"
    payload = f'fileid=&ispz=&label={location.jmname}&location_x={location.latitude}&location_y={location.longitude}&precision=200&scale=12&sm=&type=1'
    # payload=f'fileid=&ispz=&label=5aaC5a625ZWG5peF6YWS5bqXKOmpu!mprOW6l!mrmOmTgeilv!ermeW6lyko5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy65reu5rKz5aSn6YGT5LiO6YeR6aG25bGx6Lev5Lqk5Y!J5Y!j5ZCM5L!h57yk57q35LmL56qX5YyX5Yy6MeWPt!alvCjlhpzllYbpk7booYzlkI7mlrkpKSjnsr7noa4yMDDnsbMp&location_x={location.latitude}&location_y={location.longitude}&precision=200&scale=12&sm=&type=1'

    headers = {
        'Accept': 'application/json, text/javascript, */*',
        'Host': '218.29.229.34:9001',
        'Origin': 'http://218.29.229.34:9001',
        'Referer': f'http://218.29.229.34:9001/?d=we&m=ying&a=daka&yingnum=kqdaka&adminid=141&token={token}&openfrom=nppandroid&cenghei=25&hideheader=true&opentype=nei&apiwinname=newpage1693634547170_7873',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': PHPSESSID,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # 如果请求不成功，会抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        print("打卡失败：", e)

def select_location(userSelect,locations):
    for i, loc in enumerate(locations):
        print(f"{i+1}. {loc.name}\r\n")
    print(f"当前选择打卡地址为 -->  {locations[userSelect-1].name}\r\n")

    return locations[userSelect-1]


if __name__ == "__main__":
    userInput = json.loads(main())
    # 用户选择打卡地点
    selected_location = select_location(int(userInput["address"]),locations)

    login_response = login(userInput["username"], userInput["password"])
    # 使用 split() 函数分割字符串
    parts = login_response[0].split(";")
    PHPSESSID = ""
    # 遍历每个部分，找到包含 PHPSESSID 的部分
    for part in parts:
        if "PHPSESSID" in part:
            PHPSESSID = part.strip()
            break

    if  login_response[1]["code"] == 200:
        token = login_response[1]['data']['token']
        
        # 打卡请求
        add_location_response = add_location(token, selected_location,PHPSESSID)
        if(add_location_response['success']):
            send(f"{login_response[1]['data']['name']} 于 {add_location_response['data']['now']} 在 {selected_location.name}  执行成功！😂")
        else:
            send(f"打卡失败，原因：{add_location_response['msg']}")
    else:
        send(f"打卡失败，原因：{login_response[1]['msg']}")

