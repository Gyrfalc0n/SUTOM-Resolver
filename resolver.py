import time
from selenium import webdriver
from collections import Counter
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Chromedriver : https://chromedriver.chromium.org/downloads

# Merge two dict : merge-dict.py file1 file2 (output.txt)
# Sort dict in bash : sort dict -o dict
# Remove empty lines on file : sed -i '/^$/d' file.txt
# Supprimer doublons : sort file | uniq -d > file

# Enrichir les mots (FR) : https://www.dcode.fr/recherche-mot

# DEBUG
debug_time = True

# -- VARIABLES --
url = "https://sutom.nocle.fr/"
chromedriver_path = 'C:\\Program Files\\chromedriver_win32\\chromedriver.exe'

# -- CORE --
driver = webdriver.Chrome(executable_path=chromedriver_path)
action = ActionChains(driver)
driver.get(url)
#driver.maximize_window()
driver.implicitly_wait(5)

# Time
start_time = time.time()
global timerr
timerr = time.time()

# Click on cross to close rule panel
time.sleep(1)
driver.find_element(By.ID, "panel-fenetre-bouton-fermeture-icone").click()

# Dictionnaire
dictionnaire = 'full-dictionnaire.txt'
unrecognised_words_txt = 'unrecognised_words.txt'
file = open(dictionnaire, 'r')
lines = file.readlines()
# Unrecognised words
unr = open(unrecognised_words_txt, 'a+')

# Table dimension counting
row_count = len(driver.find_elements(By.XPATH, "//*[@id=\"grille\"]/table/tr"))
colums_count = int(len(driver.find_elements(By.XPATH, "//*[@id=\"grille\"]/table/tr/td"))/row_count)
print(" -- Grille du jour -- \n" + "Lignes: " + str(row_count) + ", Colonnes: " + str(colums_count))
# Table duplication
global grille, tag, actual_row, possible, unrecognised_words, exclude_letters
exclude_letters = []
possible = []
tested_words = []
unrecognised_words = []
actual_row = -1
grille = [['' for x in range(colums_count)] for x in range(row_count)]
tag = [[0 for x in range(colums_count)] for x in range(row_count)] # 1: wrong placed / 2: well placed / null: default

def refresh_table(): # Refresh grille & tag with attributes
    global grille, tag
    table_id = driver.find_element(By.XPATH, "//*[@id=\"grille\"]/table")
    for row in range(0, row_count):
        premier_word = row == 0 and actual_row == -1 # conditions for first word
        before_row_to_send = row == actual_row and actual_row != -1 # not first word, last sent word
        row_to_send = row == actual_row+1 and actual_row != -1 # not first word, row to send word
        if premier_word or before_row_to_send or row_to_send: # Only check current row = faster
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
    timer("refresh_table()")
                    
def random_word():
    lettre = grille[0][0] # Premier caractère
    for line in lines:
        line = line[:-1]
        if line.startswith(lettre):
            if len(line) == colums_count and isUniqueChars(line) and line not in unrecognised_words and not is_in_unreco(line):
                tested_words.append(line)
                return line

 # DEBUG A METTRE DANS LA FONCTION CI APRES
        #if line == "MOT":
        #    print("line mystere")
        #    if len(line) != colums_count:
        #        print("len line")
        #    elif not line.startswith(lettre):
        #        print("not start letter")
        #    elif not isUniqueChars(line):
        #        print("Not is unique")
        #    elif not containsAll(line):
        #        print("Not contains all")
        #    elif not containsSub(line):
        #        print("Not contains sub")
        #    elif line in tested_words:
        #        print("In tested words")
        #    elif line in unrecognised_words:
        #        print("line in unreco")
        #    if len(line) == colums_count and isUniqueChars(line) and containsAll(line) and containsSub(line) and line not in tested_words and line not in unrecognised_words:
        #        print("append")
        #    else:
        #        print("not append")


def possible_words():
    global possible
    local_possible = []
    lettre = grille[0][0] # Premier caractère
    if len(possible) == 0: # First word
        for line in lines:
            line = line[:-1] # Delete last end of string character
            if line.startswith(lettre):
                if len(line) == colums_count and isUniqueChars(line) and containsAll(line) and containsSub(line) and line not in tested_words and line not in unrecognised_words and not is_in_unreco(line):
                    local_possible.append(line)
    else:
        for k in range(0, len(possible)):
            line = possible[k]
            if line.startswith(lettre):
                if isUniqueChars(line) and containsAll(line) and containsSub(line):
                    local_possible.append(line)
    if len(local_possible) == 0: # If 0 words are found, add precedent unrecognised word (maybe game has been updated with new words that were precedently unrecognised)
        unreco = open(unrecognised_words_txt, 'r')
        unrlines = unreco.readlines()
        for line in unrlines:
            if len(line) == colums_count and isUniqueChars(line) and containsAll(line) and containsSub(line) and line not in tested_words and line not in unrecognised_words:
                local_possible.append(line)
    possible = local_possible # Update possible words (== reduce list)
    timer("possible_words()")
    
                
