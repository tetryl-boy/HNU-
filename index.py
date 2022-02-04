# -*- coding = utf-8 -*-
# @time=2022/2/4 17:29
# @file g.py
import requests
from bs4 import BeautifulSoup
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
def notice(f,g):
    url = 'http://jwc.hnu.edu.cn/tzgg/sytz.htm'
    page_text = requests.get(url).text
    soup = BeautifulSoup(page_text,'lxml')
    # 获取通知列表
    list = soup.find('div',class_="list").find_all('li')

    u= re.findall('href=.../(.*).htm',str(list))

    ulis=[]
    for ur in u:
        main_url = 'http://jwc.hnu.edu.cn/'
        a=main_url+ur+'.htm'
        ulis.append(a)
    print(ulis)
    title_list=''
    for url in ulis:
        r = requests.get(url=url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('div', class_="con_h").text
        pub_data = soup.find('div', class_="con_span").text
        d=re.findall('时间：(.*) ',str(pub_data))
        d=d[0]

        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if d == current_time:
            title_list=title_list+ title + '\n' + url+'\n'
        



    def mail(status):
        from_addr = ''    #填写发送邮箱的地址
	
        password = ''  #发送邮箱的效验码

        to_addr = ''   #接受邮箱地址

        smtp_server = ''  #发送邮箱的服务器

        msg = MIMEText(status, 'plain', 'utf-8')

        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('湖南大学教务处通知')

        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)

        server.login(from_addr, password)

        server.sendmail(from_addr, to_addr, msg.as_string())

        server.quit()

    if len(title_list)!=0:
        mail(str(title_list))
