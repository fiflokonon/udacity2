import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://testuser:udacity@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)
        self.new_question = {
            "question": "Qui sui-je ?",
            "answser" : "Je suis moi",
            "category": 4,
            "difficulty": 1
        }
        self.new_bad_question = {
            "question": "Qui sui-je ?",
            "answser" : "Je suis moi",
            "category": "",
            "difficulty": "!"
        }
        self.search_term = {
            "searchTerm": "title"
        }
        self.quizzes = {
            "quiz_category": "History",
            "previous_questions": [5,9]
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
    
    def tearDown(self):
        """Executed after reach test"""
        
        pass

    #--------------------------------------#
    #--------TESTS METHODS-----------------#
    #--------------------------------------#

#--------Test Get all categories---------------#
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

        
#--------Test Get all questions---------------#
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

#------------Test Question Creation---------------#
    def test_create_question(self):
        res = self.client().post("/questions", json = self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

#--------------Test Question Creation Failure--------#
    def test_bad_request(self):
        res = self.client().post('/questions', json = self.new_bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)

#--------Test Delete Question-----------------------#
    def test_delete_questions(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
#----------Test Delete Question Failed------------#
    def test_delete_questions_failed(self):
        res = self.client().delete('/questions/1')#This question doesn't exist
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

#--------------Test Search Question----------------#
    def test_search_question(self):
        res = self.client().post('/questions/search', json = self.search_term)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertEqual(data["success"], True)
    

#----------------Test Get next question----------------------#
    def test_quizzes(self):
        res = self.client().post('/quizzes', json = self.quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
        

#--------Test Get questions for a category---------------#
    def test_category_questions(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])

#--------------Test Get question for a Category Failed-------------#
    def test_category_questions_failed(self):
        res = self.client().get("/categories/41/questions")#This category doesn't exist
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)


    #--------------------------------------------------------#
    #---------------TEST ERROR HANDLING----------------------#
    #--------------------------------------------------------#
    def test_not_found(self):
        res = self.client().get('/cat')#This route doesn't exist
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual("Not found", data["message"])
        self.assertEqual(data["success"], False)
    
    def test_not_allowed(self):
        res = self.client().post('/categories')#This route is for GET method
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual("Method Not allowed", data["message"])
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()