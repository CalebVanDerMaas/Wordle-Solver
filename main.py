
from chromeDriver import *


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

# returns dictionary of guess:response (key:value) pairs
# accepts two arrays of strings as arguments
def initGuessDict(guess, response):
    guessDict = {}
    for i, val in enumerate(guess):
        guessDict[val] = response[i]
    return guessDict

# eliminates words from wordBank based on guess:response pairs
# accepts a dictionary and an array of strings as arguments
# returns array of strings
def cleanList(dict, initList):
    newWords = []
    for index, (key, value) in enumerate(dict.items()):
        if (value == '0' and index == 0):
            newWords += [x for x in initList if key not in x]
        elif (value == '0' and index != 0):
            newWords = [x for x in newWords if key not in x]
        elif (value == '1' and index == 0):
            newWords += [x for x in initList if key in x and key != x[index]]
        elif (value == '1' and index != 0):
            newWords = [x for x in newWords if key in x and key != x[index]]
        elif (value == '2' and index == 0):
            newWords += [x for x in initList if key == x[index]]
        elif (value == '2' and index != 0):
            newWords = [x for x in newWords if key == x[index]]
    print(newWords)
    return newWords

gameOver = False
guessCounter = 0
testWord = 'crane'

while not gameOver:
    print('Enter your guess:')
    print(testWord)
    tryWord(testWord)
    responseArray = getResponse(guessCounter)

    if (responseArray == '22222'):
        gameOver = True
    else:
        # generates guessDict (guess:response) from userGuess and userResponse
        guessDict = initGuessDict(initGuessArray(testWord), responseArray)
        # cleans wordBank based on guessDict key:value pairs
        words = cleanList(guessDict, words)
        testWord = words[0]






