"""
    File data_processing.py created on 2021/5/20 by kangjx
"""
import json
import re
from datetime import datetime
from data.stopwords import en_stop_words

from utils.io_utils import read_json


def split_title(title: str) -> list:
    # return re.split(r"[ +|,+|_+|:+|#+|!+|\(+|\)+|{+|}+|&+]", title)
    return list(filter(None, re.split(r"[ ,_:#!(\){}&\+\*]", title)))


def read_title2title_data():
    print(datetime.now())
    data = read_json(filename='../data/term.json')
    print(datetime.now())

    return data


def read_title2doc_data():
    print(datetime.now())
    data = read_json(filename='../data/term-doc2.json')
    print(datetime.now())

    return data


def processing():
    print('----stopwords:\n', en_stop_words)
    data = read_title2title_data()
    generated_data = {}  # new json
    for key, val in data.items():
        print(key)
        term_list = split_title(key)
        for term in term_list:
            if len(term) <= 1 or term in en_stop_words:
                continue
            term_lower = term.lower()
            if term_lower in generated_data.keys():
                generated_data[term_lower].append(key)
            else:
                generated_data[term_lower] = [key]
    print('keys in total:', len(generated_data.keys()))
    with open('../data/term-doc2.json', 'w') as f:
        json.dump(generated_data, f)


def display_info():
    data = read_title2doc_data()
    max_len = 0
    max_bytes_len = 0
    mark = ""
    for key, val in data.items():
        if max_len < len(val):
            max_len = len(val)
            mark = key
        ss = ""
        for doc_name in val:
            ss += doc_name
        max_bytes_len = max(len(ss), max_bytes_len)
        print(len(val), len(ss), flush=True)
    print("max doc num:", max_len, "bytes:", max_bytes_len)
    print("mark:", mark)


if __name__ == '__main__':
    processing()
    display_info()
