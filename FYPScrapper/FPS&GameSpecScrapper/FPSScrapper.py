from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
from threading import Thread
import os
class Game(object):
    def add_info(self, name,value):
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



def readData(in_file_path:str='grapped\gameInfo'):
    file_cnt=0
    game_array=[]
    for folder in os.listdir(in_file_path):
        try:
            folder_name=int(folder)
            if folder_name>2018 or folder_name<1999:
                continue
        except AttributeError:
            continue
        exact_path=in_file_path+'\\'+folder
        for filename in os.listdir(exact_path):
            file_cnt+=1
            try:
                assert filename.endswith('.txt')
                game_array.append({folder:filename[:-4]})
            except AssertionError:
                continue
    return game_array,file_cnt



def site1(year:int,gameIds:[],prefs:dict={"profile.managed_default_content_settings.images": 2}):
    if len(gameIds)<1:
        return
    # cont=False
    # for game_id in gameIds:
    #     if int(game_id)==33898 or int(game_id)==8514 or int(game_id)==23780 or int(game_id)==1308:
    #         cont=True
    #         break
    #     else:
    #         continue
    # if cont!=True:
    #     return
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('res/chromedriver_win32/chromedriver.exe',chrome_options=chromeOptions)
    # singleElement=[["Name","#art_g_title div span"],["Theme",".theme div a"],["Min-VRam",".systemRequirementsHwBoxVRAMMin .systemRequirementsRamContent span"],["Min-Ram",".systemRequirementsHwBoxRAMMin .systemRequirementsRamContent span"],["Min-OS",".systemRequirementsHwBoxSystemMin span"],["Min-DX",".systemRequirementsHwBoxDirectXMin span"],["Rec-VRam",".systemRequirementsHwBoxVRAM .systemRequirementsRamContent span"],["Rec-Ram",".systemRequirementsHwBoxRAM .systemRequirementsRamContent span"],["Rec-OS",".systemRequirementsHwBoxSystem span"],["Rec-DX",".systemRequirementsHwBoxDirectX span"]]
    element=[["Game-Setting",".cardHeaderGrafSetting span"],["FPS",".cardBodyFpsText"]]
    website="http://www.game-debate.com/games/index.php"
    div_count = 0
    for game_id in gameIds:
        game_records=[]
        if int(game_id)==33898 or int(game_id)==8514 or int(game_id)==23780 or int(game_id)==1308:
            print('found')
            continue
        # else:
        #     continue
        link=website+'?g_id='+str(game_id)+'&framesPerSecond'
        browser.get(link)
        page_cnt=1
        delay = 3
        tries=1
        while True:
            ###wait for loading
            try:
                result = WebDriverWait(browser, delay).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.cardWrapper'))
                )
            except exceptions.TimeoutException:
                ###Should be No Card
                try:
                    browser.find_element_by_css_selector('.memberCardsPag span.clickable')
                except exceptions.NoSuchElementException:
                    break
                ###Should be No Card
                ###Banned
                if tries < 3:
                    try:
                        browser2 = site_for_banned(link, page_cnt)
                        browser.close()
                        browser=browser2
                    except exceptions.NoSuchElementException:
                        print('Some error in the page')
                        break
                    tries += 1
                    continue
                else:
                    print('Timed Out')
                    time.sleep(20)
                    break
                ###Banned

            ###wait for loading
            tries=1
            try:
                page = browser.find_element_by_css_selector('.memberCardsPagButtons ul li.active span')
                # print('Page_CNT{},Active{}'.format(page_cnt,int(page.get_attribute('innerHTML'))))
                if page_cnt != int(page.get_attribute('innerHTML')):
                    print('Invalid Page')
                    break
                fps_divs=browser.find_elements_by_css_selector('.cardWrapper')
                for fps_div in fps_divs:
                    FPS_Record=Game()
                    ###get Resolution
                    try:
                        res_divs=fps_div.find_elements_by_css_selector('.cardBodyScreenRes div')
                        if len(res_divs)==2:
                            FPS_Record.add_info('Res-Width', str(res_divs[0].get_attribute('innerHTML'))[len('width:'):])
                            FPS_Record.add_info('Res-Height', str(res_divs[1].get_attribute('innerHTML'))[len('Height:'):])
                    except exceptions.NoSuchElementException:
                        pass
                    ###get Resolution
                    ###get Multiple Element
                    for data in element:
                        try:
                            field = fps_div.find_element_by_css_selector(data[1])
                            content = field.get_attribute('innerHTML')
                            FPS_Record.add_info(data[0], content)
                        except exceptions.NoSuchElementException:
                            continue
                    ###get Multiple Element
                    ###get Components
                    try:
                        comp_divs = fps_div.find_elements_by_css_selector('.cardFooter .thirdDiv .ellipsis')
                        if len(comp_divs) == 3:
                            FPS_Record.add_info('CPU', comp_divs[0].find_element_by_css_selector('a').get_attribute('innerHTML'))
                            FPS_Record.add_info('GPU', comp_divs[1].find_element_by_css_selector('a').get_attribute('innerHTML'))
                            FPS_Record.add_info('Ram', comp_divs[2].get_attribute('innerHTML'))
                    except exceptions.NoSuchElementException:
                        pass
                    ###get Componenets
                    ###add to Game
                    game_records.append(FPS_Record)
                    ###add to Game
                page_cnt+=1
            except exceptions.NoSuchElementException:
                print('Can`t find element')
                break
                ###goto Next Page
            try:
                next_btn = browser.find_element_by_css_selector('.page-link.next')
                next_btn.click()
            except exceptions.NoSuchElementException:
                # print('Finished...')
                break
        directory='grapped/FPSRecord/'+str(year)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory+'/'+str(game_id)+'.txt', 'w', encoding='utf8') as output_file:
            for idx,record in enumerate(game_records):
                game_keys, game_values = record.get_all_info()
                output_file.write('{}\n'.format(idx))
                for index,_ in enumerate(game_keys):
                    output_file.write(game_keys[index]+'\t'+str(game_values[index]).replace('\n','')+'\n')
                div_count+=len(game_records)
        # if len(game_records)>0:
        #     print('Found Divs Count{}'.format(len(game_records)))
    print('Founds Divs Count in this step{}'.format(div_count))
    browser.close()



