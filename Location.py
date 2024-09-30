import argparse
import json

class Location:
    def __init__(self, name, latitude, longitude, jmname):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.jmname = jmname

    @staticmethod
    def userInput():
        # 创建解析器对象
        parser = argparse.ArgumentParser(description='一个简单的命令行参数示例')

        # 添加命令行参数
        parser.add_argument('--username', default='liushuai', help='指定用户名')
        parser.add_argument('--password', default='sj@1396', help='指定密码，默认为 sj@1396')
        parser.add_argument('--address', default='1', help='指定打卡地址，默认值为IDC')

        # 解析命令行参数
        args = parser.parse_args()

        # 获取用户名和密码
        # if args.username == "":
        #     print("\r\n用户名不能为空，请重新运行程序")
        #     exit()

        return json.dumps({
            "username": args.username,
            "password": args.password,
            "address": args.address
        })

    @staticmethod
    def select_location(userSelect, locations):
        for i, loc in enumerate(locations):
            print(f"{i+1}. {loc.name}\r\n")
        print(f"当前选择打卡地址为 -->  {locations[userSelect-1].name}\r\n")

        return locations[userSelect-1]


