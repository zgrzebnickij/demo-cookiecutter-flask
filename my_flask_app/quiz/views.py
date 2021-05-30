# -*- coding: utf-8 -*-
"""User views."""
import json
from flask import (
    Blueprint, 
    render_template, 
    current_app, 
    request, 
    redirect,
    url_for,

)
from my_flask_app.quiz.utils import get_questions_from_API
from flask_login import current_user, login_required
from my_flask_app.quiz.forms import QuizForm
from my_flask_app.utils import flash_errors
from my_flask_app.quiz.models import Quiz

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
    questions = get_questions_from_API()
    current_app.logger.info(questions)
    questions_json = json.dumps(questions)
    return render_template("quiz/quiz.html", form=form, questions_json=questions_json, questions=questions)

@blueprint.route("/<quiz_id>", methods=["GET"])
@login_required
def quiz_with_id(quiz_id):
    current_app.logger.info(f"Get quiz with id={quiz_id}")
    return "<h1>aaaa</h1>"