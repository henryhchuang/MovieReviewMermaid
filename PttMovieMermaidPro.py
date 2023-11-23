from typing import NamedTuple
import urllib.request as req
import bs4
import sys 
import datetime
import math
import yahoo
import os
import subprocess
from time import sleep
from tqdm import tqdm
import databasestarter

def search(movie,day1,day2):#電影，較遠的日期，較近的日期
    wyear = int(str(day2)[0:4])-int(str(day1)[0:4])
    if wyear == 0:
        return searchless(int(str(day1)[0:4]),int(str(day1)[4:6]),int(str(day1)[6:8]),int(str(day2)[4:6]),int(str(day2)[6:8]),movie)
        #直接輸出
    elif wyear >= 1:
        gb1=[]
        gb2=[]
        gb3=[]
        abouttalk2=[]
        gb1,abouttalk1 = searchlast(int(str(day2)[0:4]),int(str(day2)[4:6]),int(str(day2)[6:8]),movie)
        abouttalk1.insert(0,"\n"+str(day2)[0:4]+"年討論串")
        for i in range(wyear-1,0,-1):##-2是因為下面有+1
            templay=[]
            temptalk=[]
            templay,temptalk = searchyear(int(str(day1)[0:4])+i ,movie)
            gb2+=templay
            temptalk.insert(0,"\n"+str(int(str(day1)[0:4])+i)+"年討論串")
            abouttalk2+=temptalk
        gb3,abouttalk3 = searchfirst(int(str(day1)[0:4]),int(str(day1)[4:6]),int(str(day1)[6:8]),movie)
        abouttalk3.insert(0,"\n"+str(day1)[0:4]+"年討論串")
        allgb=gb1+gb2+gb3
        abouttalk=abouttalk1+abouttalk2+abouttalk3
        comment=[]#過濾後的雷的
        cindex=[]
        for i in range(0,len(allgb)):
            if allgb[i] not in comment:
                comment.append(str(allgb[i])) #重複的評價整理成同一個，並且給予數字
        for i in range(0,len(comment)):
            cindex.append(str(allgb.count(comment[i])))
        #需要組合
        return totmato(comment,cindex,movie),abouttalk

def searchyear(wyear,movie):    #輸出lay 跟 abouttalk
    goodbad=[]#有雷的
    comment=[]#過濾後的雷的
    cindex=[]
    abouttalk=[]#有電影標題的討論
    alltxt=[]#取出來的原始資料
    cpath=os.path.join("資料庫","[完成]"+str(wyear)+"年搜尋資料庫.txt")
    with open(cpath, 'r+' , encoding='UTF-8') as f:
        alltxt=f.read().split("\n")
        del alltxt[0]
        
    for i in range(0,len(alltxt),2):##int()自動把0變不見
        if movie in alltxt[i]:          
            abouttalk.append(alltxt[i])
            abouttalk.append(alltxt[i+1])

    for i in range(0,len(abouttalk)):
        data=str(abouttalk[i])
        if "Re" not in str(data):
            tt = data.replace(" ","")
            if "雷]" in tt and "[有雷]" not in tt and "[無雷]" not in tt and "[結局雷]" not in tt and "[討論雷]" not in tt and "[雷]" not in tt and "[微雷]" not in tt and "[問雷]" not in tt  :
                if "[" not in tt and "]" in tt:
                    tt1 = 5
                    tt2 = tt.index("]")
                elif "]" not in tt and "[" in tt:
                    continue
                else:
                    tt1 = tt.index("[")+1
                    tt2 = tt.index("]")
                tt=tt[tt1:tt2]
                goodbad.append(tt) #擷取[]內的評價

    return goodbad,abouttalk
        
