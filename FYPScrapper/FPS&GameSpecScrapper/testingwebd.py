from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
browser = webdriver.Chrome('res/chromedriver_win32/chromedriver.exe', chrome_options=chromeOptions)
browser.get('http://www.game-debate.com/games/index.php?g_id=1308&framesPerSecond#page-1')
try:
    result = WebDriverWait(browser, 7).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.cardWrapper'))
    )
except exceptions.TimeoutException:
    pass
fps_divs = browser.find_elements_by_class_name('.cardWrapper')
print('Found Divs Count{}'.format(len(fps_divs)))