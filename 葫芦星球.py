"""
现金收益参考:每月30-40元单号
1.先浏览器访问下载APP地址http://f.youlianghuyu.com/r?p=lGpp
2.然后打开抓包软件抓登陆包http://app.huluxingqiu.com/user/loginByWx域名响应体里面#appeky #http://app.huluxingqiu.com域名下请求体data全部值就是CK。
3.必须过新人任务绑定支付宝绑定微信然后首页支付宝秒那个也得绑定和解锁底部红包微信任务否则无法获得高收益。
提交CK格式示列:备注#appkey#acc_sign=92f4dbd9d47a3d762b2bd28b4bdc8e90&androidId=ddda820a1934afc6&androidosv=35&baseband=Q_V1_P14%2CQ_V1_P14&channelId=official&deviceId=&deviceModel=PJE110%2C15%2C35&mac_address=02%3A00%3A00%3A00%3A00%3A00&networkType=1&oaid=948EE79BF0C14B80AAE289ECDF0416BCcb88afbd243bd42e670c3ba7c8a4c234&pacHlz=com.zhangy.huluz&pageType=api&phoneType=1&req=taskSign%2Fticket&rnd=1733764941233&sign=82b5d2eba2c633320b0c9a6d43e5ab6a&timeStamp=1733764941233&userAgent=Mozilla%2F5.0+%28Linux%3B+Android+15%3B+PJE110+Build%2FTP1A.220905.001%3B+wv%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Version%2F4.0+Chrome%2F130.0.6723.86+Mobile+Safari%2F537.36&userId=7994165&utdId=ZyS2NV4DWxkDAJl5HYtVpSJZ&version=data的全部值
环境变量 hlxq="备注#appeky#data"  #appeky在登陆包http://app.huluxingqiu.com/user/loginByWx，data任意http://app.huluxingqiu.com域名下请求体
"""

import requests, json, re, os, sys, time, random, datetime, hashlib
from urllib.parse import unquote
environ = "hlxq"
name = "葫芦༒星球"
session = requests.session()
#---------------------主代码区块---------------------

