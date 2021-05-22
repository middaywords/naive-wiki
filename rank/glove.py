import pandas as pd
import numpy as np
import re
from tensorflow import keras
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import codecs


def read_glove_vecs(glove_file):
    with open(glove_file, 'r', encoding='utf-8') as f:
        words = set()
        word_to_vec_map = {}

        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)

    return words, word_to_vec_map


class GloveWrapper:
    def __init__(self, stop_words_l: list):
        """
        :param stop_words_l: words to be cleaned in
        """
        self.stop_words_l = stop_words_l
        # reading Glove word embeddings into a dictionary with "word" as key and values as word vectors
        _, self.embeddings_index = read_glove_vecs(glove_file='../../glove.6B/glove.6B.100d.txt')

    def get_embeddings(self, doc_list: list):
        """
        :param doc_list: list of document string
        :return: vector of words
        """
        documents_df = pd.DataFrame(doc_list, columns=['documents'])
        documents_df['documents_cleaned'] = documents_df.documents.apply(lambda x: " ".join(
            re.sub(r'[^a-zA-Z]', ' ', w).lower() for w in x.split() if
            re.sub(r'[^a-zA-Z]', ' ', w).lower() not in self.stop_words_l))

        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(documents_df.documents_cleaned)
        tokenized_documents = tokenizer.texts_to_sequences(documents_df.documents_cleaned)
        tokenized_paded_documents = pad_sequences(tokenized_documents, maxlen=64, padding='post')
        vocab_size = len(tokenizer.word_index) + 1

        # creating embedding matrix
        # every row is a vector representation from the vocabulary indexed by the tokenizer index.
        embedding_matrix = np.zeros((vocab_size, 100))

        for word, i in tokenizer.word_index.items():
            embedding_vector = self.embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

        # prepare tfidf things
        tfidf_vectoriser = TfidfVectorizer()
        tfidf_vectoriser.fit(documents_df.documents_cleaned)
        tfidf_vectors = tfidf_vectoriser.transform(documents_df.documents_cleaned).toarray()

        # calculating average of word vectors of a document weighted by tf-idf
        document_embeddings = np.zeros((len(tokenized_paded_documents), 100))

        words = tfidf_vectoriser.get_feature_names()
        # instead of creating document-word embeddings, directly creating document embeddings
        for i in range(documents_df.shape[0]):
            for j in range(len(words)):
                document_embeddings[i] += embedding_matrix[tokenizer.word_index[words[j]]] * tfidf_vectors[i][j]

        return document_embeddings
