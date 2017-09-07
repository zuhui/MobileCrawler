# /usr/env python



import requests
import re
import time
import pymysql
from bs4 import BeautifulSoup



class GetMobileInfo():
    url = "http://product.cnmo.com/search?s="
    def __init__(self,model):
        self.model = model

    def getMobileInfo(self):
        mobileUrl = "http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html"

        mobilePage = requests.get(mobileUrl)

        soup = BeautifulSoup(mobilePage.text)
        #print(soup)

        detailUrls = soup.find_all("a",href=True)
        #print(detailUrls)
        for url in  detailUrls:
            if "/cell_phone_index/subcate57" in url.get("href"):
                print("-------------------------------------------------------")
                print(url)
                mobileHref = url.get("href")
                name = url.get_text()
                mode = re.compile(r'\d\d+')
                id = mode.findall(url.get("href"))
                print(mobileHref)
                print(name)
                print(id)

                existSql = "select * from mobile_brand where id = %s"%id[1]
                result = self.storeDate(existSql)
                print(result)
                if name == '' or name.strip()=='' or result>0:
                    continue
                else:
                    sql = "insert into mobile_brand(id,name,url,insert_time) VALUES (%s,'%s','%s','%s')"%(id[1],str(name),str(mobileHref),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    self.storeDate(sql)



        # print(mobilePage.content.decode(mobilePage.encoding))

    def storeDate(self,sql):
        conn = pymysql.connect(host='192.168.3.193', user='root', passwd='cyhc2017', db='mobile',charset = 'utf8')
        cur = conn.cursor()
        result = cur.execute(sql)

        conn.commit()

        conn.close()
        return result


if __name__=="__main__":

    mobile = GetMobileInfo("N1T")
    #mobile.storeDate()
    mobile.getMobileInfo()
