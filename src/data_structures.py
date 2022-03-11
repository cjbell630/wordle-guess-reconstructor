from dataclasses import dataclass
from enum import Enum
from typing import List, Any
from os.path import join as path_join, dirname as path_dirname

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

WORDLIST_PATH = path_join(path_dirname(__file__), "../res/wordle_nyt_full.txt")
WORD_NORMALCY = {}


class TileResult(Enum):
    BLACK = -1
    YELLOW = 0
    GREEN = 1

    def to_string(self):
        return "⬛" if self.equals(TileResult.BLACK) else "🟨" if self.equals(TileResult.YELLOW) else "🟩"

    def equals(self, tr):
        return self.value == tr.value


class WordResult(List[TileResult]):
    def to_string(self):
        return "".join(tile.to_string() for tile in self)

    def __init__(self, string: str = ""):
        super().__init__()
        for char in string:
            self.append(TileResult.GREEN if char == "🟩" else TileResult.YELLOW if char == "🟨" else TileResult.BLACK)


@dataclass
class LetterPossibility:
    letter: str  # length 1
    if_max_matched_instances: int = None
    # this letter can only go here if there are less than or equal to `if_max_matched_instances` instances of any of the following:
    #       * yellow slots with this letter to the left of this letter's index
    #       * green slots with this letter
    if_min_matched_instances: int = None

    # this letter can only go here if there are greater than or equal to `if_min_matched_instances` instances of any of the following:
    #       * yellow slots with this letter to the left of this letter's index
    #       * green slots with this letter

    def check_word(self, index: int, word: str, result: WordResult):
        if word[index] == self.letter:
            if self.if_min_matched_instances is None and self.if_max_matched_instances is None:
                return True
            else:
                matched_instances = 0
                for i in range(0, 5):
                    if word[i] == self.letter and (
                            (i < index and result[i].equals(TileResult.YELLOW)) or result[i].equals(TileResult.GREEN)
                    ):
                        matched_instances += 1
                return (
                        (self.if_min_matched_instances is None or self.if_min_matched_instances <= matched_instances) and
                        (self.if_max_matched_instances is None or matched_instances <= self.if_max_matched_instances)
                )
        else:
            #print(f"check failed for {word} bc of letter {word[index]}")
            return False

def check_word_against_possibilities( word: str, result: WordResult, possibilities: List[List[LetterPossibility]]):
    # print(f"----checking: {word}")
    for i in range(0, 5):
        check = [letter_check for letter_check in possibilities[i] if letter_check.letter == word[i]]
        # print(f"--------checking: {check}")
        if not(len(check) > 0 and check[0].check_word(i, word, result)):
            # print(f"--------failed due to letter: {word[i]}")
            return False
    # print(f"--------passed")
    return True


class TreeNode:
    data: Any
    branches: List

    def __init__(self, data):
        self.data = data
        self.branches: List = []

    def add_branch(self, new_branch):
        self.branches.append(new_branch)

    def print(self, level:int=0):
        print(f"{'--- '*level}{self.data}:")
        for node in self.branches:
            node.print(level+1)
