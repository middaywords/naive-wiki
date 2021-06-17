import time

from server.crawl_abstract import get_abstract
from utils.constants import term2doc_dict

if __name__ == '__main__':
    cnt = 0
    print(len(term2doc_dict.keys()))

    for key in term2doc_dict.keys():
        cnt += 1
        print(cnt)
        print(key)
        print(get_abstract("https://en.wikipedia.org/wiki/" + key))
        time.sleep(2)