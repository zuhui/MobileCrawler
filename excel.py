# /usr/env python
#_*_coding:utf-8_*_

import xlrd


class ReadExcel(object):
    def __init__(self,excelFileName,tableIndex):

        self.excelFileName = excelFileName
        self.tableIndex = tableIndex


    def getData(self):
        excelData = xlrd.open_workbook(self.excelFileName)

        excelTable = excelData.sheets()[self.tableIndex]

        excelRows = excelTable.nrows

        for index in range(excelRows):

            #打印正行的值
           # print(excelTable.row_values(index))

            #打印单元格的值
            print(excelTable.cell(index,1).value)
            excelTable.cell(index,0).value = "xiaomi"

if __name__ == "__main__":

    excelFile = ReadExcel("和换机所需机型.xlsx",1)
    excelFile.getData()