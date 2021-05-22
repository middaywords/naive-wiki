"""
    File save_inverted_index_to_db.py created on 2021/5/20 by kangjx
"""
import json
from datetime import datetime

import mysql.connector


def connect_to_db():
    wiki_db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="testlab",
        database="wiki",
        # auth_plugin='mysql_native_password'
    )
    return wiki_db


if __name__ == '__main__':
    connect_to_db()
