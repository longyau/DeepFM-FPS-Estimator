from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
from threading import Thread
import os
import urllib.parse as urllib
###declare a new object in python
class GPU(object):
    def add_info(self, name,value):
        value=str(value)
        self.__setattr__(name,value)
    def get_detail(self):
        return repr(self.__dict__)
    def __iter__(self):
        for key,value in self.__dict__.items():
            yield key, value
    def get_all_info(self):
        keys=[]
        values=[]
        for key,value in self.__dict__.items():
            keys.append(key)
            values.append(value)
        return keys,values

###Declare a exception in python for for-loop handling
class ContinueExcep(Exception):
    pass

###Declare a function for string replacement
def replace_string(original_str:str):
    remove_strings=['\n','\t','\r','<br>']
    target_str=original_str
    for remove_string in remove_strings:
        target_str=target_str.replace(remove_string,'')
    return target_str

###declare a function for website timeout
def timeout_site(browser,CSS:str):
    delay = 7
    try:
        result = WebDriverWait(browser, delay).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, CSS))
        )
    except exceptions.TimeoutException:
        print('Timed Out')
        return False
    return True

###declare a function for HTML scrapping on GPU specification data
def site1(series:str,gpu_links:[],prefs:dict={"profile.managed_default_content_settings.images": 2}):
    if len(gpu_links)<1:
        return
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('res/chromedriver_win32/chromedriver.exe',chrome_options=chromeOptions)
    get_partial_content={'Compatibility':["Direct X","Shader","Open GL"]}
    get_all_content=["GPU","Memory","Power"]
    get_specific_content={"GD RATING":".hardware-info-value .specificationsCenterText img","Core Speed":".hardware-info-value div"}
    for link in gpu_links:
        singleElement=get_partial_content.copy()
        multiElement=get_all_content.copy()
        specialElement=get_specific_content.copy()
        no_name=0
        game=GPU()
        game.add_info('Website',link)
        link=str(link)
        link=urllib.unquote(link)
        try:
            name=link[link.index('graphics=')+len('graphics='):]
        except ValueError:
            no_name+=1
            name='NoName'+str(no_name)
        game.add_info('Name',name)
        browser.get(link)
        if not timeout_site(browser,'.hardware-info-box'):
            continue
        hardware_boxes=browser.find_elements_by_css_selector('.hardware-info-box')
        for hardware_box in hardware_boxes:
            # print('checking {0}'.format(str(hardware_box.find_element_by_css_selector('.hardware-info-box-category').get_attribute('innerHTML'))))
            try:
                ##multiElement
                for box_name in multiElement:
                    # print('checking Element{0}'.format(str(box_name)))
                    if str(hardware_box.find_element_by_css_selector('.hardware-info-box-category').get_attribute('innerHTML')) == box_name:
                        #get all info
                        rows = hardware_box.find_elements_by_css_selector('.hardware-info-row')
                        for row in rows:
                            try:
                                game.add_info(replace_string(row.find_element_by_css_selector('.hardware-info-title span').get_attribute('innerHTML')), replace_string(row.find_element_by_css_selector('.hardware-info-value span').get_attribute('innerHTML')))
                            except exceptions.NoSuchElementException:
                                continue
                            except AttributeError:
                                continue
                        #continue to other box_name
                        multiElement.remove(box_name)
                        raise ContinueExcep()
                ##singleElement
                for box_name,row_names in singleElement.items():
                    if str(hardware_box.find_element_by_css_selector('.hardware-info-box-category').get_attribute('innerHTML')) != box_name:
                        continue
                        # get all info
                    rows = hardware_box.find_elements_by_css_selector('.hardware-info-row')
                    for row in rows:
                        try:
                            row_name =row.find_element_by_css_selector('.hardware-info-title span').get_attribute('innerHTML')
                            if row_names.index(row_name) != -1:
                                game.add_info(replace_string(row_name), replace_string(row.find_element_by_css_selector('.hardware-info-value span').get_attribute('innerHTML')))
                        except exceptions.NoSuchElementException:
                            continue
                        except AttributeError:
                            continue
                        except ValueError:
                            continue
                    # continue to other box_name
                    singleElement.pop(box_name)
                    raise ContinueExcep()
            except ContinueExcep:
                continue
        ##specialElement
        rows=browser.find_elements_by_css_selector('.hardware-info-row')
        for row in rows:
            try:
                # print(row)
                # time.sleep(1000)
                try:
                    row_name = str(row.find_element_by_css_selector('.hardware-info-title span').get_attribute('innerHTML')).strip()
                except exceptions.NoSuchElementException:
                    row_name = str(row.find_element_by_css_selector('.hardware-info-title div').get_attribute('innerHTML')).strip()
                # print('checking row{}'.format(row_name))
                CSS=specialElement.get(row_name)
                # print('Result:{}'.format(CSS))
                if CSS==None:
                    continue
                component=row.find_element_by_css_selector(CSS)
                if row_name=='GD RATING':
                    data=str(component.get_attribute('alt'))
                    game.add_info(replace_string(row_name),replace_string(data[len(data)-1:]))
                else:
                    game.add_info(replace_string(row_name),replace_string(component.get_attribute('innerHTML')))
                specialElement.pop(row_name)
            except exceptions.NoSuchElementException:
                continue
            except AttributeError:
                continue
        # print(game.get_detail())
        link=str(link)
        link=urllib.unquote(link)
        try:
            fName=link[link.index('graphics=')+len('graphics='):]
        except ValueError:
            no_name+=1
            fName='NoName'+str(no_name)
        directory='grapped/gpuSpec/'+str(series).replace(' ','')
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            output_file=open(directory+'/'+fName+'.txt', 'w', encoding='utf8')
        except FileNotFoundError:
            output_file = open(directory + '/' + link[link.index('gid=')+len('gid='):link.index('&graphics=')] + '.txt', 'w', encoding='utf8')
        keys,values=game.get_all_info()
        for index,_ in enumerate(keys):
            output_file.write(keys[index]+'\t'+values[index]+'\n')
        output_file.close()
    browser.close()

