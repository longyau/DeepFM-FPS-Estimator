from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import csv
import time
import asyncio
from threading import Thread
###declare a python object to store all CPU information
class Component(object):
    def add_info(self, name,value):
        self.__setattr__(name,value)
    def get_detail(self):
        return repr(self.__dict__)
    def __iter__(self):
        for key,value in self.__dict__.items():
            yield key, value
            # print('KEY:{0},VAL:{1}'.format(key,value))
        # yield 'a', self.a
        # yield 'b', self.b
        # yield 'c', self.c
    def get_all_info(self):
        keys=[]
        values=[]
        for key,value in self.__dict__.items():
            keys.append(key)
            values.append(value)
        return keys,values
        # cpuList.append(row)
####get data from w
# data=[["Name",".res-ca"],["Score",".uc-score .uc-score-cap"]]
# sites=["https://www.techpowerup.com/cpudb/?ajaxsrch="]
# for index,item in enumerate(data):ebsite
# path="D:/Project/PythonMachineLearning/pcConfig/res/chromedriver_win32/chromedriver.exe"
#     print("data[",index,"] Name:",item[0]," CSS:",item[1])
# browser=webdriver.Chrome(path)
    # w = csv.writer(outputfile,delimiter=',')

###search through techpowerup.com for each CPU model
def site1(cpu_list,browser:webdriver.Chrome=webdriver.Chrome('res/chromedriver_win32/chromedriver.exe')):
    for cpu in cpu_list:
        browser.get("https://www.techpowerup.com/cpudb/?ajaxsrch=" + cpu.Model)
        try:
        # if str(browser.find_element_by_tag_name('body').get_attribute('innerHTML')).__contains__('Nothing found.'):
        #     return
            cols = []
            headRow = browser.find_elements_by_css_selector('thead tr th')
            for cell in headRow:
                cols.append(cell.get_attribute('innerHTML'))
            contentRow = browser.find_element_by_css_selector('tbody tr').find_elements_by_tag_name('td')
            for index, cell in enumerate(contentRow):
                try:
                    data = cell.find_element_by_tag_name('a')
                except exceptions.NoSuchElementException:
                    data = cell
                cpu.__setattr__(cols[index], data.get_attribute('innerHTML'))
        except exceptions.NoSuchElementException:
            continue
    browser.close()


###search through price.com.hk for each CPU data
def site2(cpu_list,browser:webdriver.Chrome=webdriver.Chrome('res/chromedriver_win32/chromedriver.exe')):
    for cpu in cpu_list:
        browser.get("https://www.price.com.hk/search.php?g=A&q=" + cpu.Model)
        try:
            cpu.__setattr__('Price', str(browser.find_element_by_css_selector('.list-product .text-price-number').get_attribute('innerHTML')).replace(',',''))
        except exceptions.NoSuchElementException:
            continue
    browser.close()


###The entire workflow of this program
###Check for each row in benchmark CSV
###Check "techpowerup.com" and "price.com.hk"
###Integrate all information and store it into txt files according to model name
def main():
    start=time.time()
    cpuList = []
    with open('res/CPU_UserBenchmarks.csv', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader):
            # if index > 5:
            #     break
            cmp = Component()
            for key, itm in row.items():
                cmp.add_info(key, itm)
            cpuList.append(cmp)
    t=Thread(target=site1,args=[cpuList])
    t.start()
    t2=Thread(target=site2,args=[cpuList])
    t2.start()
    t.join()
    t2.join()
    print('finish')
        # browser = webdriver.Chrome(path)

    # browser.close()
    ####get data from website
    # with open('res/CPU_Data.csv','w', encoding='utf8') as outputfile:
    #     w = csv.writer(outputfile,delimiter=',')
    #     fieldnames,_=cpuList[0].get_all_info()
    #     w.writerow(fieldnames)
    #     for cpu in cpuList:
    #         _,values=cpu.get_all_info()
    #         # DD=list(cpu)
    #         # print(DD)
    #         # print(cpu.get_detail())
    #         w.writerow(values)
    #     # w.writerows(cpuList)
#####write information to file
    with open('res/CPU_Data.txt','w', encoding='utf8') as output_file:
        fieldnames, _ =cpuList[0].get_all_info()
        for field in fieldnames:
            output_file.write(field + '\t')
        output_file.write('\n')
        # w.writerow(fieldnames)
        for cpu in cpuList:
            # _, values = cpu.get_all_info()
            # for value in values:
            for field in fieldnames:
                try:
                    value=cpu.__getattribute__(field)
                    output_file.write(value + '\t')
                except AttributeError:
                    output_file.write('\t')
            output_file.write('\n')
            # w.writerow(values)
#####write information to file
            print(cpu.get_detail())
            # print('-------------------------------')
        end=time.time()
        print('Complete in {} seconds'.format(end-start))
main()