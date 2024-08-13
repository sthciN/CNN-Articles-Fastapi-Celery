
# CNN SIMILAR ARTICLES

## Description

This project is designed to find similar articles from CNN. It uses various text analysis techniques to compare articles and determine their similarity. This can be useful for finding related news stories, understanding the context of a news event, or tracking the coverage of a particular topic over time. The project is built in Python and uses libraries such as `NLTK` for natural language processing and `Scikit-learn` for machine learning.

### Routes

This FastAPI project is a text similarity service that calculates and returns the top 100 articles most similar to a given input text. It exposes four main routes:

- A POST route `/similar-articles` that accepts an article (including its text and ID) as input. It first checks if the similar articles for the given ID are already calculated and stored in the database. If not, it generates keywords from the input text using a TF-IDF vectorizer, calculates the cosine similarity between the generated word vector and pre-calculated word vectors stored in a .npz file, and then sorts the articles based on their similarity values. The result is then stored in a PostgreSQL database for future requests.

- A GET route `/similar-articles/{id}` that accepts an article ID and returns the pre-calculated similar articles for that ID from the database.

- A POST route `/similar-articles/celery` that accepts an article (including its text and ID) as input. If the similar articles for the given ID are not already calculated, it creates a Celery task to generate the keywords, calculate the cosine similarity, and store the result in the database. This route uses Redis as a message broker to manage the Celery tasks.

- A GET route `/similar-articles/celery/{task_id}` that accepts a Celery task ID and returns the result of the task if it's ready. If the task is not ready yet, it returns a message indicating that the task is still in progress.

The project is designed to handle large-scale text similarity tasks efficiently by using asynchronous task queues and caching the results in a database. It provides a robust and scalable solution for finding similar articles in a large corpus of text.


## Usage
`poetry install`

`poetry run uvicorn main:app --reload`


## Alternatively
`docker build -t my-fastapi-app .`

`docker run -p 8000:8000 my-fastapi-app`


## Running Tests
To run tests, use the following command:

`pytest`


### .env

WORD_VECTOR_PATH=./app/static/super_wv.npz

DATA_PATH=./archive/CNN_Articels_clean/CNN_Articels_clean.csv

TFIDF_MODEL_PATH=./app/static/tfidf_model.pkl

DB_HOST=

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_PORT=

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.