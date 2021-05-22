"""
    File io_utils.py created on 2021/5/22 by kangjx
"""

import json


def read_json(filename: str):
    f = open(filename)
    data = json.load(f)
    f.close()

    return data
