from dataclasses import dataclass
from enum import Enum
from typing import List

from os.path import join as path_join, dirname as path_dirname

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

WORDLIST_PATH = path_join(path_dirname(__file__), "../res/5letter_full.txt")


class TileResult(Enum):
    BLACK = -1
    YELLOW = 0
    GREEN = 1

    def to_string(self):
        return "⬛" if self == TileResult.BLACK else "🟨" if self == TileResult.YELLOW else "🟩"


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
    if_gt_present: str = None  # length 1
    if_lt_present: str = None  # length 1
    present_count: int = 0
    # present checks all to the left, plus greens to the right


"""
def words_for_pattern(pattern: List[TileResult], correct_word: str):
    index = 0
    checks: List[List[LetterPossibility]] = [[], [], [], [], [], []]
    not_green_letters = [correct_word[i] for i in range(0, 5) if
                       pattern[i] != TileResult.GREEN]  # TODO integrate into below loop
    green_letters = [correct_word[i] for i in range(0, 5) if
                       pattern[i] == TileResult.GREEN]  # TODO integrate into below loop

    for tile_result in pattern:
        correct_char = correct_word[index]
        # TODO get python 3.10 and change to match statement
        if tile_result == TileResult.GREEN:
            checks[index] = [LetterPossibility(correct_char)]
        elif tile_result == TileResult.YELLOW:
            print("yellow")  # TODO
            # has to be a letter in the word
            # cannot be the letter in that position
            # cannot be any green letters except duplicates
            # cannot be any yellow letters to the left (duplicates count separately)
            for letter in not_green_letters:
                if letter != correct_char:
                    checks[index].append(
                        LetterPossibility(
                            letter,
                            if_lt_present=letter,
                            present_count=correct_word.count(correct_char)
                        )
                    )
        else:
            # cannot be letter in that position
            # can only be letter in word if that letter has green somewhere else or gt word.count(letter) yellows to the left
            for letter in ALPHABET:
                if letter in correct_word:
                    if letter in green_letters:
                        checks[index].append(LetterPossibility(letter)) # only if 
                        
                if letter != correct_char:
                    checks[index].append(
                        LetterPossibility(
                            letter,
                            if_gt_present=letter,
                            present_count=correct_word.count(correct_char)
                        )
                    )

        index += 1
        
"""


def get_pattern_for_guess(guess: str, correct_word: str) -> WordResult:
    remaining_letters = []
    green_letters = []
    pattern = WordResult()
    for i in range(0, 5):
        if guess[i] == correct_word[i]:
            green_letters.append(correct_word[i])
        else:
            remaining_letters.append(correct_word[i])

    for i in range(0, 5):
        if guess[i] == correct_word[i]:
            pattern.append(TileResult.GREEN)
        elif guess[i] in remaining_letters:
            pattern.append(TileResult.YELLOW)
            remaining_letters.remove(guess[i])
        else:
            pattern.append(TileResult.BLACK)
    return pattern


def words_for_patterns(patterns: List[WordResult], correct_word: str):
    words = [[] for _ in patterns]
    with open(WORDLIST_PATH) as wordlist_file:
        for line in wordlist_file:
            line = line.strip()
            pattern = get_pattern_for_guess(line, correct_word)
            for i in range(0, len(patterns)):
                if patterns[i] == pattern:
                    words[i].append(line)
    return words

print(get_pattern_for_guess("claps", "lapse").to_string())
print(get_pattern_for_guess("phase", "lapse").to_string())

copy_paste_string = "🟨⬛🟨⬛⬛\n" \
                    "⬛⬛🟨🟨🟨\n" \
                    "🟩🟨🟨🟨🟨\n" \
                    "🟩🟩🟩🟩🟩"
correct_word = "lapse"


patterns = [WordResult(line) for line in copy_paste_string.split("\n")]
words = words_for_patterns(patterns, correct_word)
for index in range(0, len(patterns)):
    print(f"Pattern: {patterns[index].to_string()}")
    for word in words[index]:
        print(f"-----{word}")
