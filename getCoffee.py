#coding:utf-8
#Python3 
#安装 pip install requests
#安装 pip install bs4
import requests
from bs4 import BeautifulSoup
import time,datetime
import json
import os

def filepath():
	today=datetime.date.today()
	year =today.year 
	month = today.month 
	day = today.day
	fullpath="{year}\{month}\{day}".format(year=year,month=month,day=day)
	if not os.path.isdir(fullpath):
		os.makedirs(fullpath)
		return fullpath 
	else:
		return fullpath


sessions = requests.session()

number =10 #修改机器总数
post_info={
	'formhash':'0a19233e',
	'username':'',  
	'password':'',
	'loginsubmit':'登陆'

}
content = sessions.post('http://m.coffeeji.cn/space.php?do=login',data=post_info)
time.sleep(20)
for i in range(1,number):  
	body=sessions.get('http://m.coffeeji.cn/space.php?do=extension&op=getSaleCup&cid=%d'%i)
	path =filepath()
	
	if body.status_code==200:
		with open( os.path.join(path,"zhzj2&_"+str(i)+'.json'),"wb") as f:
			f.write(body.content)
	

	time.sleep(10)



#备注：
#由于网络的不确定性，需调整 time.sleep的时间 
#文件属于json格式，已经包含机器名称和数量单位
#readme  
