"""
    File query_test.py created on 2021/5/20 by kangjx
"""

from datetime import datetime
import re
import numpy as np

from data import stopwords
from rank.bert import BertWrapper
from rank.doc2vec import Doc2vecWrapper
from rank.glove import GloveWrapper
from rank.tf_idf import TfidfWrapper
from utils.io_utils import read_json

from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity


def read_term2doc_json():
    data = read_json('../data/term-doc2.json')

    return data


def dis_top10(
        distance_mat: np.ndarray,
        doc_list: list):
    top10_id = distance_mat.argsort(axis=1)[0][-10:][::-1]
    np_doc_list = np.array(doc_list)
    final_res = np_doc_list[top10_id]

    return final_res


def show_search_res(
        cos_distance_mat: np.ndarray,
        eucli_distance_mat: np.ndarray,
        doc_list: list):
    print('cosine')
    search_res = dis_top10(cos_distance_mat, doc_list)
    print(search_res)

    print('euclidean')
    search_res = dis_top10(eucli_distance_mat, doc_list)
    print(search_res)


def test_different_ranking_algo(
        algo: str,
        doc_list: list,
        stop_words_l: list):
    docs_embeddings = None
    if algo == 'tf-idf':
        print('tf-idf search result')
        print(datetime.now())
        tfidf_wrapper = TfidfWrapper(stop_words_l=stop_words_l)
        print(datetime.now())
        docs_embeddings = tfidf_wrapper.get_embeddings(doc_list=doc_list)
        print(datetime.now())
    elif algo == 'doc2vec':
        print(datetime.now())
        doc2vec_wrapper = Doc2vecWrapper(stop_words_l=stop_words_l)
        print(datetime.now())
        docs_embeddings = doc2vec_wrapper.get_embeddings(doc_list=doc_list)
        print(datetime.now())
    elif algo == 'glove':
        print(datetime.now())
        # most of time is spent on loading the model
        glove_wrapper = GloveWrapper(stop_words_l=stop_words_l)
        print(datetime.now())
        docs_embeddings = glove_wrapper.get_embeddings(doc_list=doc_list)
        print(datetime.now())
    elif algo == 'bert':
        print('bert search result')
        print(datetime.now())
        # most of time is spent on loading the model
        bert_wrapper = BertWrapper(stop_words_l=stop_words_l)
        print(datetime.now())
        docs_embeddings = bert_wrapper.get_embeddings(doc_list=doc_list)
        print(datetime.now())
    else:
        raise ValueError("Undefined ranking algorithm.")
    cosine_distance_mat = cosine_similarity([docs_embeddings[-1]], docs_embeddings[:-1])
    euclidean_distance_mat = euclidean_distances([docs_embeddings[-1]], docs_embeddings[:-1])
    print(datetime.now())
    show_search_res(cos_distance_mat=cosine_distance_mat,
                    eucli_distance_mat=euclidean_distance_mat,
                    doc_list=doc_list)


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
    test_different_ranking_algo(
        algo='bert',
        doc_list=doc_list,
        stop_words_l=stop_words_l)


if __name__ == '__main__':
    query_test(query='tencent')