def searchfirst(year,mont,dayt,movie):#文件前面全部都會收，開始到某個階段才不收 ，輸出lay 跟 abouttalk
    goodbad=[]#有雷的
    comment=[]#過濾後的雷的
    cindex=[]
    abouttalk=[]#有電影標題的討論
    alltxt=[]#取出來的原始資料
    cpath=os.path.join("資料庫","[完成]"+str(year)+"年搜尋資料庫.txt")
    if str(year)==datetime.datetime.now().strftime("%Y"):
        cpath=os.path.join("資料庫",str(year)+"年搜尋資料庫.txt")
    with open(cpath, 'r+' , encoding='UTF-8') as f:
        alltxt=f.read().split("\n")
        del alltxt[0]
    
    for i in range(0,len(alltxt),2):
        if int(alltxt[i][:2].strip()) <= mont and int(alltxt[i][3:5].strip()) < dayt:
            break
        if int(alltxt[i][:2].strip()) < mont:
            break
        elif movie in alltxt[i]:            #如果時間進到就break
            abouttalk.append(alltxt[i])
            abouttalk.append(alltxt[i+1])
    
    for i in range(0,len(abouttalk)):
        data=str(abouttalk[i])
        if "Re" not in str(data):
            tt = data.replace(" ","")
            if "雷]" in tt and "[有雷]" not in tt and "[無雷]" not in tt and "[結局雷]" not in tt and "[討論雷]" not in tt and "[雷]" not in tt and "[微雷]" not in tt and "[問雷]" not in tt  :
                if "[" not in tt and "]" in tt:
                    tt1 = 5
                    tt2 = tt.index("]")
                elif "]" not in tt and "[" in tt:
                    continue
                else:
                    tt1 = tt.index("[")+1
                    tt2 = tt.index("]")
                tt=tt[tt1:tt2]
                goodbad.append(tt) #擷取[]內的評價
    return goodbad,abouttalk
            
def searchlast(year,mont,dayt,movie):#文件前面不會收，開始到某個階段才收，輸出lay 跟 abouttalk
    goodbad=[]#有雷的
    comment=[]#過濾後的雷的
    cindex=[]
    abouttalk=[]#有電影標題的討論
    alltxt=[]#取出來的原始資料
    cpath=os.path.join("資料庫","[完成]"+str(year)+"年搜尋資料庫.txt")
    if str(year)==datetime.datetime.now().strftime("%Y"):
        cpath=os.path.join("資料庫",str(year)+"年搜尋資料庫.txt")
    with open(cpath, 'r+' , encoding='UTF-8') as f:
        alltxt=f.read().split("\n")
        del alltxt[0]
    target="no"
    for i in range(0,len(alltxt),2):
        if target == "no":
            if int(alltxt[i][:2].strip()) <= mont: ##int()自動把0變不見
                target = "focus"
        elif  target == "focus":    
            if int(alltxt[i][3:5].strip())<=dayt:
                target = "target"
        elif target == "target":
            if movie in alltxt[i]:            #漸進式的選擇出開始的時間，像打檔一樣
                abouttalk.append(alltxt[i])
                abouttalk.append(alltxt[i+1])

    for i in range(0,len(abouttalk)):
        data=str(abouttalk[i])
        if "Re" not in str(data):
            tt = data.replace(" ","")
            if "雷]" in tt and "[有雷]" not in tt and "[無雷]" not in tt and "[結局雷]" not in tt and "[討論雷]" not in tt and "[雷]" not in tt and "[微雷]" not in tt and "[問雷]" not in tt  :
                if "[" not in tt and "]" in tt:
                    tt1 = 5
                    tt2 = tt.index("]")
                elif "]" not in tt and "[" in tt:
                    continue
                else:
                    tt1 = tt.index("[")+1
                    tt2 = tt.index("]")
                tt=tt[tt1:tt2]
                goodbad.append(tt) #擷取[]內的評價
    return goodbad,abouttalk

