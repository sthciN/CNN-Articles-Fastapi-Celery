import pandas as pd
import dill as pickle
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from numpy import exp
from scipy.sparse import csr_matrix, load_npz
import math
import os

lemmatizer = WordNetLemmatizer()

def load_data(file_path, num_rows=1000):
    """
    This function loads the data.
    Parameters:
    file_path: str
    num_rows: int
    
    Returns:
    data: pd.DataFrame
    """
    data = pd.read_csv(file_path, nrows=num_rows)
    
    return data

def tokenizer(text):
    """
    This function tokenizes the text and lemmatizes the tokens.
    Parameters:
    text: str
    
    Returns:
    tokens: list
    """
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def get_vectorizer():
    """
    This function loads the vectorizer.
    Returns:
    vec: TfidfVectorizer
    """
    vec = pickle.load(open(os.environ['TFIDF_MODEL_PATH'], "rb"))
    return vec

vec = get_vectorizer()
vec.tokenizer = tokenizer
bow = vec.vocabulary_
vec.n_docs = 1000
words = [None]*len(bow)
for k,v in bow.items():
    words[v] = k

document_frequency = (vec.n_docs + 1)/exp(vec.idf_ - 1) - 1

def create_word_vector(keywords):
    """
    This function creates a word vector for the keywords.
    The word vector is a sparse matrix and the values are the inverse square root of the rank of the keyword.
    Parameters:
    keywords: list

    Returns:
    word_vec: csr_matrix
    """
    word_vec = csr_matrix((1, len(bow)))

    k = 1
    for v in keywords:
        if bow.get(v) is None:
            continue
        
        ind = bow[v]
        word_vec[0, ind] = 1/math.sqrt(k)
        k += 1

    return word_vec

def get_super_wv():
    """
    This function loads the word vector.
    Returns:
    wv: csr_matrix
    """
    wv = load_npz(os.environ['WORD_VECTOR_PATH'])
    
    return wv