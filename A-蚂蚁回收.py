"""
name: 飞蚂蚁旧衣服回收，兑换
Author: NK集团本部
Date: 2024-09-24
export fmy="备注#Authorization"
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

def userinfo(ck):
	url = 'https://openapp.fmy90.com/user/new/beans/info?type=1&version=V2.00.01&platformKey=F2EE24892FBF66F0AFF8C0EB532A9394&mini_scene=1096&partner_ext_infos='
	header = {
		"Connection": "keep-alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/3169 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
		"content-type": "application/json;charset=utf8",
		"Authorization": ck,
	}
	data = {}
	try:
		response = session.get(url=url, headers=header, data=data)
		info = json.loads(response.text)
		#print(info)
		if "操作成功" in info["message"]:
			return info["data"]["totalCount"]
	except Exception as e:
		#print(e)
		pass

def run(id,ck):
	login = 'https://openapp.fmy90.com/sign/new/do'
	header = {
		"Connection": "keep-alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/3169 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
		"content-type": "application/json;charset=utf8",
		"Authorization": ck,
	}
	data = {"version":"V2.00.01","platformKey":"F2EE24892FBF66F0AFF8C0EB532A9394","mini_scene":1096,"partner_ext_infos":""}
	try:
		userinfo(ck)
		response = session.post(url=login, headers=header, json=data)
		login = json.loads(response.text)
		#print(login)
		a = userinfo(ck)
		if "操作成功" in login["message"]:
			print(f"📱：{id}\n☁️签到：成功\n🌈积分：{a}分")
		else:
			print(f"📱：{id}\n☁️签到：{login['message']}\n🌈积分：{a}分")
		time.sleep(2)
	except Exception as e:
		print("📱：账号已过期或异常")

def main():
	if os.environ.get("fmy"):
		ck = os.environ.get("fmy")
	else:
		ck = ""
		if ck == "":
			print("请设置变量")
			sys.exit()
	if datetime.datetime.strptime('05:01', '%H:%M').time() <= datetime.datetime.now().time() <= datetime.datetime.strptime('06:59', '%H:%M').time():
		time.sleep(random.randint(100, 500))
	ck_run = ck.split('\n')
	print(f"{' ' * 10}꧁༺ 蚂蚁༒回收 ༻꧂\n")
	for i, ck_run_n in enumerate(ck_run):
		print(f'\n----------- 🍺账号【{i + 1}/{len(ck_run)}】执行🍺 -----------')
		try:
			ck_run_nm = ck_run_n.split('#')
			id = ck_run_nm[0]
			ck = ck_run_nm[1]
			run(id,ck)
			time.sleep(random.randint(1, 2))
		except Exception as e:
			print(e)
			#notify.send('title', 'message')

	print(f'\n----------- 🎊 执 行  结 束 🎊 -----------')


if __name__ == '__main__':
	main()