from app import app, celery_app
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.services.text_analysis import generate_keywords, extract_keywords
from app.services.cosine_similarity import calculate_similarity, calculate_similarity_task
from app.services.similar_articles import get_articles
from app.services.data_service import load_data
from app.models.model import Article
import os


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/fit")
# def fit_vectorizer():
#     try:
#         extract_keywords()
    
#     except Exception as e:
#         return {"message": str(e)}

#     return {"details": "The vectorizer has been fitted."}


@app.post("/similar-articles")
def find_similar_articles(article: Article):
    # Get text from the request body json
    text = article.text
    id = article.id

    if not text:
        return {"message": "No text provided."}
    if not id:
        return {"message": "No id provided."}
    
    try:
        result = get_articles(id)
        
        if result:
            return {"details": result}
        
        keywords = generate_keywords(text)

        data = load_data(os.environ['DATA_PATH'])

        similar_articles = calculate_similarity(id, keywords, data)

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    return {"details": similar_articles}


@app.get("/similar-articles/{article_id}")
def get_similar_articles(article_id: int):
    if not article_id or not isinstance(article_id, int):
        return JSONResponse(status_code=422, content={"message": "No article_id provided."})
    
    try:
        result = get_articles(article_id)
    
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    return {"details": result}



@app.post("/similar-articles/celery")
def find_similar_articles_celery(article: Article):
    # Get text from the request body json
    text = article.text
    id = article.id

    if not text:
        return JSONResponse(status_code=422, content={"message": "No text provided."})
    if not id:
        return JSONResponse(status_code=422, content={"message": "No id provided."})
    
    try:
        result = get_articles(id)
        
        if result:
            return {"details": result}
        
        keywords = generate_keywords(text)

        data = load_data(os.environ['DATA_PATH'])
        data_dict = data.to_dict('records')

        task = calculate_similarity_task.delay(id, keywords, data_dict)

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    
    return JSONResponse(status_code=200, content={"details": {"task_id": str(task.id)}})


@app.get("/similar-articles/celery/{task_id}")
def get_similar_articles_celery(task_id: str):
    if not task_id:
        return {"message": "No task_id provided."}
    
    try:
        task = celery_app.AsyncResult(task_id)
        
        if task.ready():
            print(task.state)
            print(task.get())

        else:
            return {"message": "Task not ready"}
    
    except Exception as e:
        return {"message": str(e)}
    
    return {"details": task.get()}
