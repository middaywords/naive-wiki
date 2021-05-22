import re
import pandas as pd
import numpy as np
import unittest
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer
from rank.tf_idf import *
from rank.bert import *
from rank.doc2vec import *
from rank.glove import *

# preconditions
# nltk.download('stopwords')
# nltk.download('punkt')

# consts
documents = ['Machine learning is the study of computer algorithms that improve automatically through experience.\
                    Machine learning algorithms build a mathematical model based on sample data, known as training data.\
                    The discipline of machine learning employs various approaches to teach computers to accomplish tasks \
                    where no fully satisfactory algorithm is available.',
             'Machine learning is closely related to computational statistics, which focuses on making predictions using computers.\
The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning.',
             'Machine learning involves computers discovering how they can perform tasks without being explicitly programmed to do so. \
It involves computers learning from data provided so that they carry out certain tasks.',
             'Machine learning approaches are traditionally divided into three broad categories, depending on the nature of the "signal"\
or "feedback" available to the learning system: Supervised, Unsupervised and Reinforcement',
             'Software engineering is the systematic application of engineering approaches to the development of software.\
Software engineering is a computing discipline.',
             'A software engineer creates programs based on logic for the computer to execute. A software engineer has to be more concerned\
about the correctness of the program in all the cases. Meanwhile, a data scientist is comfortable with uncertainty and variability.\
Developing a machine learning application is more iterative and explorative process than software engineering.'
             ]

stop_words_l = stopwords.words('english')


def most_similar(doc_id: int, similarity_matrix, matrix_type: str):
    """
    Given the similarity matrix, showing the distacne of doc_id to other docs
    """
    print(f'Document: {doc_id}')
    print('\n')
    print('Similar Documents:')
    if matrix_type == 'Cosine Similarity':
        similar_ix = np.argsort(similarity_matrix[doc_id])
    elif matrix_type == 'Euclidean Distance':
        similar_ix = np.argsort(similarity_matrix[doc_id])[::-1]
    for ix in similar_ix:
        if ix == doc_id:
            continue
        print('\n')
        print(f'Document: {ix}')
        print(f'{matrix_type} : {similarity_matrix[doc_id][ix]}')


def print_similarity(embeddings):
    pairwise_similarities = cosine_similarity(embeddings)
    pairwise_differences = euclidean_distances(embeddings)
    most_similar(0, pairwise_similarities, 'Cosine Similarity')
    most_similar(0, pairwise_differences, 'Euclidean Distance')


class TestCase(unittest.TestCase):
    def test_tf_idf(self):
        tf_idf_wrapper = TfidfWrapper(stop_words_l=stop_words_l)
        tfidf_vectors = tf_idf_wrapper.get_embeddings(doc_list=documents)
        print_similarity(tfidf_vectors)

    def test_bert(self):
        bert_warpper = BertWrapper(stop_words_l=stop_words_l)
        document_embeddings = bert_warpper.get_embeddings(doc_list=documents)
        print_similarity(document_embeddings)

    def test_word2vec(self):
        doc2vec_wrapper = Doc2vecWrapper(stop_words_l=stop_words_l)
        document_embeddings = doc2vec_wrapper.get_embeddings(doc_list=documents)
        print_similarity(document_embeddings)

    def test_glove(self):
        glove_wrapper = GloveWrapper(stop_words_l=stop_words_l)
        document_embeddings = glove_wrapper.get_embeddings(doc_list=documents)
        print_similarity(document_embeddings)


if __name__ == '__main__':
    unittest.main()