def searchless(year,monf,dayf,monl,dayl,movie):#兩者互用 #直接回傳輸出字串
    goodbad=[]#有雷的
    comment=[]#過濾後的雷的
    cindex=[]
    abouttalk=[]#有電影標題的討論
    alltxt=[]#取出來的原始資料
    cpath=os.path.join("資料庫","[完成]"+str(year)+"年搜尋資料庫.txt")
    if str(year)==datetime.datetime.now().strftime("%Y"):
        cpath=os.path.join("資料庫",str(year)+"年搜尋資料庫.txt")
    with open(cpath, 'r+' , encoding='UTF-8') as f:
        alltxt=f.read().split("\n")
        del alltxt[0]
    
    target="no"
    for co in range(0,len(alltxt),2):
        if target == "no":
            if int(alltxt[co][:2].strip()) <= monl: ##int()自動把0變不見
                target = "focus"
        elif  target == "focus":    
            if int(alltxt[co][3:5].strip())<=dayl:
                target = "target"
        elif target == "target":
            if int(alltxt[co][:2].strip()) == monf and int(alltxt[co][3:5].strip()) < dayf:
                break
            elif int(alltxt[co][:2].strip()) < monf:
                break
            elif movie in alltxt[co]:
                abouttalk.append(alltxt[co])
                abouttalk.append(alltxt[co+1])
    
    for i in range(0,len(abouttalk)):
        data=str(abouttalk[i])
        if "Re" not in str(data):
            tt = data.replace(" ","")
            if "雷]" in tt and "[有雷]" not in tt and "[無雷]" not in tt and "[結局雷]" not in tt and "[討論雷]" not in tt and "[雷]" not in tt and "[微雷]" not in tt and "[問雷]" not in tt  :
                if "[" not in tt and "]" in tt:
                    tt1 = 5
                    tt2 = tt.index("]")
                elif "]" not in tt and "[" in tt:
                    continue
                else:
                    tt1 = tt.index("[")+1
                    tt2 = tt.index("]")
                tt=tt[tt1:tt2]
                goodbad.append(tt) #擷取[]內的評價
    for i in range(0,len(goodbad)):
        if goodbad[i] not in comment:
            comment.append(str(goodbad[i])) #重複的評價整理成同一個，並且給予數字
    for i in range(0,len(comment)):
        cindex.append(str(goodbad.count(comment[i])))
    lay=totmato(comment,cindex,movie)
    return lay,abouttalk

def totmato(comment,cindex,movie):
    ggg=0
    bgg=0
    ngg=0
    total=0
    gg=[0,0]
    for i in range(0,len(comment)):
        cindex[i]=int(cindex[i])
        comment[i]=str(comment[i])
        if "好" in comment[i] or "爽雷" in comment[i] or"感動" in comment[i]:
            ggg+=cindex[i]
        elif "負雷" in comment[i] or "爛雷" in comment[i] or "負無雷" in comment[i] or "糞" in comment[i] or "爛" in comment[i] or "負微雷" in comment[i]:
            bgg+=cindex[i]
        elif "普" in comment[i]:
            ngg+=cindex[i]
        else:
            pass
    total=ggg+bgg+ngg
    if total==0:
        return"目前沒有人對這部電影進行評分ㄛ"
        
    else:
        score=(ggg*1+bgg*0+ngg*0.5)/total*100
        score=round(score , 2)
        gg[0]=score
    if (score>=95 and total>=10) or  (score>=90 and total>=20) or  (score>=85 and total>=30) or (score>=80 and total>=50):
        gg[1]="壓倒性好評，膾炙人口！"
    elif (score>=85 and total>=10) or (score>=85 and total>=20) or  (score>=80 and total>=30):
        gg[1]="極度好評，佳評如潮"
    elif score>=80:
        gg[1]="好評，還不錯"
    elif score>=70:
        gg[1]="大致好評"
    elif score>=40:
        gg[1]="褒貶不一，眾說紛紜"
    elif 25<=score<=35 and total>=10:      
        gg[1]="爛片，不要去看，很鳥"
    elif 15<=score<=25 and total>=10:      
        gg[1]="大糞片，你如果想感受甚麼叫做絕望就去看"
    elif 10<=score<=15 and total>=10:
        gg[1]="糞到極值，觀影前進記得要戴墨鏡！！！！！" 
    elif 5<=score<=10 and 20>=total>=10:
        gg[1]="這到底這到底這到底是甚麼爛片喔喔喔喔喔喔喔喔喔喔喔喔喔喔喔"
    elif (5<=score<=10 and total>=20) or (score<=5 and total>=10):
        gg[1]="這部片穿越了時空，跨越了人類歷史，是文明史誕生以來最邪惡的藝術結晶，他混合了這個世界上最可怕以及最噁心的爛片元素，一部片如果能夠爛成這樣，不僅僅是代表著影史上的黑暗，同時也代表著我們人類對於這個世紀的絕望以及困頓有多麼巨大，才能夠拍出來這樣的大爛糞片"
    elif score>=30 or (score<=30 and total<=10):
        gg[1]="大致壞評，觀影前三思"
    
    if 1<total<5:
        gg[1]=gg[1]+"\n目前搜尋到此片的影評不到五篇，請斟酌考量"
    else:
        pass
    
    coin=str(movie)+"的評價結果是:"+str(gg[1])+"\n總評價分數為"+str(gg[0])+"%  (0%為最負評，100%為最好評)"
    coin+="\n總共有："+str(total)+"則評價。"
    allcom=""
    for i in range(0,len(comment)-1):
        allcom+=(str(comment[i])+"有"+str(cindex[i])+"則"+"，")
    allcom+=str(comment[len(comment)-1])+"有"+str(cindex[len(cindex)-1])+"則"+"。"
    lay=coin+"\n"+allcom
    return lay


