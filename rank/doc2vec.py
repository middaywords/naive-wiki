import re
import pandas as pd
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize


class Doc2vecWrapper:
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

        tagged_data = [TaggedDocument(words=word_tokenize(doc), tags=[i]) for i, doc in
                       enumerate(documents_df.documents_cleaned)]
        model_d2v = Doc2Vec(vector_size=100, alpha=0.025, min_count=1)

        model_d2v.build_vocab(tagged_data)

        for epoch in range(100):
            model_d2v.train(tagged_data,
                            total_examples=model_d2v.corpus_count,
                            epochs=model_d2v.epochs)

        document_embeddings = np.zeros((documents_df.shape[0], 100))

        for i in range(len(document_embeddings)):
            document_embeddings[i] = model_d2v.dv[i]

        return document_embeddings
