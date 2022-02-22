import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Chrome driver download : https://chromedriver.storage.googleapis.com/index.html?path=99.0.4844.35/
# Chromedriver : https://chromedriver.storage.googleapis.com/99.0.4844.35/chromedriver_win32.zip

# TO DO
# Readme : get chrome driver good version to match chrome version!

# -- VARIABLES --
url = "https://sutom.nocle.fr/"
chromedriver_path = 'C:\\Program Files\\chromedriver_win32\\chromedriver.exe'

# -- CORE --
driver = webdriver.Chrome(executable_path=chromedriver_path)
action = ActionChains(driver)
driver.get(url)
driver.maximize_window()
driver.implicitly_wait(5)
# Click on cross to close rule panel
time.sleep(1)
driver.find_element_by_id("panel-fenetre-bouton-fermeture-icone").click()
base = driver.find_element(By.ID,("contenu"))

# Table dimension counting
row_count = len(driver.find_elements(By.XPATH, "//*[@id=\"grille\"]/table/tr"))
colums_count = int(len(driver.find_elements(By.XPATH, "//*[@id=\"grille\"]/table/tr/td"))/row_count)
print(" -- Grille du jour -- \n" + "Lignes: " + str(row_count) + ", Colonnes: " + str(colums_count))
# Table duplication
global grille
global tag
grille = [['.' for x in range(colums_count)] for x in range(row_count)]
tag = [['0' for x in range(colums_count)] for x in range(row_count)] # 1: wrong placed / 2: well placed / 0: default

def refresh_table(): # Refresh grille & tag with attributes
    global grille, tag
    table_id = driver.find_element(By.XPATH, "//*[@id=\"grille\"]/table")
    for row in range(0, row_count):
        rows = table_id.find_elements(By.XPATH, "//*[@id=\"grille\"]/table/tr[" + str(row+1) + "]")
        for row_data in rows:
            col = row_data.find_elements(By.TAG_NAME, "td")
            for i in range(len(col)):
                classe = col[i].get_attribute("class")
                if classe == "mal-place resultat":
                    tag[row][i] = 1
                elif classe == "bien-place resultat":
                    tag[row][i] = 2
                if col[i].text != '.':
                    grille[row][i] = col[i].text
refresh_table()
action.send_keys('oldats').perform()
time.sleep(0.5)
action.send_keys(Keys.RETURN).perform()
time.sleep(2)
refresh_table()
print(grille)
print(tag)
time.sleep(10)
driver.quit()