###declare a function for HTML scrapping on list of GPU specification links
def gpuList(prefs:dict={"profile.managed_default_content_settings.images": 2}):
    output=dict()
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('res/chromedriver_win32/chromedriver.exe',chrome_options=chromeOptions)
    # get all the gpu series
    series_links=dict()
    browser.get("http://www.game-debate.com/hardware/index.php?list=gfxDesktop")
    links = browser.find_elements_by_css_selector('.hardwareRow .hardwareModel a')
    for link in links:
        series_links.update({link.get_attribute('innerHTML'):link.get_attribute('href')})
    for series,link in series_links.items():#2017-2000
        gpu_link=[]
        browser.get(link)
        delay = 7
        try:
            result = WebDriverWait(browser, delay).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.hardwareRow .hardwareDeriv a'))
            )
        except exceptions.TimeoutException:
            print('Timed Out')
            continue
        # with open('grapped/tempLink'+str(year)+'.txt', 'w', encoding='utf8') as temp_file:
        #     temp_file.write(str(year) + '\n')
        try:
            links=browser.find_elements_by_css_selector('.hardwareRow .hardwareDeriv a')
            for link in links:
                gpu_link.append(link.get_attribute('href'))
                    # temp_file.write(link.get_attribute('href') + '\n')
        except exceptions.NoSuchElementException:
            continue
        output.update({series:gpu_link})
        # output[str(year)]=gameLink
    browser.close()
    return output

###declare the main function in this python for program flow
def main():
    gpu_list=gpuList()
    print(gpu_list)
    for series,links in gpu_list.items():#2017-2000
        if links is not None:
            steps=0
            while(True):
                steps = multiThread(series,steps,links)
                if steps==-1:
                    break
        print('finish grapping Series {}'.format(series))
    print('finish all')
    # site1('testing',["http://www.game-debate.com/hardware/index.php?gid=211&graphics=GeForce%20GTS%20150","http://www.game-debate.com/hardware/index.php?gid=3889&graphics=GeForce%20Titan%20XP"])

###declare a function for multithreading usage
def multiThread(series:str,steps:int,links:[]):
    if steps >= len(links):
        return -1
    print('Processing Series{},Steps{}'.format(series,steps))
    start=time.time()
    max_thread=4
    link_per_step=50
    threads=[]
    for index in range(max_thread):
        sub_links = links[steps:steps + link_per_step]
        steps += link_per_step
        t=Thread(target=site1,args=[series,sub_links])
        threads.append(t)
        t.start()
    [t.join() for t in threads]
    end=time.time()
    print('Complete in {} seconds'.format(end-start))
    return steps


main()