def guess_word():
    global tested_words
    if len(possible) >= 1:
        word = possible[0]
        tested_words.append(word)
        return word
    return None

def is_in_unreco(word):
    unreco = open(unrecognised_words_txt, 'r')
    lines = unreco.readlines()
    for line in lines:
        if word in line:
            return True
    return False
            
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

def containsAll(word): # Check if word contains all incorectly placed letters at different position from last time & not letters that are not in word to find
    local_letters = []
    local_positions = []
    global exclude_letters
    good_letters = []
    for i in range(colums_count): # Recraft string with incorrectly placed letters {letter:position....}
        if tag[actual_row][i] == 2:
            good_letters.append(grille[actual_row][i])
        if tag[actual_row][i] == 1:
            local_letters.append(grille[actual_row][i])
            local_positions.append(i)
        if tag[actual_row][i] == 0:
            if grille[actual_row][i] not in exclude_letters and grille[actual_row][i] not in good_letters:
                exclude_letters.append(grille[actual_row][i])
    for j in range(len(local_letters)):
        if word.find(local_letters[j]) == -1 or word.find(local_letters[j]) == local_positions[j]: # If not found or in same position
            return False
    for k in range(len(exclude_letters)): # Exclude letters not in word to find
        if exclude_letters[k] in word:
            return False
    return True

def isUniqueChars(string): # Check if word contains unique letters (only check on the non valid letters (== exclusion of well placed )) ######## CHECK IF DOUBLE LETTERS 
    #local_string = [] 
    if actual_row == -1: # First execution == all letters have to be unique to reduce possibility faster
        freq = Counter(string)
        if(len(freq) == len(string)):
            return True
        else:
            return False
    else: # Not first execution, letters can be double
        return True


def isWin():
    win = driver.find_elements(By.XPATH, "//*[@id=\"panel-fenetre-contenu\"]/p[1]")
    if len(win) != 0:
        classe = win[0].get_attribute("class")
        if classe == "fin-de-partie-panel-phrase":
            return True
    return False
    
def send_word(word):
    global actual_row
    action.send_keys(word).perform()
    time.sleep(0.5)
    action.send_keys(Keys.RETURN).perform()
    actual_row += 1
    time.sleep(0.4*colums_count)
    timer("send_word()")

def update_unreco():
    for i in range(len(unrecognised_words)):
        unr.writelines(unrecognised_words[i]+"\n")

def check_if_word_exist(word): # Check if last sent word is in grille, if not, then word is not recognised
    global actual_row, unrecognised_words
    sent_words = []
    index = 0
    for i in range(row_count):
        last_word = ""
        for j in range(colums_count):
            last_word += grille[i][j]
        sent_words.append(last_word)
    for k in range(len(sent_words)):
        if sent_words[k] == '':
            index = k-1 # Index of row to send next word
            if word == "ECAMET":
                print("index: " + str(index))
            break
    if index == 0 and actual_row == 0: # First sent word
        print(word + " is unknown to the game")
        actual_row -= 1 # Not count last sent word, as it is not recognised
        unrecognised_words.append(word)
        possible.pop(word)
        timer("check_if_word_exist()")
        return False
    elif actual_row >= index:
        print(word + " is unknown to the game")
        actual_row -= 1 # Not count last sent word, as it is not recognised
        unrecognised_words.append(word)
        possible.remove(word)
        timer("check_if_word_exist()")
        return False
    else:
        timer("check_if_word_exist()")
        return True

def timer(string):
    if debug_time:
        global timerr
        local = time.time()
        print("\t" + string + " time = " + str(round(local - timerr,2)))
        timerr = local

# -- MAIN --
count = 0
while True:
    refresh_table()
    first_word = random_word()
    print("Guess(1): " + str(first_word))
    send_word(first_word)
    driver.refresh()
    refresh_table()
    if check_if_word_exist(first_word):
        break
while True:
    driver.refresh()
    refresh_table()
    possible_words()
    print(" - " + str(len(possible)) + " possible words")
    word = guess_word()
    if word != None:
        print("Guess(" + str(count+2) + "): " + str(word))
        send_word(word)
        if not isWin():
            driver.refresh()
            refresh_table()
            if check_if_word_exist(word):
                if len(possible) >= 1:
                    count += 1
    else:
        print("ERROR : NO MORE WORD IN DICT TO GUESS")
        time.sleep(10)
        update_unreco()
        break
    if isWin() or count >= row_count:
        if count >= row_count:
            print("WARNING : WORD NOT FOUND IN GIVEN TRY COUNT")
        else: # WIN
            end_time = time.time()
            execution_time = round(end_time - start_time, 1)
            print("\n -[ Word was " + word + " found in " + str(count+2) + " try and " + str(execution_time) + " seconds! ]- \n")
        update_unreco()
        input("Press Enter to quit...")
        time.sleep(1)
        driver.close()
        break;