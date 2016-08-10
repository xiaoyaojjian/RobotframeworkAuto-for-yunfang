# encoding: utf-8
# !C:\Python27
# Filename: TestDataLib.py

import MySQLdb
import os, sys
from robot.libraries.BuiltIn import BuiltIn


class TestDataLib:
    conn = ''
    cursor = ''

    def __init__(self, host='localhost', user='root', password='root', db='robot_result'):
        try:
            self.conn = MySQLdb.connect(host, user, password, db,charset='utf8')
        except Exception, e:
            print e
            sys.exit()
        self.cursor = self.conn.cursor()

    def _query(self, sql):
        return self.cursor.execute(sql)

    def _show(self):
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def _get_test_data(self,caseName,dataName ):
        """根据数据名称和用例名获取数据列表，返回一个List
        """
        strsql = 'SELECT '
        for index in range(len(dataName)):
            if index == len(dataName)-1:
                strsql =strsql+ ' max(if(dataName=\''+dataName[index]+'\',dataContent,\'\'))'
            else:
                strsql =strsql+ ' max(if(dataName=\''+dataName[index]+'\',dataContent,\'\')),'
        strsql = strsql +' FROM	dict_test_data td WHERE	EXISTS (	SELECT 1 FROM	dict_test_case tc	 WHERE	tc.id = td.caseId AND tc.caseName = \''+caseName+'\')'
        strsql = strsql +' GROUP BY groupid'
        print strsql
        self._query(strsql)
        data = self._show()
        return  data

    def run_keyword_by_testdata(self,caseName,keywordName, *dataName):
        """根据用例名称去查询数据库，获取测试数据，并运行指定关键字
            参数说明：caseName<数据库测试数据的用例名>
                      keywordName<需要运行的关键字名称>
                      dataName<数据库中测试数据的中文名称>
            例子：
            | Run Keyword By Testdata | 用例名称 | 某个关键字 | 参数名称1 | 参数名称2 | 参数名称3 | 参数名称4 |
        """
        data = self._get_test_data(caseName,list(dataName))
        bi = BuiltIn()
        for i in data:
            args = tuple(i)
            bi.run_keyword_and_continue_on_failure(keywordName,*args)

if __name__ == '__main__':
    td = TestDataLib()
    '''data = td.get_test_data('线上业务',['流水号','交易编号','物业地址'])
    for i in data:
        print i[2]
    #print data'''
    #td.run_keyword_by_testdata('线上业务','name','流水号','交易编号','物业地址')