def MENU():
    print("=======MENU=======")
    print("以下是美人魚我能夠提供的功能：\n1.查詢最近幾天內的特定電影評價\n2.列出最近上映的電影\n3.指定期間內的特定電影評價\n4.檢查資料庫狀況並重新載入\n5.離開程式")
    print("請輸入功能編號(阿拉伯數字)，輸入後按enter：")
    choice=askintsmart(1,5)
    ##################################################
    if (choice==1):
        while(True):
            print("請輸入要查詢的特定電影名稱")
            movie=askstr()
            print("請輸入要查詢幾天內的影評，未輸入天數則預設為3個月內")
            print("請輸入天數(整數阿拉伯數字)：")
            askday=askintplus()
            temp_date = datetime.datetime.now()
            new = temp_date + datetime.timedelta(days=-askday)
            new=new.date()
            old = datetime.date(2004, 1, 8)
            if new < old:
                print("你輸入的天數已超過Ptt所有文章範圍")
                break
            day2 = temp_date.strftime("%Y%m%d")
            day1 = (temp_date + datetime.timedelta(days=-askday)).strftime("%Y%m%d")
            print("小美人魚出海為你搜尋資訊~~~")
            lay, abouttalk =search(movie,day1,day2)
            print("\n"+lay)
            print()
            date = datetime.datetime.now().strftime("%Y%m%d")
            path=date+movie+str(askday)+"天內的影評查詢結果.txt"
            path=os.path.join("輸出資料夾",path)
            exist=os.path.isfile(path)
            i=1
            while(exist):
                path=date+movie+str(askday)+"天內的影評查詢結果"+" ("+str(i)+").txt"
                path=os.path.join("輸出資料夾",path)
                exist=os.path.isfile(path)
                i+=1
            with open(path, 'w' , encoding='UTF-8') as f: 
                    print(lay+"\n",file=f)
                    
            date = datetime.datetime.now().strftime("%Y%m%d")
            f = open(path, 'a+', encoding='UTF-8')########請愛用a+，用w就要想到覆蓋問題
            for data in abouttalk:
                print(data,file=f)
            
            print("小美人魚海巡完畢~請至輸出資料夾查看查詢文件~相關討論串已經放入資料夾了")
            break


    if(choice==2):
        while(True):
            print("本程式是利用Yahoo電影以提供最新的上映電影名單\n以下順序以最新上映的為最優先顯示\n已下映的電影不會顯示\n請等待大約5~10秒的運作時間")
            mlist=yahoo.yahoo()
            for movie in mlist:
                print(movie)
            date = datetime.datetime.now().strftime("%Y%m%d")
            path=date+"電影上映查詢結果.txt"
            path=os.path.join("輸出資料夾",path)
            exist=os.path.isfile(path)
            i=1
            while(exist):
                path=date+"電影上映查詢結果"+" ("+str(i)+").txt"
                path=os.path.join("輸出資料夾",path)
                exist=os.path.isfile(path)
                i+=1
            with open(path, 'w' , encoding='UTF-8') as f: 
                for movie in mlist:
                    print(movie,file=f)
            print("小美人魚海巡完畢~請至輸出資料夾查看查詢文件~")
            break
    
    if(choice==3):
        while(True):    
            print("請輸入要查詢的特定電影名稱")
            movie=askstr()
            time1, time2=asktime()
            print("小美人魚出海為你搜尋資訊~~~")
            lay, abouttalk =search(movie,time1,time2)
            lay = "以下為"+time1+"至"+time2+"的影評搜尋結果：\n"+lay
            print("\n"+lay)
            print()
            date = datetime.datetime.now().strftime("%Y%m%d")
            path=date+movie+time1+"至"+time2+"的搜尋結果.txt"
            path=os.path.join("輸出資料夾",path)
            exist=os.path.isfile(path)
            i=1
            while(exist):
                path=date+movie+time1+"至"+time2+"的搜尋結果"+" ("+str(i)+").txt"
                path=os.path.join("輸出資料夾",path)
                exist=os.path.isfile(path)
                i+=1
            with open(path, 'w' , encoding='UTF-8') as f: 
                    print(lay+"\n",file=f)
                    
            
            date = datetime.datetime.now().strftime("%Y%m%d")
            f = open(path, 'a+', encoding='UTF-8')########請愛用a+，用w就要想到覆蓋問題
            for data in abouttalk:
                print(data,file=f)
            print("小美人魚海巡完畢~請至輸出資料夾查看查詢文件~相關討論串已經放入資料夾了")
            break


    if(choice==4):
        print("請問要重新檢查資料庫嗎？將會將所有資料庫進行更新，有可能會需要超過5分鐘以上的時間")
        print("要的話輸入1，不要話輸入2")
        anw = askintsmart(1,2)
        if anw == 1:
            databasestarter.databasestarter()
            print("更新完畢，回到MENU")
        else:
            print("回到MENU")
        
    if(choice==5):
        print("Bye~Bye❤")
        sys.exit()


