"""
name: 兴银理财
Author: MK集团本部
入口:兴银理财公众号关注后会推送入口。
环境变量xylc ck格式备注#Cookie 一次性0.3毛多号多撸
ck示列:备注#SESSION=MDE1NjQ4NjUtNzVlOS00NTJlLThkM2UtM2M2NWQ0ODFhM2Ji;
cron: 0 5 * * *
"""
#import notify
import requests, json, re, os, sys, time, random, datetime, execjs
response = requests.get("https://mkjt.jdmk.xyz/mkjt.txt")
response.encoding = 'utf-8'
txt = response.text
print(txt)
environ = "xylc"
name = "兴银༒理财"
session = requests.session()
#---------------------主代码区块---------------------

def run(Cookie):
    header = {"content-type":"application/x-www-form-urlencoded;charset=UTF-8","Host": "xy-monthly-sign-v2.weijuju.com", "Cookie": Cookie}
    try:
        res = session.post(url='https://xy-newcomer-gift.weijuju.com/app/receive',headers={"Host": "xy-newcomer-gift.weijuju.com", "Cookie": Cookie}, data="").json()
        print(res)
        if '成功' in res['msg']:
            print(f"🌥️新人：{res['data']['award']['awardName']}")
        elif '已' in res['msg']:
            print(f"🌥️新人：已领取")
        else:
            print(f"⭕新人：res['msg']")
            return
        msg = session.post(url='https://xy-monthly-sign-v2.weijuju.com/app/sign', headers=header, data="").json().get('msg')
        print(msg)
        if '成功' in msg:
            print(f"🌥️签到：成功")
        elif '已' in msg:
            print(f"🌥️签到：已签到")
        lotteryid = "signDayStr=P0SLmd8wExG3zIP9tezPcUnY5%2FeuBeewt0awm6y9FYxZ5JuP2Dyz2WY97djfZEhVxgYaIWG%2F4zco6indlHbMHcPPvBsgGuU59uaYJvOkKjec2nwCLobEqHEYv7a6QIKEiTlvPaWwtT7F2CsvAA09wLAWR5a6gejJZVPg7pRE3dk%3D"
        msg = session.post(url='https://xy-monthly-sign-v2.weijuju.com/app/lottery',headers=header,data=lotteryid).json().get('msg')
        print(msg)
        if '成功' in msg:
            print(f"🌥️抽奖1：成功")
        elif '已' in msg:
            print(f"🌥️抽奖1：已抽奖")
    except Exception as e:
        print(e)

def main():
    if os.environ.get(environ):
        ck = os.environ.get(environ)
    else:
        ck = ""
        if ck == "":
            print("请设置变量")
            sys.exit()
    ck_run = ck.split('\n')
    ck_run = [item for item in ck_run if item]
    print(f"{' ' * 10}꧁༺ {name} ༻꧂\n")
    for i, ck_run_n in enumerate(ck_run):
        print(f'\n----------- 🍺账号【{i + 1}/{len(ck_run)}】执行🍺 -----------')
        try:
            id,two = ck_run_n.split('#',2)
            id = id[:3] + "*****" + id[-3:]
            print(f"📱：{id}")
            run(two)
            time.sleep(random.randint(1, 2))
        except Exception as e:
            print(e)
            #notify.send('title', 'message')
    print(f'\n----------- 🎊 执 行  结 束 🎊 -----------')

if __name__ == '__main__':
    main()