# import os
# import sys
import re

from selenium.webdriver.remote.webelement import WebElement
from Selenium2Library.locators import TableElementFinder
from Selenium2Library.locators import ElementFinder
# from Selenium2Library import Selenium2Library
from robot.libraries.BuiltIn import BuiltIn


class RobotExt(TableElementFinder):
    def get_table_values(self, table_locator):
        selenium2lib = BuiltIn().get_library_instance('Selenium2Library')

        # self._table_element_finder = TableElementFinder()
        dict = {}
        key = None
        # table = selenium2lib._table_element_finder.find(selenium2lib._current_browser, table_locator)
        table = selenium2lib._element_find(table_locator, True, True)
        if table is not None:
            rows = table.find_elements_by_xpath("./tbody/tr")
            # BuiltIn().log("######rows"+str(len(rows)))
            # return rows
            if len(rows) > 0:
                for row in rows:
                    columns = row.find_elements_by_tag_name('td')
                    # BuiltIn().log('##### NO fdf row have '+str(len(columns))+' cell')
                    # return columns[1].text
                    if len(columns) > 0:
                        for i in range(len(columns)):
                            # return range(len(columns)-1)
                            # BuiltIn().log('##########No '+str(i)+' for ')
                            if (i + 1) % 2 == 1:
                                try:
                                    key = columns[i].find_elements_by_tag_name('label')[0].text
                                except Exception, ex:
                                    key = ''
                                if len(key) == 0:
                                    # BuiltIn().log('########## key is null ##########')
                                    break
                                key = key[0:len(key) - 1]
                                # BuiltIn().log('##########key = '+key+'  ')
                            else:
                                dict[key] = columns[i].text
                                # BuiltIn().log('##########value = '+columns[i].text+'  ')

            return dict

    def get_dict_value(self,key,**dict):
        value = dict[key]
        return value

    def string_to_list(self,str):
        str = str.replace('(',',')
        str = str.replace(')','')
        ls =str.split(',')
        return ls