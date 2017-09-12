# /usr/env python
#_*_coding:utf-8_*_

import pymysql
import requests
from bs4 import BeautifulSoup
import re
import time

class  GetMobileDetailInfo(object):

    def __init__(self):
        self.mobileId = None
        self.marketTime = None
        self.touchScreenType = None
        self.screenSzie = None
        self.os = None
        self.cpuCount = None
        self.cpuType = None
        self.cpuRate = None
        self.ram = None
        self.rom = None
        self.sensorType = None

        print("Began to get detail info of the mobile")

    def getMobileId(self):

        conn = pymysql.connect(host='192.168.3.193', user='root', passwd='cyhc2017', db='mobile',charset = 'utf8')
        cur = conn.cursor()
        cur.execute("select count(1) from mobile_model")
        brandCount = cur.fetchone()

        print(brandCount[0])
        for index in range(brandCount[0]):
            cur.execute("select id from mobile_model limit %s,%s" % (index, index + 1))

            id = str(cur.fetchone()[0])
            self.getMobileParam(id)
        conn.close()

    def getMobileParam(self,id):

        paramUrl = "http://detail.zol.com.cn/1175/"+id+"/param.shtml"

        print("*****************"+paramUrl+"********************")

        paramPage = requests.get(paramUrl)

        soup = BeautifulSoup(paramPage.text)


        allParamNames =soup.find_all('span',attrs={'class':"param-name"})
        self.mobileId = id
        sensorType = None
        for paramName in allParamNames:
            if paramName.get_text() == '上市日期':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.marketTime = soup.find_all(id='newPmVal_'+id[0])[0].get_text()
            elif paramName.get_text() == '触摸屏类型':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.touchScreenType = soup.find_all(id='newPmVal_'+id[0])[0].get_text()
            elif paramName.get_text() == '主屏尺寸':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.screenSzie = soup.find_all(id='newPmVal_'+id[0])[0].get_text()
            elif paramName.get_text() == '操作系统':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                print(id)
                self.os = soup.find_all(id='newPmVal_'+id[1])[0].get_text()
            elif paramName.get_text() == '核心数':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.cpuCount = soup.find_all(id='newPmVal_'+id[0])[0].get_text()
            elif paramName.get_text() == 'CPU型号':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.cpuType = soup.find_all(id='newPmVal_'+id[0])[0].get_text()
            elif paramName.get_text() == 'CPU频率':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.cpuRate = soup.find_all(id='newPmVal_'+id[0])[0].get_text()

            elif paramName.get_text() == 'RAM容量':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.ram = soup.find_all(id='newPmVal_'+id[0])[0].get_text()
            elif paramName.get_text() == 'ROM容量':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.rom = soup.find_all(id='newPmVal_'+id[0])[0].get_text()
            elif paramName.get_text() == '感应器类型':
                mode = re.compile(r'\d+')
                id = mode.findall(str(paramName))
                self.sensorType = soup.find_all(id='newPmVal_' + id[0])[0].get_text()
        #allInfo = soup.find_all("li")


        print(self.mobileId)
        print(self.marketTime)
        print(self.touchScreenType)
        print(self.screenSzie)
        print(self.os)
        print(self.cpuCount)
        print(self.cpuType)
        print(self.cpuRate)
        print(self.ram)
        print(self.rom)
        print(self.sensorType)

        sql = "INSERT INTO mobile_model_info (`id`, `market_time`, `touch_screen_type`, `screen_szie`, `os`, `cpu_count`, `cpu_type`, `cpu_rate`, `ram`, `rom`, `sensor_type`, `insert_time`) " \
              "VALUES ('%s', '%s','%s', '%s', '%s', '%s', '%s', '%s',' %s', '%s','%s',' %s')"\
              %(self.mobileId,self.marketTime,self.touchScreenType,self.screenSzie,self.os,self.cpuCount,self.cpuType,self.cpuRate,self.ram,self.rom,self.sensorType,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #print(sql)
        existSql = "select * from mobile_model_info where id = %s" % self.mobileId
        result = self.storeModelDate(existSql)
        print(result)
        if result > 0:
            print("This model was existed!")
        else:
            print(sql)
            # sql = "INSERT INTO `mobile`.`mobile_model_info` (`id`, `name`, `market_time`, `touch_screen_type`, `screen_szie`, `os`, `cpu_count`, `cpu_type`, `cpu_rate`, `gpu_type`, `ram`, `rom`, `sensor_type`, `insert_time`) " \
            #       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
            #       mobileId, marketTime, touchScreenType, screenSzie, os, cpuCount, cpuType, cpuRate, ram, rom,
            #       sensorType, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # print(sql)
            try:
                print(self.storeModelDate(sql))
            except Exception as e:
                print(e)
    def storeModelDate(self,sql):

        conn = pymysql.connect(host='192.168.3.193', user='root', passwd='cyhc2017', db='mobile',charset = 'utf8')
        cur = conn.cursor()
        result = cur.execute(sql)
        conn.commit()
        conn.close()
        return result


if __name__ == "__main__":
    mobileInfo = GetMobileDetailInfo()
    mobileInfo.getMobileId()


