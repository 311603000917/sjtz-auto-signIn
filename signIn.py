import json
import base64
import requests
# 获取用户信息
def readUserConfig(fileName):
    with open('userConfig.json', 'r') as file:
        userConfigData = json.load(file)
    return userConfigData

def writeUserConfig(fileName,content):
    with open(fileName, "w") as file:
        file.write(str(json.dumps(content)))
        file.close()
        
# 获取app会话窗口
def getAppPHPSESSION(url):
    endUrl = f"{url}?a=appupdate&m=login&ver=0.0.2&btype=new"
    headers = {
        'Accept': '*/*',
        'Host': '218.29.229.34:9001',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers)
    return response.headers

# 用户登录
def userLogin(url,PHPSESSID,username, password):
    url = f"{url}?a=check&m=login&cfrom=nppandroid"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip',
        'Charset': 'UTF-8',
        'Connection': 'Keep-Alive',
        'Host': '218.29.229.34:9001',
        'Cookie':PHPSESSID,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    #  payload = {
    #     "cfrom": "nppandroid",
    #     "device": "f6139b7dee",
    #     "ltype": 0,
    #     "pass": base64.b64encode(password.encode("utf-8")).decode("utf-8"),
    #     "token": "",
    #     "user": base64.b64encode(username.encode("utf-8")).decode("utf-8"),
    #     "web": "v1913avivo",
    #     "yanzm": ""
    # }

    
    payload = {
        "cfrom": "豫资OA",
        "device": "860166074509785",
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

# 获取最新的Cookie
def getCookie(cookie,token):
    url = f"http://218.29.229.34:9001/?d=we&m=ying&a=daka&yingnum=kqdaka&adminid=102&token={token}&openfrom=nppandroid&hideheader=true&opentype=nei&apiwinname=newpage1715053096015_5758"
    print('getCookie',url)
    headers = {
        'Accept': '*/*',
        'Host': '218.29.229.34:9001',
        'Connection': 'keep-alive',
        'Cookie':cookie
    }
    response = requests.request("GET", url, headers=headers)
    return response.headers

# 打卡
def add_location(url,Cookie,token, location):
    url = f"{url}?m=weixin&a=addlocation&addminid=102&device=1693480732947&cfrom=mweb&token={token}"
    payload = f'fileid=&ispz=&label={location.jmname}&location_x={location.latitude}&location_y={location.longitude}&precision=200&scale=12&sm=&type=1'
    # payload=f'fileid=&ispz=&label=5aaC5a625ZWG5peF6YWS5bqXKOmpu!mprOW6l!mrmOmTgeilv!ermeW6lyko5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy65reu5rKz5aSn6YGT5LiO6YeR6aG25bGx6Lev5Lqk5Y!J5Y!j5ZCM5L!h57yk57q35LmL56qX5YyX5Yy6MeWPt!alvCjlhpzllYbpk7booYzlkI7mlrkpKSjnsr7noa4yMDDnsbMp&location_x={location.latitude}&location_y={location.longitude}&precision=200&scale=12&sm=&type=1'

    headers = {
        'Accept': 'application/json, text/javascript, */*',
        'Host': '218.29.229.34:9001',
        'Origin': 'http://218.29.229.34:9001',
        'Referer': f'http://218.29.229.34:9001/?d=we&m=ying&a=daka&yingnum=kqdaka&adminid=141&token={token}&openfrom=nppandroid&cenghei=25&hideheader=true&opentype=nei&apiwinname=newpage1693634547170_7873',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': Cookie,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # 如果请求不成功，会抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        print("打卡失败：", e)
