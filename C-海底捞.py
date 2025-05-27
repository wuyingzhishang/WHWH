#群718505085
# 入口:海底捞小程序
#海底捞养号签到
#每日签到一次获得10碎片，碎片可以兑换菜品。
#需抓取数据：手机抓包请协议头里抓 _HAIDILAO_APP_TOKEN这个值
#变量名称： HAIDILAO_TOKENS
#
# --------------------------------祈求区--------------------------------
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
import os
import requests
import time
def sign_in(token):
    url = "https://superapp-public.kiwa-tech.com/activity/wxapp/signin/signin"
    
    headers = {
        "Host": "superapp-public.kiwa-tech.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "ReqType": "APPH5",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors",
        "Content-Type": "application/json",
        "Origin": "https://superapp-public.kiwa-tech.com",
        "deviceId": "null",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.59(0x18003b20) NetType/WIFI Language/zh_CN miniProgram/wx1ddeb67115f30d1a",
        "_HAIDILAO_APP_TOKEN": token,
        "Referer": f"https://superapp-public.kiwa-tech.com/app-sign-in/?SignInToken={token}&source=MiniApp",
        "Sec-Fetch-Dest": "empty",
        "Cookie": "acw_tc=2760829c17469282547662540e2e2e284c0680d04d6a9492ccb270b7c6f823"
    }

    data = {"signinSource": "MiniApp"}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status() 
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
  
    tokens_env = os.getenv("HAIDILAO_TOKENS")
    if not tokens_env:
        print("❌ 未找到环境变量 HAIDILAO_TOKENS，请检查是否设置！")
        exit(1)

    tokens = [t.strip() for t in tokens_env.split("#") if t.strip()]
    if not tokens:
        print("❌ 未找到有效的 Token，请检查环境变量格式！")
        exit(1)

    print(f"🔍 共找到 {len(tokens)} 个 Token，开始签到...\n")
    success_count = 0
    fail_count = 0

    for idx, token in enumerate(tokens, 1):
        print(f"🔄 账号 {idx}/{len(tokens)}: 正在签到...")
        result = sign_in(token)
        
        if result["success"]:
            print(f"✅ 签到成功: {result['data']}")
            success_count += 1
        else:
            print(f"❌ 签到失败: {result['error']}")
            fail_count += 1
        
        print("-" * 40)
        time.sleep(1) 

    print("\n📊 签到结果统计:")
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {fail_count} 个")
    print("\n🎉 所有账号处理完成！")