import json
from os.path import join as path_join, dirname as path_dirname

from src.data_structures import WordResult, TreeNode
import src.data_structures
from src.tree_approach import get_prev_possibilities

GUESS_FOLDER_PATH = path_join(path_dirname(__file__), "../res/guesses")
WORD_NORMS_PATH = path_join(path_dirname(__file__), "../res/word_norms.json")

# really good ones: month 11

correct_word = "month"
attempt_num = 12


def dict_to_json_string(elem):
    if type(elem) is dict:
        return "{" + ", ".join([f"\"{k}\": {dict_to_json_string(v)}" for k, v in elem.items()]) + "}"
    elif type(elem) is list:
        return "[" + ", ".join([dict_to_json_string(e) for e in elem]) + "]"
    elif type(elem) is str:
        return "\"" + elem.replace("\"", "\\\"") + "\""
    elif type(elem) is bool:
        # return "\"true\"" if elem else "\"false\""
        return "true" if elem else "false"
    else:
        return str(elem)


def load_word_norms():
    with open(WORD_NORMS_PATH, "r", encoding="utf-8") as jsonFile:
        src.data_structures.WORD_NORMALCY = json.load(jsonFile)


def save_word_norms():
    with open(WORD_NORMS_PATH, "w+", encoding="utf-8") as file:
        file.write(dict_to_json_string(src.data_structures.WORD_NORMALCY))


def print_tree_exclude(top_node: TreeNode, level: int = 0):
    string = f"{'--- ' * level}{top_node.data}:\n"
    for node in top_node.branches:
        if node.data not in src.data_structures.WORD_NORMALCY.keys():
            src.data_structures.WORD_NORMALCY[node.data] = input(f"is \"{node.data}\" a normal word? (y/n) ") == "y"
            save_word_norms()
        if src.data_structures.WORD_NORMALCY[node.data]:
            string += print_tree_exclude(node, level + 1)
    return string


if __name__ == "__main__":
    with open(f"{GUESS_FOLDER_PATH}/{correct_word}/{attempt_num}.txt", encoding="utf-8") as attempt_file:
        patterns = [WordResult(line.strip()) for line in attempt_file]

    print(patterns)

    print("loading...")
    head_node = get_prev_possibilities(patterns, [correct_word])

    load_word_norms()
    print(print_tree_exclude(head_node))
    #head_node.print()

    print("Done!")
