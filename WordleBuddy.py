import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class SolutionsList:
    def __init__(self):
        # read word list from file
        f = open("solutions.txt", "r")
        self.__wordlist = f.readlines()

    def getwordlist(self):
        return self.__wordlist

class PreviousSolutions:
    def __init__(self):
        self.__pastanswers = []

        # download previous solutions
        browser.get("https://www.rockpapershotgun.com/wordle-past-answers")
        html = browser.page_source
        answersoup = bs4.BeautifulSoup(html, 'html.parser')

        # parse the last 7 words
        answerlinks = answersoup.select('a[href^="/wordle-answer-"]')
        for answerlink in answerlinks[1:]:
            self.__pastanswers.append(answerlink.text)

        # parse older words
        answerlinks = answersoup.select('ul.inline li')
        for answerlink in answerlinks[1:]:
            self.__pastanswers.append(answerlink.text)

    def getprevioussolutions(self):
        return self.__pastanswers

class LetterRanker:
    def __init__(self, wordlist):
        self.__charsCountDict = {}
        for word in wordlist:
            word = word[:5] # strip newlines
            # get letters in word
            chars = list(word)
            charsDict = {}
            for char in chars:
                charsDict[char] = char
            uniqueChars = charsDict.keys()
            for uniqueChar in uniqueChars:
                if uniqueChar in self.__charsCountDict:
                    charCount = self.__charsCountDict[uniqueChar]
                    self.__charsCountDict[uniqueChar] = charCount + 1
                else:
                    self.__charsCountDict[uniqueChar] = 1

    def getlettersranked(self):
        sorted_letters = sorted(self.__charsCountDict.items(), key=lambda kv: kv[1])
        return sorted_letters[::-1]

class WordRanker:
    def __init__(self, wordlist, charsRanked):
        charsRankedDict = dict(charsRanked)
        self.__wordsRankedDict = {}
        for word in wordlist:
            word = word[:5] # strip newlines
            wordScore = 0
            # get letters in word
            chars = list(word)
            charsDict = {}
            for char in chars:
                charsDict[char] = char
            uniqueChars = charsDict.keys()
            for uniqueChar in uniqueChars:
                # get score for letter
                charScore = charsRankedDict[uniqueChar]
                wordScore = wordScore + charScore
            self.__wordsRankedDict[word] = wordScore

    def getwordsranked(self):
        sortedwords = sorted(self.__wordsRankedDict.items(), key=lambda kv: kv[1])
        return sortedwords[::-1]

class RemainingSolutions:
    def __init__(self, guess, yellowsAndGreens, remainingWordsRanked):
        # first parse the yellows and greens
        # default to all black cubes
        guessletters = list(guess)
        cubes = []
        for x in range(5):
            cubes.append(Cube("black", guessletters[x], x+1))
        if yellowsAndGreens:
            # parse yellows and greens
            yellowsAndGreensSplit = yellowsAndGreens.split()
            for yellowOrGreen in yellowsAndGreensSplit:
                chars = list(yellowOrGreen)
                position = int(chars[1])
                if chars[0] == 'y':
                    # yellow cube
                    cube = Cube("yellow", guessletters[position-1], position)
                    cubes[position-1] = cube
                    #print(cube)
                elif chars[0] == 'g':
                    # green cube
                    cube = Cube("green", guessletters[position-1], position)
                    cubes[position-1] = cube
        else:
            print("You entered no yellows or greens")

        wordstoremove = []
        for cube in cubes:
            #print(cube)
            if cube.getcolor() == 'black':
                for remainingword in remainingWordsRanked:
                    if cube.getletter() in remainingword[0] and self.nogreencubeshaveletter(cube.getletter(), cubes):
                        #print("remaining word " + remainingword[0] + " has black letter " + cube.getletter() + ", removing")
                        wordstoremove.append(remainingword)
            elif cube.getcolor() == 'yellow':
                for remainingword in remainingWordsRanked:
                    # for yellow letters, remove if not in word or in the same position
                    if cube.getletter() not in remainingword[0]:
                        wordstoremove.append(remainingword)
                    if cube.getletter() == remainingword[0][cube.getposition()-1]:
                        wordstoremove.append(remainingword)
            elif cube.getcolor() == 'green':
                for remainingword in remainingWordsRanked:
                    if cube.getletter() != remainingword[0][cube.getposition()-1]:
                        wordstoremove.append(remainingword)

        self.__updatedremainingwords = []
        for remainingword in remainingWordsRanked:
            wordistoberemoved = False
            for wordtoremove in wordstoremove:
                if wordtoremove[0] == remainingword[0] or guess == remainingword[0]:
                    wordistoberemoved = True
            if not wordistoberemoved:
                self.__updatedremainingwords.append(remainingword)

    def nogreencubeshaveletter(self, letter, cubes):
        for cube in cubes:
            if cube.getcolor() == 'green' and cube.getletter() == letter:
                return False
        return True

    def getremainingsolutions(self):
        return self.__updatedremainingwords

class Cube:
    def __init__(self, color, letter, position):
        self.__color = color
        self.__letter = letter
        self.__position = position

    def __str__(self):
        return "Cube(color=" + self.__color + ", letter=" + self.__letter + ", position=" + str(self.__position) + ")"

    def getcolor(self):
        return self.__color

    def getletter(self):
        return self.__letter

    def getposition(self):
        return self.__position

print()
print("Welcome to WordleBuddy v1.0!")
print()

print("Loading list of all Wordle words...")
solutions = SolutionsList()
wordlist = solutions.getwordlist()

letterRanker = LetterRanker(wordlist)
charsRanked = letterRanker.getlettersranked()
#print(charsRanked)

print("Ranking words by letter popularity...")
wordRanker = WordRanker(wordlist, charsRanked)
wordsRanked = wordRanker.getwordsranked()

print("Loading previous answers...")
browser = webdriver.Chrome(executable_path='./chromedriver')
previousSolutions = PreviousSolutions()
pastanswers = previousSolutions.getprevioussolutions()
#print(pastanswers)
browser.quit()
print()

# remove previous answers from the ranked words list
for word in wordsRanked:
    for pastanswer in pastanswers:
        if pastanswer == word[0].upper():
            wordsRanked.remove(word)

solved = False
while not solved:
    print(str(len(wordsRanked)) + " solutions remaining")
    print("Here are my recommendations:")
    for word in wordsRanked[:5]:
        print(word[0].upper() + ' (' + str(word[1]) + ')')
    print()

    guess = input("Enter your guess: ")
    print("You entered " + guess.upper())
    yellowsAndGreens = input("Now, enter your yellow and green letters\nFor example, if first letter is yellow and last letter is green type \"y1 g5\": ")
    if yellowsAndGreens == "g1 g2 g3 g4 g5":
        print("Splendid!")
        solved = True
        break

    print("Calculating remaining solutions...")
    remainingSolutions = RemainingSolutions(guess, yellowsAndGreens, wordsRanked)
    updatedremainingsolutions = remainingSolutions.getremainingsolutions()
    wordsRanked = updatedremainingsolutions