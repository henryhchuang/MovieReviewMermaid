from typing import NamedTuple
import urllib.request as req
import bs4
import sys 
import datetime
import math

def yahoo():
    mlist=[]
    url="https://movies.yahoo.com.tw/movie_intheaters.html?page=1"
    request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    root = bs4.BeautifulSoup(data,"html.parser")
    dates=str(root.find_all("div", class_="release_time _c"))
    numbers=int(dates[dates.find("共")+1:dates.find("筆")])//10+2
    for i in range(numbers):
        url="https://movies.yahoo.com.tw/movie_intheaters.html?page="+str(i)
        request=req.Request(url,headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
            })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data,"html.parser")
        titles=root.find_all("div", class_="release_movie_name")#不可以自己先轉型，標籤會不見
        for title in titles:
            title=str(title.a.text.strip())#清洗資料
            if(title=="[]"):#清洗資料
                pass
            if("電影" in title):#清洗資料
                title=title.replace("電影版","")
                title=title.replace("電影","")
                title=title.replace(" ","")
            mlist.append(title)
    return mlist

    


        