def asktime():
    while(True):
        flag = False
        now = datetime.datetime.now().date()
        old = datetime.date(2004, 1, 8)
        print("請輸入指定期間，先輸入較遠的日期，再輸入較近的日期")
        today = datetime.datetime.now().strftime("%Y%m%d")
        yestarday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        print("日期請輸入符合格式的年月日，以今天來說就是："+today)
        anw1=input("較遠的日期：")
        if not anw1 == "":
            if anw1.isdigit() and len(anw1)==8:
                try:
                    anw1date = datetime.date(int(anw1[:4]), int(anw1[4:6]), int(anw1[6:8]))
                except:
                    print("你輸入的日期格式不正確，請重新輸入")
                    continue
                else:
                    if now > anw1date >= old:
                        flag = True
                    else:
                        print("輸入錯誤，已超過Ptt有效文章範圍，請你輸入範圍內的數字，Ptt最老的一篇文章是2004年1月8號的文章")
            else:
                print("輸入錯誤，請你輸入有效數字")
        if(flag):
            anw2=input("較近的日期：")
            if not anw2 == "":
                if anw2.isdigit() and len(anw2)==8:
                    try:
                        anw2date = datetime.date(int(anw2[:4]), int(anw2[4:6]), int(anw2[6:8]))
                    except:
                        print("你輸入的日期格式不正確，請重新輸入")
                        continue
                    else:
                        if now >= anw2date > old:
                            if anw1date < anw2date:
                                break
                            else:
                                print("輸入錯誤，第二次輸入請輸入較近的日期，例如第一次輸入為"+today+"，第二次輸入就不能是"+yestarday+"，要輸入之後的日期")
                        else:
                            print("輸入錯誤，已超過Ptt有效文章範圍，請你輸入範圍內的數字")
                else:
                    print("輸入錯誤，請你輸入有效數字")
            else:
                print("輸入錯誤，請你輸入有效數字")
    return anw1 ,anw2


def askintplus():
    while(True):
        anw=input("：")
        if anw=="":
            anw=90
        if str(anw).isdigit():
            if 0<int(anw):
                anw=int(anw)
                break
        print("輸入錯誤，請你輸入正整數")
    return anw

def askintsmart(min,max):
    while(True):
        anw=input("：")
        if not anw == "":
            if str(anw).isdigit():
                if min<=int(anw)<=max:
                    anw=int(anw)
                    break
        print("輸入錯誤，請你輸入範圍內的數字")
    return anw


def askstr():
    while(True):
        anw=input("：")
        if not anw == "":
            break
        print("輸入錯誤，請勿輸入空白")
    return anw


########起頭
print("❤Hello, stranger❤\n❤我是PTT Movie版的水水小美人魚❤\n❤跟風的我能夠告訴你最近Movie版上發文者對於電影的大致評價❤\n❤讓你知道最近又在紅甚麼電影~❤\n❤隨時都能跟上流行喔❤\n#注意，功能2目前壞掉待維修，因Yahoo電影網站關閉")
dirpath=os.path.join("輸出資料夾")
if not os.path.isdir(dirpath):
    os.mkdir("輸出資料夾")
while(True):
    MENU()


