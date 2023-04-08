# WordleBuddy

NOTE: This script should no longer be used, the word dictionary is obsolete as of 3/27 when the NY Times' Wordle editor started adding new words to the puzzle.

Assistant for playing Wordle word game.  Uses NY Times solution list and scrape of previous answers to recommend guesses.  Algorithm ranks words by letter frequency to generate recommendations.

To install, you will need Python3, BeautifulSoup and Selenium.

https://www.python.org/downloads/

`pip install beautifulsoup4`
`pip install -U selenium`

Sample output:


```
Welcome to WordleBuddy v1.0!

Loading list of all Wordle words...
Ranking words by letter popularity...
Loading previous answers...
/Users/matthewbonness/wordle/WordleBuddy.py:180: DeprecationWarning: executable_path has been deprecated, please pass in a Service object
  browser = webdriver.Chrome(executable_path='./chromedriver')

1968 solutions remaining
Here are my recommendations:
IRATE (4107)
LATER (4106)
ALTER (4106)
ALERT (4106)
AROSE (4083)

Enter your guess: irate
You entered IRATE
Now, enter your yellow and green letters
For example, if first letter is yellow and last letter is green type "y1 g5": g4
Calculating remaining solutions...
20 solutions remaining
Here are my recommendations:
SLOTH (2978)
SOUTH (2789)
GUSTO (2711)
LOFTY (2606)
YOUTH (2588)

Enter your guess: sloth
You entered SLOTH
Now, enter your yellow and green letters
For example, if first letter is yellow and last letter is green type "y1 g5": y3 g4 g5
Calculating remaining solutions...
2 solutions remaining
Here are my recommendations:
YOUTH (2588)
MOUTH (2470)

Enter your guess: youth
You entered YOUTH
Now, enter your yellow and green letters
For example, if first letter is yellow and last letter is green type "y1 g5": g1 g2 g3 g4 g5
Splendid!
```
