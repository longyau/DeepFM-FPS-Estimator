from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
from threading import Thread
import os
###Declare a python object to store all information of a game
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


###Search through website to get all game information
def site1(year:int,gameLinks:[],prefs:dict={"profile.managed_default_content_settings.images": 2}):
    if len(gameLinks)<1:
        return
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('res/chromedriver_win32/chromedriver.exe',chrome_options=chromeOptions)
    singleElement=[["Name","#art_g_title div span"],["Theme",".theme div a"],["Min-VRam",".systemRequirementsHwBoxVRAMMin .systemRequirementsRamContent span"],["Min-Ram",".systemRequirementsHwBoxRAMMin .systemRequirementsRamContent span"],["Min-OS",".systemRequirementsHwBoxSystemMin span"],["Min-DX",".systemRequirementsHwBoxDirectXMin span"],["Rec-VRam",".systemRequirementsHwBoxVRAM .systemRequirementsRamContent span"],["Rec-Ram",".systemRequirementsHwBoxRAM .systemRequirementsRamContent span"],["Rec-OS",".systemRequirementsHwBoxSystem span"],["Rec-DX",".systemRequirementsHwBoxDirectX span"]]
    multiElement=[["Release Date",".tdRelease a"],["Genre",".genre span a"],["Min-CPU",".systemRequirementsHwBoxCPUMin .systemRequirementsLink div a"],["Min-GPU",".systemRequirementsHwBoxGPUMin .systemRequirementsLink div a"],["Rec-CPU",".systemRequirementsHwBoxCPU .systemRequirementsLink div a"],["Rec-GPU",".systemRequirementsHwBoxGPU .systemRequirementsLink div a"]]
    website="http://www.game-debate.com/games/index.php"
    for link in gameLinks:
        no_name=0
        game=Game()
        game.add_info('Website', website + link)
        browser.get(website + link)
        for data in singleElement:
            try:
                content = browser.find_element_by_css_selector(data[1]).get_attribute('innerHTML')
                game.add_info(data[0],content)
            except exceptions.NoSuchElementException:
                continue
        for data in multiElement:
            try:
                fields = browser.find_elements_by_css_selector(data[1])
                for index,field in enumerate(fields):
                    content=field.get_attribute('innerHTML')
                    game.add_info(data[0]+str(index), content)
            except exceptions.NoSuchElementException:
                continue
            except AttributeError:
                continue
        # print(game.get_detail())
        link=str(link)
        try:
            fName=link[link.index('g_id=')+len('g_id='):link.index('&',link.index('g_id='))]
        except ValueError:
            no_name+=1
            fName='NoName'+str(no_name)
        directory='grapped/gameInfo/'+str(year)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory+'/'+fName+'.txt', 'w', encoding='utf8') as output_file:
            keys,values=game.get_all_info()
            for index,_ in enumerate(keys):
                output_file.write(keys[index]+'\t'+values[index]+'\n')
    browser.close()


###Generate a list to games link to work on
def gameList(prefs:dict={"profile.managed_default_content_settings.images": 2}):
    output=dict()
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('res/chromedriver_win32/chromedriver.exe',chrome_options=chromeOptions)
    for year in range(2000,2018):#2017-2000
        gameLink=[]
        browser.get("http://www.game-debate.com/games/index.php?year="+str(year))
        delay = 7
        try:
            result = WebDriverWait(browser, delay).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.srTitleFull a'))
            )
        except exceptions.TimeoutException:
            print('Timed Out')
            continue
        # with open('grapped/tempLink'+str(year)+'.txt', 'w', encoding='utf8') as temp_file:
        #     temp_file.write(str(year) + '\n')
        try:
            links=browser.find_elements_by_css_selector('.srTitleFull a')
            for link in links:
                gameLink.append(link.get_attribute('href'))
                    # temp_file.write(link.get_attribute('href') + '\n')
        except exceptions.NoSuchElementException:
            continue
        output.update({str(year):gameLink})
        # output[str(year)]=gameLink
    browser.close()
    return output

###the flow of this program
###read the list of game link
###scrapped through each link and get all information
def main():
    game_list=gameList()
    # game_list={'2018':["http://www.game-debate.com/games/index.php?g_id=9229&game=Kingdom%20Come:%20Deliverance"]}
    for year in range(2017,1999,-1):#2017-2000
    # for year in range(2018,1999,-1):#2017-2000
        links=game_list.get(str(year))
        if links is not None:
            steps=0
            while(True):
                steps = multiThread(year,steps,links)
                if steps==-1:
                    break
        print('finish Year {}'.format(year))
    print('finish all')


###A function for multi-threading the scrapping machine
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
