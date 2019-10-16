from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib import urlopen as uReq  # Web client
import csv
import pandas as pd

semts=["atasehir","beykoz","cekmekoy","kadikoy","kartal","kucukcekmece","maltepe","pendik","sancaktepe","sultanbeyli","sile","tuzla","umraniye","uskudar"]


def strToNum(s):
    i=s.find('.')
    if(i!=-1):
        s=s[0:i] + s[i+1:]
    return int(s)/20
for semt in semts:
    page_url = "https://www.hurriyetemlak.com/"+semt+"-satilik"

    buildings=[]
    count=0
    page_limit=2
    page=1
    while (page != page_limit):
        pagesUrl=page_url+"?page="+str(page)
        print("Semt: "+semt+" Sayfa : " + str(page))


        # opens the connection and downloads html page from url
        uClient = uReq(page_url)

        page_soup = soup(uClient.read(), "html.parser")
        uClient.close()
        rows=page_soup.findAll("div",{"class":"list-item timeshare clearfix"})
        
        if(page==1):
            numberofPost=page_soup.findAll("strong",{"data-ads-count":""})
            page_limit=strToNum(numberofPost[5].text)

        for r in rows:
            suburl="https://www.hurriyetemlak.com"+r.a["href"]
            count+=1
            try:
                RuClient= uReq(suburl)
            except:
                print("Processing... "+ str(count))
                continue
            page_detail = soup(RuClient.read(),"html.parser")
            RuClient.close()
            
            try:
                price=page_detail.find("li",{"class":"price-line clearfix"})
                pr = price.span.text
                adress=page_detail.find("li",{"class":"address-line"})
                add = adress.span.text
                info=dict()
                
                phones=page_detail.find("ul",{"class":"phone-numbers"})

                info["Telefon No"]=phones.li.a.text

                ilanID= page_detail.find("li",{"class":"realty-numb"})

                idModi=ilanID.span.text[8:-1]
                info["Ilan No"]=idModi
                

                info["Baslik"]=page_detail.h1.text
                info["Fiyat"]=pr
                add=add.replace('\n','')
                v=add.split('/')
                info["Sehir"]=v[0]
                info["Semt"]=v[1]
                info["Mahalle"]=v[2]
                infos=page_detail.findAll("li",{"class":"info-line"})
                infoList=infos[0].ul.findAll("li")
                for i in range(0,len(infoList)-1):
                    rc=infoList[i].findAll("span")
                    s=rc[1].text
                    if(s[0:5]=="Uygun"):
                        s="Uygun"
                    info[rc[0].text]=s
                buildings.append(info)
            except:
                continue
        page+=1
    df=pd.DataFrame.from_records(buildings)
    df.to_excel(semt+".xlsx",sheet_name="Sheet_1")
