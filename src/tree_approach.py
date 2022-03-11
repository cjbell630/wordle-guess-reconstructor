import json
from typing import List

from data_structures import TileResult, WordResult, LetterPossibility, ALPHABET, WORDLIST_PATH, TreeNode, \
    check_word_against_possibilities
import data_structures
from os.path import join as path_join, dirname as path_dirname
WORD_NORMS_PATH = path_join(path_dirname(__file__), "../res/word_norms.json")



WORD_NORMALCY = {}


def load_word_norms():
    global WORD_NORMALCY
    with open(WORD_NORMS_PATH, "r", encoding="utf-8") as jsonFile:
        WORD_NORMALCY = json.load(jsonFile)

def get_prev_possibilities(results: List[WordResult], words: List[str]) -> TreeNode:
    # print(f"len words: {len(words)}, len results: {len(results)}, looking at word {words[-1]}")  # TODO
    level = len(words)  # TODO off by 1?
    # print(f"words: {words}, results[-level-1]: {results[-level-1]}")

    node = TreeNode(words[-1])

    if len(words) == len(results):  #len(results) if on first guess
        # print("returning node")
        return node

    # results[-level - 1] = results for words to be generated
    # results[-level - 2] = results for words in line above this one
    # results[-level] = results for words in line below this one
    checks: List[List[LetterPossibility]] = [[], [], [], [], []]
    correct_word = words[0]
    index = 0
    curr_green = {i: correct_word[i] for i in range(0, 5) if results[-level - 1][i].equals(TileResult.GREEN)}
    gets_green_next = {i: correct_word[i] for i in range(0, 5) if
                       results[-level][i].equals(TileResult.GREEN) and not results[-level - 1][i].equals(TileResult.GREEN)}
    yellows_in_next = {i: words[-1][i] for i in range(0, 5) if
                       results[-level][i].equals(TileResult.YELLOW)}
    for tile_result in results[-level - 1]:
        correct_char = correct_word[index]
        # TODO get python 3.10 and change to match statement
        if tile_result.equals(TileResult.GREEN):
            checks[index] = [LetterPossibility(correct_char)]
        elif tile_result.equals(TileResult.YELLOW):
            # print("yellow")  # TODO
            # has to be in either gets_green_next or yellows_in_next
            # cannot be the letter in this index in any subsequent guesses (only way that would be possible is if green)
            impossible_letters = [word[index] for word in words]
            # cannot be the letter in that position
            # cannot be any green letters except duplicates
            # cannot be any yellow letters to the left (duplicates count separately)

            # below should not contain any letters that are green this turn because it only includes by->g and
            possible_letters = [letter for letter in gets_green_next.values()] + [letter for letter in yellows_in_next.values()]
            # print(f"word: {words[-1]}, possible_letters: {possible_letters}, impossible_letters: {impossible_letters}")
            for letter in possible_letters:
                if letter != correct_char and letter not in impossible_letters:
                    checks[index].append(
                        LetterPossibility(
                            letter,
                            if_max_matched_instances=correct_word.count(correct_char) - 1
                        )
                    )
        else:
            # cannot be letter in that position
            # can only be letter in correct word if that letter has green somewhere else, or gt correct_word.count(letter) yellows to the left
            # cannot be the letter in this index in any subsequent guesses (only way that would be possible is if green)
            # cannot be used in any further guesses UNLESS used as a duplicate this guess, and said duplicate is yellow or green
            impossible_letters = {letter: True for word in words for letter in
                                  word}.keys()  # this should remove duplicates
            for letter in ALPHABET:
                instances_in_correct_word = correct_word.count(letter)
                if letter in impossible_letters:
                    # would need to have been matched
                    if instances_in_correct_word > 0:
                        checks[index].append(LetterPossibility(letter, if_min_matched_instances=instances_in_correct_word))
                elif letter in correct_word:
                    if letter != correct_char:
                        checks[index].append(
                            LetterPossibility(letter, if_min_matched_instances=instances_in_correct_word))
                else:  # not in correct word
                    checks[index].append(LetterPossibility(letter))

            #if "norah" in words:
                #print(f"word: {words[-1]}, impossible_letters: {impossible_letters}, checks: {checks[index]}")
        index += 1

    #for check in checks:
        #print(check)
    """ FINDING WORDS """

    # find word
    with open(WORDLIST_PATH) as wordlist_file:
        for line in wordlist_file:
            curr_word = line.strip()
            if (curr_word not in WORD_NORMALCY or WORD_NORMALCY[curr_word]) and check_word_against_possibilities(curr_word, results[-level-1], checks):
                new_branch = get_prev_possibilities(results, words + [curr_word])
                # if curr_word == "mobie":
                    # print(WORD_NORMALCY)
                    # print( f"len(words): {len(words)}, len(results): {len(results)}, len(new_branch.branches): {len(new_branch.branches)}, curr_word in WORD_NORMALCY: {curr_word in WORD_NORMALCY}")
                if len(words) == len(results) - 1 or len(new_branch.branches) > 0:

                    node.branches.append(new_branch)
                # TODO check length of branches of new node and remove if they dead end too soon
    return node


if __name__ == "__main__":
    copy_paste_string = "⬛⬛⬛⬛⬛\n" \
                        "🟨🟩⬛⬛🟩\n" \
                        "🟩🟩🟩🟩🟩"
    correct_word = "month"

    patterns = [WordResult(line) for line in copy_paste_string.split("\n")]
    print(patterns)
    print("loading...")
    head_node = get_prev_possibilities(patterns, [correct_word])
    head_node.print()

    print("Done!")

    # TODO if letter is guessed as black on one level, it considers guessing that letter as valid on previous level

load_word_norms()