def site_for_banned(url:str,page:int,prefs:dict={"profile.managed_default_content_settings.images": 2}):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('res/chromedriver_win32/chromedriver.exe',chrome_options=chromeOptions)
    browser.get(url)
    try:
        next_btn = browser.find_element_by_css_selector('.memberCardsPag span.clickable')
        next_btn.click()
        input_field = browser.find_element_by_css_selector('.memberCardsPag span.clickable input')
        for i in range(5):
            input_field.send_keys(Keys.BACK_SPACE)
            input_field.send_keys(Keys.DELETE)
        input_field.send_keys(str(page))
        input_field.send_keys(Keys.ENTER)
    except exceptions.NoSuchElementException:
        browser.close()
        raise
    print('Retrying')
    return browser

# def gameList(prefs:dict={"profile.managed_default_content_settings.images": 2}):
#     output=dict()
#     chromeOptions = webdriver.ChromeOptions()
#     chromeOptions.add_experimental_option("prefs", prefs)
#     browser = webdriver.Chrome('res/chromedriver_win32/chromedriver.exe',chrome_options=chromeOptions)
#     for year in range(2000,2018):#2017-2000
#         gameLink=[]
#         browser.get("http://www.game-debate.com/games/index.php?year="+str(year))
#         delay = 7
#         try:
#             result = WebDriverWait(browser, delay).until(
#                 EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.srTitleFull a'))
#             )
#         except exceptions.TimeoutException:
#             print('Timed Out')
#             continue
#         # with open('grapped/tempLink'+str(year)+'.txt', 'w', encoding='utf8') as temp_file:
#         #     temp_file.write(str(year) + '\n')
#         try:
#             links=browser.find_elements_by_css_selector('.srTitleFull a')
#             for link in links:
#                 gameLink.append(link.get_attribute('href'))
#                     # temp_file.write(link.get_attribute('href') + '\n')
#         except exceptions.NoSuchElementException:
#             continue
#         output.update({str(year):gameLink})
#         # output[str(year)]=gameLink
#     browser.close()
#     return output


def main():
    games,cnt=readData()
    year_games_list=[]
    for i in range(2000,2018):
        year_games_list.append([])
    for game in games:
        Game=dict(game)
        for key,value in Game.items():
            # print('Key{}:Value{}'.format(int(key),value))
            year_games_list[int(key) - 2000].append(int(value))
    for idx,game in enumerate(year_games_list):
        print('Year{}: {}'.format(str(idx+2000), str(len(game))))
    print('Total count{}'.format(cnt))
    for idx,game in enumerate(year_games_list):#2017-2000
        year=idx+2000
        # if year < 2015:
        #     continue
        if game is not None:
            steps=0
            while(True):
                steps = multiThread(year,steps,game)
                if steps==-1:
                    break
        print('finish Year {}'.format(year))
    print('finish all')


def multiThread(year:int,steps:int,links:[]):
    if steps >= len(links):
        return -1
    print('Processing Year{},Steps{}'.format(year,steps))
    start=time.time()
    max_thread=4
    link_per_step=50
    threads=[]
    for index in range(max_thread):
        sub_links = links[steps:steps + link_per_step]
        steps += link_per_step
        t=Thread(target=site1,args=[year,sub_links])
        threads.append(t)
        t.start()
    [t.join() for t in threads]
    end=time.time()
    print('Complete in {} seconds'.format(end-start))
    return steps


main()
