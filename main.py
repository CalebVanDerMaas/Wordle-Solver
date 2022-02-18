wordBankObj = open("wordBank.txt", "r")
words = wordBankObj.read().splitlines()
wordBankObj.close()

gameOver = False


def initGuessArray(guess):
    guessArray = []
    for i in guess:
        guessArray.append(i)
    return guessArray


def initResponseArray(response):
    responseArray = []
    for i in response:
        responseArray.append(i)
    return responseArray


def initGuessDict(guess, response):
    guessDict = {}
    for i, val in enumerate(guess):
        guessDict[val] = response[i]
    return guessDict


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





while not gameOver:
    userGuess = input("Enter your guess: ")
    userResponse = input("0 = Grey, 1 = Yellow, 2 = Green \n"
                     "Enter the results of your first guess based on the key above:")
    if (userResponse == 22222):
        gameOver = True
    else:
        guessDict = initGuessDict(initGuessArray(userGuess), initResponseArray(userResponse))
        words = cleanList(guessDict, words)






