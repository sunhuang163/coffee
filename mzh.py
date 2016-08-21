#coding:utf-8
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from host import host
def getPagecontent(username,password,fullpath):
	#driver = webdriver.Firefox(timeout=30)
	#driver = webdriver.PhantomJS("D:\\app\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
	driver = webdriver.PhantomJS("phantomjs.exe")
	driver.set_window_size(1280, 800)
	driver.get("http://m.coffeeji.cn/space.php?do=login")
	# input username and password
	user = driver.find_element_by_id('username').send_keys(username)
	pwd = driver.find_element_by_id('password').send_keys(password)
	#click login
	#time.sleep(2)

	driver.find_element_by_name('loginsubmit').click()
	#driver.find_element_by_partial_link_text('登陆').click()
	time.sleep(10)
	try:
		driver.find_element_by_partial_link_text('分机管理').click()
		time.sleep(5)
		driver.find_element_by_partial_link_text('详情').click()
		time.sleep(5)
		driver.find_element_by_partial_link_text('实时查询杯数').click()
		time.sleep(40)
		try:
			content=driver.find_element_by_id('showbeishu')
			#datetime_now=time.strftime('%M',time.localtime())		
			f=open(os.path.join(fullpath,username),"w+",encoding="utf-8")
			f.write(driver.page_source)
			f.close()
			print(" complete fetch network")
		except:
			print("Offline ")
	except:
		print("Can't Login , please check password")
	driver.close()

def getTableContent(path,username):	
	from bs4 import BeautifulSoup	
	print("start %s"%username)
	f = open(os.path.join(path,username), "r",encoding="utf-8")
	str = f.read()

	f.close()


	soup = BeautifulSoup(str,"html.parser")
	soup.prettify()
	table=soup.find(id='showbeishu')
	tr= table.find_all('tr')
	txt=[]
	for t in tr:		
		td=t.find_all('td')
		if len(td)==3:
			datetime_now=time.strftime('%Y-%m-%d %X',time.localtime())
			line="{username},{name},{value1},{value2},{datetime_now} \n".format(username=username,datetime_now=datetime_now,name=td[0].text,value1=td[1].find('input').get('value'),value2=td[2].find('input').get('value'))
			print(line)
			datetime_now=time.strftime('_%H_%M_',time.localtime())
			dbfile=open(os.path.join(path,username+datetime_now+"db.csv"),"a+",encoding="utf-8")
			dbfile.writelines(line)
			dbfile.close()


def create_dir():
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

if __name__ == '__main__':
	start = time.clock()
	

	for h in host:
		username =h[0]
		password=h[1]
		fullpath =os.path.join(os.getcwd(),create_dir())
		getPagecontent(username,password,fullpath)
		time.sleep(1)
		getTableContent(fullpath,username)


				
		

	end = time.clock()
	print("程序消耗时间: %f s" % (end - start))




	


