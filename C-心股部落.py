#微信扫码小程序 ：https://youke1.picui.cn/s1/2025/08/20/68a53655060f7.jpg
#使用教程 首页→冯浩昱轻创→抓立即签到的包 https://fhywib.cn/query/checkin/records的表单openId→
#OPEN_IDS青龙环境变量 多帐号回车
import requests
from datetime import datetime
import time
import random
import os  # 用于读取环境变量

class User:
    def __init__(self, openid):
        self.url = 'https://fhywib.cn'
        self.header = {
            'Host': 'fhywib.cn',
            'Connection': 'keep-alive',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c32) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wxe5cde23a31cb0f3b/4/page-frame.html'
        }
        self.openid = openid
        self.unionid = ''

    def user_info(self):
        res = requests.get(f'{self.url}/user/info?openid={self.openid}', headers=self.header).json()
        if res['code'] != 0:
            print(f"🔛出错了，请检查")
        else:
            self.unionid = res['data']['users']['unionid']
            print(self.unionid)
            print(f"🎉️账号现有金币{res['data']['userAccount']}个")

    def checkin(self):
        payload = {
            "openId": self.openid,
            "checkinDate": datetime.now().strftime("%Y-%m")  # 动态获取当前年月
        }
        res = requests.post(f'{self.url}/query/checkin/records', headers=self.header, json=payload).json()
        if res['code'] != 0:
            print(f"🔛查询签到记录出错：{res.get('msg', '未知错误')}")
            return
        print(f"🎉️现有金币{res['data']['totalPoints']}个,已签到{res['data']['checkinNumber']}次")
        
        # 若签到次数不足4次，补签
        if res['data']['checkinNumber'] < 4:
            current_date = datetime.now().strftime("%Y-%m-%d")
            for _ in range(4 - res['data']['checkinNumber']):
                payload2 = {
                    "openId": self.openid,
                    "isRetro": 1,
                    "checkinDate": current_date,
                    "appId": "wx19c782057b961ed8"
                }
                res2 = requests.post(f'{self.url}/wechat/checkin/records', headers=self.header, json=payload2).json()
                if res2['code'] != 0:
                    print(f"🔛签到失败：{res2.get('msg', '未知错误')}")
                else:
                    print(f"🔛{res2['msg']},当前签到是第{res2['data']['checkinNumber']}次，获得金币{res2['data']['points']}")
                time.sleep(35)  # 每次签到间隔35秒

    def run(self):
        # self.user_info()  # 如需获取用户信息可取消注释
        self.checkin()


if __name__ == "__main__":
    # 从青龙面板环境变量读取OPEN_IDS，多账号用回车分隔
    open_ids = os.getenv("OPEN_IDS", "").split('\n')
    # 过滤空值（避免环境变量末尾有空行）
    open_ids = [uid.strip() for uid in open_ids if uid.strip()]
    
    if not open_ids:
        print("❌未获取到账号，请检查环境变量OPEN_IDS是否配置")
    else:
        print(f"获取到{len(open_ids)}个账号，开始执行签到...")
        for i, openid in enumerate(open_ids, 1):
            try:
                print(f"=========开始第{i}个账号=========")
                User(openid).run()
            except Exception as e:
                print(f"第{i}个账号执行出错：{str(e)}")
            if i < len(open_ids):
                print(f"=========等待30秒执行第{i+1}个账号=========")
                time.sleep(30)  # 账号间间隔30秒
        print("✅所有账号执行完毕")
