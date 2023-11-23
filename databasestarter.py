import os
import datetime
import bs4
import urllib.request as req

def databasestarter():  
#建立特定年檔
    yearnow = int(datetime.datetime.now().strftime("%Y"))

    dirpath=os.path.join("資料庫")
    if not os.path.isdir(dirpath):
        os.mkdir("資料庫")
    url = "https://www.ptt.cc/bbs/movie/index.html"
    for year in range(yearnow,2003,-1):
        run = True
        ypath=os.path.join("資料庫",str(year)+"年搜尋資料庫.txt")
        cpath=os.path.join("資料庫","[完成]"+str(year)+"年搜尋資料庫.txt")
        gpath=os.path.join("資料庫","每年開頭紀錄.txt")
         
        if os.path.isfile(gpath) & os.path.isfile(cpath):
            with open(gpath, 'r+' , encoding='UTF-8') as f:
                allurl = f.read()
                allurl = allurl.split("\n")
            for i in range(0,len(allurl)):
                if str(year) in allurl[i]:
                    url = allurl[i][5:]
                    run = False
    
        if(run):   
            f= open(ypath, 'w' , encoding='UTF-8')
            f.write("")
            f.close()
            url = datarealprinter(year,url) 
                

#把所有第一年的movie版文章抓出來，然而因為一頁一頁爬，其實跟一頁頁抓全部的文章比起來是一樣快的，所以乾脆改寫，改成為我邊抓邊分類
#由於前面的starter已經幫忙判斷檔案的存在與否和完整性了
#所以dataprinter就會直接取代txt
#專心輸出一年的txt檔
      
def datarealprinter(year,url):
    year1 = (datetime.datetime.now()).strftime("%Y")
    turnout = True
    #出現12/31就代表今年結束，但如果第一頁是前一年的12/31，所以下面的第一個if會避免break，所以會再弄回來
    ppath = os.path.join("資料庫",str(year)+"年搜尋資料庫.txt")
    f = open(ppath, 'a+' , encoding='UTF-8')
    while(True):
        templist=[]
        ##f.seek(0, 0)無法按照時間順序去存，因為不可能在不改變文件結構時去插入前面的文字，這是完全行不通的
        request=req.Request(url,headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data,"html.parser")
        titles=root.find_all("div", class_="title")#尋找class="title"的div檔案
        dates=root.find_all("div", class_="date")
        dates = [str(e.text) for e in dates]#清出資料 不要有<div>標籤
        
        if(turnout):
            if "12/" not in str(dates):
                turnout = False
            if(turnout):   
                for i in range(0,len(dates)):
                    if titles[i].a !=None: 
                        if " 1/" in str(dates[i])  or " 2/" in str(dates[i]) :
                            pass
                        else:
                            link = "https://www.ptt.cc"+str(titles[i].select_one("a").get("href"))
                            templist.insert(0,"\n"+str(dates[i])+" "+str(titles[i].a.text.strip())+"\n"+link) 
        
        if not(turnout):
            if "12/" in str(dates):
                #避免首頁公告與M文
                if url == "https://www.ptt.cc/bbs/movie/index.html":
                    for i in range(0,len(dates)):
                        if "1/" in str(dates[0])  or "2/" in str(dates[0]):
                            templist.insert(0,"\n"+str(dates[i])+" "+str(titles[i].a.text.strip())+"\n"+link)    
                else:   
                    specialurl = url#記住當年的第一篇文章在哪一頁
                    for i in range(0,len(dates)):
                        if titles[i].a !=None: 
                            if "1/" in str(dates[i])  or "2/" in str(dates[i]):
                                pass
                            else:
                                link = "https://www.ptt.cc"+str(titles[i].select_one("a").get("href"))
                                templist.insert(0,"\n"+str(dates[i])+" "+str(titles[i].a.text.strip())+"\n"+link)
                    break
            else:
                for i in range(0,len(dates)):
                    if titles[i].a !=None: 
                        link = "https://www.ptt.cc"+str(titles[i].select_one("a").get("href"))
                        templist.insert(0,"\n"+str(dates[i])+" "+str(titles[i].a.text.strip())+"\n"+link)         
        

        ppath = os.path.join("資料庫",str(year)+"年搜尋資料庫.txt")  
        for temp in templist:
            f.write(temp)
        
        #全站最後一頁
        if url == "https://www.ptt.cc/bbs/movie/index1.html":
            ypath=os.path.join("資料庫","每年開頭紀錄.txt")
            with open(ypath, 'a+' , encoding='UTF-8') as f:
                f.write("2004 https://www.ptt.cc/bbs/movie/index1.html"+"\n") 
            f.close()
            cpath=os.path.join("資料庫","[完成]"+str(year)+"年搜尋資料庫.txt")
            if os.path.isfile(cpath):
                os.remove(cpath)
            os.rename(ppath, cpath)
            return "最後一頁"
        #翻頁
        btn = root.select('div.btn-group > a')
        up_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + up_page_href
        url=next_page_url
    f.close()    
    if str(year) != year1:
        cpath=os.path.join("資料庫","[完成]"+str(year)+"年搜尋資料庫.txt")
        if os.path.isfile(cpath):
            os.remove(cpath)
        os.rename(ppath, cpath)

    ypath=os.path.join("資料庫","每年開頭紀錄.txt")
    with open(ypath, 'a+' , encoding='UTF-8') as f:
        f.write(str(year) + " " + specialurl+"\n") 
        return specialurl

