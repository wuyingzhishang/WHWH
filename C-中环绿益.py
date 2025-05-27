"""
name: 中环绿益行旧衣回收，兑换
Author: MK集团本部
Date: 2024-09-24
export zhlv="token#openid"
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

def userinfo(ck,od):
	url = 'https://hsadmin.zhuyy.cn/api/User/getInfo'
	url2 = 'https://hsadmin.zhuyy.cn/api/intergral/taskList'
	header = {
		"Connection": "keep-alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/3169 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
		"content-type": "application/x-www-form-urlencoded",
		"token": ck,
		"openid": od,
	}
	data = f'openid={od}'
	try:
		response = session.post(url=url, headers=header, data=data)
		list = session.post(url=url2, headers=header, data=data)
		info = json.loads(response.text)
		#print(info)
		if "成功" in info["msg"]:
			return info["data"]["score"],info["data"]["nickname"]
	except Exception as e:
		#print(e)
		pass

def run(ck,od):
	login = 'https://hsadmin.zhuyy.cn/api/Usersign/sign'
	header = {
		"Connection": "keep-alive",
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/3169 MicroMessenger/8.0.50.2701(0x2800325B) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
		"content-type": "application/x-www-form-urlencoded",
		"token": ck,
		"openid": od,
	}
	data = f'openid={od}'
	try:
		userinfo(ck,od)
		response = session.post(url=login, headers=header, data=data)
		login = json.loads(response.text)
		#print(login)
		a , b = userinfo(ck,od)
		if login["code"] == 1:
			print(f"📱：{b}\n☁️签到：成功\n🌈积分：{a}分")
		else:
			print(f"📱：{b}\n☁️签到：{login['msg']}\n🌈积分：{a}分")
		time.sleep(2)
	except Exception as e:
		print("📱：账号已过期或异常")

def main():
	if os.environ.get("zhlv"):
		ck = os.environ.get("zhlv")
	else:
		ck = ""
		if ck == "":
			print("请设置变量")
			sys.exit()
	if datetime.datetime.strptime('05:01', '%H:%M').time() <= datetime.datetime.now().time() <= datetime.datetime.strptime('06:59', '%H:%M').time():
		time.sleep(random.randint(100, 500))
	ck_run = ck.split('\n')
	print(f"{' ' * 10}꧁༺ 中环༒绿益 ༻꧂\n")
	for i, ck_run_n in enumerate(ck_run):
		print(f'\n----------- 🍺账号【{i + 1}/{len(ck_run)}】执行🍺 -----------')
		try:
			ck_run_nm = ck_run_n.split('#')
			ck = ck_run_nm[0]
			od = ck_run_nm[1]
			run(ck,od)
			time.sleep(random.randint(1, 2))
		except Exception as e:
			print(e)
			#notify.send('title', 'message')

	print(f'\n----------- 🎊 执 行  结 束 🎊 -----------')


if __name__ == '__main__':
	main()