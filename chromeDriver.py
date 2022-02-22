import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from html.parser import HTMLParser
from bs4 import BeautifulSoup

#-------------------------------------Solver Logic--------------------------------------#

# creates array of strings from wordBank.txt
wordBankObj = open("wordBank.txt", "r")
words = wordBankObj.read().splitlines()
wordBankObj.close()

# returns array of characters from user guess
# accepts string argument
def initGuessArray(guess):
    guessArray = []
    for i in guess:
        guessArray.append(i)
    return guessArray

# returns array of characters from user response
# accepts string argument
def initResponseArray(response):
    responseArray = []
    for i in response:
        responseArray.append(i)
    return responseArray

def cleanWordBank(guess, response, initList, gCounter):
    if (gCounter > 0):
        newWords = initList
    else:
        newWords = []
    l1 = []
    dupes = []
    guessCounter = gCounter

    def removeAllWordsWithCharacterX(guessCount):
        newList = []
        if (guessCount == 0):
            newList += [x for x in initList if key not in x]
        else:
            newList += [x for x in newWords if key not in x]
        return newList

    def rmvWrdsWthChrsXAtInd(guessCount):
        newList = []
        if (guessCount == 0):
            newList += [x for x in initList if key != x[ind]]
        else:
            newList += [x for x in newWords if key != x[ind]]
        return newList

    def rmvWrdsThatDontHaveCorrectCharacter(guessCount):
        newList = []
        if (guessCount == 0):
            newList += [x for x in initList if key == x[ind]]
        else:
            newList += [x for x in newWords if key == x[ind]]
        return newList

    def rmvWrdsWithoutCharX(guessCount):
        newList = []
        if (guessCount == 0):
            newList += [x for x in initList if key in x]
        else:
            newList += [x for x in newWords if key in x]
        return newList

# finds duplicated characters and appends them to dupes list
    if (len(guess) != len(set(guess))):
        for char in guess:
            if char not in l1:
                l1.append(char)
            else:
                dupes.append(char)
        #handles duped characters in words with dupes
        for ind in range(5):
            key = guess[ind]
            value = response[ind]
            if key in dupes:
                if (value == '0' or value == '1'):
                    newWords = rmvWrdsWthChrsXAtInd(guessCounter)
                    guessCounter += 1
                elif (value == '2'):
                    newWords = rmvWrdsThatDontHaveCorrectCharacter(guessCounter)
                    guessCounter += 1
                print("doing nothing")

            #handles non duped characters in words with dupes
            else:
                if (value == '0'):
                    newWords = removeAllWordsWithCharacterX(guessCounter)
                    guessCounter += 1
                elif (value == '1' and ind == 0):
                    newWords = rmvWrdsWthChrsXAtInd(guessCounter)
                    guessCounter += 1
                elif (value == '2'):
                    newWords = rmvWrdsThatDontHaveCorrectCharacter(guessCounter)
                    guessCounter += 1
                else:
                    print('hit a filler')
    #handles words with no dupes
    else:
        for ind in range(5):
            key = guess[ind]
            value = response[ind]
            if (value == '0'):
                newWords = removeAllWordsWithCharacterX(guessCounter)
                guessCounter += 1
            elif (value == '1'):
                newWords = rmvWrdsWthChrsXAtInd(guessCounter)
                guessCounter += 1
                newWords = rmvWrdsWithoutCharX(guessCounter)
                guessCounter += 1
            elif (value == '2'):
                newWords = rmvWrdsThatDontHaveCorrectCharacter(guessCounter)
                guessCounter += 1
            else:
                print('hit a filler')
    return newWords


#-------------------------------------Browser Driver----------------------------------#

# init list of keyboard characters
keyboardList = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k',
                'l', 'Enter', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Del']

# creates dictionary of keyBoardChars:seleniumElements (key:value) pairs
# accepts two arrays of strings as arguments
KeyboardDictionary = {}
def createKeyboardDictionary(elements, keysList):
    for i, val in enumerate(keysList):
        KeyboardDictionary[val] = elements[i]
    return KeyboardDictionary

# splits string into array of characters && clicks corresponding elements
# accepts string as an argument
def tryWord(string):
    stringArray = []
    for i in string:
        stringArray.append(i)
    actions = ActionChains(driver)
    for ind, x in enumerate(stringArray):
        actions.click(KeyboardDictionary[x]).perform()
    actions.click(KeyboardDictionary['Enter']).perform()

def getResponse(guessCount):
    RowListElements = driver.find_elements_by_class_name('RowL')
    RowListElementsSoup = BeautifulSoup(RowListElements[guessCount].get_attribute("innerHTML"), 'html.parser').find_all(
        'div')

    SoupString = str(RowListElementsSoup)
    SoupStringList = SoupString.split(',')
    responseArray = []
    for x in SoupStringList:
        if "letter-correct" in x:
            responseArray += '2'
        elif "letter-elsewhere" in x:
            responseArray += '1'
        elif "letter-absent" in x:
            responseArray += '0'
        else:
            print("Error: getResponse did not detect character indicator")
    return responseArray

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        return attrs

#-------------------------------------------Main---------------------------------------------#

gameOver = False
guessCounter = 0
testWord = 'crane'
gameOverArray = ['2', '2', '2', '2', '2']

# init selenium ChromeDriver
driver = webdriver.Chrome('venv/bin/chromedriver')  # Optional argument, if not specified will search path.

# init browser instance @ given URL
driver.get('https://www.wordleunlimited.com/');

# creates list of selenium elements targeting given class
elementsList = driver.find_elements_by_class_name('Game-keyboard-button')

print(elementsList)

createKeyboardDictionary(elementsList, keyboardList)

while not gameOver:
    print('Enter your guess:')
    tryWord(testWord)
    responseArray = getResponse(guessCounter)

    if (responseArray == gameOverArray):
        gameOver = True
    else:
        # generates guessDict (guess:response) from userGuess and userResponse
        # guessDict = initGuessDict(initGuessArray(testWord), responseArray)
        # cleans wordBank based on guessDict key:value pairs
        words = cleanWordBank(initGuessArray(testWord), responseArray, words, guessCounter)
        # gets first word in array from newly cleaned list
        testWord = words[0]
        #progresses guessCounter by 1 to move the getResponse 1 row down
        guessCounter += 1

time.sleep(20) # Let the user actually see something!

# driver.quit()