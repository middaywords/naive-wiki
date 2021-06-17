from utils.io_utils import read_json


import os
print(os.getcwd())
term2doc_dict = read_json('data/term-doc3.json')
permuterm = read_json('data/permutermIndex.json')
