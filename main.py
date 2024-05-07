from signIn import readUserConfig,writeUserConfig,getAppPHPSESSION,getCookie,userLogin,add_location
from Location import Location

if __name__ == "__main__":
    userConfig = readUserConfig('userConfig.json')

    # 打卡地点信息列表
    locations = [
        Location("IDC", 32.999749, 113.967228,"5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy66am.5Z!O5Yy65YiY6ZiB6KGX6YGT6auY5qW8"),
        Location("置地办公区",33.001344,113.98826,'5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy65reu5rKz5aSn6YGT6am.5Z!O5Yy6572u5Zywwrflm73pmYXlub.lnLoo5reu5rKz5aSn6YGT5YyXKQ::'),
        Location("市豫资办公区", 32.998817,114.016507,'5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy65paH5piO5aSn6YGT6am.5Z!O5Yy66am76ams5bqX6LSi5pS.5bGAKOmHkembgOi3r!WMlzUw57GzKQ::'),
        Location("大数据中心", 32.975491,114.020093,'KOmpu!mprOW6l!W4guaUv!WKoeacjeWKoeWSjOWkp!aVsOaNrueuoeeQhuWxgC3ljZfpl6go5rKz5Y2X55yB6am76ams5bqX5biC6am.5Z!O5Yy66Kej5pS!5aSn6YGTNTQ25Y!36ZmE6L!RKSk:')
    ]

    # 获取PHPSESSID
    if not userConfig['app']['PHPSESSID']:
        print("___获取PHPSESSID___\r\n")
        PHPSESSID_RESPONSE_HEADERS = getAppPHPSESSION(userConfig['url']['base'])
        PHPSESSID_COOKIE = PHPSESSID_RESPONSE_HEADERS['Set-Cookie'].split(';')
        for part in PHPSESSID_COOKIE:
            if "PHPSESSID" in part:
                userConfig['app']['PHPSESSID'] = part.strip()
                break
    
    # 用户登录
    if not userConfig['user']['token']:
        print("___用户登录___\r\n")
        LOGIN_RESULT = userLogin(userConfig['url']['base'],userConfig['app']['PHPSESSID'],userConfig['user']['username'],userConfig['user']['password'])
        LOGIN_COOKIE = LOGIN_RESULT[0]
        yzoa_mo_adminid = LOGIN_COOKIE.split(';')[0]
        LOGIN_RESPONE = LOGIN_RESULT[1]
        if(LOGIN_RESPONE['code'] == 200):
            userConfig['user']['token'] = LOGIN_RESPONE['data']['token']
        userConfig['app']['Cookie'] = userConfig['app']['PHPSESSID'] + ';' + yzoa_mo_adminid
    
    # 获取cookie
    COOKIE_RESPONSE_HEADER = getCookie(userConfig['app']['Cookie'],userConfig['user']['token'])
    # print('上次',userConfig['app']['Cookie'])
    if 'PHPSESSID' in  COOKIE_RESPONSE_HEADER['Set-Cookie']:
        userConfig['app']['PHPSESSID'] = COOKIE_RESPONSE_HEADER['Set-Cookie'].split(';')[0]
        userConfig['app']['Cookie'] = userConfig['app']['PHPSESSID'] + ';' + COOKIE_RESPONSE_HEADER['Set-Cookie'].split(';')[1].split(',')[1].strip()
    else:
        userConfig['app']['Cookie'] = userConfig['app']['PHPSESSID'] + ';' + COOKIE_RESPONSE_HEADER['Set-Cookie'].split(';')[0]
    # print('当前',userConfig['app']['Cookie'])

    # 打卡
    add_location_response = add_location(userConfig['url']['base'],userConfig['app']['Cookie'],userConfig['user']['token'],locations[3])

    if(add_location_response['success']):
        print(f"{userConfig['user']['username']} 于 {add_location_response['data']['now']} 在 {locations[3].name}  执行成功！😂")
    else:
        print(f"打卡失败，原因：{add_location_response['msg']}")
    
    # # 保存内容
    writeUserConfig('userConfig.json',userConfig)
    
# python3 ./autoSignIn.py --username chaizhiyang --address 4
    