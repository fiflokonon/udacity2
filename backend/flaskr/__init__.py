from crypt import methods
import os
from unicodedata import category
from webbrowser import get
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    #---------------------------------------------------#
    #-----------GET ALL CATEGORIES----------------------#
    #---------------------------------------------------#
    @app.route('/categories')
    def get_categories():
        datas = {}
        categories = Category.query.all()
        for form in categories:
            datas[str(form.id)] = form.type
        return jsonify({
            "categories": datas
        })
    
    #----------------------------------------------------#
    #---------------GET ALL QUESTIONS WITH PAGINATE------#
    #----------------------------------------------------#
    @app.route('/questions')
    def get_questions():
        datas = {}
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.all()
        formatted = [question.format() for question in questions]
        categories = Category.query.all()
        for form in categories:
            datas[str(form.id)] = form.type
        return jsonify({
            "questions": formatted[start:end],
            "total_questions": len(formatted),
            "categories": datas
        })

    #-----------------------------------------------------#
    #--------------DELETE A QUESTION----------------------#
    #-----------------------------------------------------#
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id = question_id).one_or_none()
        try:
            question.delete()
            return jsonify({
                "success": True
            })
        except:
            return jsonify({
                "success": False
            })
    
    #------------------------------------------------#
    #----------CREATE QUESTION-----------------------#
    #------------------------------------------------#
    @app.route('/questions', methods=['POST'])
    def create_question():
        requestBody = request.get_json()
        question = Question(
            question = requestBody.get('question'), 
            answer = requestBody.get('answer'), 
            category = requestBody.get("category"), 
            difficulty = requestBody.get("difficulty"))
        try:
            question.insert()
            return jsonify({
                "success": True,
                "message": "created",
                "code": 201
            })
        except:
            return jsonify({
                "success": False
            })
    
    #-----------------------------------------------#
    #------------SEARCH A QUESTION------------------#
    #-----------------------------------------------#
    @app.route('/questions/search', methods=["POST"])
    def search_question():
        search_term = request.get_json().get('searchTerm')
        print(search_term)
        questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
        categories = Category.query.all()
        formatted_cat = [category.format() for category in categories]
        formatted = [question.format() for question in questions]
        return jsonify({
            "success": True,
            "questions": formatted,
            "total_questions": len(formatted),
            "categories": formatted_cat
        })
    
    #--------------------------------------#
    #---------GET QUESTIONS BY CATEGORY----#
    #--------------------------------------#
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def category_questions(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        formatted = [question.format() for question in questions]
        category = Category.query.filter_by(id = category_id).first()
        return jsonify({
            "questions": formatted,
            "current_category": category.type,
            "total_questions": len(formatted) 
        })
    
    #---------------------------------------------#
    #-----------GET NEXT QUESTION-----------------#
    #---------------------------------------------#
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        category = request.get_json().get('quiz_category')
        previous = request.get_json().get('previous_questions')
        category_id = Category.query.with_entities(Category.id).filter(Category.type == category).first()
        quizze = Question.query.filter(Question.category == category_id).filter(Question.id.notin_(previous)).first()
        return jsonify({
            "question": quizze.format()
        })

    #------------------------------------------------#
    #-----------ERROR HANDLING-----------------------#
    #------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
        }), 400 

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        })


    return app

