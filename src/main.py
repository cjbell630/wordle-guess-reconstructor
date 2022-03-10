from dataclasses import dataclass

from typing import List


class Level:
    num: int
    word: str
    prev_level_guesses: List[str]
    possible_prev_guess: List[Level]

    def __init__(self, num, word):
        print("init") #TODO
        

    def get_prev_levels(self):
        print("get_prev_levels") #TODO

# unguessed letters
#