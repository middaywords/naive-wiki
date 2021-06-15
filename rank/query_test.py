"""
    File query_test.py created on 2021/5/20 by kangjx
"""

from datetime import datetime
import re

import autocorrect
import numpy as np

from data import stopwords
from rank.bert import BertWrapper
from rank.count import CountWrapper
from rank.doc2vec import Doc2vecWrapper
from rank.glove import GloveWrapper
from rank.tf_idf import TfidfWrapper
from utils.wild_card import AutocorrectWC
from utils.constants import term2doc_dict

from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity


def dis_top(
        distance_mat: np.ndarray,
        doc_list: list):
    top_id = distance_mat.argsort(axis=1)[0]
    np_doc_list = np.array(doc_list)
    final_res = np_doc_list[top_id]

    return final_res


def show_search_res(
        cos_distance_mat: np.ndarray,
        eucli_distance_mat: np.ndarray,
        doc_list: list) -> list:
    print('cosine')
    search_res = dis_top(cos_distance_mat, doc_list)
    print(search_res)

    # print('euclidean')
    # search_res = dis_top10(eucli_distance_mat, doc_list)
    # print(search_res)
    return search_res


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
    elif algo == 'count':
        print('count search result')
        print(datetime.now())
        # most of time is spent on loading the model
        count_wrapper = CountWrapper(stop_words_l=stop_words_l)
        print(datetime.now())
        docs_embeddings = count_wrapper.get_embeddings(doc_list=doc_list)
        print(datetime.now())
    else:
        raise ValueError("Undefined ranking algorithm.")
    cosine_distance_mat = cosine_similarity([docs_embeddings[-1]], docs_embeddings[:-1])
    euclidean_distance_mat = euclidean_distances([docs_embeddings[-1]], docs_embeddings[:-1])
    print(datetime.now())
    search_res = show_search_res(cos_distance_mat=cosine_distance_mat,
                                 eucli_distance_mat=euclidean_distance_mat,
                                 doc_list=doc_list)

    return search_res


def match_query_doc(query: str, search_res: list) -> list:
    for id in range(len(search_res)):
        if query == search_res[id]:
            search_res[0], search_res[id] = search_res[id], search_res[0]
    return search_res


def query_test(query: str, top_k=10):
    corrector_wc = AutocorrectWC()
    query = query.lower()
    query_terms = list(filter(None, re.split(r"[ ,_:#!(\){}&\+]", query)))
    doc_count = dict()
    wrong_term_num = 0
    for term in query_terms:
        possible_terms = []
        # wildcard
        if term.find('*') >= 0:
            possible_terms = corrector_wc.wild_card(term)
        else:
            if term not in term2doc_dict.keys():
                corrected_term = corrector_wc.correct_term(term)
                if corrected_term not in term2doc_dict.keys():
                    wrong_term_num += 1
                    continue
                else:
                    possible_terms.append(corrected_term)
            else:
                possible_terms.append(term)
        for possible_term in possible_terms:
            for doc in term2doc_dict[possible_term]:
                if doc in doc_count.keys():
                    doc_count[doc] += 1
                else:
                    doc_count[doc] = 1
    doc_list = []
    for key in doc_count.keys():
        if doc_count[key] == len(query_terms) - wrong_term_num:
            doc_list.append(key)
    doc_list.append(query)

    stop_words_l = stopwords.en_stop_words
    # algo_list = ['bert', 'tf-idf', 'glove', 'doc2vec', 'count']
    # for algo in algo_list:
    #     test_different_ranking_algo(
    #         algo=algo,
    #         doc_list=doc_list,
    #         stop_words_l=stop_words_l)
    search_res = test_different_ranking_algo(
        algo='tf-idf',
        doc_list=doc_list,
        stop_words_l=stop_words_l)
    search_res = match_query_doc(query, search_res)
    search_res = search_res[:top_k]

    return search_res


if __name__ == '__main__':
    query_test(query='ten*nt qq')
