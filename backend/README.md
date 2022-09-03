# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`


### Documentation 

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'` or `GET '/questions?page=${integer}'`
- `GET '/questions?page=${integer}'` : This endpoint is used to PAGINATE------the return
- Fetches a dictionaryof questions in which the keys all categories, a questions list in which by question we have all question attributes
- Request Arguments: None
- Returns: An object with differents keys such as :
  *`categories`, that contains an object of `id: category_string` key: value pairs
  *`questions`, that contains a questions list
  *`total_questions`, that contains the total number of questions that we get

```json
{
  "total_questions": 27,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ]
}
```

`POST '/questions'`

- Create new question
- Request Arguments : 
```json
{
    "question": "question",
    "answer": "answer",
    "category": category_id,
    "difficulty": difficulty
}
```
- Returns: An object with differents keys like:
  *`code`, that contains the response status code
  *`message`, that contains the response message
  *`success`, that contains the success status
```json
{
    "code": 201,
    "message": "created",
    "success": true
}
```

`DELETE '/questions/${id}'`

- Delete a question
- Url Arguments: 
  *`id`, that contains the question id
- Request Arguments: None
- Returns: An object with single key `success`, that contains the operation success status
```json
{
    "success": false
}
```
`POST 'questions/search'`

- Search questions
- Request Arguments : 
```json
{
  "searchTerm": "searchTerm"
}
```
- Returns: An object with differents keys such as:
  *`categories`, that contains an object of `id: category_string` key: value pairs
  *`questions`, that contains a questions list
  *`total_questions`, that contains the total number of questions that we get
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```

`GET '/categories/${id}/questions'`

- Fetches questions list for a category
- Url Arguments: 
  *`id`, that contains the category id
- Request Arguments: None
- Returns: An object with differents keys such as:
  *`current_category`, that contains type of current category
  *`questions`, that questions list
  *`total_questions`, that contains total number of questions for this category
```json
{
    "current_category": "History",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
    ],
    "total_questions": 5
}
```

`POST '/quizzes'`

- Fetches next question
- Request Arguments:
```json
{
  "quiz_category": "History",
  "previous_questions": [5,9]
}
```
- Returns: An object with single key `question`, that contains a question object
```json
{
  "question": {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
  }
}
```
## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
