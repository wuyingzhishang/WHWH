"""
name:小程序所有女生
Author: MK集团本部
Date: 2024-09-21
export syns="authorization"，必须电脑抓包
cron: 0 0,5 * * *
"""

import requests,os,sys,time,random
response = requests.get("https://mkjt.jdmk.xyz/mkjt.txt")
response.encoding = 'utf-8'
txt = response.text
print(txt)

def signin(auth):
    signin_url = "https://7.meionetech.com/api/operate/wx/record/signIn"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c0f)XWEB/11275',
        'content-type': 'application/json',
        'authorization': auth,
    }
    response = requests.post(signin_url, headers=headers)
    result = response.json()
    if result.get('code') == "000":
        print(f"☁️签到：成功")
    else:
        print(f"☁️签到：{result.get('message')}")

def viewcust(auth):
    signin_url = "https://7.wawo.cc/api/task/wx/ver2/task/done"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c0f)XWEB/11275',
        'content-type': 'application/json',
        'authorization': auth,
    }
    data = {"path":"/course-body/pages/memberHome2/memberHome2"}
    response = requests.post(signin_url, headers=headers, json=data)
    result = response.json()
    if result.get('code') == "000":
        print(f"☁️浏览：任务完成")
    else:
        print(f"☁️浏览：{result.get('message')}")

def score(auth):
    score_url = "https://7.meionetech.com/api/account/wx/member/assets"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c0f)XWEB/11275',
        'authorization': auth,
    }
    response = requests.get(score_url, headers=headers)
    result = response.json()
    if result.get('code') == "000":
        print(f"☁️积分：{result.get('data').get('score')}")
    else:
        print(f"☁️积分：{result.get('message')}")

def main():
    if os.environ.get("syns"):
        ck = os.environ.get("syns")
    else:
        ck = ""
        if ck == "":
            print("请设置变量")
            sys.exit()
    ck_run = ck.split('\n')
    print(f"{' ' * 10}꧁༺ 所有༒女生 ༻꧂\n")
    for i, ck_run_n in enumerate(ck_run, start=1):
        print(f'\n----------- 🍺账号【{i}/{len(ck_run)}】执行🍺 -----------')
        try:
            ck_run_num = ck_run_n.split('#')
            id= ck_run_num[0]
            id = id[:3] + "*****" + id[-3:]
            auth = ck_run_num[1]
            print(f"📱：{id}")
            signin(auth)
            viewcust(auth)
            time.sleep(5)
            score(auth)
            time.sleep(random.randint(1, 2))
        except Exception as e:
            print(e)
            #notify.send('title', 'message')

    print(f'\n----------- 🎊 执 行  结 束 🎊 -----------')

if __name__ == '__main__':
    main()