from secrets import choice
import json
import string
from functools import wraps


class Hangman:


#### Initialization of game. Pick random word. Create sets. Creating guessing plane ####

    def __init__(self):
        with open ('words.json','r') as json_file:                  # Open up the json file. Read it and save to variable
            data = json_file.read()                                 # Convert to a py. dictionary
        pydata = json.loads(data)

        self.word = choice(pydata.get('data'))                      # Choose a random word from the json file. Ensure we
        while "-" in self.word or " " in self.word or len(self.word) > 6: # Choose a valid word without a dash or a space
            self.word = choice(pydata.get('data'))

        self.length = len(self.word)                                # Get length of that random word
        self.guessing_plane = ("_") * self.length                   # Create a guessing plane
        self.words = set(self.word)                                 # Get each individual letter in the randomly chosen word.
                                                                    # save it as a set

        self.alphabet = set(string.ascii_lowercase)                 # Get all english letters in a set
        self.guessed_letters = set()                                # Set of guessed letters by the user

        self.guesses = 0                                            # Instance attribute keeping track of number of guesses



#### Verifying decorator to ensure it's a single letter. No numbers or multiple letters. Not a previously guessed letter ####

    def _verify_letter(letters):
        def inner(func):
            @wraps(func)
            def wrapper(*args,**kwargs):
                if args[1] not in letters or len(args[1]) != 1 or args[1] in args[2]:
                    return print(f"Must be a single letter that hasn't been previously guessed. Previous guesses are: {args[2]}")
                return func(*args,**kwargs)
            return wrapper
        return inner


### Main function ###

    def main(self):
        while not self._check_guesses() and self.guesses < 6:
            print(self._hangman_pic(self.guesses))
            self.hangman(input("Select a letter: ").lower(),self.guessed_letters)

        if self.guesses >= 6:
            return f"You lose. The word was {self.word}"

        return f"You win. The word was '{self.word}' and you guessed {len(self.guessed_letters)} times"




### Hangman code. If it passes the decorator to ensure it's a valid letter, it will add the letter to your guessed set
### of letters

    @_verify_letter(string.ascii_lowercase)
    def hangman(self,letter,guessed_letters):
        self.guessed_letters.add(letter)
        print(self.update_guessing_plane(letter))
        self.guesses += 1



### Check and see if everything in the self.words set is also in self.guessed_letters set. If so, then we've guessed
### All the letters correctly and we win

    def _check_guesses(self):
        return self.guessed_letters.issuperset(self.words)



### Create a new string if we successfully guessed a letter in the word

    def update_guessing_plane(self,letter):
        paired_letters = zip(self.guessing_plane,self.word)
        for idex,pair in enumerate(paired_letters):
            if letter == pair[1].lower():
                self.guessing_plane = self.guessing_plane[:idex] + letter + self.guessing_plane[idex+1:]
        return self.guessing_plane



    def _hangman_pic(self,remaining_guesses):
        hangman_pic = {
            5:"""
                     |/      |
                     |      (_)
                     |      \|/
                     |       |
                     |      / \\
                                 """,
            4:"""                       _______
                     |/      |
                     |      (_)
                     |      \|/
                     |       |
                     |      / 
                                 """,
            3:"""                       _______
                     |/      |
                     |      (_)
                     |      \|/
                     |       |
                     |      
                                 """,
            2:"""                       _______
                     |/      |
                     |      (_)
                     |      \|/
                     |       
                     |      
                                 """,
            1:"""                       _______
                     |/      |
                     |      (_)
                     |      
                     |       
                     |      
                                 """,
            0:"""                       _______
                     |/      |
                     |      
                     |      
                     |       
                     |      
                                 """


        }
        return hangman_pic.get(remaining_guesses)


if __name__ == '__main__':
    test1 = Hangman()
    print(test1.main())

