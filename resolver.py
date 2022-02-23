import time
from selenium import webdriver
from collections import Counter
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Chromedriver : https://chromedriver.chromium.org/downloads

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
driver.find_element(By.ID, "panel-fenetre-bouton-fermeture-icone").click()

# Dictionnaire
file = open('dictionnaire.txt', 'r')
lines = file.readlines()

# Table dimension counting
row_count = len(driver.find_elements(By.XPATH, "//*[@id=\"grille\"]/table/tr"))
colums_count = int(len(driver.find_elements(By.XPATH, "//*[@id=\"grille\"]/table/tr/td"))/row_count)
print(" -- Grille du jour -- \n" + "Lignes: " + str(row_count) + ", Colonnes: " + str(colums_count))
# Table duplication
global grille, tag, actual_row
tested_words = []
actual_row = -1
grille = [['.' for x in range(colums_count)] for x in range(row_count)]
tag = [[0 for x in range(colums_count)] for x in range(row_count)] # 1: wrong placed / 2: well placed / null: default

def refresh_table(): # Refresh grille & tag with attributes
    global grille, tag, actual_row
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
                grille[row][i] = col[i].text
                    
def random_word():
    lettre = grille[0][0] # Premier caractère
    for line in lines:
        line = line[:-1]
        if line.startswith(lettre):
            if len(line) == colums_count and isUniqueChars(line):
                tested_words.append(line)
                return line

def possible_words():
    possible = []
    lettre = grille[0][0] # Premier caractère
    for line in lines:
        line = line[:-1] # Delete last end of string character
        if line.startswith(lettre):
            if len(line) == colums_count and isUniqueChars(line) and containsAll(line) and containsSub(line) and line not in tested_words:
                possible.append(line)
    return possible

def guess_word():
    possible = possible_words()
    if len(possible) >= 1:
        word = possible[0]
        tested_words.append(word)
        return word
    return None
            
def containsSub(word): # Check if word contains all correct letters in correct position
    local_string = "" 
    for i in range(colums_count): # Recraft string with correct letters in position
        if tag[actual_row][i] == 2:
            local_string += grille[actual_row][i]
        else:
            local_string += '*'
    for j in range(len(word)):
        if word[j] != local_string[j] and local_string[j] != '*':
            return False
    return True

def containsAll(word): # Check if word contains all incorectly placed letters & not letters that are not in word to find
    local_letters = []
    local_positions = []
    exclude_letters = []
    for i in range(colums_count): # Recraft string with incorrectly placed letters {letter:position....}
        if tag[actual_row][i] == 1:
            local_letters.append(grille[actual_row][i])
            local_positions.append(i)
        if tag[actual_row][i] == 0:
            exclude_letters.append(grille[actual_row][i])
    for j in range(len(local_letters)):
        if word.find(local_letters[j]) == -1 or word.find(local_letters[j]) == local_positions[j]: # If not found or in same position
            return False
    for k in range(len(exclude_letters)): # Exclude letters not in word to find
        if exclude_letters[k] in word:
            return False
    return True

def isUniqueChars(string): # Check if word contains unique letters (only check on the non valid letters (== exclusion of well placed )) ######## CHECK IF DOUBLE LETTERS 
    local_string = [] 
    if actual_row != -1: # If not first execution (== word with unique letters)
        for i in range(colums_count): # Recraft string with correct letters in position
            if tag[actual_row][i] == 2:
                local_string.append(grille[actual_row][i])
                for char in local_string:
                    string = string.replace(char,'')
    freq = Counter(string)
    if(len(freq) == len(string)):
        return True
    else:
        return False

def isWin():
    win = driver.find_elements(By.XPATH, "//*[@id=\"panel-fenetre-contenu\"]/p[1]")
    if len(win) != 0:
        classe = win[0].get_attribute("class")
        if classe == "fin-de-partie-panel-phrase":
            print("END GAME")
            return True
    return False
    
def send_word(word):
    global actual_row
    action.send_keys(word).perform()
    time.sleep(0.5)
    action.send_keys(Keys.RETURN).perform()
    actual_row += 1
    time.sleep(0.4*colums_count)

# -- MAIN --
count = 0
refresh_table()
first_word = random_word()
print("Initial guess: " + str(first_word))
send_word(first_word)
while True:
    driver.refresh()
    refresh_table()
    possible = possible_words()
    print("Possible words are (" + str(len(possible)) + "): " + str(possible))
    word = guess_word()
    print("Guess word is: " + str(word))
    send_word(word)
    count += 1
    if isWin() or count >= row_count:
        if count >= row_count:
            print("WORD NOT FOUND")
        time.sleep(10)
        break;