# /usr/env python

import pymysql
import requests
from bs4 import BeautifulSoup



class GetMobileModel(object):

    #def __init__(self):

    def getMobileModel(url):
        modelPage = requests.get(url)

        soup = BeautifulSoup(modelPage.text,from_encoding="gbk")
        print(soup.decode("gbk"))

    def getBrandUrl(self):
        conn = pymysql.connect(host='192.168.3.193', user='root', passwd='cyhc2017', db='mobile',charset = 'utf8')
        cur = conn.cursor()
        cur.execute("select count(*) from mobile_brand")
        brandCount = cur.fetchone()

        print(brandCount[0])
        for index in range(brandCount[0]):
            cur.execute("select url from mobile_brand limit %s,%s" % (index, index + 1))

            brandUrl = cur.fetchone()[0]

            print("began:%s:data"%brandUrl)

            self.getMobileModel(brandUrl)
        conn.close()


if __name__ == "__main__":

    mobileModel = GetMobileModel
    mobileModel.getBrandUrl(mobileModel)
