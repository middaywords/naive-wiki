import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfWrapper:
    def __init__(self, stop_words_l: list):
        """
        :param stop_words_l: words to be cleaned in
        """
        self.stop_words_l = stop_words_l

    def get_tfidf_vector(self, doc_list: list):
        """
        :param doc_list: list of document string
        :return: vector of words
        """
        documents_df = pd.DataFrame(doc_list, columns=['documents'])
        documents_temp = documents_df.documents.apply(lambda x: " ".join(re.sub(
            r'[^a-zA-Z]', ' ', w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]', ' ',
                                                                       w).lower() not in self.stop_words_l))
        tfidf_vectoriser = TfidfVectorizer()
        tfidf_vectoriser.fit(documents_temp)
        tfidf_vectors = tfidf_vectoriser.transform(documents_temp)

        return tfidf_vectors
