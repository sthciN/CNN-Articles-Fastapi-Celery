from .data_service import create_word_vector, get_super_wv
import numpy as np
import pandas as pd
import  json
from .utils import NpEncoder, convert_np_to_python
from app import celery_app
from app.database import conn, write_result_to_db
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(id, keywords, data):
    """
    This function calculates the similarity between the current article and the top 100 most similar articles.
    Parameters:
    id: int
    keywords: list
    data: pd.DataFrame

    Returns:
    result: str
    """
    
    # create a word vector for the article
    wv = create_word_vector(keywords) 
    super_wv = get_super_wv()
    
    # calculate the similarity that is 2D array
    similarity = cosine_similarity(wv, super_wv) 
    
    # get the top 100 most similar articles
    top_inds = similarity.argsort()[:,::-1][:,1:101] 
    
    # get the similarity values between the current article and the top 100 articles
    sim_values = similarity[np.arange(top_inds.shape[0])[:, None], top_inds][0] 
    top_inds = top_inds[0]
    result = []

    for j in range(len(top_inds)):
        idx = int(top_inds[j])
        article_id = data.iloc[idx]['Index']
        result.append({'article_id': id,
                            'similar_article_id': article_id,
                            'title': data.iloc[idx]['Headline'],
                            'url': data.iloc[idx]['Url'],
                            'similarity': sim_values[j]})
    
    # convert numpy array to python list
    if result:
        write_result_to_db(conn, id, [convert_np_to_python(d) for d in result]) 

    result = json.dumps(result, cls=NpEncoder)

    return result


@celery_app.task
def calculate_similarity_task(id, keywords, data):
    """
    This function calculates the similarity between the current article and the top 100 most similar articles.
    Parameters:
    id: int
    keywords: list
    data: pd.DataFrame
    
    Returns:
    result: str
    """

    # create a word vector for the article
    wv = create_word_vector(keywords) 
    super_wv = get_super_wv()
    
    # calculate the similarity that is 2D array
    similarity = cosine_similarity(wv, super_wv) 
    
    # get the top 100 most similar articles
    top_inds = similarity.argsort()[:,::-1][:,1:101] 
    
    # get the similarity values between the current article and the top 100 articles
    sim_values = similarity[np.arange(top_inds.shape[0])[:, None], top_inds][0] 
    top_inds = top_inds[0]
    
    data = pd.DataFrame(data)
    
    result = []

    for j in range(len(top_inds)):
        idx = int(top_inds[j])
        article_id = data.iloc[idx]['Index']
        result.append({'article_id': id,
                            'similar_article_id': article_id,
                            'title': data.iloc[idx]['Headline'],
                            'url': data.iloc[idx]['Url'],
                            'similarity': sim_values[j]})
    
    write_result_to_db(conn, id, result)
    
    result = json.dumps(result, cls=NpEncoder)

    return result
