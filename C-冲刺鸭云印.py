#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#环境变量添加ccyyy_token，格式为备注#openid，多账号&
import requests
import time
import random
import os

# ====================== 配置 ======================
ccyyy_token = os.environ.get("ccyyy_token", "")
pushplus_token = os.environ.get("PUSPLUS_TOKEN", None)
proxy_api_url = os.environ.get("proxy_api_url", None)
# =================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.188 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/17H35 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G9910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.7 Mobile/15E148 Safari/604.1"
]

# ------------------ 获取代理 ------------------
def get_proxy(retry=3):
    if not proxy_api_url:
        print("[提醒] 未配置代理变量 proxy_api_url，将直接使用本地网络")
        return None
    for attempt in range(1, retry+1):
        try:
            resp = requests.get(proxy_api_url, timeout=10)
            resp.raise_for_status()
            proxy_addr = resp.text.strip()
            if proxy_addr:
                print(f"[代理] 第 {attempt} 次获取代理成功: {proxy_addr}")
                return {"http": proxy_addr, "https": proxy_addr}
            else:
                print(f"[提醒] 代理 API 返回为空，第 {attempt} 次重试")
        except Exception as e:
            print(f"[提醒] 获取代理失败，第 {attempt} 次重试: {e}")
        time.sleep(1)
    print("[提醒] 三次代理获取失败，将使用本地网络")
    return None

# ------------------ 推送函数 ------------------
def pushplus_send(content):
    if not pushplus_token:
        print("[提醒] 未配置 PushPlus token，无法推送通知")
        return
    try:
        url = "https://www.pushplus.plus/send"
        payload = {
            "token": pushplus_token,
            "title": "冲刺鸭云印运行结果",
            "content": content,
            "template": "html"
        }
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            print("[提醒] PushPlus 推送成功")
        else:
            print(f"[提醒] PushPlus 推送失败，状态码: {resp.status_code}")
    except Exception as e:
        print(f"[提醒] PushPlus 推送失败: {e}")

# ------------------ 签到 + 查询积分 + 提现 ------------------
def do_sign_query_withdraw(remark, token, proxies=None):
    headers = {
        "Host": "cloudprint.chongci.shop",
        "User-Agent": random.choice(USER_AGENTS),
        "xweb_xhr": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxAPPID/page-frame.html",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Priority": "u=1, i"
    }

    # ------------------ 签到 ------------------
    sign_url = "https://cloudprint.chongci.shop/app/index.php"
    sign_params = {
        "i": 2, "c": "entry", "m": "ewei_shopv2", "do": "mobile",
        "r": "sign.dosign", "app": 1, "openid": token
    }
    for attempt in range(1,4):
        try:
            resp = requests.post(sign_url, headers=headers, params=sign_params, proxies=proxies, timeout=15)
            resp.raise_for_status()
            sign_data = resp.json()
            break
        except Exception as e:
            print(f"[{remark}] 签到异常，第 {attempt} 次重试 ❌ {e}")
            if attempt == 3:
                return f"[{remark}] 签到异常 ❌ {e}"
            time.sleep(2)

    if sign_data.get("status") == 1:
        result = sign_data.get("result", {})
        addcredit = float(result.get("addcredit", 0))
        signsum = result.get("signsum", 0)
        sign_msg = f"签到成功 ✅ 累计签到 {signsum} 天，本次获得积分 {addcredit}"
    elif sign_data.get("status") == 2:
        sign_msg = "今日已签到 ⏰"
    else:
        sign_msg = f"签到失败 ❌ 返回：{sign_data}"

    # ------------------ 查询总积分 ------------------
    credit_url = "https://cloudprint.chongci.shop/app/index.php"
    credit_params = {
        "i": 2, "c": "entry", "m": "ewei_shopv2", "do": "mobile",
        "r": "api.index.get_detail_list", "app": 1, "openid": token,
        "type": "credit1", "page": 1
    }
    try:
        resp = requests.post(credit_url, headers=headers, params=credit_params, proxies=proxies, timeout=15)
        resp.raise_for_status()
        credit_data = resp.json()
        total_credit = float(credit_data.get("total", 0))
    except Exception as e:
        total_credit = 0
        print(f"[{remark}] 查询积分异常 ❌ {e}")

    # ------------------ 判断提现 ------------------
    withdraw_msg = ""
    if total_credit >= 1:
        withdraw_url = "https://cloudprint.chongci.shop/app/index.php"
        withdraw_params = {
            "i": 2, "c": "entry", "m": "ewei_shopv2", "do": "mobile",
            "r": "api.index.jf_tx", "app": 1, "openid": token, "num": 1
        }
        for attempt in range(1,4):
            try:
                resp = requests.post(withdraw_url, headers=headers, params=withdraw_params, proxies=proxies, timeout=15)
                resp.raise_for_status()
                tx_data = resp.json()
                if tx_data.get("error") == 0:
                    withdraw_msg = f"提现成功 ✅"
                else:
                    withdraw_msg = f"提现失败 ❌ {tx_data.get('message', '')}"
                break
            except Exception as e:
                withdraw_msg = f"提现异常 ❌ {e}，第 {attempt} 次重试"
                if attempt < 3:
                    time.sleep(2)
                    continue
                break
    else:
        withdraw_msg = f"当前积分不足提现 ⏰ ({total_credit})"

    # ------------------ 拼接结果 ------------------
    final_msg = f"[{remark}] {sign_msg} | 当前总积分: {total_credit} | {withdraw_msg}"
    return final_msg

# ================== 执行 ==================
if not ccyyy_token:
    print("[提醒] 未配置 ccyyy_token，请设置环境变量")
else:
    accounts = ccyyy_token.split("&")
    print(f"[提醒] 获取到 {len(accounts)} 个账号，即将开始签到...\n")
    all_results = []

    for idx, account in enumerate(accounts, 1):
        if "#" not in account:
            print(f"[提醒] 账号格式错误: {account}")
            continue
        remark, token = account.split("#", 1)

        # 每个账号单独获取代理
        proxies = get_proxy()

        result = do_sign_query_withdraw(remark.strip(), token.strip(), proxies)
        print(result)
        all_results.append(result)

        # 非最后一个账号才延迟
        if idx != len(accounts):
            delay = random.randint(10, 15)
            print(f"等待 {delay} 秒后执行下一个账号...\n")
            time.sleep(delay)

    # ================== 统一推送 ==================
    if all_results:
        msg = "<br>".join(all_results)
        pushplus_send(msg)
