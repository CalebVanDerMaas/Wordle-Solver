[![HitCount](https://hits.dwyl.com/CalebVanDerMaas/Wordle-Solver.svg?style=flat-square)](http://hits.dwyl.com/CalebVanDerMaas/Wordle-Solver)
# Wordle-Solver
Using selenium
Wordle! The internets most recent obsession as of early 2022. A simple game consisting of an unknown 5 letter word, a 26 english-alphabet keyboard
and 6 guesses. But don't be fooled, this games simple mechanism makes for a joy of a puzzle.
The game works like this: 
  The user gets 6 attemps to guess the random 5-letter word of the day
  For each guess, clues are given to inch the player closer to the answer
  There are only three clues and they are as follows:
    1. Grey - This letter is not found in the word
    2. Yellow - This letter is found in the word, but not in this position
    3. Green - This letter is found in the word in this position
  You can imagine that the goal of the game is to get all five character spaces to green indicating that you have all of the correct letters in the correct places and hence you
  have guessed the correct word.
  
Wordle is a fun game. It's fun to play alone, and it's fun to challenge your friends. One limitation of Wordle is that you can only play it once per day. Since the hidden word
is universal for all players, and it only changes every 24 hours, this means that you get one full gameplay and then it's over. To combat this, a replica game -- Wordle Unlimited 
was created to supplement all of your Worldle solving cravings. It's no suprise though, after a while, even this enjoyable game gets a little boring. After spending a few hours 
enjoying the game's simple gameplay, I started to think: how could I get better at wordle. At this point, I was averaging a score of around 4 gueses per round, a quite average score
for most. But I knew there had to be a way to get better.

One day, while scrolling through my YouTube feed, I stumbled across a video of someone who had automated the wordle gameplay and used machine-learning to make their program better at
Wordle. Before I could get a quarter of the way through the video, I booted up by computer and started working on a wordle solver for myself.

It started with just the solver.
How could I systematically take the information from the clues and programatically get closer to an answer? It really started with all 5 letter words. 'How many were there?' I thought,
'It has to be a finite amount'. I found a convienient list from Stanford of all known 5-letter words organized neatly into a list with consistent seperation. I could use Python to 
split this list into a pythonic list. From here I could chop this list down based on the infromation from the clues and eventually I would get closer and closer to the answer until
only the answer fits. 

To clean the list
I first needed to know the word that was guessed and the clue that was returned for each letter. Since these both needed to be input manually, I would start with strings, one for the
word that was guessed, and another for a string of values based on the clues that were returned. I decided to turn the color system into a number system so it would be easier to pass
the values around. 0 = grey, 1 = yellow, and 2 = green. Since the two lists should always be the same length and the order of the characters and clue values should be corresponding, I 
could then loop through these lists and make a dictionary with character:guess_value key:value pairs. Now that I had the characters from the guessed word and the guess_values associated
with each character, I could loop through this dictionary and implement rules based on the logic of the game.

The meat and brains
It started off well. If a characters value was grey, this means the character was not in the word at all. Just like a guess who game, I could eliminate all the words in my word bank that
did not match the specific critereon for each of my rules. For example, assume the first guess was 'CRANE' and the guess_values was '00120'. This means that there is no character 'C' in the
word at all. This means that I could eliminate all of the words from my word bank that had a letter 'C' in it. Since 'R' has the same value, words that contained an 'R' could be eliminated
from the list as well. 
Similarly, the value 1 means that the letter is in the word, just not in that position. For the letter 'A', this means two things: we can eliminate all the words that don't have a letter 'A', 
and we can eliminate all of the words that have a letter 'A' in the 3rd letter position. 
2 means that the character is the correct letter in the correct position. Since 'N' is 2, we can eliminate all words from the list that don't have an N in the 4th character position.
Finally, the same steps are repeated for the letter 'E'. 
At the end of all of this, we have a much shorter list. Sometimes, depending on the first guess and the clues that are returned back, these three rules can narrow the 5,000+ 5-letter word list
down to just 3 words. That's a 33% chance that you guess the correct word on just the second try. But there's a problem...

Words with duplicate characters :(
