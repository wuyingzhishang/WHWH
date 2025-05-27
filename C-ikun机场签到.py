import json
import os
import requests




#   --------------------------------注释区--------------------------------
#   ikun机场签到
#   by for:风华正太D猫
#   域名: https://ikuuu.one/
#   变量:maodieIkun 邮箱#密码
#
#   --------------------------------一般不动区-------------------------------
#                     _ooOoo_
#                    o8888888o
#                    88" . "88
#                    (| -_- |)
#                     O\ = /O
#                 ____/`---'\____
#               .   ' \\| |// `.
#                / \\||| : |||// \
#              / _||||| -:- |||||- \
#                | | \\\ - /// | |
#              | \_| ''\---/'' | |
#               \ .-\__ `-` ___/-. /
#            ___`. .' /--.--\ `. . __
#         ."" '< `.___\_<|>_/___.' >'"".
#        | | : `- \`.;`\ _ /`;.`/ - ` : | |
#          \ \ `-. \_ __\ /__ _/ .-` / /
#  ======`-.____`-.___\_____/___.-`____.-'======
#                     `=---='
#
#  .............................................
#           佛祖保佑             永无BUG
#           佛祖镇楼             BUG辟邪
# 佛曰:
#        写字楼里写字间，写字间里程序员；
#        程序人员写程序，又拿程序换酒钱。
#        酒醒只在网上坐，酒醉还来网下眠；
#        酒醉酒醒日复日，网上网下年复年。
#        但愿老死电脑间，不愿鞠躬老板前；
#        奔驰宝马贵者趣，公交自行程序员。
#        别人笑我忒疯癫，我笑自己命太贱；
#        不见满街漂亮妹，哪个归得程序员？
#
#   --------------------------------代码区--------------------------------
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    payload = {}
    maodieIkun = os.environ.get('maodieIkun') or "123456@qq.com#54321"
    email = maodieIkun.split("#")[0]
    password = maodieIkun.split("#")[1]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }
    url = f"https://ikuuu.one/auth/login?email={email}&passwd={password}&code&remember_me=on"

    response = requests.request("POST", url, headers=headers, data=payload)

    print(json.loads(response.content.decode('utf-8')))

    setCookie = response.headers.get('Set-Cookie','')
    cookies = setCookie.split(', ')
    cookie_dict = {}

    for cookie in cookies:
        parts = cookie.split(';')[0].split('=', 1)
        if len(parts) == 2:
            key, value = parts
            cookie_dict[key] = requests.utils.unquote(value)

    # 提取特定的 cookie 值
    email = cookie_dict.get('email', 'N/A')
    expire_in = cookie_dict.get('expire_in', 'N/A')
    ip = cookie_dict.get('ip', 'N/A')
    key = cookie_dict.get('key', 'N/A')
    uid = cookie_dict.get('uid', 'N/A')

    print(f"Email: {email}")
    print(f"Expire In: {expire_in}")
    print(f"IP: {ip}")
    print(f"Key: {key}")
    print(f"UID: {uid}")
    headers = {
        'Cookie': f'email={email}; expire_in={expire_in}; ip={ip}; key={key}; uid={uid}'
    }
    url = "https://ikuuu.one/user/checkin"
    response = requests.request("POST", url, headers=headers, data=payload)
    print(json.loads(response.content.decode('utf-8')))