def run(two,three):
    url_zfb = 'http://app.huluxingqiu.com/user/userWatchVideoAndAlipayCash'
    url_info = 'http://app.huluxingqiu.com/user/get'
    url_account_get = 'http://app.huluxingqiu.com/account/get'
    url_account_day = 'http://app.huluxingqiu.com/account/TodayAndAll'
    url_today = "http://app.huluxingqiu.com/redPackage/receiveUptask"
    url_receive = "http://app.huluxingqiu.com/redPackage/receiveRedPackage"
    url_open = "http://app.huluxingqiu.com/redPackage/openRedPackage"
    url_unLock = "http://app.huluxingqiu.com/redPackage/unLockRedPackage"
    url_reward = "http://app.huluxingqiu.com/task/rewardTodayTask"
    userId,body_zfb,body_receive,body_open,body_unLock,body_today1,body_today3,body_reward = enc(two,three)
    coin = 0
    try:
        response_info = session.post(url=url_info, headers=header, data=body_zfb).json()
        response_account_get = session.post(url=url_account_get, headers=header, data=body_zfb).json()
        response_account_day = session.post(url=url_account_day, headers=header, data=body_zfb).json()
        print("------- 信 息 -------")
        print(f"🌥️当前可提：{(response_account_get['data']['hulubi']+response_account_get['data']['hulubi_send']):.2f}元")
        if response_info['code'] == 200:
            #if response_info['data']['recomUserId'] == 7967069 or response_info['data']['recomUserId'] == 7988714 or int(userId) in white:
            if 'recomUserId' in response_info['data']:
                del response_info['data']['recomUserId']
                print("------- 支付宝 -------")
                for i in range(100):
                    response = session.post(url=url_zfb, headers=header, data=body_zfb).json()
                    if response['code'] == 200:
                        data = float(response['data'])
                        print(f"☁️红包获取：{data}元")
                        coin = coin + data
                        time.sleep(10)
                    elif "抢完" in response['msg']:
                        if coin != 0:
                            print(f"🌈红包合计：{coin:.2f}元")
                        else:
                            print(f"🌥️获取红包：完成")
                        break
                    elif "人太多" in response['msg']:
                        time.sleep(60)
                    else:
                        print(f'⭕{response["msg"]}')
                        break
                print("------- 微 信 -------")
                response_unLock = session.post(url=url_unLock, headers=header, data=body_unLock).json()
                if response_unLock['code'] == 200:
                    print(f"🌥️解锁：成功")
                    response_receive = session.post(url=url_receive, headers=header, data=body_receive).json()
                    if "提现成功" in response_receive.get('data',{}).get('message',""):
                        print(f"🌈提现：{response_receive['data']['receiveMoney']}元")
                    else:
                        pass
                    response_open = session.post(url=url_open, headers=header, data=body_open).json()
                    #print("------- 提 升 -------")
                    for i in range(100):
                        response_today1 = session.post(url=url_today, headers=header, data=body_today1).json()
                        if response_today1['code'] == 200:
                            data = float(response_today1['data']['upMoney'])
                            #print(f"☁️日常提升：{data}元")
                        elif "任务状态有误, 无法领取" in response_today1['msg']:
                            time.sleep(20)
                            pass
                        elif "不能重复领取哦" in response_today1['msg']:
                            #print(f"🌥️日常提升：完成")
                            break
                    for i in range(100):
                        response_today3 = session.post(url=url_today, headers=header, data=body_today3).json()
                        if response_today3['code'] == 200:
                            data = float(response_today3['data']['upMoney'])
                            #print(f"☁️视频提升：{data}元")
                            if i == 4:
                                print(f"🌈微信：红包提升{float(response_today3['data']['receiveMoney'])}元")
                        elif "任务状态有误, 无法领取" in response_today3['msg']:
                            #print(f"🌥️视频提升：完成")
                            break
                print(f"🌥️获取红包：完成")
            else:
                random_number = random.randint(1, 2)
                print("------- 提 示 -------")
                if random_number == 1:
                    print(f"⭕你的邀请人ID：{response_info['data']['recomUserId']}\n⭕不好意思，你无法使用此脚本\n⭕请使用以下链接注册后运行脚本\n☘️ http://f.youlianghuyu.com/r?p=lGpp ☘️")
                else:
                    print(f"⭕你的邀请人ID：{response_info['data']['recomUserId']}\n⭕不好意思，你无法使用此脚本\n⭕请使用以下链接注册后运行脚本\n☘️ http://l.qiantwx.com/r?p=lGpp ☘️")
        else:
            print(f"⭕异常：CK异常")
        response_info = session.post(url=url_info, headers=header, data=body_zfb).json()
        response_account_get = session.post(url=url_account_get, headers=header, data=body_zfb).json()
        response_account_day = session.post(url=url_account_day, headers=header, data=body_zfb).json()
        print("------- 信 息 -------")
        print(f"🌥️今日收入：{response_account_day['data']['todayIncome']}元")
        print(f"🌥️当前可提：{(response_account_get['data']['hulubi']+response_account_get['data']['hulubi_send']):.2f}元")
        print(f"🌥️累计收入：{response_account_day['data']['allIncome']}元")
    except Exception as e:
        print(e)

