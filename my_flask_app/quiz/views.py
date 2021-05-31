# -*- coding: utf-8 -*-
"""User views."""
import json
import requests
from flask import (
    Blueprint, 
    render_template, 
    current_app, 
    request, 
    redirect,
    url_for,
    abort,
)
from requests import models
from my_flask_app.quiz.utils import get_questions_from_API
from flask_login import current_user, login_required
from my_flask_app.quiz.forms import QuizForm
from my_flask_app.utils import flash_errors
from my_flask_app.quiz.models import Quiz
from my_flask_app.user.models import User

blueprint = Blueprint("quiz", __name__, url_prefix="/quiz", static_folder="../static")

@blueprint.route("/", methods=["GET", "POST"])
@login_required
def quiz():
    form = QuizForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        current_app.logger.info(dir(form))
        if form.validate_on_submit():
            questions = json.loads(form.questions.data)
            for index, question in enumerate(questions['results'], start=1):
                print(form[f'answer_{index}'])
                question['answer'] = form[f'answer_{index}'].data

            user_id = current_user.id
            quiz = Quiz(questions, user_id)
            quiz.save()
            quiz_id = quiz.id
            return redirect(url_for('quiz.quiz_with_id', quiz_id=quiz_id))
        else:
            flash_errors(form)
    # get question
    try:
        questions = get_questions_from_API()
    except requests.RequestException:
        abort(503)
    current_app.logger.info(questions)
    questions_json = json.dumps(questions)
    return render_template("quiz/quiz.html", form=form, questions_json=questions_json, questions=questions)

@blueprint.route("/<quiz_id>", methods=["GET"])
@login_required
def quiz_with_id(quiz_id):
    current_app.logger.info(f"Get quiz with id={quiz_id}")
    quiz = Quiz.get_by_id(quiz_id)
    current_app.logger.info(quiz)
    if not quiz:
        abort(404)
    questions = quiz.json_question
    for question in questions['results']:
        question['colors'] =[]
        for answer in question['answers']:
            current_app.logger.info((answer, question['answer'], question['correct_answer']))
            if answer == question['correct_answer'] == question['answer']:
                question['colors'].append('green')
            elif answer != question['correct_answer'] and answer == question['answer']:
                question['colors'].append('red')
            else:
                question['colors'].append('yellow')
        current_app.logger.info(question['colors'])
    return render_template("quiz/quiz.html", questions=questions, score=quiz.score)

@blueprint.route("/quizzes", methods=["GET"])
def quiz_scoreboard():
    current_app.logger.info(User.get_all())
    current_app.logger.info(Quiz.get_all())
    current_app.logger.info(User.get_users_with_quizzes())
    scoreboard = []
    for user in User.get_users_with_quizzes():
        current_app.logger.info(user)
        total_score = 0
        for quiz in user.quizzes:
            current_app.logger.info(quiz)
            total_score += quiz.score
        scoreboard.append({"user": user.username, "total_score": total_score/(len(user.quizzes)*5)})
    return render_template("quiz/quizzes.html", scoreboard=sorted(scoreboard, key=lambda x: x['total_score']))