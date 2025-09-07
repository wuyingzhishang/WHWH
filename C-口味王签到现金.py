"""
export kww=""
CK可能一天过期有能力的自己对接CODE
活动限期的目前参加没问题
"""
#import notify
import requests,json,re,os,sys,time,random,datetime,threading,execjs,hashlib,base64,urllib3,certifi
retrycount = 1  #重试次数
environ = "kww"
name = "꧁༺ 口味༒签到 ༻꧂"
#---------------------主代码区块---------------------

def run(arg1,arg2, session):
    global id, messages
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090b13)XWEB/14315",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": f"{arg1};{arg2}",
        "priority": "u=1, i"
        }
    over = False
    for retry in range(int(retrycount)):
        try:
            for i in range(2):
                url = f'https://89420-1-activity.m.dexfu.cn/projectx/p16480c32/challenge/index.do?user_type=1&is_from_share=1'
                response = session.get(url=url, headers=header).json()
                #print(f"☁️{response}")
                completedSize = response['data']['taskInfoList'][0]['completedSize']  #0 未签到，1 签到
                if i == 0:
                    hasChallengeDay = response['data']['hasChallengeDay']   #签到天数
                else:
                    hasChallengeDay2 = response['data']['hasChallengeDay']   #签到天数
                url = f'https://89420-1-activity.m.dexfu.cn/projectx/p16480c32/main/sign.do?user_type=1&is_from_share=1'
                response = session.get(url=url, headers=header).json()
                if i == 1:
                    if "已签到" in response["message"]:
                        print(f"☁️签到状态：ok ~")
                    if hasChallengeDay == hasChallengeDay2:
                        print(f"☁️签到天数：{hasChallengeDay}/30天")
                    else:
                        print(f"☁️签到天数：({hasChallengeDay}→{hasChallengeDay2})/30天")
            
            break  #运行到此处表示正常，打断循环
        except Exception as e:
            if retry >= int(retrycount)-1:
                print(f"⭕模块：{e}")

def main():
    response = requests.get("https://mkxc.mkjt.xyz/mkjt.txt")
    response.encoding = 'utf-8'
    txt = response.text
    print(txt)
    global id, message
    messages = []
    if os.environ.get(environ):
        ck = os.environ.get(environ)
    else:
        ck = ""
        if ck == "":
            print("⭕请设置变量")
            sys.exit()
    ck_run = ck.split('\n')
    ck_run = [item for item in ck_run if item]
    print(f"{' ' * 7}{name}\n\n")
    print(f"-------- ☁️ 开 始  执 行 ☁️ --------")
    for i, ck_run_n in enumerate(ck_run):
        try:
            session = requests.session()
            mark,arg1,arg2 = ck_run_n.split('#',2)
            print(f"\n\n🌥️ 账号 [{i + 1}/{len(ck_run)}] ：")
            id = mark[:3] + "*****" + mark[-3:]
            print(f"☁️当前账号：{id}")
            run(arg1,arg2, session)
            time.sleep(random.randint(1, 3))
        except Exception as e:
            print(e)
    print(f"\n\n-------- ☁️ 执 行  结 束 ☁️ --------\n\n")
    if messages:
        output = '\n'.join(num for num in messages)
        notify.send(name, output)

if __name__ == '__main__':
    main()