def enc(two,three):
    timeclient = int(time.time()*1000)
    params = three.split('&')
    params_dict = {}
    for param in params:
        key, value = param.split('=')
        params_dict[key] = value
    try:
        userId = params_dict['userId']
        req = unquote(params_dict['req'])
        req_zfb = "dialogRedEnvelop/getDialogRedEnvelopCashCard"
        req_today = "redPackage/receiveUptask"
        req_receive = "redPackage/receiveRedPackage"
        req_open = "redPackage/openRedPackage"
        req_unLock = "redPackage/unLockRedPackage"
        req_reward = "task/rewardTodayTask"
        utdId = unquote(params_dict['utdId'])
        md5_zfb = hashlib.md5(f"{two}{timeclient}{req_zfb}{utdId}".encode('utf-8')).hexdigest()
        md5_today = hashlib.md5(f"{two}{timeclient}{req_today}{utdId}".encode('utf-8')).hexdigest()
        md5_receive = hashlib.md5(f"{two}{timeclient}{req_receive}{utdId}".encode('utf-8')).hexdigest()
        md5_open = hashlib.md5(f"{two}{timeclient}{req_open}{utdId}".encode('utf-8')).hexdigest()
        md5_unLock = hashlib.md5(f"{two}{timeclient}{req_unLock}{utdId}".encode('utf-8')).hexdigest()
        md5_reward = hashlib.md5(f"{two}{timeclient}{req_reward}{utdId}".encode('utf-8')).hexdigest()
        params_dict["rnd"] = timeclient+2
        params_dict["timeStamp"] = timeclient
        body_zfb = f"acc_sign={params_dict['acc_sign']}&androidId={params_dict['androidId']}&androidosv={params_dict['androidosv']}&baseband={params_dict['baseband']}&channelId={params_dict['channelId']}&deviceId={params_dict['deviceId']}&deviceModel={params_dict['deviceModel']}&mac_address={params_dict['mac_address']}&networkType={params_dict['networkType']}&oaid={params_dict['oaid']}&pacHlz={params_dict['pacHlz']}&pageType={params_dict['pageType']}&phoneType={params_dict['phoneType']}&req={req_zfb}&rnd={params_dict['rnd']}&sign={md5_zfb}&timeStamp={params_dict['timeStamp']}&userAgent={params_dict['userAgent']}&userId={params_dict['userId']}&utdId={params_dict['utdId']}&version={params_dict['version']}"
        body_receive = f"acc_sign={params_dict['acc_sign']}&androidId={params_dict['androidId']}&androidosv={params_dict['androidosv']}&baseband={params_dict['baseband']}&channelId={params_dict['channelId']}&deviceId={params_dict['deviceId']}&deviceModel={params_dict['deviceModel']}&mac_address={params_dict['mac_address']}&networkType={params_dict['networkType']}&oaid={params_dict['oaid']}&pacHlz={params_dict['pacHlz']}&pageType={params_dict['pageType']}&phoneType={params_dict['phoneType']}&req={req_receive}&rnd={params_dict['rnd']}&sign={md5_receive}&timeStamp={params_dict['timeStamp']}&userAgent={params_dict['userAgent']}&userId={params_dict['userId']}&utdId={params_dict['utdId']}&version={params_dict['version']}"
        body_open = f"acc_sign={params_dict['acc_sign']}&androidId={params_dict['androidId']}&androidosv={params_dict['androidosv']}&baseband={params_dict['baseband']}&channelId={params_dict['channelId']}&deviceId={params_dict['deviceId']}&deviceModel={params_dict['deviceModel']}&mac_address={params_dict['mac_address']}&networkType={params_dict['networkType']}&oaid={params_dict['oaid']}&pacHlz={params_dict['pacHlz']}&pageType={params_dict['pageType']}&phoneType={params_dict['phoneType']}&req={req_open}&rnd={params_dict['rnd']}&sign={md5_open}&timeStamp={params_dict['timeStamp']}&userAgent={params_dict['userAgent']}&userId={params_dict['userId']}&utdId={params_dict['utdId']}&version={params_dict['version']}"
        body_unLock = f"acc_sign={params_dict['acc_sign']}&androidId={params_dict['androidId']}&androidosv={params_dict['androidosv']}&baseband={params_dict['baseband']}&channelId={params_dict['channelId']}&deviceId={params_dict['deviceId']}&deviceModel={params_dict['deviceModel']}&mac_address={params_dict['mac_address']}&networkType={params_dict['networkType']}&oaid={params_dict['oaid']}&pacHlz={params_dict['pacHlz']}&pageType={params_dict['pageType']}&phoneType={params_dict['phoneType']}&req={req_unLock}&rnd={params_dict['rnd']}&sign={md5_unLock}&timeStamp={params_dict['timeStamp']}&userAgent={params_dict['userAgent']}&userId={params_dict['userId']}&utdId={params_dict['utdId']}&version={params_dict['version']}"
        body_today1 = f"acc_sign={params_dict['acc_sign']}&androidId={params_dict['androidId']}&androidosv={params_dict['androidosv']}&baseband={params_dict['baseband']}&channelId={params_dict['channelId']}&deviceId={params_dict['deviceId']}&deviceModel={params_dict['deviceModel']}&mac_address={params_dict['mac_address']}&networkType={params_dict['networkType']}&oaid={params_dict['oaid']}&pacHlz={params_dict['pacHlz']}&pageType={params_dict['pageType']}&phoneType={params_dict['phoneType']}&req={req_today}&rnd={params_dict['rnd']}&sign={md5_today}&timeStamp={params_dict['timeStamp']}&type=1&userAgent={params_dict['userAgent']}&userId={params_dict['userId']}&utdId={params_dict['utdId']}&version={params_dict['version']}"
        body_today3 = f"acc_sign={params_dict['acc_sign']}&androidId={params_dict['androidId']}&androidosv={params_dict['androidosv']}&baseband={params_dict['baseband']}&channelId={params_dict['channelId']}&deviceId={params_dict['deviceId']}&deviceModel={params_dict['deviceModel']}&mac_address={params_dict['mac_address']}&networkType={params_dict['networkType']}&oaid={params_dict['oaid']}&pacHlz={params_dict['pacHlz']}&pageType={params_dict['pageType']}&phoneType={params_dict['phoneType']}&req={req_today}&rnd={params_dict['rnd']}&sign={md5_today}&timeStamp={params_dict['timeStamp']}&type=3&userAgent={params_dict['userAgent']}&userId={params_dict['userId']}&utdId={params_dict['utdId']}&version={params_dict['version']}"
        body_reward = f"acc_sign={params_dict['acc_sign']}&androidId={params_dict['androidId']}&androidosv={params_dict['androidosv']}&baseband={params_dict['baseband']}&channelId={params_dict['channelId']}&deviceId={params_dict['deviceId']}&deviceModel={params_dict['deviceModel']}&mac_address={params_dict['mac_address']}&networkType={params_dict['networkType']}&oaid={params_dict['oaid']}&pacHlz={params_dict['pacHlz']}&pageType={params_dict['pageType']}&phoneType={params_dict['phoneType']}&req={req_reward}&rnd={params_dict['rnd']}&sign={md5_reward}&timeStamp={params_dict['timeStamp']}&userAgent={params_dict['userAgent']}&userId={params_dict['userId']}&utdId={params_dict['utdId']}&version={params_dict['version']}"

        return userId,body_zfb,body_receive,body_open,body_unLock,body_today1,body_today3,body_reward
    except Exception as e:
        pass

def main():
    response = requests.get("https://mkjt.jdmk.xyz/mkjt.txt")
    response.encoding = 'utf-8'
    txt = response.text
    print(txt)
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
            id,two,three = ck_run_n.split('#',2)
            #id = id[:3] + "*****" + id[-3:]
            print(f"📱：{id}")
            run(two,three)
            time.sleep(random.randint(1, 2))
        except Exception as e:
            print(e)
    print(f'\n----------- 🎊 执 行  结 束 🎊 -----------')

if __name__ == '__main__':
    #white = [7988714,7967069]
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "app.huluxingqiu.com",
        "Connection": "Keep-Alive",
    }
    main()