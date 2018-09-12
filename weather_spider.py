import requests
import csv
import random
from bs4 import BeautifulSoup
import socket
import csv

def get_content(url,data=None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
        }

    timeout = random.choice(range(80,180))
    r = requests.get(url,headers=header,timeout=timeout)
    r.encoding = "utf-8"

    return r.text

def get_data(html_text):
    final = []
    bs =BeautifulSoup(html_text,"html.parser")
    body = bs.body
    data = body.find("div",{"id":"7d"})
    ul = data.find("ul")
    li = ul.find_all("li")

    for day in li:
        temp = []
        date = day.find("h1").string
        temp.append(date)
        inf = day.find_all("p")
        temp.append(inf[0].string,)
        if inf[1].find('span') is None:
            temperature_highest = None # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
        else:
            temperature_highest = inf[1].find('span').string  # 找到最高温
            temperature_highest = temperature_highest.replace('℃', '')  # 到了晚上网站会变，最高温度后面也有个℃
        temperature_lowest = inf[1].find('i').string  # 找到最低温
        temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
        temp.append(temperature_highest)   # 将最高温添加到temp中
        temp.append(temperature_lowest)   #将最低温添加到temp中
        final.append(temp)   #将temp加到final中

    return final

def write_data(data,name):
    file_name = name
    with open(file_name,"a",errors="ignore",newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)

if __name__ == "__main__":
    url = "http://www.weather.com.cn/weather/101190401.shtml"
    
    html = get_content(url)
    #print(html)
    result = get_data(html)
    #print(result)
    write_data(result,"weather.csv")
    