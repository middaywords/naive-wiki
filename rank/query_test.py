"""
    File query_test.py created on 2021/5/20 by kangjx
"""

from datetime import datetime
import re
import numpy as np

from data import stopwords
from rank.tf_idf import TfidfWrapper
from utils.io_utils import read_json


from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity


def read_term2doc_json():
    data = read_json('../data/term-doc2.json')

    return data



def query_test(query: str):
    term2doc_dict = read_term2doc_json()
    terms = list(filter(None, re.split(r"[ ,_:#!(\){}&\+\*]", query)))
    doc_count = dict()
    for term in terms:
        if term not in term2doc_dict.keys():
            continue
        for doc in term2doc_dict[term]:
            if doc in doc_count.keys():
                doc_count[doc] += 1
            else:
                doc_count[doc] = 1

    doc_list = list(doc_count.keys())
    doc_list.append(query)

    stop_words_l = stopwords.en_stop_words

    # # bert
    # print(datetime.now())
    # bert_wrapper = BertWrapper(stop_words_l=stop_words_l)
    # docs_embeddings = bert_wrapper.get_embeddings(doc_list=doc_list)
    # query_embedding = bert_wrapper.get_embeddings(doc_list=[query])
    # cosine_distance_mat = cosine_similarity(query_embedding, docs_embeddings)
    # euclidean_distance_mat = euclidean_distances(query_embedding, docs_embeddings)
    # print(datetime.now())

    # tf-idf
    print(datetime.now())
    tfidf_wrapper = TfidfWrapper(stop_words_l=stop_words_l)
    docs_embeddings = tfidf_wrapper.get_embeddings(doc_list=doc_list)
    cosine_distance_mat = cosine_similarity([docs_embeddings[-1]], docs_embeddings[:-1])
    euclidean_distance_mat = euclidean_distances([docs_embeddings[-1]], docs_embeddings[:-1])
    print(datetime.now())

    print('cosine')
    top10_id = cosine_distance_mat.argsort(axis=1)[0][-10:][::-1]
    np_doc_list = np.array(doc_list)
    final_res = np_doc_list[top10_id]
    print(final_res)

    print('euclidean')
    top10_id = euclidean_distance_mat.argsort(axis=1)[0][-10:][::-1]
    np_doc_list = np.array(doc_list)
    final_res = np_doc_list[top10_id]
    print(final_res)


if __name__ == '__main__':
    query_test(query='tencent')
