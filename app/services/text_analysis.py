from sklearn.feature_extraction.text import TfidfVectorizer
from .data_service import vec, words, document_frequency
import numpy as np
import os
import dill as pickle
from scipy.sparse import save_npz
from .data_service import load_data

def generate_keywords(article):
    """
    This function generates keywords from the article.
    Parameters:
    article: str

    Returns:
    keywords: list
    """
    # transform the article into a sparse matrix with tfidf score
    mt = vec.transform([article]) 
    
    # get one dimensional array
    mtx = mt.toarray()[0] 
    ww = []

    # get the index of the non-zero elements
    for i in mtx.nonzero()[0]: 
        if document_frequency[i] >= 2: # filter out the words that appear less than 2 times
            ww.append(words[i])
    
    keywords = sorted(ww, reverse=True)[:100] or None

    return keywords


def extract_keywords(num_keywords=100):
    """
    This function extracts keywords from the articles and saves the word vector and the vectorizer.
    Parameters:
    num_keywords: int

    Returns:
    True
    """

    if os.path.exists(os.environ['WORD_VECTOR_PATH']):
        return True

    vectorizer = TfidfVectorizer()
    data = load_data(os.environ['DATA_PATH'])
    
    X = vectorizer.fit_transform(data['Article text'])    

    # get the top features for future reference
    # indices = np.argsort(vectorizer.idf_)[::-1]
    # features = vectorizer.get_feature_names_out()
    # top_features = [features[i] for i in indices[:num_keywords]]

    with open(os.environ['TFIDF_MODEL_PATH'], 'wb') as f:
        pickle.dump(vectorizer, f)

    # save the word vector
    save_npz(os.environ['WORD_VECTOR_PATH'], X)
    
    return True
