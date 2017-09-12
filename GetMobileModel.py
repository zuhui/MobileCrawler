# /usr/env python

import pymysql
import requests
from bs4 import BeautifulSoup
import re
import time



class GetMobileModel(object):

    def __init__(self):
        print("began to get the mobile model")

    def getMobileModel(self):

        mobileUrl = "http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html"
        while mobileUrl:

            tempUrl = mobileUrl
            print("********%s*************"%mobileUrl)
            modelPage = requests.get(mobileUrl)

            #print(modelPage.text)
            soup = BeautifulSoup(modelPage.text)

            nextPage = soup.find_all("small-page-next",href = True)
            print(nextPage)
            allUrls = soup.find_all("a",href =True)

            for url in allUrls:
                #print(url)
                if "/cell_phone_index/subcate57_0_list_1_0_1_2" in url.get("href"):
                    print(url)
                    mobileUrl = "http://detail.zol.com.cn/"+url.get("href")
                elif "/cell_phone/index" in url.get("href") and url.get("title") !='' and url.get("title")!=None:

                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    modelName = url.get("title").replace("'","").split("）")
                    modelUrl  = url.get("href")
                    mode = re.compile(r'\d\d+')
                    id = mode.findall(url.get("href"))
                    print(url)
                    print(modelName)
                    print(modelUrl)
                    print(id)

                    existSql = "select * from mobile_model where id = %s" % id[0]
                    result = self.storeModelDate(self,existSql)
                    print(result)
                    if result > 0:
                        continue
                    else:
                        sql = "INSERT INTO `mobile`.`mobile_model` (`id`, `model_name`, `model_url`, `insert_time`) VALUES(%s,'%s','%s','%s')" % (id[0], str(modelName[0])+"）", str(modelUrl), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        print(sql)
                        try:
                            self.storeModelDate(self,sql)
                        except Exception:
                            print(Exception)
                            continue
                    print("********************************")

            if tempUrl == mobileUrl:
                break

    def storeModelDate(self,sql):
        conn = pymysql.connect(host='192.168.3.193', user='root', passwd='cyhc2017', db='mobile',charset = 'utf8')
        cur = conn.cursor()
        result = cur.execute(sql)

        conn.commit()

        conn.close()
        return result

    def getBrandUrl(self):
        conn = pymysql.connect(host='192.168.3.193', user='root', passwd='cyhc2017', db='mobile',charset = 'utf8')
        cur = conn.cursor()
        cur.execute("select count(*) from mobile_brand")
        brandCount = cur.fetchone()

        print(brandCount[0])
        for index in range(brandCount[0]):
            cur.execute("select url from mobile_brand limit %s,%s" % (index, index + 1))

            brandUrl = cur.fetchone()[0]

            print("began to get:%s:"%brandUrl)

            self.getMobileModel()
        conn.close()


if __name__ == "__main__":

    mobileModel = GetMobileModel
    #mobileModel.getBrandUrl(mobileModel)
    mobileModel.getMobileModel(mobileModel)
