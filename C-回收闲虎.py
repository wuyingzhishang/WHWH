"""
name: 旧衣服回收闲虎，2.5起提
Author: MK集团本部
Date: 2024-09-24
export hsxh="authorization"
cron: 0 5 * * *
"""
#import notify
import requests, json, os, sys, time, random, datetime
response = requests.get("https://mkjt.jdmk.xyz/mkjt.txt")
response.encoding = 'utf-8'
txt = response.text
print(txt)
#---------------------主代码区块---------------------
session = requests.session()

def userinfo(wx, authorization):
	url = f'https://openapp.fmy90.com/user/paid/base/info?platformKey={wx}&mini_scene=1007'
	header = {
		"Connection": "keep-alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/3169 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
		"content-type": "application/json",
		"authorization": authorization
	}
	data = ""
	try:
		response = session.get(url=url, headers=header, json=data)
		info = json.loads(response.text)
		#print(info)
		if "操作成功" in info["message"]:
			return info["data"]["base_info"]["userPhone"],info["data"]["base_info"]["userBeans"],info["data"]["direct_balance"]
	except Exception as e:
		#print(e)
		pass

def run(wx,authorization):
	userinfo(wx, authorization)
	login = 'https://openapp.fmy90.com/active/sign-in/do'
	header = {
		"Connection": "keep-alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/3169 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
		"content-type": "application/json",
		"authorization": authorization
	}
	data = {
		"platformKey" : wx,
		"mini_scene":"1007"
	}
	try:
		response = session.post(url=login, headers=header, json=data)
		login = json.loads(response.text)
		#print(login)
		a , b, c = userinfo(wx, authorization)
		if "操作成功" in login["message"]:
			print(f"📱：{a}\n☁️签到：成功\n🌈积分：{b}分\n🌈现金：{c}元")
		elif "今天已经签到" in login["message"]:
			print(f"📱：{a}\n☁️签到：成功\n🌈积分：{b}分\n🌈现金：{c}元")
		else:
			print("📱：账号已过期或异常")
	except Exception as e:
		print("📱：账号已过期或异常")
def main():
	if os.environ.get("hsxh"):
		ck = os.environ.get("hsxh")
	else:
		ck = ""
		if ck == "":
			print("请设置变量")
			sys.exit()

	if datetime.datetime.strptime('05:01','%H:%M').time() <= datetime.datetime.now().time() <= datetime.datetime.strptime('06:59', '%H:%M').time():
		time.sleep(random.randint(100, 500))
	ck_run = ck.split('\n')
	print(f"{' ' * 10}꧁༺ 回收༒闲虎 ༻꧂\n")
	for i, ck_run_n in enumerate(ck_run):
		print(f'\n----------- 🍺账号【{i + 1}/{len(ck_run)}】执行🍺 -----------')
		try:
			wx = "wxc5f5d433d0de2894"
			authorization = ck_run_n
			run(wx, authorization)
			time.sleep(random.randint(1, 2))
		except Exception as e:
			print(e)
			#notify.send('title', 'message')

	print(f'\n----------- 🎊 执 行  结 束 🎊 -----------')


if __name__ == '__main__':
	main()