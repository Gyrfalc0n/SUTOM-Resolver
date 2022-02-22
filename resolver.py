import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Chrome driver download : https://chromedriver.storage.googleapis.com/index.html?path=99.0.4844.35/
# Chromedriver : https://chromedriver.storage.googleapis.com/99.0.4844.35/chromedriver_win32.zip

# TO DO
# Readme : get chrome driver good version to match chrome version!

# Variables
url = "https://sutom.nocle.fr/"
chromedriver_path = 'C:\\Program Files\\chromedriver_win32\\chromedriver.exe'

# Core
driver = webdriver.Chrome(executable_path=chromedriver_path)
driver.get(url)
driver.implicitly_wait(5)
# Click on cross to close rule panel
time.sleep(1)
driver.find_element_by_id("panel-fenetre-bouton-fermeture-icone").click()


soup = BeautifulSoup(driver.page_source, 'lxml')
tables = soup.find_all('table')
dfs = pd.read_html(str(tables))

print(f'Total tables: {len(dfs)}')
print(dfs[0])

time.sleep(10)
driver.quit()