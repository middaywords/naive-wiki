from autocorrect import Speller
import os
import json


def correct_term(term: str) -> str:
    # Autocorrect
    correcter = Speller()

    return correcter.autocorrect_word(term)


def prefix_match(term, prefix):
    term_list = []
    for tk in term[prefix[0]].keys():
        if tk.startswith(prefix):
            term_list.append(term[prefix[0]][tk])
    return term_list


def prefix_matchA(term, prefix):
    term_list = {}
    for tk in term[prefix[0]].keys():
        if tk.startswith(prefix):
            term_list[term[prefix[0]][tk]] = 1
    return term_list


def prefix_matchB(term, prefix, termA):
    term_list = []
    for tk in term[prefix[0]].keys():
        if tk.startswith(prefix):
            if term[prefix[0]][tk] in termA:
                term_list.append(term[prefix[0]][tk])
    return term_list


def wild_card(term: str):
    """
    query: lower case str
    """
    parts = term.split("*")

    if len(parts) == 3:
        case = 4
    elif parts[1] == '':
        case = 1
    elif parts[0] == '':
        case = 2
    elif parts[0] != '' and parts[1] != '':
        case = 3

    if case == 4:
        if parts[0] == '':
            case = 1

    if case == 1:
        query = parts[0]
    elif case == 2:
        query = parts[1] + "$"
    elif case == 3:
        query = parts[1] + "$" + parts[0]
    elif case == 4:
        queryA = parts[2] + "$" + parts[0]
        queryB = parts[1]

    with open(f"../data/permutermIndex.json", 'r') as loadFile:
        permuterm = json.load(loadFile)

    print('start')

    if case != 4:
        term_list = prefix_match(permuterm, query)

    elif case == 4:
        # queryA Z$X
        term_listA = prefix_matchA(permuterm, queryA)

        # queryB Y
        term_list = prefix_matchB(permuterm, queryB, term_listA)

    return term_list


if __name__ == '__main__':
    inputSentence = 'h*l*o'
    terms = wild_card(inputSentence)
    print(terms)
