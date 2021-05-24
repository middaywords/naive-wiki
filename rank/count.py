"""
    File count.py created on 2021/5/24 by kangjx
"""
import re

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


class CountWrapper:
    def __init__(self, stop_words_l: list):
        """
        :param stop_words_l: words to be cleaned in
        """
        self.stop_words_l = stop_words_l

    def get_embeddings(self, doc_list: list):
        """
        :param doc_list: list of document string
        :return: vector of words
        """
        documents_df = pd.DataFrame(doc_list, columns=['documents'])
        documents_df['documents_cleaned'] = documents_df.documents.apply(lambda x: " ".join(
            re.sub(r'[^a-zA-Z]', ' ', w).lower() for w in x.split() if
            re.sub(r'[^a-zA-Z]', ' ', w).lower() not in self.stop_words_l))

        count_vectoriser = CountVectorizer(max_features=50)
        document_embeddings = count_vectoriser.fit_transform(documents_df.documents_cleaned).toarray()

        return document_embeddings
